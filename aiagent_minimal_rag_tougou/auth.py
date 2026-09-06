# -*- coding: utf-8 -*-
"""ログイン（認証）。社内LDAP認証APIへ差し替えることを前提に、この1ファイルに分離してある。

ログイン関係の設定は env や config.py には置かず、**すべてこのファイルの冒頭**にある。
LDAPを繋ぐとき・管理者パスワードを変えるときは、このファイルだけを編集すればよい。

  local … auth_users.yaml のユーザーで認証（既定。LDAP導入前の暫定）
  http  … 社内の認証API（LDAP連携API）にHTTPで問い合わせる

どちらのプロバイダでも、常設アカウントは常に使える:
  admin（ADMIN_USER / ADMIN_PASS）        … 管理者。LDAP障害時の非常口
  user1・user2・user3（BUILTIN_USERS）    … 一般ユーザー。ID とパスワードが同じ

アプリ本体（core.py）はこのファイルの User / authenticate / get_provider などを
使うだけなので、画面やカタログ側のコードは変更不要。

アプリ側が認証結果に求めるのは User だけ:
    username     … カタログとチャット履歴の保存先フォルダ名に使う識別子
    display_name … 画面表示名
    groups       … 所属グループ（LDAP側の情報をそのまま持つ）
    is_admin     … AUTH_ADMIN_GROUP に属しているか（管理者画面に入れるかの判定に使う）

※ このログインは「ユーザーごとにカタログとチャット履歴を分ける」ための仕組みであって、
   OSレベルのアクセス制御ではない。data/ のファイルを直接読める人には効かない。
   詳しくは README の「ログインについての注意」を参照。
"""

import hashlib
import hmac
import json
import os
import secrets
import urllib.error
import urllib.request
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path

import yaml

# ==========================================================================
# ===== 設定（ログイン関係はすべてここ。env や config.py には置かない）
# ==========================================================================

# どの方式で認証するか。
#   "local" … auth_users.yaml のユーザーで認証（既定。LDAP導入前の暫定）
#   "http"  … 社内の認証API（LDAP連携API）にHTTPで問い合わせる
AUTH_PROVIDER = "local"

# local 用: ユーザー定義ファイルの置き場所（python core.py users で管理する）
AUTH_USERS_FILE = Path(__file__).resolve().parent / "auth_users.yaml"

# 管理者とみなすグループ名。
# http では認証APIが返すグループ名の実物と完全一致させること（部分一致はしない）。
AUTH_ADMIN_GROUP = "admin"

# 常設の管理者アカウント。LDAPや auth_users.yaml とは別枠で、どのプロバイダを
# 使っていても必ずログインできる「非常口」。LDAPが落ちても設定画面に入れる。
# このアカウントで入ると、データの取り込み・テーブルの削除・メール設定の
# 変更ができるため、**本番では必ず ADMIN_PASS を強いパスワードに変えること**。
# ADMIN_PASS を空文字にすると、このアカウント自体が無効になる
# （空パスワードでログインできてしまう事故を防ぐため）。
ADMIN_USER = "admin"
ADMIN_PASS = "adminpass"

# 常設の一般ユーザー（チャットだけ使える権限）。ID とパスワードは同じ文字列
# （例: user1 / user1）。増減はこのリストを書き換えるだけで、空にすれば
# この仕組みごと無効になる。
# ※ パスワード＝ID なので推測は容易。社内ネットワーク限定で使う前提の
#    簡易アカウントであり、LDAP へ切り替えたらリストを空にすること。
BUILTIN_USERS = ["user1", "user2", "user3"]

# --- http プロバイダ用（社内APIの仕様に合わせて書き換える） -------------------
AUTH_API_URL = ""                        # 例: "https://auth.example.co.jp/api/login"
AUTH_API_USER_FIELD = "username"         # 送信JSONの、ユーザーIDを入れる項目名
AUTH_API_PASS_FIELD = "password"         # 送信JSONの、パスワードを入れる項目名
AUTH_API_SUCCESS_FIELD = ""              # 応答の成功フラグの場所（空 = HTTP 200 なら成功扱い）
AUTH_API_DISPLAY_FIELD = "display_name"  # 応答の表示名の場所（"user.name" のような入れ子指定も可）
# 応答のどこにグループ一覧があるか。グループを返さないAPIでは空のままにする
# （空なら全員が一般ユーザーになり、管理者は ADMIN_PASS の admin だけになる）。
AUTH_API_GROUPS_FIELD = ""
AUTH_API_TIMEOUT = 10                    # 認証APIの応答を待つ秒数

# --- ユーザー ------------------------------------------------------------------

@dataclass
class User:
    username: str
    display_name: str = ""
    groups: list = field(default_factory=list)
    is_admin: bool = False

    def __post_init__(self):
        self.display_name = self.display_name or self.username

    @property
    def safe_key(self) -> str:
        """フォルダ名に使える識別子（個人カタログの保存先）。"""
        return "".join(c if (c.isalnum() or c in "-_.@") else "_" for c in self.username)[:64]


# --- パスワードのハッシュ（localプロバイダ用） --------------------------------------

_ITER = 200_000


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, _ITER)
    return f"pbkdf2_sha256${_ITER}${salt.hex()}${dk.hex()}"


def verify_password(password: str, stored: str) -> bool:
    try:
        algo, iters, salt_hex, hash_hex = str(stored).split("$")
        if algo != "pbkdf2_sha256":
            return False
        dk = hashlib.pbkdf2_hmac("sha256", password.encode(),
                                 bytes.fromhex(salt_hex), int(iters))
        return hmac.compare_digest(dk.hex(), hash_hex)
    except (ValueError, AttributeError):
        return False


# --- プロバイダ ----------------------------------------------------------------

class AuthProvider(ABC):
    """認証方式の共通インタフェース。差し替えるときはこれを実装する。"""

    name = "base"
    #: 画面のログインフォームに出す補足
    hint = ""

    @abstractmethod
    def authenticate(self, username: str, password: str) -> User | None:
        """成功なら User、失敗なら None を返す。
        通信エラーなど「認証以前の失敗」は AuthError を送出する。"""


class AuthError(RuntimeError):
    """認証処理そのものが行えなかった（設定不備・通信不可など）。"""


class LocalAuthProvider(AuthProvider):
    """auth_users.yaml のユーザーで認証する（LDAP導入までの暫定）。

    ユーザーの追加は python core.py users add で行う（パスワードはハッシュ化して保存）。
    """

    name = "local"
    hint = "社内LDAP導入までの暫定アカウントです。"

    def __init__(self, path: Path | None = None):
        self.path = Path(path or AUTH_USERS_FILE)

    def _load(self) -> list:
        if not self.path.exists():
            return []
        try:
            data = yaml.safe_load(self.path.read_text(encoding="utf-8")) or {}
        except Exception as e:
            raise AuthError(f"ユーザー定義を読めませんでした: {self.path} ({e})")
        return data.get("users") or []

    def authenticate(self, username: str, password: str) -> User | None:
        users = self._load()
        if not users:
            # ファイルにユーザーが居なくても異常ではない（常設の admin と
            # BUILTIN_USERS だけで運用できるため）。通常の「一致せず」として返す
            return None
        for u in users:
            if str(u.get("username", "")).lower() != str(username).lower():
                continue
            if not verify_password(password, u.get("password_hash", "")):
                return None
            groups = list(u.get("groups") or [])
            return User(username=str(u["username"]), display_name=str(u.get("display_name") or ""),
                        groups=groups, is_admin=AUTH_ADMIN_GROUP in groups)
        return None


class HttpApiAuthProvider(AuthProvider):
    """社内の認証API（LDAP連携API）にHTTPで問い合わせる。

    エンドポイントの仕様に合わせて、このファイル冒頭の AUTH_API_* を
    書き換えるだけで動く想定。レスポンスのJSONからどのキーを読むかも指定できる。

      AUTH_API_URL           = https://example.co.jp/api/auth
      AUTH_API_USER_FIELD    = username     # 送信するJSONのキー
      AUTH_API_PASS_FIELD    = password
      AUTH_API_SUCCESS_FIELD = authenticated  # 真偽値が入るキー（省略時はHTTP200で成功）
      AUTH_API_DISPLAY_FIELD = displayName
      AUTH_API_GROUPS_FIELD  = memberOf
      AUTH_API_TIMEOUT       = 10

    仕様が上記で表現できない場合は、この authenticate() だけ書き換えればよい。
    """

    name = "http"
    hint = "社内アカウントでログインしてください。"

    def authenticate(self, username: str, password: str) -> User | None:
        url = AUTH_API_URL
        if not url:
            raise AuthError("AUTH_API_URL が設定されていません（auth.py 冒頭を確認してください）。")

        payload = json.dumps({
            AUTH_API_USER_FIELD: username,
            AUTH_API_PASS_FIELD: password,
        }).encode()
        req = urllib.request.Request(
            url, data=payload, method="POST",
            headers={"Content-Type": "application/json", "Accept": "application/json"},
        )
        try:
            with urllib.request.urlopen(req, timeout=AUTH_API_TIMEOUT) as res:
                body = res.read().decode("utf-8", "replace")
                status = res.status
        except urllib.error.HTTPError as e:
            # 401/403 は「認証失敗」、それ以外は異常として扱う
            if e.code in (400, 401, 403):
                return None
            raise AuthError(f"認証APIがエラーを返しました: HTTP {e.code}")
        except Exception as e:
            raise AuthError(f"認証APIに接続できません: {e}")

        try:
            data = json.loads(body) if body.strip() else {}
        except json.JSONDecodeError:
            raise AuthError("認証APIの応答がJSONではありません。")

        ok_field = AUTH_API_SUCCESS_FIELD
        if ok_field:
            if not bool(_dig(data, ok_field)):
                return None
        elif status != 200:
            return None

        # グループを返さない認証APIは珍しくない。その場合は全員を一般ユーザーとして扱う
        # （管理者は上記 ADMIN_PASS で入る admin だけになる）。
        # 応答に無いものを推測して管理者にするのは危険なので、迷ったら一般にする。
        groups = []
        if AUTH_API_GROUPS_FIELD:
            raw = _dig(data, AUTH_API_GROUPS_FIELD) or []
            groups = [str(g) for g in ([raw] if isinstance(raw, str) else raw)]
        return User(
            username=str(_dig(data, AUTH_API_USER_FIELD) or username),
            display_name=str(_dig(data, AUTH_API_DISPLAY_FIELD) or ""),
            groups=groups,
            is_admin=bool(AUTH_ADMIN_GROUP) and AUTH_ADMIN_GROUP in groups,
        )


def _dig(data: dict, path: str):
    """'user.displayName' のようなドット区切りでネストしたJSONから値を取る。"""
    if not path:
        return None
    cur = data
    for part in str(path).split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


_PROVIDERS = {"local": LocalAuthProvider, "http": HttpApiAuthProvider}


def get_provider(name: str | None = None) -> AuthProvider:
    """設定に応じた認証プロバイダを返す。"""
    key = (name or AUTH_PROVIDER or "local").strip().lower()
    cls = _PROVIDERS.get(key)
    if cls is None:
        raise AuthError(f"未知の AUTH_PROVIDER です: {key} / 使えるのは {', '.join(_PROVIDERS)}")
    return cls()


# --- 常設の管理者（冒頭の ADMIN_USER / ADMIN_PASS） -------------------------------------------
#
# LDAPにも auth_users.yaml にも依存しない固定アカウント。
# LDAPが落ちている・まだ繋いでいない状況でも設定画面に入れるようにするための口。
#
# 安全のための決めごと:
#   1. ADMIN_PASS が空なら、このアカウントは存在しない扱い（空パスワードで入れない）
#   2. 比較は hmac.compare_digest（入力の長さや内容で処理時間が変わらないように）
#   3. 通常のプロバイダより先に判定する（LDAP側に同名ユーザーがいても取り違えない）

def admin_enabled() -> bool:
    return bool(ADMIN_USER and ADMIN_PASS)


def _try_builtin_admin(username: str, password: str) -> User | None:
    if not admin_enabled():
        return None
    if str(username).strip().lower() != ADMIN_USER.lower():
        return None
    # compare_digest は非ASCIIの str を受け付けない（TypeError）ため bytes で比べる
    if not hmac.compare_digest(str(password).encode("utf-8"),
                               str(ADMIN_PASS).encode("utf-8")):
        return None
    return User(username=ADMIN_USER, display_name="管理者",
                groups=[AUTH_ADMIN_GROUP], is_admin=True)


def _try_builtin_user(username: str, password: str) -> User | None:
    """常設の一般ユーザー（BUILTIN_USERS）。ID とパスワードが同じなら成功。"""
    name = str(username).strip().lower()
    for u in BUILTIN_USERS:
        if name != str(u).strip().lower():
            continue
        if hmac.compare_digest(str(password).encode("utf-8"),
                               str(u).encode("utf-8")):
            return User(username=str(u), display_name="", groups=[], is_admin=False)
        return None  # ID一致・パスワード違い
    return None


def authenticate(username: str, password: str) -> User | None:
    """ログインの入口。常設の管理者→常設の一般ユーザー→プロバイダの順に見る。

    画面からはこの関数だけを呼ぶ。プロバイダを差し替えても、管理者の非常口と
    常設の一般ユーザーはそのまま残る（不要になったら BUILTIN_USERS を空にする）。
    """
    admin = _try_builtin_admin(username, password)
    if admin is not None:
        return admin
    # 常設管理者と同じIDなら、パスワード違いとして扱いプロバイダには渡さない
    if admin_enabled() and str(username).strip().lower() == ADMIN_USER.lower():
        return None
    # 常設の一般ユーザーも同様に、IDが一致したらここで確定させる
    if any(str(username).strip().lower() == str(u).strip().lower()
           for u in BUILTIN_USERS):
        return _try_builtin_user(username, password)
    return get_provider().authenticate(username, password)


# --- ユーザー定義ファイルの操作（core.py の users CLI から使う） --------------------------

def load_users_file(path: Path | None = None) -> dict:
    p = Path(path or AUTH_USERS_FILE)
    if not p.exists():
        return {"users": []}
    return yaml.safe_load(p.read_text(encoding="utf-8")) or {"users": []}


def save_users_file(data: dict, path: Path | None = None) -> None:
    p = Path(path or AUTH_USERS_FILE)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False),
                 encoding="utf-8")
    try:                       # 他ユーザーから読めないようにする（Windowsでは無視される）
        os.chmod(p, 0o600)
    except OSError:
        pass


