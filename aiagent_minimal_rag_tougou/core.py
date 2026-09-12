"""core.py — アプリ本体（土台・データと画面）。

ファイルは5本。

  core.py    土台・データ（db / catalog / importer / jobs / chats …）と
             画面（Flask のルート11本）、起動とCLI
  brain.py   AI・分析（llm / tools / rag / models / グラフ / Excel / PowerPoint）
  assets.py  画面の素材（HTML・CSS・JS。ロジックは無い）
  config.py  設定
  auth.py    ログイン

起動とCLIはこのファイル（末尾の「起動」セクション参照）:
  python core.py                 ← 通常はこれで起動する
  python core.py users <...>     ユーザー管理CLI（list / add / passwd / remove）
  python core.py refresh <...>   定期取り込みCLI（--all / --job <ID> / --list）
  python core.py selftest        SQLガードのセルフテスト

読み込みの順に意味がある:

  1. 土台・データをこのファイルで定義する
  2. 自分自身を元のモジュール名（db / catalog / chats …）で sys.modules に登録する
  3. import brain（brain の中の `import db` はここへ戻ってくる）
  4. 画面をこのファイルで定義する（llm / tools は brain のものを使う）

統合前と同じく `import db` / `db.run_select(...)` と書けるよう、
それぞれのファイルを元のモジュール名でも参照できるよう登録している。
そのため呼び出し側のコードは統合前のまま動く。

このファイルに残っている元のファイル:
  run.py（起動口）
  web.py（画面・ルーティング）と web/ の11モジュール
  db.py / filecheck.py / chats.py / history.py / catalog_history.py
  prefs.py / catalog.py / verify.py / sqlusage.py
  importer.py / jobs.py / scheduler.py / cleanup.py
  manage_users.py / refresh.py（CLI）
"""
from __future__ import annotations

import sys as _sys

# 元のモジュール名でも import できるようにする（呼び出し側を変えないため）
# ここに挙げた名前の中身は、このファイル（土台・データと画面）にある。
# AI・分析側の名前（llm / tools / rag / models / charts …）は brain.py が
# 自分自身を登録する。下の「import brain」より後なら、そちらも使える。
for _alias in ("db", "filecheck", "chats", "history", "catalog_history",
               "prefs", "catalog", "verify", "sqlusage", "importer",
               "jobs", "scheduler", "cleanup", "web"):
    _sys.modules[_alias] = _sys.modules[__name__]
del _alias

# 直起動（python core.py）だとこのモジュール名は "__main__" になる。
# "core" も同じ実体に向けておかないと、あとから import core が走ったときに
# 同じファイルがもう1回読み込まれ、スケジューラ等が二重に立つ。
# ファイルが3本に分かれたので、brain を読み込むより前にここで済ませる。
_sys.modules.setdefault("core", _sys.modules[__name__])

# 画面の素材（HTML・CSS・JS）。ロジックが無く量だけ多いので別ファイル。
from assets import STATIC_FILES, TEMPLATES  # noqa: E402,F401


# ==========================================================================
# ===== 元 db.py
# SQLite アクセス層（複数DB対応）。
#
# data/ フォルダの .db ファイルを列挙し、選択されたDB群を読み取り専用で
# ATTACH した1つの接続に対して SELECT を実行する。複数DBを選択した場合は
# `エイリアス.テーブル名` でファイルをまたいだ JOIN が可能。
#
# 最重要: ユーザー(LLM)が生成したSQLは SELECT のみ 実行を許可する。
# 多層防御で守る:
#   1. 構文チェック   : 単一ステートメント / SELECT・WITH で始まる / 書込キーワード禁止
#   2. 読み取り専用接続: mode=ro で ATTACH するのでそもそも書込不可
#   3. オーソライザ    : SQLite の authorizer で SELECT/READ 以外を DENY
#   4. タイムアウト    : progress handler で暴走クエリを中断
# ==========================================================================
import re
import sqlite3
import time
from pathlib import Path

import config

# --- data/ フォルダのDBファイル ----------------------------------------------

def list_db_files() -> list[Path]:
    """data/ 直下の .db ファイル一覧（名前順）。"""
    if not config.DATA_DIR.exists():
        return []
    return sorted(p for p in config.DATA_DIR.glob("*.db") if p.is_file())


def path_for(name) -> Path:
    """画面から渡されたDB名を data/ の実ファイルに解決する。

    名前を data/ に連結するのではなく、列挙済みの一覧から名前が一致するものを
    探す。こうしておくと "../" のような指定が入っても data/ の外には出ない。
    """
    target = Path(str(name or "")).name          # ディレクトリ部分は捨てる
    for p in list_db_files():
        if p.name == target:
            return p
    raise FileNotFoundError(f"DBが見つかりません: {name}")


# 記号と空白だけを潰す。日本語などのマルチバイト文字はそのまま残す
# （SQLiteは非ASCIIの識別子をクオート無しで扱えるので、"売上.db" は 売上.受注 と書ける）。
# ここでASCIIだけに絞ると「店舗マスタ」が "_____" になり、
# 複数の日本語DBを選んだときに区別できなくなる。
_ALIAS_BAD = re.compile(r"[^\w]", re.UNICODE)
_RESERVED_ALIASES = {"main", "temp"}


def alias_for(path: Path) -> str:
    """ファイル名から SQL で使うエイリアス名（英数字と_のみ）を作る。"""
    a = _ALIAS_BAD.sub("_", Path(path).stem)
    if not a or a[0].isdigit():
        a = "db_" + a
    if a.lower() in _RESERVED_ALIASES:
        a += "_db"
    return a


def aliases_for(paths: list[Path]) -> list[str]:
    """複数ファイルに一意なエイリアスを割り当てる（衝突時は連番を付ける）。"""
    result: list[str] = []
    used: set[str] = set()
    for p in paths:
        a = alias_for(p)
        base, n = a, 2
        while a.lower() in used:
            a = f"{base}_{n}"
            n += 1
        used.add(a.lower())
        result.append(a)
    return result


# --- 接続ヘルパ ---------------------------------------------------------------

def _ro_uri(path) -> str:
    return Path(path).resolve().as_uri() + "?mode=ro"


def connect_ro(path) -> sqlite3.Connection:
    """単一DBへの読み取り専用接続（プロファイリング用）。"""
    return sqlite3.connect(_ro_uri(path), uri=True)


# SQLiteが同時にATTACHできる数の上限（既定10）。main を1つ使うので実質これだけ。
MAX_ATTACHED = 10


def connect_scope(paths_aliases: list[tuple]) -> sqlite3.Connection:
    """空の :memory: を main とし、各DBを読み取り専用で ATTACH した接続を作る。

    paths_aliases: [(path, alias), ...]
    """
    if len(paths_aliases) > MAX_ATTACHED:
        raise ValueError(
            f"1つのSQLで扱えるDBは{MAX_ATTACHED}個までです"
            f"（この問い合わせは{len(paths_aliases)}個を必要としています）。SQLiteの制限です。"
            "テーブル名を『DB名.テーブル名』の形で書けば、実際に使うDBだけを繋ぐので"
            "多くの場合はこの制限に当たりません。")
    conn = sqlite3.connect("file::memory:", uri=True)
    for path, alias in paths_aliases:
        # alias は英数字と_のみに正規化済みなので識別子として安全
        conn.execute(f'ATTACH DATABASE ? AS "{alias}"', (_ro_uri(path),))
    return conn


def dbs_named_in(sql: str) -> list[str]:
    """SQLが「エイリアス.」の形で名指ししているDBファイル名。"""
    out = []
    for p in list_db_files():
        a = alias_for(p)
        if a and re.search(r'(?<![\w."])' + re.escape(a) + r'\s*\.', sql, re.IGNORECASE):
            out.append(p.name)
    return out


def widen_scope(sql: str, scope: list[dict]) -> list[dict]:
    """SQLが必要とするDBを、選ばれていなくても繋ぐ。

    ユーザー定義ツールは作った人がDBを意識せずに書くので、SQLが別DBに入ることがある。
    選択中のDBだけを繋ぐと、正しいツールが "no such table" で落ちる。
    読むだけであり、DBの選択はもともと「見る範囲を絞る」ためのもので
    アクセス制御ではない（README参照）ため、必要なものは繋いでよい。

    ATTACH の上限があるので、そこで打ち止める（超えた分は元のエラーで気づける）。
    """
    out = list(scope or [])
    have = {str(s.get("alias") or "").lower() for s in out}
    for p in list_db_files():
        if len(out) >= MAX_ATTACHED:
            break
        a = alias_for(p)
        if a.lower() in have:
            continue
        if re.search(r'(?<![\w."])' + re.escape(a) + r'\s*\.', sql, re.IGNORECASE):
            out.append({"path": str(p), "alias": a, "name": p.name, "tables": None})
            have.add(a.lower())
    return out


def narrow_scope(sql: str, scope: list[dict]) -> list[dict]:
    """そのSQLに関係するDBだけに絞る。

    選択中のDBを全部つなぐ必要はない。SQLiteは一度に10個までしかATTACHできないので、
    11個以上選んでいると、2つのテーブルを見るだけの問い合わせも実行できなくなっていた。
    「エイリアス.テーブル」で名指しされたDBと、修飾なしのテーブル名が一致するDBだけを残す。

    どちらでも判断できないときは、今までどおり全部を返す（勝手に減らして
    「no such table」にするより、元の分かりやすいエラーの方がよい）。
    """
    if len(scope) <= 1:
        return scope

    picked, seen = [], set()

    def add(s):
        key = str(s.get("path"))
        if key not in seen:
            seen.add(key)
            picked.append(s)

    # 名指しされているDB（複数DBを選んでいるときは必ずこの形で書かせている）
    for s in scope:
        alias = str(s.get("alias") or "")
        if alias and re.search(r'(?<![\w."])' + re.escape(alias) + r'\s*\.',
                               sql, re.IGNORECASE):
            add(s)
    # 修飾なしのテーブル名で参照されているDB。上と混在したSQLでも取りこぼさない
    for s in scope:
        for t in (s.get("tables") or []):
            if re.search(r'(?<![\w."])' + re.escape(str(t)) + r'(?![\w"])',
                         sql, re.IGNORECASE):
                add(s)
                break

    return picked[:MAX_ATTACHED] if picked else scope


# --- SELECT 専用ガード --------------------------------------------------------

# replace はここに入れない。SQLite の replace(X,Y,Z) は文字列関数で、
# 「株式会社」を落とすといった用途でごく普通に使う。書き込みになるのは
# REPLACE INTO の形だけなので、それは下で別に見る。
_FORBIDDEN = re.compile(
    r"\b(insert|update|delete|drop|alter|create|truncate|attach|detach|"
    r"reindex|vacuum|pragma|grant|revoke|begin|commit|rollback|savepoint|merge)\b",
    re.IGNORECASE,
)
_REPLACE_INTO = re.compile(r"\breplace\s+into\b", re.IGNORECASE)

#: SQLite自身の管理表と、その代わりになる仕組み。
#: sqlite_master には全テーブル・全ビューの名前とCREATE文が入っているので、
#: 読めると「対象から外した表」の名前と定義まで見えてしまう。
_SCHEMA_TABLE = re.compile(r"\bsqlite_(master|schema|temp_master|temp_schema|"
                           r"sequence|stat\d*)\b|\bpragma_\w+", re.IGNORECASE)

#: 文字列リテラルと引用符付き識別子。'' や "" のエスケープも1つの塊として食う。
_QUOTED = re.compile(r"'(?:[^']|'')*'|\"(?:[^\"]|\"\")*\"|`(?:[^`]|``)*`|\[[^\]]*\]")


def _strip_sql_comments(sql: str) -> str:
    """コメントを外す。**必ず _blank_quoted を通した後に呼ぶこと。**

    生のSQLに当てると、値の中の -- や /* */ まで消してしまう。
    """
    sql = re.sub(r"--[^\n]*", " ", sql)                     # 行コメント
    sql = re.sub(r"/\*.*?\*/", " ", sql, flags=re.DOTALL)   # ブロックコメント
    return sql


def _trim_tail(sql: str) -> str:
    """前後の空白と、末尾に並んだ ';' を落とす。"""
    return sql.strip().rstrip(";").strip()


def _blank_quoted(sql: str) -> str:
    """引用符で囲まれた中身を空にした、検査用のコピーを作る。

    キーワードや ';' をそのまま探すと、値の中の文字まで拾ってしまう。
    WHERE status = 'delete' や WHERE note = ';' が「危険なSQL」として
    弾かれていた。実行するのは元のSQLで、これは検査にしか使わない。
    """
    return _QUOTED.sub(lambda m: m.group(0)[0] + m.group(0)[-1], sql)


def validate_select(sql: str) -> str:
    """SELECT文として安全か検証し、整形済みSQLを返す。問題があれば ValueError。

    実行するのは「コメントを残したままの元のSQL」。コメント除去は検査用の
    コピーにしか使わない。値の中の -- や /* */ まで消してしまうため:
      SELECT '2024/*x*/end'      → 除去すると '2024 end' になり、黙って値が変わる
      WHERE note = 'foo -- bar'  → 除去すると引用符が閉じず構文エラーになる
    除去の順序も逆にできない。先に引用符の中身を空にしてからコメントを外す。
    そうしないと、リテラルの中の -- をコメントの開始と誤認する。
    """
    if not sql or not sql.strip():
        raise ValueError("SQLが空です。")
    cleaned = _trim_tail(sql)
    if not cleaned:
        raise ValueError("実行可能なSQLがありません。")
    # 検査用: 引用符の中身を空に → その上でコメントを外す → 末尾の ; を落とす
    probe = _trim_tail(_strip_sql_comments(_blank_quoted(cleaned)))
    if not probe:
        raise ValueError("実行可能なSQLがありません。")
    if ";" in probe:
        raise ValueError("複数ステートメントは実行できません(SELECT文を1つだけ指定してください)。")
    low = probe.lower()
    if not (low.startswith("select") or low.startswith("with")):
        raise ValueError("SELECT文(または WITH ... SELECT)のみ実行できます。")
    m = _FORBIDDEN.search(probe) or _REPLACE_INTO.search(probe)
    if m:
        raise ValueError(f"書き込み・DDL系のキーワード '{m.group(0)}' は使用できません。読み取り専用です。")
    m = _SCHEMA_TABLE.search(probe)
    if m:
        # ここはLLMにも返る文面。代わりに何を見ればよいかまで書く
        raise ValueError(
            f"SQLiteの管理表 '{m.group(0)}' は読めません。"
            "テーブルの一覧・列の名前・型は、データカタログの説明として"
            "すでに渡されています。そちらを見てください。")
    return cleaned


# SQLite オーソライザで許可するアクション
_ALLOWED_ACTIONS = {sqlite3.SQLITE_SELECT, sqlite3.SQLITE_READ, sqlite3.SQLITE_FUNCTION}
for _name in ("SQLITE_RECURSIVE",):  # 環境によって存在しない場合がある
    if hasattr(sqlite3, _name):
        _ALLOWED_ACTIONS.add(getattr(sqlite3, _name))


def _names_in(text: str, name: str) -> bool:
    r"""その文章（SQL）が、この名前を1語として挙げているか。

    表名は日本語を含むので \w は Unicode のまま使う。英数字だけで境界を見ると
    「品質__x」が「高品質__x」の一部に当たる。
    """
    # SQLの識別子は大小を区別しない。区別して探すと、定義に 品質__CLAIMS と
    # 書かれたビューの元表が「読んでよい表」に入らず、読んだ瞬間に断られる
    return bool(re.search(r'(?<![\w."])"?' + re.escape(name) + r'"?(?![\w])',
                          text, re.IGNORECASE))


def _view_closure(conn, aliases: list, allowed: set | None, sql: str = "") -> set:
    """このSQLが名指ししているビューの定義が、たどり着く表・ビューを全部集める。

    ビューは実体を持たないので、読むと必ず元の表でも SQLITE_READ が飛ぶ。
    ビューがビューを参照することもあるため、増えなくなるまでたどる。

    sql を渡すと、**そのSQLに名前が出てくるビュー**からだけたどる。
    ビューは名前を書かなければ読めないので、名前が出てこないなら元表を通す
    理由が無い。ここを絞らないと、入れ子のビューのために開けてある穴
    （列名が空の READ を通す）から、対象外の表の COUNT(*) が読めてしまう。
    """
    if not allowed:
        return set()
    views: dict = {}          # ビュー名 → 定義SQL
    names: set = set()        # 表とビューの全名前
    for a in aliases:
        try:                  # alias は英数字と_のみに正規化済み
            rows = conn.execute(
                f'SELECT name, type, sql FROM "{a}".sqlite_master '
                f"WHERE type IN ('table','view')").fetchall()
        except sqlite3.Error:
            continue
        for n, t, body in rows:
            names.add(str(n))
            if t == "view":
                views[str(n)] = str(body or "")
    out: set = set()
    todo = [v for v in allowed if v in views and (not sql or _names_in(sql, v))]
    seen: set = set()
    while todo:
        v = todo.pop()
        if v in seen:
            continue
        seen.add(v)
        body = views.get(v, "")
        for n in names:
            if n == v or n in out:
                continue
            if _names_in(body, n):
                out.add(n)
                if n in views:
                    todo.append(n)
    return out


def _make_authorizer(allowed: set | None, via_view: set | None = None):
    """SELECT専用ガード。allowed を渡すと、その表以外は読ませない。

    サイドバーで対象から外した表を、SQLiteが実際に読む一歩手前で止める。
    プロンプトから消すだけでは、AIが名前を覚えている・推測できる場合に
    読めてしまうため、最後の関門はデータ層に置く。

    via_view は「許可したビューが内部で読む表」。ここに入っている表は
    ビュー経由のときだけ通す（第5引数 trigger にビュー名が入るのが目印）。
    無条件に通すと、対象から外した表を直に名指しして読めてしまう。
    """
    # SQLiteは「SQLに書かれたとおりの綴り」で名前を渡してくる。ビューの定義が
    # 品質__CLAIMS と書いていれば、許可の一覧に 品質__claims があっても
    # そのままでは一致しない。SQLが同じ表として扱うものは、ここでも同じとみなす
    allow_ci = None if allowed is None else {str(x).lower() for x in allowed}
    via_ci = {str(x).lower() for x in (via_view or ())}

    def _authorizer(action, arg1, arg2, db_name, trigger):
        if action not in _ALLOWED_ACTIONS:
            return sqlite3.SQLITE_DENY
        # SQLite自身の管理表（sqlite_master など）は、絞り込みの有無によらず読ませない。
        # 全テーブル・全ビューの名前とCREATE文が入っているので、読めると
        # 「対象から外した表」の存在と定義が分かってしまう。
        # 内部の解決には使われない（普通のSELECTでもビュー経由でも飛んでこないことを実測）。
        if action == sqlite3.SQLITE_READ and str(arg1 or "").startswith("sqlite_"):
            return sqlite3.SQLITE_DENY
        # SQLITE_READ は (テーブル名, 列名)。対象外の表なら止める
        if allowed is not None and action == sqlite3.SQLITE_READ and arg1:
            name = str(arg1).lower()
            if name in allow_ci:
                return sqlite3.SQLITE_OK
            # ビューの中身を読んでいる最中だけ、その定義が使う表を通す。
            # 列名が空の READ は「その表を参照する」ことの照会で、値は読まない
            # （COUNT(*) や入れ子のビューの解決で trigger 無しに飛んでくる）。
            # これも via_view に入っている名前に限って通す。
            if via_ci and name in via_ci and (trigger or not arg2):
                return sqlite3.SQLITE_OK
            return sqlite3.SQLITE_DENY
        return sqlite3.SQLITE_OK
    return _authorizer


# SQLiteに無い関数 → 代わりに使うもの。
# エラーメッセージにこれを添えないと、LLMは同じ関数で何度も書き直す。
_MISSING_FUNC_HINTS = {
    "stddev": "analyze_stats(method='describe')", "stdev": "analyze_stats(method='describe')",
    "stddev_samp": "analyze_stats(method='describe')",
    "variance": "analyze_stats(method='describe')", "var_samp": "analyze_stats(method='describe')",
    "median": "analyze_stats(method='describe')",
    "percentile": "analyze_stats(method='describe')",
    "percentile_cont": "analyze_stats(method='describe')",
    "percentile_disc": "analyze_stats(method='describe')",
    "corr": "analyze_stats(method='correlation')",
    "regr_slope": "regression", "stddev_pop": "analyze_stats(method='describe')",
    "sqrt": "analyze_stats か advanced 系のツール",
    "power": "掛け算で書き換える（x*x など）",
    "date_trunc": "strftime('%Y-%m', 列) など strftime を使う",
    "now": "date('now') / datetime('now')",
    "year": "strftime('%Y', 列)", "month": "strftime('%m', 列)",
    "day": "strftime('%d', 列)", "concat": "|| で連結する",
    "ifnull_": "IFNULL は使える", "listagg": "group_concat",
    "string_agg": "group_concat", "top": "LIMIT",
}


def explain_error(e: Exception) -> str:
    """SQLの失敗を、次に何をすればよいかまで書いた文にする。"""
    msg = str(e)
    m = re.search(r"no such function:\s*([A-Za-z_0-9]+)", msg)
    if m:
        fn = m.group(1)
        hint = _MISSING_FUNC_HINTS.get(fn.lower())
        if hint:
            return (f"{msg} … SQLite には {fn}() がありません。"
                    f"SQLで書き直そうとせず、{hint} を使ってください。")
        return (f"{msg} … SQLite には {fn}() がありません。"
                "標準のSQLite関数だけで書き直すか、専用の分析ツールを使ってください。")
    m = re.search(r"no such column:\s*(\S+)", msg)
    if m:
        return (f"{msg} … 列名が違います。describe_table でテーブルの列を確認してから"
                "書き直してください（推測で列名を作らないこと）。")
    if "syntax error" in msg:
        return (f"{msg} … SQLite で解釈できない書き方です。"
                "ウィンドウ関数の一部・WITHIN GROUP・PIVOT などは使えません。"
                "集計や統計は専用ツール（pivot_table / analyze_stats）に任せてください。")
    return msg


def run_select(sql: str, scope: list[dict], max_rows: int | None = None,
               timeout_s: int | None = None, params: dict | None = None):
    """検証済みSELECTを、選択スコープのDB群に対して実行する。

    scope:  [{"path": str, "alias": str, "tables": [...]}, ...]
            tables があれば、その表しか読めない（利用者がサイドバーで
            対象から外した表を、ここで確実に止める）
    params: バインド変数（:name）に渡す値。値はSQL文字列に埋め込まれず
            プレースホルダ経由で渡るため、SQLインジェクションは起こらない。
    戻り値: (columns, rows, truncated)
    """
    if not scope:
        # ここはLLMにも返る文面。DBの用意を促すだけだと、AIは「出力できません」と
        # 答えて止まってしまう。DBに無いデータを出す道（rows）があることを教える。
        raise ValueError(
            "対象のDBがありません。SQLは実行できません。"
            "出力したい内容が手元にある（文書を調べた・自分で整理した）なら、"
            "sql の代わりに rows で表をそのまま渡して呼び直すこと。"
            "DBのデータが必要なら、data/ にDBを置くよう利用者に案内する。")
    safe_sql = validate_select(sql)
    max_rows = max_rows or config.MAX_RESULT_ROWS
    timeout_s = timeout_s or config.QUERY_TIMEOUT_SEC

    # 選択中のDBを全部つながない。このSQLが要るものだけを繋ぐ（ATTACHは10個まで）
    use = narrow_scope(safe_sql, scope)
    # 「読んでよい表」。scope が表を持っていないDBが1つでもあれば制限しない
    allowed: set | None = set()
    for s_ in use:
        if s_.get("tables"):
            allowed |= set(s_["tables"])
        else:
            allowed = None
            break

    conn = connect_scope([(s["path"], s["alias"]) for s in use])
    try:
        # ビューを選んでいるときは、その定義が読む表も（ビュー経由に限り）通す。
        # 接続してからでないと定義を読めないので、ここで組み立てる。
        conn.set_authorizer(_make_authorizer(
            allowed, _view_closure(conn, [s["alias"] for s in use], allowed, safe_sql)))
        start = time.time()
        conn.set_progress_handler(lambda: 1 if (time.time() - start) > timeout_s else 0, 10000)
        try:
            cur = conn.execute(safe_sql, params or {})  # 単一ステートメントのみ実行可能
        except sqlite3.Error as e:
            # 「何が悪いか」だけでなく「代わりに何を使うか」まで返す
            raise sqlite3.OperationalError(explain_error(e)) from e
        columns = [d[0] for d in cur.description] if cur.description else []
        rows = cur.fetchmany(max_rows + 1)
        truncated = len(rows) > max_rows
        rows = [tuple(r) for r in rows[:max_rows]]
        return columns, rows, truncated
    finally:
        conn.close()


def _sql_guard_selftest() -> int:
    """SELECT専用ガード + ATTACH横断クエリのセルフテスト（python core.py selftest で実行）。"""
    import tempfile, os

    ok_cases = [
        "SELECT 1",
        "select a.x from t a join u b on a.id=b.id",
        "WITH t AS (SELECT 1 AS a) SELECT a FROM t",
        # 文字列リテラルの中のキーワードや記号で弾かないこと
        "SELECT replace(name,'株式会社','') FROM t",
        "SELECT * FROM t WHERE x='delete me'",
        "SELECT * FROM t WHERE note=';'",
        "SELECT * FROM t WHERE s='don''t drop it'",
        'SELECT "delete" FROM t',
    ]
    ng_cases = [
        "DELETE FROM t",
        "DROP TABLE t",
        "UPDATE t SET x=1",
        "SELECT 1; DELETE FROM t",
        "INSERT INTO t VALUES(1)",
        "PRAGMA table_info(t)",
        "ATTACH DATABASE 'x.db' AS z",
        "REPLACE INTO t VALUES(1)",
        "SELECT * FROM t WHERE x='a'; DROP TABLE t",
    ]
    for s in ok_cases:
        validate_select(s)
        print("OK   ", s)
    for s in ng_cases:
        try:
            validate_select(s)
            print("!! ガードすり抜け:", s)
        except ValueError as e:
            print("BLOCK", s, "=>", e)

    # ATTACH 横断クエリ
    d = tempfile.mkdtemp()
    p1, p2 = os.path.join(d, "a.db"), os.path.join(d, "b.db")
    c = sqlite3.connect(p1); c.execute("CREATE TABLE t(id INTEGER, v TEXT)")
    c.execute("INSERT INTO t VALUES(1,'x'),(2,'y')"); c.commit(); c.close()
    c = sqlite3.connect(p2); c.execute("CREATE TABLE u(id INTEGER, w TEXT)")
    c.execute("INSERT INTO u VALUES(1,'A'),(2,'B')"); c.commit(); c.close()
    scope = [{"path": p1, "alias": "a"}, {"path": p2, "alias": "b"}]
    cols, rows, tr = run_select("SELECT t.v, u.w FROM a.t t JOIN b.u u ON t.id=u.id", scope)
    print("CROSS-DB JOIN:", cols, rows)
    # 書込は物理的に拒否されるか
    try:
        run_select("SELECT 1", scope)  # ガード通過の確認
        conn = connect_scope([(p1, "a")])
        conn.execute("INSERT INTO a.t VALUES(9,'z')")
        print("!! 読み取り専用が効いていない")
        return 1
    except sqlite3.OperationalError as e:
        print("RO-GUARD:", e)
    return 0


# ==========================================================================
# ===== 元 filecheck.py
# そのファイルが「そのまま取り込める表」かを判定する。
#
# 取り込みは 1行=1レコード / 1列=1項目 の素直な表を前提にしている。
# ところが現場のExcelは、見出しがセル結合されていたり、月が横に並んでいたり、
# 合計行が混ざっていたりする。そのまま取り込むと、列名が「Unnamed: 3」になったり、
# 合計が二重に数えられたりして、後の集計が静かに狂う。
#
# ここでは中身を読む前に形を見て、次のどれかを返す。
#   そのまま取り込める / 手直しが要る / 取り込みに向かない / 対応していない形式
#
# 判定は「取り込みボタンを押す前に気づけるようにする」ためのもので、
# 最終的に決めるのは人。だから理由と直し方を必ず添える。
# ==========================================================================
import csv
import re
from pathlib import Path

import config

#: 形を見るために読む最大行数。これ以上は見なくても判断できる。
MAX_SCAN_ROWS = 200
#: 見出し行を探す範囲（先頭から何行目まで）。
HEADER_SEARCH_ROWS = 12
#: 結合セルの調査は通常読み込みが要る（メモリを食う）ので、この大きさまで。
MERGE_CHECK_MAX_MB = 20

#: 合計・小計の行に出やすい言葉。混ざったまま取り込むと二重計上になる。
_TOTAL_WORDS = ("合計", "総計", "小計", "計", "累計", "total", "subtotal", "sum")
#: 見出しが日付・期間になっている＝横持ち（クロス表）の目印
_PERIOD_RE = re.compile(
    r"^\s*(?:"
    r"(?:19|20)\d{2}[-/年.]?(?:0?[1-9]|1[0-2])?[月]?"      # 2026-04 / 2026年4月
    r"|(?:0?[1-9]|1[0-2])月"                                # 4月
    r"|[QＱ][1-4]|第[1-4一二三四]四半期"                     # Q1 / 第1四半期
    r"|上期|下期|上半期|下半期"
    r")\s*$")


def _blank(v) -> bool:
    return v is None or str(v).strip() == ""


def _issue(level: str, text: str, fix: str = "") -> dict:
    return {"level": level, "text": text, "fix": fix}


# =============================================================================
# ファイルを「素の格子」として読む（見出しがどこかは、まだ決めつけない）
# =============================================================================

def _grid_excel(path: Path, sheet: str | None) -> tuple:
    import openpyxl

    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    try:
        names = list(wb.sheetnames)
        target = sheet if (sheet and sheet in names) else names[0]
        ws = wb[target]
        rows = []
        for i, row in enumerate(ws.iter_rows(values_only=True)):
            if i >= MAX_SCAN_ROWS:
                break
            rows.append(list(row))
        return rows, names, target
    finally:
        wb.close()


def _merged_ranges(path: Path, sheet: str) -> list | None:
    """結合セルの範囲。読み取り専用モードでは取れないので通常読み込みする。

    大きいファイルで開くと重いので、その場合は調べずに None を返す
    （「分からなかった」と「無かった」を混同しないため）。
    """
    try:
        if path.stat().st_size > MERGE_CHECK_MAX_MB * 1024 * 1024:
            return None
    except OSError:
        return None
    try:
        import openpyxl
        wb = openpyxl.load_workbook(path, read_only=False, data_only=True)
        try:
            ws = wb[sheet] if sheet in wb.sheetnames else wb[wb.sheetnames[0]]
            return [(r.min_row, r.min_col, r.max_row, r.max_col)
                    for r in ws.merged_cells.ranges]
        finally:
            wb.close()
    except Exception:
        return None


def _grid_text(path: Path) -> tuple:
    """CSV/TSV/TXT。区切り文字と文字コードもここで見当をつける。"""
    from importer import CSV_ENCODINGS

    raw = None
    for enc in CSV_ENCODINGS:
        try:
            raw = path.read_text(encoding=enc)
            used = enc
            break
        except (UnicodeDecodeError, OSError):
            continue
    if raw is None:
        raise ValueError("文字コードを判定できませんでした（UTF-8 か Shift_JIS で保存し直してください）。")

    head = "\n".join(raw.splitlines()[:MAX_SCAN_ROWS])
    if path.suffix.lower() == ".tsv":
        delim = "\t"
    else:
        try:
            delim = csv.Sniffer().sniff(head[:4000], delimiters=",\t;|").delimiter
        except csv.Error:
            delim = "\t" if head.count("\t") > head.count(",") else ","
    rows = [r for r in csv.reader(head.splitlines(), delimiter=delim)]
    return rows, used, delim


# =============================================================================
# 形を見る
# =============================================================================

def _guess_header(rows: list) -> int:
    """見出しの行番号（0始まり）を当てる。

    「文字が並んでいて、その下に中身が続いている行」を見出しとみなす。
    タイトル行（1セルだけ埋まっている）や空行は飛ばす。
    """
    best, best_score = 0, -1.0
    for i, row in enumerate(rows[:HEADER_SEARCH_ROWS]):
        filled = [v for v in row if not _blank(v)]
        if len(filled) < 2:
            continue                       # タイトル行や空行
        below = rows[i + 1] if i + 1 < len(rows) else []
        if not [v for v in below if not _blank(v)]:
            continue                       # 下に中身が無いなら見出しではない
        texty = sum(1 for v in filled if not _looks_number(v))
        # 埋まり具合＋文字らしさ。上の行ほど見出しらしいので少し優遇する
        score = (len(filled) / max(len(row), 1)) + (texty / len(filled)) - i * 0.06
        if score > best_score:
            best, best_score = i, score
    return best


def _looks_number(v) -> bool:
    s = str(v).strip().replace(",", "")
    if not s:
        return False
    try:
        float(s)
        return True
    except ValueError:
        return False


def _is_total_row(row: list) -> bool:
    head = " ".join(str(v) for v in row[:2] if not _blank(v)).strip().lower()
    return bool(head) and any(w in head for w in _TOTAL_WORDS)


def _analyze(rows: list, header_row: int) -> dict:
    """見出し行を決めた上で、中身の形を調べる。"""
    header = rows[header_row] if header_row < len(rows) else []
    body = rows[header_row + 1:]
    width = max((len(r) for r in rows), default=0)

    names = [("" if _blank(v) else str(v).strip()) for v in header]
    names += [""] * (width - len(names))

    empty_names = [i for i, n in enumerate(names) if not n]
    dup = sorted({n for n in names if n and names.count(n) > 1})
    period_cols = [n for n in names if n and _PERIOD_RE.match(n)]
    numeric_names = [n for n in names if n and _looks_number(n)]

    blank_rows = sum(1 for r in body if all(_blank(v) for v in r))
    total_rows = [i for i, r in enumerate(body) if _is_total_row(r)]
    ragged = sum(1 for r in body if len([v for v in r if not _blank(v)]) > len(names))
    multiline = any(isinstance(v, str) and "\n" in v for r in body[:50] for v in r)

    # 全部空の列（見出しだけあって中身が無い／見出しも中身も無い）
    empty_cols = []
    for c in range(width):
        col = [r[c] for r in body if c < len(r)]
        if col and all(_blank(v) for v in col):
            empty_cols.append(names[c] or f"{c + 1}列目")

    # 数字と文字が混ざる列（"-" や "N/A" が入ると、数値として取り込めない）
    mixed = []
    for c in range(width):
        col = [r[c] for r in body if c < len(r) and not _blank(r[c])]
        if len(col) < 4:
            continue
        nums = sum(1 for v in col if _looks_number(v))
        if 0.6 <= nums / len(col) < 1.0:
            odd = [str(v) for v in col if not _looks_number(v)][:3]
            mixed.append((names[c] or f"{c + 1}列目", odd))

    return {
        "names": names, "width": width, "body_rows": len(body),
        "empty_names": empty_names, "dup_names": dup,
        "period_cols": period_cols, "numeric_names": numeric_names,
        "blank_rows": blank_rows, "total_rows": total_rows,
        "ragged": ragged, "multiline": multiline,
        "empty_cols": empty_cols, "mixed": mixed,
    }


def _blocks(rows: list, header_row: int) -> int:
    """1シートに表がいくつ入っていそうか（空行で切れて、また見出しが始まる）。"""
    blocks, in_block, gap = 1, True, 0
    for r in rows[header_row + 1:]:
        if all(_blank(v) for v in r):
            gap += 1
            in_block = False
        else:
            if not in_block and gap >= 2:
                blocks += 1
            in_block, gap = True, 0
    return blocks


# =============================================================================
# 判定
# =============================================================================

def inspect_file(path, sheet: str | None = None) -> dict:
    """1ファイル（Excelは1シート）の形を見て、取り込めるかを判定する。

    名前を inspect ではなく inspect_file にしているのは、後ろの画面セクションが
    標準ライブラリの inspect を使うため。1ファイルに統合してスコープが1つに
    なった今、同じ名前だと後から書かれた import が勝ってこの関数が消える。
    """
    p = Path(path)
    ext = p.suffix.lower()
    out = {"file": p.name, "sheet": sheet, "sheets": [], "header_row": 0,
           "verdict": "", "issues": [], "shape": {}}

    if ext not in config.IMPORT_EXTENSIONS:
        out["verdict"] = "対応していない形式"
        out["issues"] = [_issue(
            "高", f"{ext or '拡張子なし'} は取り込みに対応していません。",
            f"扱えるのは {'、'.join(config.IMPORT_EXTENSIONS)} です。"
            "元のシステムからCSVで出し直すか、Excelで開いて「名前を付けて保存」で"
            ".xlsx か .csv にしてください。")]
        return out

    try:
        if ext in (".xlsx", ".xlsm"):
            rows, names, target = _grid_excel(p, sheet)
            out["sheets"], out["sheet"] = names, target
            merged = _merged_ranges(p, target)
        else:
            rows, enc, delim = _grid_text(p)
            merged = []
            out["encoding"] = enc
            out["delimiter"] = {"\t": "タブ", ",": "カンマ", ";": "セミコロン",
                                "|": "パイプ"}.get(delim, delim)
    except Exception as e:
        out["verdict"] = "取り込みに向かない"
        out["issues"] = [_issue("高", f"ファイルを開けませんでした: {e}",
                                "壊れているか、パスワードが掛かっている可能性があります。")]
        return out

    rows = [r for r in rows if r is not None]
    if not any(any(not _blank(v) for v in r) for r in rows):
        out["verdict"] = "取り込みに向かない"
        out["issues"] = [_issue("高", "中身が空です。", "データの入ったファイルを指定してください。")]
        return out

    header_row = _guess_header(rows)
    info = _analyze(rows, header_row)
    blocks = _blocks(rows, header_row)
    out["header_row"] = header_row
    out["shape"] = {"列数": info["width"], "読んだ行数": info["body_rows"],
                    "見出し行": header_row + 1}
    out["columns"] = info["names"]

    issues: list[dict] = []

    # --- そのままでは取り込めないもの ---------------------------------------
    if merged:
        hrow = header_row + 1                    # 1始まりの行番号にそろえる
        # 見出しの行と、そのすぐ上をまたぐ横方向の結合＝多段見出し。
        # いちばん上のタイトル行（1セルだけの飾り）は、これに含めない。
        in_header = [m for m in merged
                     if m[1] != m[3] and m[0] <= hrow and m[2] >= hrow - 1
                     and not (m[0] == m[2] == 1 and hrow > 2)]
        in_body = [m for m in merged if m[0] > hrow]
        if in_header:
            issues.append(_issue(
                "高", f"見出しがセル結合されています（{len(in_header)}箇所）。"
                      "多段の見出しは1行の列名にできません。",
                "結合を解除し、見出しを1行にまとめてください"
                "（例:「上期／4月」→「上期_4月」）。"))
        if in_body:
            issues.append(_issue(
                "高", f"データ部分にセル結合があります（{len(in_body)}箇所）。"
                      "結合されたセルは先頭以外が空になり、行が正しく揃いません。",
                "結合を解除し、空いたセルに同じ値を埋めてください。"))

    if len(info["period_cols"]) >= 3:
        issues.append(_issue(
            "高", f"月や期間が横に並んでいます（{'、'.join(info['period_cols'][:5])}…）。"
                  "いわゆるクロス表で、1行=1レコードになっていません。",
            "「年月」「値」の2列に縦持ちへ直してください"
            "（Excelなら [データ]→[パワークエリ]→[列のピボット解除]）。"))
    elif len(info["numeric_names"]) >= 3:
        issues.append(_issue(
            "高", f"見出しが数字になっています（{'、'.join(info['numeric_names'][:5])}…）。"
                  "見出し行の位置が違うか、横持ちの表の可能性があります。",
            "1行目に列名が来るようにしてください。"))

    if blocks > 1:
        issues.append(_issue(
            "高", f"1つのシートに表が{blocks}個あるように見えます（間に空行があります）。",
            "表ごとにシートを分けてください。取り込みは1シート=1テーブルです。"))

    # --- 直せば取り込めるもの ------------------------------------------------
    if header_row > 0:
        issues.append(_issue(
            "中", f"{header_row + 1}行目が見出しに見えます（1行目ではありません）。"
                  "上にタイトルや空行が入っています。",
            f"取り込み画面の「見出しの行」に {header_row + 1} を指定するか、"
            "上の行を削除してください。"))

    if info["total_rows"]:
        issues.append(_issue(
            "中", f"合計・小計らしい行が {len(info['total_rows'])} 行あります。"
                  "そのまま取り込むと二重に数えられます。",
            "合計行を削除してから取り込んでください（集計はアプリ側でできます）。"))

    if info["empty_names"]:
        issues.append(_issue(
            "中", f"列名が空の列が {len(info['empty_names'])} 個あります。",
            "列名を付けてください（空のままだと自動で仮の名前が付きます）。"))

    if info["dup_names"]:
        issues.append(_issue(
            "中", f"同じ列名が複数あります: {'、'.join(info['dup_names'][:5])}",
            "区別できる名前に変えてください（取り込み時は連番が付きます）。"))

    if info["ragged"]:
        issues.append(_issue(
            "中", f"見出しより列が多い行が {info['ragged']} 行あります。"
                  "区切り文字がデータの中に入っている可能性があります。",
            "その列を引用符で囲むか、区切り文字を変えて出し直してください。"))

    # --- 気に留めておく程度 --------------------------------------------------
    for name, odd in info["mixed"][:3]:
        issues.append(_issue(
            "低", f"「{name}」は数字の列に見えますが、文字が混ざっています"
                  f"（{'、'.join(odd)}）。",
            "空欄や「-」「N/A」は空にしておくと、数値として取り込めます。"))
    if info["empty_cols"]:
        issues.append(_issue(
            "低", f"中身が空の列があります: {'、'.join(info['empty_cols'][:5])}",
            "取り込む列の選択から外せます。"))
    if info["blank_rows"]:
        issues.append(_issue(
            "低", f"途中に空行が {info['blank_rows']} 行あります。", "空行は取り込み時に残ります。"))
    if info["multiline"]:
        issues.append(_issue(
            "低", "セルの中で改行しているところがあります。",
            "表示は崩れませんが、検索や集計がしにくくなります。"))
    if merged is None:
        issues.append(_issue(
            "低", "ファイルが大きいため、セル結合までは調べていません。", ""))

    levels = {i["level"] for i in issues}
    out["issues"] = issues
    out["verdict"] = ("取り込みに向かない" if "高" in levels else
                      "手直しが要る" if "中" in levels else
                      "そのまま取り込める")
    return out


def summary_line(res: dict) -> str:
    """一覧に出す一言。"""
    high = [i for i in res["issues"] if i["level"] == "高"]
    if res["verdict"] == "そのまま取り込める":
        return "そのまま取り込める"
    if high:
        return f"{res['verdict']}（{high[0]['text'][:40]}）"
    mid = [i for i in res["issues"] if i["level"] == "中"]
    return f"{res['verdict']}（{mid[0]['text'][:40]}）" if mid else res["verdict"]


# ==========================================================================
# ===== 元 chats.py
# ユーザーごとのチャット履歴。
#
#   data/users/<ユーザー>/chats/index.json … 一覧（タイトルと日時だけ）
#   data/users/<ユーザー>/chats/<ID>.json  … 会話の中身
#
# 会話1件に保存するのは次の2つ。
#
#   messages    … LLMに送るメッセージ列。これが無いと「続きから」会話できない
#   render_log  … 画面に描くアイテム（テキスト・SQL・表・グラフ・作成ファイル）
#
# 一覧を別ファイルにしているのは、サイドバーを描くたびに全会話を読み込まないため。
# index.json が壊れた/消えた場合は、置いてある会話ファイルから作り直す。
#
# 古い会話は2つの条件で自動的に消える。
#   本数   … CHAT_HISTORY_LIMIT を超えたぶん（古い順）
#   保存期間 … 最後に使った日から CHAT_HISTORY_DAYS を過ぎたもの（既定90日）
# 掃除は一覧を読むついでに行う。常駐の掃除役を置かずに済ませるため。
#
# Excel等の作成ファイルはバイト列なのでJSONに入らない。上限までは base64 で埋め込み、
# 超えるものは本体を捨てる（過去の会話を開いても再ダウンロードはできない）。
# ==========================================================================
import base64
import json
import re
import threading
import uuid
from collections import OrderedDict
from datetime import datetime
from pathlib import Path

import config

_INDEX_NAME = "index.json"
_ID_RE = re.compile(r"[^0-9a-zA-Z_-]")
_TITLE_MAX = 40


# --- 場所 ---------------------------------------------------------------------

def chats_dir(user) -> Path:
    key = getattr(user, "safe_key", None) or str(user)
    return config.USER_META_DIR / key / "chats"


def _safe_id(chat_id: str) -> str:
    """ファイル名に使う前に無害化する（.. や / を混ぜられないように）。"""
    return _ID_RE.sub("", str(chat_id))[:64]


def _chat_file(user, chat_id: str) -> Path:
    return chats_dir(user) / f"{_safe_id(chat_id)}.json"


def new_id() -> str:
    # 先頭に日時を置いて、ファイル名を見ただけで新しい順に並ぶようにする
    return datetime.now().strftime("%Y%m%d-%H%M%S-") + uuid.uuid4().hex[:6]


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def now() -> str:
    """表示物に打つ時刻。会話を積む側（chat_bp）から使う。"""
    return _now()


# --- ファイル入出力 -------------------------------------------------------------

def _read_json(p: Path):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[chats] 読めませんでした: {p} ({e})")
        return None


def _write_json(p: Path, data) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, default=str), encoding="utf-8")


#: 会話1つにつき1本の鍵。「読む → 足す → まるごと書き戻す」を直列にするため。
#: 鍵が無いと、同じ会話への送信が重なったとき、後から終わった方が
#: 先に終わった方のやり取りを消してしまう（丸ごと上書きするので）。
_chat_locks: dict = {}
_chat_locks_guard = threading.Lock()


def lock_for(user, chat_id: str):
    """その会話の鍵を返す（同じ会話なら毎回同じもの）。

    同じスレッドが二重に取ることがある（load → persist）ので RLock。
    """
    key = f"{getattr(user, 'safe_key', None) or str(user)}/{_safe_id(chat_id)}"
    with _chat_locks_guard:
        lk = _chat_locks.get(key)
        if lk is None:
            lk = _chat_locks[key] = threading.RLock()
        return lk


# --- 一覧 ---------------------------------------------------------------------

def _index_path(user) -> Path:
    return chats_dir(user) / _INDEX_NAME


def _rebuild_index(user) -> list[dict]:
    """会話ファイルから一覧を作り直す（index.json を失った場合の保険）。"""
    items = []
    for p in chats_dir(user).glob("*.json"):
        if p.name == _INDEX_NAME:
            continue
        data = _read_json(p)
        if not isinstance(data, dict) or not data.get("id"):
            continue
        items.append(_summary(data))
    items.sort(key=lambda c: c.get("updated_at") or "", reverse=True)
    items = _drop_expired(user, items)
    if items:
        _write_json(_index_path(user), {"chats": items})
    return items


def _expired(summary: dict) -> bool:
    """保存期間を過ぎた会話か。

    数えるのは「最後に使った日」から。開いて続きを話した会話は寿命が延びる。
    日付が読めないものは、消して困る方が大きいので残す。
    """
    if config.CHAT_HISTORY_DAYS <= 0:
        return False
    stamp = summary.get("updated_at") or summary.get("created_at") or ""
    try:
        used = datetime.fromisoformat(str(stamp))
    except ValueError:
        return False
    return (datetime.now() - used).days > config.CHAT_HISTORY_DAYS


def _drop_expired(user, items: list[dict]) -> list[dict]:
    """期限切れの会話を実体ごと消して、残ったぶんを返す。"""
    keep, gone = [], 0
    for c in items:
        if _expired(c):
            f = _chat_file(user, c.get("id", ""))
            if f.exists():
                f.unlink()
            gone += 1
        else:
            keep.append(c)
    if gone:
        print(f"[chats] 保存期間({config.CHAT_HISTORY_DAYS}日)を過ぎた会話を"
              f"{gone}件削除しました（{_key_label(user)}）")
    return keep


def _key_label(user) -> str:
    return getattr(user, "username", None) or str(user)


def list_chats(user) -> list[dict]:
    """会話の一覧（新しい順）。中身は読まない。"""
    if user is None or not chats_dir(user).exists():
        return []
    data = _read_json(_index_path(user)) if _index_path(user).exists() else None
    items = data.get("chats") if isinstance(data, dict) else data
    if not isinstance(items, list):
        items = None
    if not items:
        return _rebuild_index(user)
    # 実体が消えているものは一覧からも落とす
    items = [c for c in items
             if isinstance(c, dict) and c.get("id") and _chat_file(user, c["id"]).exists()]
    items.sort(key=lambda c: c.get("updated_at") or "", reverse=True)
    # 期限切れは、一覧を出すついでに片付ける（掃除専用の仕組みを持たない）
    kept = _drop_expired(user, items)
    if len(kept) != len(items):
        _save_index(user, kept)
    return kept


def _summary(chat: dict) -> dict:
    return {
        "id": chat.get("id"),
        "title": chat.get("title") or "（無題）",
        "created_at": chat.get("created_at") or "",
        "updated_at": chat.get("updated_at") or "",
        "db_names": list(chat.get("db_names") or []),
        "n_turns": sum(1 for m in (chat.get("messages") or []) if m.get("role") == "user"),
    }


def _save_index(user, items: list[dict]) -> None:
    _write_json(_index_path(user), {"chats": items})


def _upsert_index(user, summary: dict) -> list[dict]:
    items = [c for c in list_chats(user) if c.get("id") != summary["id"]]
    items.insert(0, summary)
    items.sort(key=lambda c: c.get("updated_at") or "", reverse=True)

    # 上限を超えた古い会話は実体ごと削除
    for old in items[config.CHAT_HISTORY_LIMIT:]:
        f = _chat_file(user, old.get("id", ""))
        if f.exists():
            f.unlink()
    items = items[:config.CHAT_HISTORY_LIMIT]
    _save_index(user, items)
    return items


# --- 作成ファイル(bytes)の出し入れ ------------------------------------------------

def _encode_item(item: dict) -> dict:
    out = dict(item)
    # 表示物1つずつに時刻を持たせる。会話の created_at だけでは
    # 「その日に始めた」までしか分からず、いつ何を聞いたのかを追えない。
    # 質問には積んだ時刻が入っているので、ここで入るのは応答側の完了時刻になる。
    # 差を取れば、その質問にどれだけ待たされたかも分かる。
    out.setdefault("at", _now())
    data = out.get("data")
    if isinstance(data, (bytes, bytearray)):
        if len(data) <= config.CHAT_EMBED_FILE_MAX_BYTES:
            out["data"] = base64.b64encode(bytes(data)).decode("ascii")
            out["_b64"] = True
        else:                              # 大きすぎるので中身は保存しない
            out.pop("data", None)
            out["_no_data"] = True
    return out


def _decode_item(item: dict) -> dict:
    out = dict(item)
    if out.pop("_b64", False):
        try:
            out["data"] = base64.b64decode(out.get("data") or "")
        except Exception:
            out.pop("data", None)
            out["_no_data"] = True
    return out


# --- 読み書き -------------------------------------------------------------------

def make_title(messages: list[dict]) -> str:
    """最初のユーザー発言をタイトルにする。"""
    for m in messages or []:
        if m.get("role") != "user" or not m.get("content"):
            continue
        content = m["content"]
        if isinstance(content, list):
            # 画像つきの発言は content が配列。文字の部分だけ拾う。
            content = "".join(p.get("text", "") for p in content
                              if isinstance(p, dict) and p.get("type") == "text")
        t = " ".join(str(content).split())
        if t:
            return t[:_TITLE_MAX] + ("…" if len(t) > _TITLE_MAX else "")
    return "（無題）"


def heal_messages(messages: list) -> list:
    """結果の付いていない tool_calls を履歴から落とす。

    配信の途中で切断されると、「AIがツールを呼ぼうとした」という記録だけが
    残り、対応する {"role": "tool"} が無い履歴になる。OpenAI互換APIは
    これを 400 で拒むので、その会話は以後ずっと使えなくなる。

    落とすのは呼び出しの記録だけ。利用者の発言と、実行が終わっている
    ツール結果はそのまま残す。
    """
    if not messages:
        return messages
    answered = {str(m.get("tool_call_id")) for m in messages
                if isinstance(m, dict) and m.get("role") == "tool"}
    out, drop_ids = [], set()
    for m in messages:
        if not isinstance(m, dict):
            out.append(m)
            continue
        calls = m.get("tool_calls") or []
        if m.get("role") == "assistant" and calls:
            ids = {str(c.get("id")) for c in calls if isinstance(c, dict)}
            if ids - answered:                 # 1つでも結果が無ければ丸ごと落とす
                drop_ids |= ids
                # 本文だけ書いていたなら、それは残す価値がある
                if (m.get("content") or "").strip():
                    out.append({"role": "assistant", "content": m["content"]})
                continue
        if m.get("role") == "tool" and str(m.get("tool_call_id")) in drop_ids:
            continue                           # 落とした呼び出しの結果も外す
        out.append(m)
    return out


#: 削除された会話のID（利用者ごと）。回答を流している最中に削除されると、
#: 流し終えた側が手元の内容を書き戻して復活してしまうので、ここで断つ。
#: プロセスの中だけで持つ（削除も書き戻しも同じプロセスで起きる）。
_deleted_chats: "OrderedDict[str, bool]" = OrderedDict()
_DELETED_MAX = 500


def _deleted_key(user, chat_id: str) -> str:
    return f"{getattr(user, 'safe_key', None) or str(user)}/{_safe_id(chat_id)}"


def mark_deleted(user, chat_id: str) -> None:
    """この会話は消えたことにする（以後の書き戻しを受け付けない）。"""
    _deleted_chats[_deleted_key(user, chat_id)] = True
    while len(_deleted_chats) > _DELETED_MAX:
        _deleted_chats.popitem(last=False)


def is_deleted(user, chat_id: str) -> bool:
    return _deleted_key(user, chat_id) in _deleted_chats


def save_chat(user, chat_id: str, messages: list[dict], render_log: list[dict],
              db_names=None, tables=None, title: str = "", created_at: str = "",
              table_names=None) -> dict:
    """会話を保存し、一覧用の要約を返す。"""
    if is_deleted(user, chat_id):
        # 回答の途中で削除された会話。書き戻すと画面上で復活してしまう
        print(f"[chats] 削除済みの会話 {chat_id} は保存しません。")
        return {"id": chat_id, "deleted": True}
    chat = {
        "id": chat_id,
        "title": title or make_title(messages),
        "created_at": created_at or _now(),
        "updated_at": _now(),
        "db_names": list(db_names or []),
        # 実際にSQLが触った表（"DBファイル名.テーブル名"）。表ルーターの控え
        "table_names": list(table_names or []),
        "tables": dict(tables or {}),
        # system prompt は開くたびに作り直すので保存しない（カタログ変更に追従させる）
        # 途中で切れた tool_calls はここで落とす（残すと次から必ず400になる）
        "messages": heal_messages(
            [m for m in (messages or []) if m.get("role") != "system"]),
        "render_log": [_encode_item(i) for i in (render_log or [])],
    }
    _write_json(_chat_file(user, chat_id), chat)
    summary = _summary(chat)
    _upsert_index(user, summary)
    return summary


def load_chat(user, chat_id: str) -> dict | None:
    p = _chat_file(user, chat_id)
    if not p.exists():
        return None
    data = _read_json(p)
    if not isinstance(data, dict):
        return None
    data["render_log"] = [_decode_item(i) for i in (data.get("render_log") or [])]
    # 既に壊れて保存されている会話も、開いた時点で直す
    data["messages"] = heal_messages(data.get("messages") or [])
    return data


def delete_chat(user, chat_id: str) -> bool:
    p = _chat_file(user, chat_id)
    existed = p.exists()
    # 先に印を付ける。回答を流している最中でも、その処理の書き戻しを断つため
    mark_deleted(user, chat_id)
    if existed:
        p.unlink()
    _save_index(user, [c for c in list_chats(user) if c.get("id") != chat_id])
    return existed


def label(summary: dict) -> str:
    """サイドバーのプルダウンに出す1行。"""
    stamp = (summary.get("updated_at") or "")[5:16].replace("T", " ")   # MM-DD HH:MM
    title = summary.get("title") or "（無題）"
    return f"{title}　（{stamp}）" if stamp else title


# ==========================================================================
# ===== 元 history.py
# 取り込みの更新履歴。
#
# ジョブ定義（import_jobs.yaml）が持っているのは直前1回ぶんの結果だけなので、
# 「先週の火曜は何行入ったのか」「いつから失敗し続けているのか」を追えない。
# そこで、1回の取り込みにつき1件をここに追記していく。
#
# 置き場所は data/import_history.jsonl（1行1件のJSON）。
# YAML ではなく追記型にしているのは、実行のたびに全件を書き直したくないため。
# 手動の取り込みも定期取り込みも同じ形で残し、kind で区別する。
# ==========================================================================
import json
import threading
from datetime import datetime
from pathlib import Path

import config

_history_lock = threading.Lock()
# 追記のたびに全件を数え直さないよう、行数はプロセス内で覚えておく。
# 別プロセス（cron の python core.py refresh など）が書くとずれるが、間引きは後追いで効けばよい。
_count: int | None = None

IMPORT_RECORD_KINDS = {"manual": "手動", "auto": "定期", "job": "定期（手動実行）",
                       "realtime": "リアルタイム"}


def _history_path() -> Path:
    return config.IMPORT_HISTORY_FILE


def add_import_record(db_file: str, table: str, ok: bool, message: str, *,
        kind: str = "manual", mode: str = "replace", rows: int = 0,
        removed: int = 0, kept=None, keep=None, source: str = "",
        sheet: str | None = None, job_id: str | None = None,
        job_name: str | None = None, user: str | None = None,
        started: datetime | None = None) -> dict:
    """1回ぶんの結果を残す。記録に失敗しても取り込み自体は止めない。"""
    now = datetime.now()
    rec = {
        "at": (started or now).isoformat(timespec="seconds"),
        "db_file": db_file, "table": table,
        "ok": bool(ok), "kind": kind, "mode": mode,
        "rows": int(rows or 0), "removed": int(removed or 0),
        "kept": kept, "keep": keep,
        "source": str(source or ""), "sheet": sheet,
        "job_id": job_id, "job_name": job_name, "user": user,
        "message": message,
        "seconds": round((now - started).total_seconds(), 1) if started else None,
    }
    global _count
    try:
        with _history_lock:
            p = _history_path()
            p.parent.mkdir(parents=True, exist_ok=True)
            if _count is None:
                _count = _line_count(p)
            with p.open("a", encoding="utf-8") as f:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            _count += 1
            _trim_if_needed(p)
    except Exception as e:                       # 履歴が書けなくても取り込みは成功扱い
        print(f"[history] 記録できませんでした: {e}")
    return rec


def _line_count(p: Path) -> int:
    if not p.exists():
        return 0
    with p.open("rb") as f:
        return sum(1 for line in f if line.strip())


def _trim_if_needed(p: Path) -> None:
    """行数が上限を超えたら、新しい方から上限ぶんだけ残す。

    毎回書き直すと重いので、1割ぶん超えてからまとめて間引く。
    """
    global _count
    limit = max(1, config.IMPORT_HISTORY_MAX)
    if (_count or 0) <= limit * 1.1:
        return
    lines = [x for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]
    keep = lines[-limit:]
    p.write_text("\n".join(keep) + "\n", encoding="utf-8")
    _count = len(keep)


def _read_all() -> list[dict]:
    p = _history_path()
    if not p.exists():
        return []
    out = []
    try:
        for line in p.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue                          # 壊れた行は飛ばす
            if isinstance(rec, dict):
                out.append(rec)
    except Exception as e:
        print(f"[history] 読めませんでした: {p} ({e})")
    return out


def _newest_first(items: list[dict]) -> list[dict]:
    """新しい順に並べる。

    at は秒までしか持たないので、同じ秒の中は「後に書いた方が新しい」で決める。
    先に並びを逆にしてから安定ソートすると、同着がその順で残る。
    """
    items = list(reversed(items))
    items.sort(key=lambda r: r.get("at") or "", reverse=True)
    return items


def for_table(db_file: str, table: str, limit: int = 30) -> list[dict]:
    """あるテーブルの履歴を新しい順で。"""
    hit = _newest_first([r for r in _read_all()
                         if r.get("db_file") == db_file and r.get("table") == table])
    return hit[:limit] if limit else hit


def recent_import_records(limit: int = 100) -> list[dict]:
    """テーブルを問わず、新しい順に。取り込み全体の傾向を見るとき用。"""
    hit = _newest_first(_read_all())
    return hit[:limit] if limit else hit


def counts() -> dict[tuple, int]:
    """(DB, テーブル) ごとの件数。"""
    out: dict[tuple, int] = {}
    for r in _read_all():
        key = (r.get("db_file"), r.get("table"))
        out[key] = out.get(key, 0) + 1
    return out


def latest_by_source() -> dict[str, dict]:
    """取り込み元ファイルごとの、いちばん新しい記録。

    「このファイルはもう取り込んだのか」「いつ・どのテーブルに入ったのか」を
    ファイルの一覧と突き合わせるために使う。キーはファイルパス。
    """
    out: dict[str, dict] = {}
    for r in _newest_first(_read_all()):
        src = str(r.get("source") or "")
        if src and src not in out:
            out[src] = r
    return out


# ==========================================================================
# ===== 元 catalog_history.py
# 用語集・例文の変更履歴。誰が・いつ・何を・どう変えたかを残す。
#
# カタログは全員共通の土台で、チャットからは一般ユーザーも書けるようにした。
# 書けるようにした以上、「いつの間にか定義が変わっていた」が起きるので、
# 変更のたびに1件を追記して、後から辿れるようにする。
#
# 置き場所は data/catalog_history.jsonl（1行1件のJSON・追記型）。
# import_history と同じ考え方で、YAMLに混ぜない（メタ情報は「現在の定義」だけを
# 持ち、履歴で膨らませない。normalize が知らないキーを消す作りとも衝突しない）。
# ==========================================================================
import json
import threading
from datetime import datetime
from pathlib import Path

import config

_catalog_history_lock = threading.Lock()

#: 表示用のラベル
OPS = {"add": "新規", "update": "変更", "remove": "削除"}


def _catalog_history_path() -> Path:
    return config.CATALOG_HISTORY_FILE


def add_catalog_change(kind: str, op: str, db_file: str, name: str, *,
        user: str | None = None, table: str | None = None,
        before=None, after=None, source: str = "chat") -> None:
    """1件追記する。失敗しても本体の保存は止めない（履歴は本体より弱い）。"""
    rec = {
        "at": datetime.now().isoformat(timespec="seconds"),
        "kind": kind, "op": op, "db": db_file, "table": table or "",
        "name": name, "user": user or "不明", "source": source,
        "before": before, "after": after,
    }
    try:
        with _catalog_history_lock:
            p = _catalog_history_path()
            p.parent.mkdir(parents=True, exist_ok=True)
            with p.open("a", encoding="utf-8") as f:
                f.write(json.dumps(rec, ensure_ascii=False, default=str) + "\n")
            _trim(p)
    except Exception as e:
        print(f"[catalog_history] 書けませんでした: {e}")


def _trim(p: Path) -> None:
    """上限を超えたら古い行から捨てる（毎回数えず、たまに間引く）。"""
    lines = p.read_text(encoding="utf-8").splitlines()
    if len(lines) > config.CATALOG_HISTORY_MAX * 1.2:
        keep = lines[-config.CATALOG_HISTORY_MAX:]
        p.write_text("\n".join(keep) + "\n", encoding="utf-8")


# ==========================================================================
# ===== 元 prefs.py
# ログインユーザーごとの画面の状態。
#
#   data/users/<ユーザー>/prefs.yaml
#
# 覚えておくのは次の2つ。
#
#   selection … 対象データの選択（{DBファイル名: [テーブル名, ...]}）
#   model     … 使うモデル
#
# セッション（Cookie）に置くとログアウトやブラウザを閉じたときに消えてしまう。
# 毎回選び直すのは手間なので、そのユーザーのフォルダにファイルとして残す。
# カタログやチャット履歴と同じ場所に置くので、退職者のデータを消すときは
# そのユーザーのフォルダごと消せばよい。
# ==========================================================================
import threading

import yaml

import config

_prefs_lock = threading.Lock()

# ここに挙げたキーだけを読み書きする（余計なものが混ざっても無視する）
# rag_off      … 検索対象から外したナレッジベースのid（外したものを持つ理由は
#                 rag_excluded_ids のコメントを参照）
# rag_settings … 検索の効き方（rag/settings.py の RAG_SPECS）
# tables_off   … 分析の対象から外したテーブル名（外したものを持つ理由は
#                 rag_off と同じ。新しく取り込んだ表は既定で対象に入る）
KEYS = ("model", "rag_off", "rag_settings", "tables_off")


def _key(user) -> str:
    """保存先のフォルダ名。catalog / chats と同じ決め方にする。"""
    return getattr(user, "safe_key", None) or str(user)


def _prefs_path(user):
    return config.USER_META_DIR / _key(user) / "prefs.yaml"


def load(user) -> dict:
    if user is None:
        return {}
    p = _prefs_path(user)
    if not p.exists():
        return {}
    try:
        data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    except Exception as e:
        print(f"[prefs] 読めませんでした: {p} ({e})")
        return {}
    return {k: v for k, v in data.items() if k in KEYS} if isinstance(data, dict) else {}


def _save(user, data: dict) -> None:
    p = _prefs_path(user)
    p.parent.mkdir(parents=True, exist_ok=True)
    with _prefs_lock:
        p.write_text(yaml.safe_dump({k: data[k] for k in KEYS if k in data},
                                    allow_unicode=True, sort_keys=False),
                     encoding="utf-8")


def set_value(user, key: str, value) -> None:
    """1項目だけ更新する。他の項目は触らない。"""
    if user is None or key not in KEYS:
        return
    data = load(user)
    data[key] = value
    _save(user, data)


# --- モデルの選択 ----------------------------------------------------------------

def get_model(user) -> str:
    return str(load(user).get("model") or "").strip()


def set_model(user, model: str) -> None:
    set_value(user, "model", str(model or "").strip())


# ==========================================================================
# ===== 元 catalog.py
# データカタログ層。
#
# 「自動プロファイル（機械の知識）」と「サイドカーYAML（人間の知識）」を統合し、
# UI表示・ER図・LLM用 system prompt を **同じ情報源** から生成する。
#
# ファイル配置:
#   data/sales.db                                 … DB本体（読み取り専用で扱う）
#   data/sales.db.meta.yaml                       … メタ情報（全員で1つ。編集は管理者のみ）
#   data/.profile_cache/sales.db.profile.json     … 自動プロファイル（mtime+sizeで自動再生成）
#
# メタ情報(YAML)の構造:
#   title: 受注管理DB
#   description: |            # 何のデータか＋AIが知らないと間違える前提（※で始める行）
#     受注と請求。金額は明細側にしかない。
#     ※ 退職者も employees に残る。現役だけなら active_flag = 1 で絞る。
#   tables:
#     orders:
#       description: 受注明細。1行 = 1受注明細行。
#       ai_draft: true          # AI下書きのまま人間が未確認ならtrue
#       columns:
#         status: { description: 受注状態, values: { "1": 受付, "2": 出荷済 } }
#       glossary:               # そのテーブル固有の業務用語
#         有効な受注:
#           description: キャンセル以外の、実際に売上になる受注   # 自然言語だけでもよい
#           sql: status != '9'                                  # あればAIはこの式をそのまま使う
#   relationships:
#     - { from: orders.customer_id, to: customers.id, cardinality: "N:1" }
#       # to には "他DBエイリアス.テーブル.列" の3要素形式も書ける
#     - { from: "明細.(工場CD, 受注NO)", to: "受注.(工場CD, 受注NO)", cardinality: "N:1" }
#       # 複合キーは括弧で列をまとめる（from/to の列数は同じ・対応順）
#   glossary:                   # テーブルをまたぐ業務用語だけをここに書く
#     稼働率: { description: 実働時間÷所定時間 }
#   examples:
#     - q: 今月の売上は？
#       description: 締め日は月末。キャンセルは除く   # 任意。この例の読み方をAIに伝える
#       sql: SELECT ...
# ==========================================================================
import hashlib
import json
import sqlite3
import time
from datetime import datetime
from pathlib import Path

import yaml

import config
import db

# =============================================================================
# メタ情報（サイドカーYAML）
# =============================================================================

_META_KEYS = ("tables", "groups", "relationships", "glossary",
              "examples", "checks", "er_layout", "tools", "builtin_tools",
              # 旧形式の読み込み互換のため残す（新規には書かない）
              "title", "description")


# カタログは全員で1つ。DBの中身が何かは人によって変わらないので、
# 定義を分けると「同じ質問なのに人によって答えが違う」ことになる。
#   data/<DB>.db.meta.yaml … 唯一のカタログ。書き換えるのは管理者だけ
#                            （画面側は web/catalog_bp.py が admin_required で守る）

def meta_path(db_path) -> Path:
    """カタログの置き場所。DBファイルの隣に同じ名前で置く。"""
    return Path(str(db_path) + ".meta.yaml")


#: 読み込んだカタログの控え。キーはファイルのパス、値は (更新時刻, 大きさ, 中身)。
#: ファイルが書き換わったら自動で読み直すので、画面から編集した内容はすぐ反映される。
_meta_cache: dict = {}


class MetaUnreadable(RuntimeError):
    """カタログのファイルが壊れていて読めない。

    読む側（プロンプト・ER図・一覧）は「説明が無い」として動いてよいが、
    書くために読む側はこれを受け取って断る。断らずに空として保存すると、
    書かれていた説明・用語・例文・検算がまるごと消える。
    """


def _read_yaml(p: Path, strict: bool = False) -> dict:
    """カタログのYAMLを読む。同じファイルの2度目以降は控えを返す。

    1画面を描くのに同じファイルを何度も読むことがある（ER図の候補・結合の相手先・
    ユーザー定義ツールの収集などが、それぞれ全DBのカタログを見に行くため）。
    DBが増えるとこれが効いてきて、21DBでは1画面で66回のパースが走り、
    表示に2.4秒かかっていた。YAMLの解釈は重いので、ここで一度だけにする。

    更新時刻と大きさが変わっていれば読み直すので、外部のエディタで直しても効く。
    """
    try:
        st = p.stat()
    except OSError:
        _meta_cache.pop(str(p), None)
        return {}
    key = str(p)
    hit = _meta_cache.get(key)
    if hit and hit[0] == st.st_mtime_ns and hit[1] == st.st_size:
        return hit[2]
    try:
        data = yaml.safe_load(p.read_text(encoding="utf-8"))
        data = data if isinstance(data, dict) else {}
    except Exception as e:
        print(f"[catalog] メタ情報を読めませんでした: {p} ({e})")
        if strict:
            raise MetaUnreadable(
                f"カタログのファイルが壊れていて読めません（{p.name}）。"
                "このまま保存すると、書かれていた説明・用語・例文・検算が"
                "すべて消えるため、保存を中止しました。"
                "ファイルを直すか、隣の .bak から戻してから操作してください。"
                f"（読めなかった理由: {e}）") from e
        return {}
    # 控えは読み取り専用のつもりで扱う。呼び出し側が書き換えると次の人に伝染するため、
    # 書き込みは必ず save_meta を通す決まりにしている（画面もそうしている）。
    _meta_cache[key] = (st.st_mtime_ns, st.st_size, data)
    return data


def load_meta(db_path) -> dict:
    """カタログを読む（全員が同じものを見る）。

    戻り値は控え（キャッシュ）そのものなので、**書き換えてはいけない**。
    書き換えると、同じファイルを読んだ他の画面にもその変更が漏れる。
    編集して save_meta に渡すときは load_meta_for_edit を使うこと。
    """
    return _read_yaml(meta_path(db_path))


def load_meta_for_edit(db_path) -> dict:
    """編集するためにカタログを読む。控えとは切り離した複製を返す。

    画面からの保存は「読む → 一部を書き換える → save_meta」という流れで、
    そのまま控えを渡すと保存前の途中状態が他の画面へ漏れる。
    ここで複製しておけば、保存が終わるまで控えは元のままでいられる。
    """
    import copy
    # 書くために読むので strict。壊れていたら空として通さず、その場で止める
    return copy.deepcopy(_read_yaml(meta_path(db_path), strict=True))


def merge_caveats(description, caveats) -> str:
    """説明と、かつて別欄だった注意書き(caveats)を1つの文章にする。

    以前は「説明」と「注意書き（1行に1つ）」の2欄だったが、AIへの渡り方は
    同じ場所に続けて書かれた文章で、分ける意味が薄かった。いまは「説明」1欄で、
    注意したい事実は行頭に ※ を付けて書く。古いYAMLの caveats はここで合流させる。
    """
    lines = [str(description or "").strip()]
    for c in (caveats or []):
        c = str(c or "").strip()
        if c:
            lines.append(c if c.startswith(("※", "⚠")) else f"※ {c}")
    return "\n".join(l for l in lines if l)


def db_groups(meta: dict) -> dict:
    """まとまり（表名の接頭辞）ごとのメモ。{prefix: {description}}

    まとまりの名前は表名の接頭辞そのもので、別の表示名は持たない
    （名前を2つ持つと、どちらを信じるかという問題が生まれるだけ）。
    「データ全体の説明」という欄も持たない。全体に書かれた文章は対象の
    入れ替えに追随できず腐るため、知識は必ず対象物（表・まとまり・用語）に
    付ける。まとまりのメモは、そのまとまりの表を選んでいるときだけAIに渡る。
    """
    out = {}
    for k, v in (meta.get("groups") or {}).items():
        if isinstance(v, dict):
            out[str(k)] = {"description": str(v.get("description") or "")}
    return out


def section_stamp(meta: dict, kind: str) -> str:
    """用語集・例文・検算の「いまの中身」を短い印にする。

    画面はその節を丸ごと置き換えて保存するので、開いてから保存するまでの間に
    別の経路（チャットの登録カード・別の管理者）で足されたものが黙って消える。
    開いたときの印を持たせて、変わっていたら保存を断るための材料。

    用語は「全体の用語」と「表ごとの用語」があり、画面はその両方を一度に
    受け持つので、まとめて1つの印にする。
    """
    if kind == "glossary":
        data = {"": db_glossary(meta),
                **{t: table_glossary(meta, t) for t in (meta.get("tables") or {})}}
        data = {k: v for k, v in data.items() if v}
    elif kind == "examples":
        data = meta.get("examples") or []
    elif kind == "checks":
        data = meta.get("checks") or []
    else:
        raise ValueError(f"unknown kind: {kind}")
    raw = json.dumps(data, ensure_ascii=False, sort_keys=True, default=str)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def save_meta(db_path, meta: dict) -> None:
    """カタログを保存する（内容をまるごと書く）。呼べるのは管理者の画面だけ。"""
    target = meta_path(db_path)
    # 保存したら控えを捨てる。更新時刻でも気づけるが、
    # 同じ秒内に読み書きが続くと取りこぼすことがあるため明示的に消す。
    _meta_cache.pop(str(target), None)
    # 説明は1欄。古い caveats が残っていれば説明に合流させてから書く
    if meta.get("caveats"):
        meta["description"] = merge_caveats(meta.get("description"), meta.get("caveats"))
        meta.pop("caveats", None)
    cleaned = {}
    for k in _META_KEYS:
        v = meta.get(k)
        if v in (None, "", [], {}):
            continue
        cleaned[k] = v

    target.parent.mkdir(parents=True, exist_ok=True)
    if not cleaned:
        target.write_text("", encoding="utf-8")
        return
    target.write_text(
        yaml.dump(cleaned, Dumper=_MetaDumper, allow_unicode=True, sort_keys=False,
                  default_flow_style=False),
        encoding="utf-8",
    )


class _MetaDumper(yaml.SafeDumper):
    """複数行の文字列（説明・SQL）は '...' の折り返しではなく | ブロックで書く。
    手で開いて読める・直せるファイルにしておくため。"""


def _repr_str(dumper, data: str):
    if "\n" in data:
        # 行末の空白があると PyYAML は | を使えず引用符に落ちるので、先に落とす
        data = "\n".join(l.rstrip() for l in data.splitlines())
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


_MetaDumper.add_representer(str, _repr_str)


# =============================================================================
# 業務用語（用語集）
# =============================================================================
#
# 用語は「テーブル固有」と「テーブルをまたぐもの」の2種類あるので、置き場所も2つ。
#   meta["tables"][テーブル名]["glossary"]  … そのテーブルの用語（基本はこちら）
#   meta["glossary"]                        … 複数テーブルにまたがる用語
# テーブル側に置くと、そのテーブルが選択されているときだけプロンプトに載る。
#
# 1つの用語は次の2つを持つ。どちらか一方だけでもよい。
#   description … 自然言語の説明（AIはこれを読んで自分でSQLを組み立てる）
#   sql         … SQLの条件式や計算式（あればAIはこの式をそのまま使う）

def normalize_glossary(gl) -> dict:
    """用語集を {用語: {"description":…, "sql":…}} の形に揃える。

    値は必ず辞書。手でYAMLを書いて文字列になっていた場合は「説明」として扱う。
    以前はSQL式として扱っていたが、説明文が書かれていると
    「この式をそのまま使う」とAIに渡してしまい、構文エラーのSQLを作らせていた。
    説明として扱えば、間違っていてもAIが列情報から組み立て直せる。
    """
    out = {}
    for term, val in (gl or {}).items():
        term = str(term).strip()
        if not term:
            continue
        if isinstance(val, dict):
            desc = str(val.get("description") or "").strip()
            sql = str(val.get("sql") or "").strip()
        else:
            print(f"[catalog] 用語 '{term}' が古い書き方です。説明として扱います。")
            desc, sql = str(val or "").strip(), ""
        if desc or sql:
            out[term] = {"description": desc, "sql": sql}
    return out


def table_glossary(meta: dict, tname: str) -> dict:
    """テーブル固有の用語。"""
    return normalize_glossary(((meta.get("tables") or {}).get(tname) or {}).get("glossary"))


def db_glossary(meta: dict) -> dict:
    """テーブルをまたぐ用語。"""
    return normalize_glossary(meta.get("glossary"))


def set_table_glossary(meta: dict, tname: str, gl: dict) -> None:
    """テーブル固有の用語を書き戻す（空なら削除）。"""
    tm = meta.setdefault("tables", {}).setdefault(tname, {})
    if gl:
        tm["glossary"] = gl
    else:
        tm.pop("glossary", None)
        if not tm:
            meta["tables"].pop(tname, None)


def glossary_lines(gl: dict) -> list[str]:
    """プロンプトに載せる用語の行。"""
    lines = []
    for term, e in gl.items():
        desc, sql = e.get("description") or "", e.get("sql") or ""
        lines.append(f"- {term}: {desc}" if desc else f"- {term}:")
        if sql:
            lines.append(f"    SQL式: {sql}   ← この式をそのまま使う")
        else:
            lines.append("    （SQL式は未登録。上の列情報をもとに自分で組み立てる）")
    return lines


def glossary_count(meta: dict) -> int:
    """DB全体＋全テーブルの用語数。"""
    n = len(db_glossary(meta))
    for tname in (meta.get("tables") or {}):
        n += len(table_glossary(meta, tname))
    return n


# =============================================================================
# 自動プロファイル
# =============================================================================

def _qi(name: str) -> str:
    """SQLite識別子のクオート。"""
    return '"' + str(name).replace('"', '""') + '"'


def _cache_path(db_path) -> Path:
    return config.PROFILE_CACHE_DIR / (Path(db_path).name + ".profile.json")


def _make_timeout(conn: sqlite3.Connection, seconds: float):
    """接続にタイムアウトを仕掛け、クエリごとに呼ぶ reset 関数を返す。"""
    box = {"t": time.time()}
    conn.set_progress_handler(lambda: 1 if (time.time() - box["t"]) > seconds else 0, 100000)

    def reset():
        box["t"] = time.time()
    return reset


def _profile_table(conn: sqlite3.Connection, name: str, reset) -> dict:
    t = _qi(name)
    info: dict = {"columns": [], "fks": [], "row_count": None,
                  "sample_columns": [], "sample_rows": [], "col_stats": {}}

    reset()
    # PRAGMA table_info の pk は 0=非キー / 1以上=複合主キー内の順番。
    # 複合キーの構成順は「1行が何を表すか」の手がかりになるので pk_seq に残す。
    for cid, cname, ctype, notnull, dflt, pk in conn.execute(f"PRAGMA table_info({t})"):
        info["columns"].append({"name": cname, "type": ctype or "", "notnull": bool(notnull),
                                "pk": bool(pk), "pk_seq": int(pk or 0)})

    reset()
    try:
        for row in conn.execute(f"PRAGMA foreign_key_list({t})"):
            # (id, seq, table, from, to, on_update, on_delete, match)
            info["fks"].append({"from": row[3], "table": row[2], "to": row[4] or "id"})
    except sqlite3.Error:
        pass

    reset()
    try:
        info["row_count"] = conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
    except sqlite3.Error:
        pass  # タイムアウト等 → 行数不明として続行

    reset()
    try:
        cur = conn.execute(f"SELECT * FROM {t} LIMIT {config.PROFILE_SAMPLE_ROWS}")
        info["sample_columns"] = [d[0] for d in cur.description] if cur.description else []
        info["sample_rows"] = [[_jsonable(v) for v in r] for r in cur.fetchall()]
    except sqlite3.Error:
        pass

    # 列統計（巨大テーブルはスキップ）
    rc = info["row_count"]
    if rc is not None and rc <= config.PROFILE_STATS_MAX_ROWS and rc > 0:
        limit = config.PROFILE_LOW_CARDINALITY
        for col in info["columns"]:
            c = _qi(col["name"])
            stat: dict = {}
            reset()
            try:
                vals = conn.execute(
                    f"SELECT {c} AS v, COUNT(*) AS n FROM {t} GROUP BY 1 ORDER BY n DESC LIMIT {limit + 1}"
                ).fetchall()
                if len(vals) <= limit:
                    stat["values"] = [[_jsonable(v), n] for v, n in vals]
                else:
                    reset()
                    mn, mx = conn.execute(f"SELECT MIN({c}), MAX({c}) FROM {t}").fetchone()
                    stat["min"], stat["max"] = _jsonable(mn), _jsonable(mx)
            except sqlite3.Error:
                pass
            if stat:
                info["col_stats"][col["name"]] = stat
    return info


def _jsonable(v):
    if isinstance(v, bytes):
        return f"<BLOB {len(v)} bytes>"
    return v


def profile_db(db_path, force: bool = False) -> dict:
    """DBを読み取り専用でプロファイリング。mtime+sizeが一致するキャッシュがあれば再利用。"""
    db_path = Path(db_path)
    st = db_path.stat()
    # v はプロファイルの構造バージョン。上げると古いキャッシュが無効になる。
    key = {"v": 2, "mtime": st.st_mtime, "size": st.st_size}

    cache = _cache_path(db_path)
    if not force and cache.exists():
        try:
            data = json.loads(cache.read_text(encoding="utf-8"))
            if data.get("key") == key:
                return data
        except Exception:
            pass

    conn = db.connect_ro(db_path)
    try:
        reset = _make_timeout(conn, config.PROFILE_TIMEOUT_SEC)
        tables: dict = {}
        reset()
        rows = conn.execute(
            "SELECT name, type FROM sqlite_master "
            "WHERE type IN ('table','view') AND name NOT LIKE 'sqlite_%' ORDER BY name"
        ).fetchall()
        for name, typ in rows:
            try:
                t = _profile_table(conn, name, reset)
                t["type"] = typ
                tables[name] = t
            except sqlite3.Error as e:
                tables[name] = {"type": typ, "error": str(e), "columns": [], "fks": [],
                                "row_count": None, "sample_columns": [], "sample_rows": [],
                                "col_stats": {}}
    finally:
        conn.close()

    profile = {
        "file": db_path.name,
        "key": key,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "tables": tables,
    }
    config.PROFILE_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache.write_text(json.dumps(profile, ensure_ascii=False, default=str), encoding="utf-8")
    return profile


# =============================================================================
# 乖離検知・結合候補・カバレッジ
# =============================================================================

def _memo_bad_tables(memo: str, ptables, prefixes) -> list[str]:
    """まとまりメモの中の「表名のつもりで書かれた、実在しない名前」を返す。

    例文・検算・用語で使っている _missing（\\w+ で切る）はここでは使えない。
    メモは散文で、Python の \\w は日本語も語構成文字なので
    「品質__defectsは社内で見つけた不良」が丸ごと1語になり、実在する表を
    書いたメモほど誤警告が出る（実際に出した）。

    なので逆から見る。実在する表名がメモの中で占める位置を先に塗り、
    そこから外れた "__" だけを「表名のつもりで書かれた別物」として拾う。
    「人事_勤怠__*」のような、まとまり全体を指す書き方は数えない。
    """
    covered: set = set()
    for t in ptables:
        i = memo.find(t)
        while i >= 0:
            covered.update(range(i, i + len(t)))
            i = memo.find(t, i + 1)
    out = []
    for m in re.finditer(r"__", memo):
        if m.start() in covered:
            continue
        head = memo[:m.start()]
        # 「まとまり__*」「まとまり__」で終わる書き方は、まとまり全体を指す言い方
        if any(head.endswith(p) for p in prefixes) and \
                not memo[m.end():m.end() + 1].strip(" *、。」）"):
            continue
        snip = memo[max(0, m.start() - 14):m.start() + 16]
        out.append(snip.replace("\n", " ").strip())
    return out


def drift_warnings(profile: dict, meta: dict) -> list[str]:
    """メタ情報がスキーマの実体からズレている箇所を警告として返す。"""
    warns = []
    ptables = profile.get("tables", {})
    for tname, tmeta in (meta.get("tables") or {}).items():
        if tname not in ptables:
            warns.append(f"メタ情報のテーブル '{tname}' はDBに存在しません（改名/削除された可能性）。")
            continue
        pcols = {c["name"] for c in ptables[tname]["columns"]}
        for cname in ((tmeta or {}).get("columns") or {}):
            if cname not in pcols:
                warns.append(f"メタ情報の列 '{tname}.{cname}' はDBに存在しません。")
        for cname in ((tmeta or {}).get("primary_key") or []):
            if cname not in pcols:
                warns.append(f"指定された主キーの列 '{tname}.{cname}' はDBに存在しません。")
    for rel in (meta.get("relationships") or []):
        eps = []
        for end in (rel.get("from", ""), rel.get("to", "")):
            ep = parse_endpoint_cols(end, "@own")
            eps.append(ep)
            if not ep or ep[0] != "@own":
                continue  # 解けないか、db付き＝他DBなので対象外
            tname, cols = ep[1], ep[2]
            if tname in ptables:
                have = {c["name"] for c in ptables[tname]["columns"]}
                for cname in cols:
                    if cname not in have:
                        warns.append(f"結合定義の '{end}' に対応する列がありません。")
            else:
                warns.append(f"結合定義の '{end}' に対応するテーブルがありません。")
        if eps[0] and eps[1] and len(eps[0][2]) != len(eps[1][2]):
            warns.append(f"結合定義 '{rel.get('from')} → {rel.get('to')}' の列数が合っていません。")
    # 例文・検算・用語のSQLが、存在しないテーブルを使っていないか。
    # 削除の掃除が中断された（アプリ停止・強制終了）ときの取り残しはここで見つける
    def _missing(sql: str):
        toks = set(re.findall(r"\w+", str(sql or "")))   # \w は日本語のテーブル名も拾う
        # 末尾が __ で切れたものは表名ではない（メモの「人事_勤怠__*」のような
        # まとまり全体を指す書き方が、存在しない表として挙がってしまう）
        return sorted(t for t in toks
                      if "__" in t and not t.endswith("__") and t not in ptables)
    for e in (meta.get("examples") or []):
        for t in _missing(e.get("sql")):
            warns.append(f"例文「{str(e.get('q') or '')[:30]}」が、存在しないテーブル '{t}' を使っています。")
    for c in (meta.get("checks") or []):
        used = " ".join(str(x) for x in (c.get("left"), c.get("right"), c.get("drilldown")))
        for t in _missing(used):
            warns.append(f"検算「{str(c.get('name') or '')[:30]}」が、存在しないテーブル '{t}' を使っています。")
    for term, v in (meta.get("glossary") or {}).items():
        for t in _missing((v or {}).get("sql") if isinstance(v, dict) else ""):
            warns.append(f"用語「{term}」のSQL式が、存在しないテーブル '{t}' を使っています。")
    # ユーザー定義ツールのSQLも見る。ここが抜けていたので、消した表を使うツールが
    # そのまま残り、AIに配られ続けていた
    for tool in (meta.get("tools") or []):
        for t in _missing((tool or {}).get("sql")):
            warns.append(f"ツール「{str((tool or {}).get('name') or '')[:30]}」が、"
                         f"存在しないテーブル '{t}' を使っています。")

    # まとまりのメモ。改名すると本文だけ古い名前のまま残る（_rename_in_text は
    # 「まとまり__表名」という完全な表名しか置換しないので、裸のまとまり名は残る）。
    # メモはプロンプトの最上段に無印で入るので、腐ると回答に直に効く。
    prefixes = {t.split("__", 1)[0] for t in ptables if "__" in t}
    for gname, ginfo in (meta.get("groups") or {}).items():
        memo = str((ginfo or {}).get("description") or "")
        if not any(t.startswith(str(gname) + "__") for t in ptables):
            warns.append(f"まとまり「{gname}」のメモが残っていますが、そのまとまりの表がありません。")
        for snip in _memo_bad_tables(memo, ptables, prefixes):
            warns.append(f"まとまり「{gname}」のメモの「{snip}」は、実在する表の名前ではありません。")
        for named in re.findall(r"まとまり[（(「]([^）)」]+)[）)」]", memo):
            if named not in prefixes:
                warns.append(f"まとまり「{gname}」のメモが、存在しないまとまり '{named}' を案内しています。")
    return warns


#: 列の値の標本。DBファイルの更新時刻が変わるまで使い回す
#: （候補APIは関連を触るたびに呼ばれるので、毎回700列を読み直さない）。
_suggest_cache: dict = {}


def _suggest_values(db_path, profile: dict) -> tuple[dict, dict]:
    """(列ごとの値の標本, 単独主キーの全値) を返す。

    標本は列あたり最大200個。主キー側は照合の分母になるので全部持つ
    （このアプリの表は大きくても数千行）。
    """
    key = (str(db_path), Path(db_path).stat().st_mtime_ns)
    hit = _suggest_cache.get(key)
    if hit:
        return hit
    samples: dict = {}
    pk_values: dict = {}
    conn = db.connect_ro(db_path)
    try:
        for tname, t in profile["tables"].items():
            pks = [c["name"] for c in t["columns"] if c["pk"]]
            for c in t["columns"]:
                if c["type"] not in ("TEXT", "INTEGER"):
                    continue
                try:
                    if len(pks) == 1 and c["name"] == pks[0]:
                        rows = conn.execute(
                            f'SELECT DISTINCT "{c["name"]}" FROM "{tname}" '
                            f'WHERE "{c["name"]}" IS NOT NULL LIMIT 20000').fetchall()
                        pk_values[(tname, c["name"])] = {str(r[0]) for r in rows}
                    rows = conn.execute(
                        f'SELECT DISTINCT "{c["name"]}" FROM "{tname}" '
                        f'WHERE "{c["name"]}" IS NOT NULL LIMIT 200').fetchall()
                    samples[(tname, c["name"])] = {str(r[0]) for r in rows}
                except Exception:
                    continue
    finally:
        conn.close()
    _suggest_cache.clear()          # DBは1つ。古い版を抱えない
    _suggest_cache[key] = (samples, pk_values)
    return samples, pk_values


def join_suggestions(profile: dict, meta: dict, db_path=None) -> list[dict]:
    """結合候補。列名のヒューリスティックに加えて、db_path があれば
    実データの値の重なりで裏を取る（一致率を根拠に添え、0%は出さない。
    さらに、列名が違っても値がほぼ一致する列は候補として拾い上げる）。"""
    ptables = profile.get("tables", {})
    existing = set()
    for rel in (meta.get("relationships") or []):
        pr = rel_pairs(rel, "@own")
        if pr:  # 複合キーは列ペアごとに「既存」とみなす（片列の候補を出さない）
            (fa, ftb), (ta, ttb), pairs = pr
            for fc, tc in pairs:
                existing.add((f"{ftb}.{fc}".lower(), f"{ttb}.{tc}".lower()))
        else:
            existing.add((str(rel.get("from", "")).lower(), str(rel.get("to", "")).lower()))
    for tname, t in ptables.items():
        for fk in t.get("fks", []):
            existing.add((f"{tname}.{fk['from']}".lower(), f"{fk['table']}.{fk['to']}".lower()))

    sugs = []
    for tname, t in ptables.items():
        for col in t.get("columns", []):
            cname = col["name"]
            low = cname.lower()
            if not low.endswith("_id") and not low.endswith("id"):
                continue
            base = low[:-3] if low.endswith("_id") else None
            if not base:
                continue
            # 候補テーブル名: base / base+"s" / base+"es"
            for cand in (base, base + "s", base + "es"):
                target = next((n for n in ptables if n.lower() == cand), None)
                if not target or target == tname:
                    continue
                tcols = ptables[target]["columns"]
                pk = next((c["name"] for c in tcols if c["pk"]), None)
                # 複合主キーの相手に1列だけで結合する候補は誤りになるので出さない
                if len([c for c in tcols if c["pk"]]) > 1:
                    continue
                to_col = pk or next((c["name"] for c in tcols if c["name"].lower() in ("id", low)), None)
                if not to_col:
                    continue
                frm, to = f"{tname}.{cname}", f"{target}.{to_col}"
                if (frm.lower(), to.lower()) in existing:
                    continue
                sugs.append({"from": frm, "to": to, "cardinality": "N:1",
                             "reason": f"列名 '{cname}' → テーブル '{target}' の推測"})
                break

    # 同じ名前の列が、別の表の「単独の主キー」になっている（equip_code →
    # equipment.equip_code のようなマスタ参照の型）。*_id の規約が無いデータでは
    # こちらが本命になる。まとまり違いの同型表（兄弟）同士は誤りなので出さない。
    def _suffix(name):
        return name.split("__", 1)[1] if "__" in name else name

    def _group(name):
        return name.split("__", 1)[0] if "__" in name else ""

    pk_owner: dict = {}
    for tname, t in ptables.items():
        pks = [c["name"] for c in t["columns"] if c["pk"]]
        if len(pks) == 1:
            pk_owner.setdefault(pks[0].lower(), []).append((tname, pks[0]))

    seen = {(s["from"].lower(), s["to"].lower()) for s in sugs}
    for tname, t in ptables.items():
        for col in t.get("columns", []):
            cands = [(tt, tc) for tt, tc in pk_owner.get(col["name"].lower(), [])
                     if tt != tname and _suffix(tt) != _suffix(tname)]
            if not cands:
                continue
            # 同じまとまりに相手がいればそれだけ。いなければ「またぎ」の候補に
            # なるが、相手が多すぎる（同名の主キーが4表以上）ものは曖昧すぎる
            # ので出さない（equip の部品コード → 全拠点の部品表、のような総当たり）
            same = [c for c in cands if _group(c[0]) == _group(tname)]
            if not same and len(cands) > 3:
                continue
            for target, to_col in (same or cands):
                frm, to = f"{tname}.{col['name']}", f"{target}.{to_col}"
                if (frm.lower(), to.lower()) in existing or (frm.lower(), to.lower()) in seen:
                    continue
                seen.add((frm.lower(), to.lower()))
                sugs.append({"from": frm, "to": to, "cardinality": "N:1",
                             "reason": f"同じ名前の列 '{col['name']}' が "
                                       f"'{target}' の主キー"})

    if db_path is None:
        return sugs

    samples, pk_values = _suggest_values(db_path, profile)

    def _overlap(frm: str, to: str):
        ft, fc = frm.split(".")
        tt, tc = to.split(".")
        s_ = samples.get((ft, fc))
        p_ = pk_values.get((tt, tc)) or samples.get((tt, tc))
        if not s_ or not p_:
            return None
        return len(s_ & p_) / len(s_)

    # 名前ベースの候補に一致率を添える。値が全く重ならない候補は、
    # JOINしても1行も繋がらない＝間違いなので出さない
    checked = []
    for sg in sugs:
        r = _overlap(sg["from"], sg["to"])
        if r is not None:
            if r == 0:
                continue
            sg = {**sg, "reason": sg["reason"] + f"／値の一致 {r * 100:.0f}%"}
        checked.append(sg)
    sugs = checked
    seen = {(s_["from"].lower(), s_["to"].lower()) for s_ in sugs}

    # 列名が違っても、値がほぼすべて相手の主キーに存在する列（9割以上）。
    # 名前の手がかりが無いぶん厳しめに見る。小さすぎる集合は偶然一致する
    # （例: 2値のコード）ので、両側とも5種類以上あるときだけ。
    for tname, t in ptables.items():
        for col in t.get("columns", []):
            frm_key = (tname, col["name"])
            s_ = samples.get(frm_key)
            if not s_ or len(s_) < 5:
                continue
            hits = []
            for (tt, tc), p_ in pk_values.items():
                if tt == tname or _suffix(tt) == _suffix(tname) or len(p_) < 5:
                    continue
                frm, to = f"{tname}.{col['name']}", f"{tt}.{tc}"
                if (frm.lower(), to.lower()) in existing or (frm.lower(), to.lower()) in seen:
                    continue
                r = len(s_ & p_) / len(s_)
                if r >= 0.9:
                    hits.append((r, tt, tc))
            if not hits:
                continue
            # 名前の手がかりが無い発見は、相手が1つに絞れるときだけ出す。
            # 日付列は全拠点のカレンダーに一致してしまうので、同じまとまりの
            # カレンダーが無ければ「どれと繋ぐべきか」を機械では決められない
            same = [h for h in hits if _group(h[1]) == _group(tname)]
            if not same and len(hits) > 1:
                continue
            for r, tt, tc in (same or hits):
                frm, to = f"{tname}.{col['name']}", f"{tt}.{tc}"
                seen.add((frm.lower(), to.lower()))
                sugs.append({"from": frm, "to": to, "cardinality": "N:1",
                             "reason": f"列名は違うが値が一致"
                                       f"（{r * 100:.0f}%が '{tt}.{tc}' に存在）"})
    return sugs


def coverage(profile: dict, meta: dict) -> dict:
    """メタ情報の充実度。カタログページの案内表示に使う。"""
    ptables = profile.get("tables", {})
    mtables = meta.get("tables") or {}
    n_tables = len(ptables)
    n_tdesc = sum(1 for t in ptables if (mtables.get(t) or {}).get("description"))
    n_cols = sum(len(t["columns"]) for t in ptables.values())
    n_cdesc = 0
    for tname, t in ptables.items():
        mcols = (mtables.get(tname) or {}).get("columns") or {}
        for c in t["columns"]:
            cm = mcols.get(c["name"]) or {}
            if cm.get("description") or cm.get("values"):
                n_cdesc += 1
    return {
        "tables": (n_tdesc, n_tables),
        "columns": (n_cdesc, n_cols),
        "relationships": len(meta.get("relationships") or []),
        "glossary": glossary_count(meta),
        "examples": len(meta.get("examples") or []),
    }


# =============================================================================
# 結合の端点表記（"table.col" / "alias.table.col" の相互変換）
# =============================================================================

def parse_endpoint(end: str, default_alias: str):
    """'table.col' または 'alias.table.col' を (alias, table, column) に解く。"""
    parts = [p.strip() for p in str(end).split(".")]
    if len(parts) == 3:
        return parts[0], parts[1], parts[2]
    if len(parts) == 2:
        return default_alias, parts[0], parts[1]
    return None


def parse_endpoint_cols(end: str, default_alias: str):
    """端点を (alias, table, [列, ...]) に解く。複合キーの括弧形式にも対応。

      'table.col'            → (default_alias, table, [col])
      'alias.table.col'      → (alias, table, [col])
      'table.(c1, c2)'       → (default_alias, table, [c1, c2])   ※複合キー
      'alias.table.(c1, c2)' → (alias, table, [c1, c2])
    """
    raw = str(end).strip()
    m = re.match(r"^(.+?)\.\(([^()]*)\)$", raw)
    if m:
        cols = [c.strip() for c in m.group(2).split(",") if c.strip()]
        parts = [p.strip() for p in m.group(1).split(".")]
        if not cols:
            return None
        if len(parts) == 1:
            return default_alias, parts[0], cols
        if len(parts) == 2:
            return parts[0], parts[1], cols
        return None
    p = parse_endpoint(raw, default_alias)
    return (p[0], p[1], [p[2]]) if p else None


def format_endpoint(alias: str, table: str, cols: list, own_alias: str) -> str:
    """(alias, table, 列リスト) を保存用の文字列に戻す。自DBなら alias は書かない。"""
    head = table if alias == own_alias else f"{alias}.{table}"
    if len(cols) == 1:
        return f"{head}.{cols[0]}"
    return f"{head}.({', '.join(cols)})"


def rel_pairs(rel: dict, own_alias: str):
    """関連1件を ((from側 alias, table), (to側 alias, table), [(from列, to列), ...]) に解く。

    解けない・列数が合わないときは None（乖離検知が別途知らせる）。
    単一列の関連は列ペア1つのリストになるので、呼び出し側は形を区別しなくてよい。
    """
    a = parse_endpoint_cols(rel.get("from", ""), own_alias)
    b = parse_endpoint_cols(rel.get("to", ""), own_alias)
    if not a or not b or len(a[2]) != len(b[2]):
        return None
    return (a[0], a[1]), (b[0], b[1]), list(zip(a[2], b[2]))


def node_id(alias: str, table: str) -> str:
    """テーブル（親ノード）のID。"""
    return f"{alias}.{table}"


# 列ノード（親テーブルの中に並ぶ子ノード）のID。
# テーブルIDが "alias.table" なので、列との区切りには "::" を使う。
COL_SEP = "::"


def col_node_id(alias: str, table: str, column: str) -> str:
    return f"{alias}.{table}{COL_SEP}{column}"


def edge_label(cardinality: str | None) -> str:
    """IPA表記の関連ラベル。線は列ノード同士を結ぶので、列名はラベルに出さず
    多重度だけを示す（始点側 ─ 終点側）。例: "* ─ 1"
    """
    tail, head = _CARD_ENDS.get(cardinality or "N:1", ("*", "1"))
    return f"{tail} ─ {head}"


def collect_edges(entries: list[dict]) -> list[dict]:
    """キャンバス/ER図に描く結合を集める。

    entries: [{"alias": str, "profile": dict, "meta": dict}, ...]
    戻り値の各要素:
      {"id", "source", "target", "label", "kind": "fk"|"meta", "owner", "index"}
      kind="fk"   … DBに宣言されたFOREIGN KEY（削除不可）
      kind="meta" … .meta.yaml の relationships（編集・削除可。index は配列位置）
    """
    nodes = {node_id(e["alias"], t) for e in entries for t in e["profile"].get("tables", {})}

    # メタ側の端点集合（FKと重複したら FK 側を出さない）。複合キーは列ペアごとに持つ
    meta_pairs = set()
    for e in entries:
        for rel in (e["meta"].get("relationships") or []):
            pr = rel_pairs(rel, e["alias"])
            if pr:
                (fa, ftb), (ta, ttb), pairs = pr
                for fc, tc in pairs:
                    meta_pairs.add(((fa, ftb, fc), (ta, ttb, tc)))

    def valid(alias_, table_, cols_):
        """端点のテーブルがキャンバス上にあり、列もすべて実在するか。"""
        if node_id(alias_, table_) not in nodes:
            return False
        e = next((x for x in entries if x["alias"] == alias_), None)
        have = {c["name"] for c in (e["profile"]["tables"].get(table_) or {}).get("columns", [])}
        return all(c in have for c in cols_)

    edges: list[dict] = []
    for e in entries:
        alias = e["alias"]
        for tname, t in e["profile"].get("tables", {}).items():
            for fk in t.get("fks", []):
                a = (alias, tname, fk["from"])
                b = (alias, fk["table"], fk["to"])
                if (not valid(a[0], a[1], [a[2]]) or not valid(b[0], b[1], [b[2]])
                        or (a, b) in meta_pairs):
                    continue
                edges.append({
                    "id": f"fk||{a[0]}.{a[1]}.{a[2]}||{b[0]}.{b[1]}.{b[2]}",
                    "source": col_node_id(*a), "target": col_node_id(*b),
                    "from": a, "to": b,
                    "pairs": [[a[2], b[2]]],
                    "from_ref": format_endpoint(a[0], a[1], [a[2]], alias),
                    "to_ref": format_endpoint(b[0], b[1], [b[2]], alias),
                    "label": edge_label("N:1"), "cardinality": "N:1",
                    "kind": "fk", "owner": alias, "index": None,
                })
        for i, rel in enumerate(e["meta"].get("relationships") or []):
            pr = rel_pairs(rel, alias)
            if not pr:
                continue
            (fa, ftb), (ta, ttb), pairs = pr
            if (not valid(fa, ftb, [p_[0] for p_ in pairs])
                    or not valid(ta, ttb, [p_[1] for p_ in pairs])):
                continue
            card = rel.get("cardinality") or "N:1"
            # 線は先頭の列ペアに係留する（複合キーでも線は1本）
            a = (fa, ftb, pairs[0][0])
            b = (ta, ttb, pairs[0][1])
            edges.append({
                "id": f"rel||{alias}||{i}",
                "source": col_node_id(*a), "target": col_node_id(*b),
                "from": a, "to": b,
                "pairs": [[fc, tc] for fc, tc in pairs],
                "from_ref": rel.get("from"), "to_ref": rel.get("to"),
                "label": edge_label(card), "cardinality": card,
                "kind": "meta", "owner": alias, "index": i,
            })
    return edges


def declared_pk(profile: dict, tname: str) -> list[str]:
    """DBが宣言している主キー（複合キーは構成順）。宣言が無ければ空リスト。"""
    t = profile.get("tables", {}).get(tname) or {}
    cols = [c for c in t.get("columns", []) if c.get("pk")]
    cols.sort(key=lambda c: c.get("pk_seq") or 0)
    return [c["name"] for c in cols]


def effective_pk(profile: dict, meta: dict, tname: str):
    """実際に主キーとして扱う列と、その出所を返す。

    戻り値: (列名リスト, "override" | "declared" | "none")
    メタの tables.<name>.primary_key があれば、DB宣言より優先する。
    主キーが宣言されていないテーブル（CSV取込など）に人が指定できるようにするため。
    """
    valid = [c["name"] for c in (profile.get("tables", {}).get(tname) or {}).get("columns", [])]
    ov = ((meta.get("tables") or {}).get(tname) or {}).get("primary_key")
    if ov:
        cols = [c for c in ov if c in valid]
        if cols:
            return cols, "override"
    d = declared_pk(profile, tname)
    return (d, "declared") if d else ([], "none")


def fk_columns(entries: list[dict], alias: str, tname: str) -> set:
    """外部キーとして扱う列（FK宣言 + メタの relationships の from 側）。"""
    out = set()
    for e in entries:
        if e["alias"] == alias:
            t = e["profile"].get("tables", {}).get(tname) or {}
            for fk in t.get("fks", []):
                out.add(fk["from"])
        for rel in (e["meta"].get("relationships") or []):
            p = parse_endpoint_cols(rel.get("from", ""), e["alias"])
            if p and p[0] == alias and p[1] == tname:
                out.update(p[2])
    return out


# --- IPA表記のノードラベル -------------------------------------------------------
#: 1DBあたりに持つ例文の上限。例文は毎回 system prompt に載るので、
#: 増えるほどテーブル定義の説明が押し出される。DB統一で1ファイルに
#: 全拠点分（現在105件）が集まるため、その全量が収まる値にしてある。
EXAMPLES_MAX = 200


def _norm_sql(sql: str) -> str:
    """比べるためだけの正規化。空白の入れ方と大小の違いを無視する。"""
    return " ".join(str(sql or "").split()).lower()


def dedupe_examples(examples: list[dict]) -> list[dict]:
    """例文から重複を落とす。

    重複は「質問文とSQLの両方が同じ」ものだけ（後勝ち）。
    質問文だけ・SQLだけの一致は重複扱いしない。DB統一後は
    「同じ質問に拠点ごとの別SQL」が正当に共存するため
    （質問文だけで束ねると、保存のたびに他拠点の例文が消える）。
    説明は任意なので、書かれているものだけを残す。上限は呼び出し側で扱う。
    """
    by_key: dict = {}
    for ex in examples or []:
        q = str(ex.get("q") or "").strip()
        sql = str(ex.get("sql") or "").strip()
        if not q or not sql:
            continue
        desc = str(ex.get("description") or "").strip()
        by_key[(q, _norm_sql(sql))] = {
            "q": q, **({"description": desc} if desc else {}), "sql": sql}
    return list(by_key.values())


def find_example(examples: list[dict], sql: str) -> dict | None:
    """同じSQLの例文が既にあれば返す。"""
    key = _norm_sql(sql)
    for ex in examples or []:
        if _norm_sql(ex.get("sql")) == key:
            return ex
    return None


def load_layout(meta: dict) -> dict:
    """メタからノード座標を読む。{'alias.table': (x, y)}"""
    raw = meta.get("er_layout") or {}
    if not isinstance(raw, dict):
        return {}
    out = {}
    for k, v in raw.items():
        # 期待する形は [x, y]。辞書や文字列など形の違う項目は読み飛ばす
        # （1つ壊れているだけでER図全体が出なくなるのを避ける）
        if not isinstance(v, (list, tuple)) or len(v) < 2:
            continue
        try:
            out[str(k)] = (float(v[0]), float(v[1]))
        except (TypeError, ValueError):
            continue
    return out


def _dbmod():
    """db モジュール。循環importを避けるため使うときに読む。"""
    import db
    return db


def er_payload(path, profile: dict | None = None,
               meta: dict | None = None) -> dict:
    """自前キャンバス用に、テーブル・列・関連を素のJSONで渡す。"""
    profile = profile if profile is not None else profile_db(path)
    meta = meta if meta is not None else load_meta(path)
    alias = _dbmod().alias_for(path)
    entries = [{"alias": alias, "profile": profile, "meta": meta,
                "path": path, "editable": True}]

    layout = load_layout(meta)
    nodes = []
    for i, (tname, t) in enumerate(profile["tables"].items()):
        fks = fk_columns(entries, alias, tname)
        pk = set(effective_pk(profile, meta, tname)[0])
        nid = node_id(alias, tname)
        pos = layout.get(nid) or [40 + (i % 4) * 300, 40 + (i // 4) * 320]
        nodes.append({
            "id": nid, "alias": alias, "table": tname,
            "x": pos[0], "y": pos[1], "rows": t.get("row_count"),
            "columns": [{"name": c["name"], "type": c["type"],
                         "pk": c["name"] in pk, "fk": c["name"] in fks}
                        for c in t["columns"]],
        })

    # 描いていないテーブルに向かう線が混じらないよう、置いたノードで絞る
    placed = {n["id"] for n in nodes}
    edges = []
    for e in collect_edges(entries):
        if (node_id(*e["from"][:2]) not in placed
                or node_id(*e["to"][:2]) not in placed):
            continue
        owner = e.get("owner")
        edges.append({"id": e["id"], "kind": e["kind"], "label": e["label"],
                      "cardinality": e["cardinality"], "index": e.get("index"),
                      "from": list(e["from"]), "to": list(e["to"]),
                      "pairs": [list(p) for p in (e.get("pairs")
                                                  or [[e["from"][2], e["to"][2]]])],
                      "from_ref": e.get("from_ref"), "to_ref": e.get("to_ref"),
                      "owner": owner, "editable": e["kind"] == "meta"})
    return {"nodes": nodes, "edges": edges, "alias": alias}


# =============================================================================
# 関連の向きと多重度（ER図とデータ検査が共有する規則）
# =============================================================================

# IPA表記の多重度ラベル: 線の両端に "1" と "*" を置く
_CARD_ENDS = {
    "N:1": ("*", "1"),   # from(多側) ─ to(1側)
    "1:N": ("1", "*"),
    "1:1": ("1", "1"),
    "N:M": ("*", "*"),
}

#: 向きを入れ替えたときの多重度。1:1 と N:M は入れ替えても同じ。
_CARD_FLIP = {"N:1": "1:N", "1:N": "N:1", "1:1": "1:1", "N:M": "N:M"}


def _is_sole_pk(profile: dict, meta: dict, table: str, column: str) -> bool:
    """その列が、そのテーブルの主キー全体か（単独主キーか）。"""
    pk, _ = effective_pk(profile, meta, table)
    return len(pk) == 1 and pk[0] == column


def normalize_direction(a: tuple, b: tuple, cardinality: str, lookup) -> tuple:
    """関連の向きを「子（外部キー側）→ 親（主キー側）」に揃える。

    ER図はIPA表記なので矢印を描かない。見た目に向きが無いぶん、人は
    好きな方向にドラッグする。ところが from/to は単なる描画順ではなく、
    「どちらが参照している側か」を表しており、参照整合性の検査
    （親に居ない子を数える）はこの向きに依存する。逆向きに登録されると
    「入金の無い請求」を異常として数えるような、意味の反転が起きる。

    lookup(alias) は (profile, meta) を返す関数。判断できないときは触らない。

    戻り値: (from, to, cardinality)
    """
    card = cardinality or "N:1"
    try:
        pa, ma = lookup(a[0])
        pb, mb = lookup(b[0])
    except Exception:
        return a, b, card
    if not (pa and pb):
        return a, b, card
    a_is_pk = _is_sole_pk(pa, ma, a[1], a[2])
    b_is_pk = _is_sole_pk(pb, mb, b[1], b[2])
    # 片方だけが主キーなら、そちらを親（to）にする
    if a_is_pk and not b_is_pk:
        return b, a, _CARD_FLIP.get(card, card)
    return a, b, card


def _sample_values(profile: dict, table: str, column: str) -> list:
    """プロファイルに残っている実値（あれば）。警告文に例として添える用。"""
    st = ((profile or {}).get("tables", {}).get(table) or {}).get("col_stats", {}).get(column) or {}
    vals = st.get("values") or []
    return [v[0] if isinstance(v, (list, tuple)) else v for v in vals]


def tuple_unique(path, table: str, cols: list) -> bool:
    """その表で「列の組」ごとに1行しかない（＝組として一意）か。実データで数える。

    複合キーの判定に使う。単独の列では重複していても、組で一意なら
    N:1 の親として成立する。数えられないときは False（安全側）。
    """
    try:
        conn = db.connect_scope([(str(path), "p")])
        try:
            q = lambda x: '"' + str(x).replace('"', '""') + '"'
            sql = (f"SELECT 1 FROM p.{q(table)} GROUP BY "
                   + ", ".join(q(c) for c in cols)
                   + " HAVING COUNT(*) > 1 LIMIT 1")
            return conn.execute(sql).fetchone() is None
        finally:
            conn.close()
    except Exception:
        return False


def link_check(child: tuple, parent: tuple, lookup, path_of) -> dict:
    """この2列を関連として結んでよいかを、実データを見て判定する。

    child / parent は (alias, table, column)。normalize_direction を通した後の向き。
    lookup(alias) は (profile, meta)、path_of(alias) は DBファイルのパスを返す。

    戻り値: {"level": "ok" | "warn" | "block", "issues": [{level, title, detail}]}
      block … 結んではいけない（値が全く重ならない等）。保存しない
      warn  … 結べるが、意味を確かめてほしい（型が違う・親が一意でない等）。確認して保存
      ok    … 問題なし

    なぜ止めるかを人が読める形で必ず添える。ER図の線は「この列で JOIN してよい」という
    AIへの指示なので、実データで JOIN が成立しない線を引くと、AIが自信を持って
    間違った結合を書くようになる。
    """
    issues: list[dict] = []
    ca, ct, cc = child
    pa, pt, pc = parent

    def add(level, title, detail):
        issues.append({"level": level, "title": title, "detail": detail})

    # --- カタログ上の情報（プロファイル）で分かること ---------------------------------
    prof_c, meta_c = lookup(ca)
    prof_p, meta_p = lookup(pa)
    col_c = next((c for c in (prof_c["tables"].get(ct) or {}).get("columns", [])
                  if c["name"] == cc), {}) if prof_c else {}
    col_p = next((c for c in (prof_p["tables"].get(pt) or {}).get("columns", [])
                  if c["name"] == pc), {}) if prof_p else {}
    type_c = str(col_c.get("type") or "").upper()
    type_p = str(col_p.get("type") or "").upper()

    def kind(t):
        if any(k in t for k in ("INT",)):
            return "整数"
        if any(k in t for k in ("REAL", "FLOA", "DOUB", "NUM", "DEC")):
            return "小数"
        if any(k in t for k in ("CHAR", "TEXT", "CLOB")):
            return "文字"
        if "DATE" in t or "TIME" in t:
            return "日時"
        return t or "不明"

    if type_c and type_p and kind(type_c) != kind(type_p):
        add("warn", "型が違います",
            f"{ct}.{cc} は {type_c}（{kind(type_c)}）、{pt}.{pc} は {type_p}（{kind(type_p)}）です。"
            "SQLite は型が違っても比較できてしまいますが、たいてい別の意味の列です"
            "（例: 数値のIDと文字のコード）。本当に同じものを指すか確かめてください。")

    pk_c = set(effective_pk(prof_c, meta_c, ct)[0]) if prof_c else set()
    pk_p = set(effective_pk(prof_p, meta_p, pt)[0]) if prof_p else set()
    if cc in pk_c and pk_c == {cc} and pc in pk_p and pk_p == {pc} and (ct != pt or ca != pa):
        add("warn", "主キー同士を結んでいます",
            f"{ct}.{cc} も {pt}.{pc} もそれぞれのテーブルの主キーです。"
            "1対1の関連（同じIDを持つ2つのテーブル）なら正しいですが、"
            "「たまたま両方IDという名前」なら結ぶべきではありません。")

    # --- 実データで分かること（読み取り専用で数える） ---------------------------------
    try:
        pc_path, pp_path = path_of(ca), path_of(pa)
        conn = db.connect_scope([(pc_path, "c"), (pp_path, "p")] if pc_path != pp_path
                                else [(pc_path, "c")])
        # どこで落ちても閉じる。外側の except が拾うので、finally が無いと接続が残る
        try:
            pal = "c" if pc_path == pp_path else "p"
            q = lambda s: '"' + str(s).replace('"', '""') + '"'
            C = f'"c".{q(ct)}', q(cc)
            P = f'"{pal}".{q(pt)}', q(pc)

            n_child = conn.execute(f"SELECT COUNT(*) FROM {C[0]} WHERE {C[1]} IS NOT NULL").fetchone()[0]
            n_parent = conn.execute(f"SELECT COUNT(*) FROM {P[0]} WHERE {P[1]} IS NOT NULL").fetchone()[0]
            n_parent_distinct = conn.execute(
                f"SELECT COUNT(DISTINCT {P[1]}) FROM {P[0]} WHERE {P[1]} IS NOT NULL").fetchone()[0]
            # 子の値のうち親に存在するもの / しないもの
            matched = conn.execute(
                f"SELECT COUNT(*) FROM {C[0]} c0 WHERE c0.{C[1]} IS NOT NULL "
                f"AND EXISTS (SELECT 1 FROM {P[0]} p0 WHERE p0.{P[1]} = c0.{C[1]})").fetchone()[0]
            # 子の「異なる値」の数と、親の値のうち子から参照されている数（親側のカバー率）。
            # 「status(1,2,3,9) → product_id(1〜40)」のような偶然の一致は、子の値は全部
            # 親に見つかるのに、親の値はほとんど参照されない。本物の外部キーなら親の多くが
            # 参照される。値の一致だけでは見抜けないので、この角度を足す。
            n_child_distinct = conn.execute(
                f"SELECT COUNT(DISTINCT {C[1]}) FROM {C[0]} WHERE {C[1]} IS NOT NULL").fetchone()[0]
            parent_hit = conn.execute(
                f"SELECT COUNT(DISTINCT p0.{P[1]}) FROM {P[0]} p0 "
                f"WHERE EXISTS (SELECT 1 FROM {C[0]} c0 WHERE c0.{C[1]} = p0.{P[1]})").fetchone()[0]
        finally:
            conn.close()

        if n_child and n_parent and matched == 0:
            add("block", "値が1件も一致しません",
                f"{ct}.{cc} の {n_child:,} 件は、{pt}.{pc} の {n_parent:,} 件のどれとも一致しません。"
                "この2列で JOIN しても結果は必ず0行になります。別の意味の列です。")
        elif n_child and matched:
            miss = n_child - matched
            rate = miss / n_child * 100
            if rate >= 30:
                add("warn", "一致しない値が多すぎます",
                    f"{ct}.{cc} の {n_child:,} 件のうち {miss:,} 件（{rate:.0f}%）が {pt}.{pc} に存在しません。"
                    "外部キーなら親に無い値はごく少数のはずです。列の取り違えの可能性があります。")
            elif miss:
                add("info", "親に無い値があります",
                    f"{ct}.{cc} の {miss:,} 件（{rate:.1f}%）が {pt}.{pc} に存在しません"
                    "（未登録・削除済みの参照。数が少なければ通常の範囲です）。")
            # 子の値の種類が極端に少なく、親のごく一部にしか当たらない → 区分値とIDの偶然の一致
            if n_parent_distinct >= 10 and n_child_distinct <= 10                     and parent_hit / n_parent_distinct < 0.5:
                add("warn", "区分値とIDを結んでいる可能性があります",
                    f"{ct}.{cc} は値の種類が {n_child_distinct} 種類しかなく"
                    f"（{', '.join(str(v) for v in _sample_values(prof_c, ct, cc)[:6])} など）、"
                    f"{pt}.{pc} の {n_parent_distinct:,} 種類のうち {parent_hit} 種類にしか当たりません。"
                    "ステータスや区分のような「コード値」の列を、番号がたまたま重なるIDの列に"
                    "結ぼうとしていませんか。")
        if n_parent and n_parent_distinct < n_parent:
            dup = n_parent - n_parent_distinct
            add("warn", "参照先（1側）の値が一意ではありません",
                f"{pt}.{pc} は {n_parent:,} 件中 {dup:,} 件が重複しています。"
                "「1側」は本来ユニークです。重複したまま JOIN すると行が増えて集計が膨らみます。"
                "多重度を N:M にするか、参照先を主キー列に変えてください。")
    except Exception as e:
        add("info", "実データでの確認ができませんでした", str(e)[:120])

    level = "ok"
    if any(i["level"] == "block" for i in issues):
        level = "block"
    elif any(i["level"] == "warn" for i in issues):
        level = "warn"
    return {"level": level, "issues": issues}


def child_parent(entries: list[dict], edge: dict) -> tuple:
    """この関連の (子, 親)。参照整合性の検査はこの向きでしか意味を持たない。

    保存済みの from/to を鵜呑みにせず、主キーがどちら側にあるかで決め直す。
    手で書いた .meta.yaml が逆向きでも、検査は正しい向きで走る。
    """
    frm, to = tuple(edge["from"]), tuple(edge["to"])
    by_alias = {e["alias"]: e for e in entries}

    def sole_pk(ep):
        e = by_alias.get(ep[0])
        if not e:
            return None
        return _is_sole_pk(e["profile"], e.get("meta") or {}, ep[1], ep[2])

    f_pk, t_pk = sole_pk(frm), sole_pk(to)
    if f_pk and not t_pk:
        return to, frm            # from が親だった。入れ替える
    return frm, to


# =============================================================================
# LLM用テキスト生成（プロンプト＝カタログの直列化）
# =============================================================================

def _fmt_value_list(values, col_meta_values: dict) -> str:
    """実値一覧を '1=受付(120), 2=出荷済(300)' 形式で。メタのコード値辞書で意味を補完。"""
    parts = []
    for v, n in values:
        key = "" if v is None else str(v)
        label = (col_meta_values or {}).get(key)
        disp = "NULL" if v is None else str(v)
        if label:
            disp += f"={label}"
        parts.append(f"{disp}({n})")
    return ", ".join(parts)


def table_text(alias: str, tname: str, profile: dict, meta: dict, full: bool) -> str:
    """1テーブル分の説明テキスト。full=False なら1行要約のみ。

    表の名前に「DB名.」は付けない。このアプリのDBは常に1つで、
    AIにその名前を教えると、回答やSQLにまでDB名が出てくる
    （画面ではDBという概念を見せていないので、利用者には意味不明になる）。
    """
    t = profile["tables"].get(tname)
    if t is None:
        return f"- {tname} : (プロファイル未取得)"
    tmeta = ((meta.get("tables") or {}).get(tname)) or {}
    desc = (tmeta.get("description") or "").strip()
    draft = "（AI推測・未確認）" if tmeta.get("ai_draft") else ""
    rc = t.get("row_count")
    rc_s = f"{rc:,}行" if rc is not None else "行数不明"
    head = f"{tname}（{rc_s}）"
    if not full:
        line = f"- {head}" + (f" : {desc}{draft}" if desc else "")
        terms = list(table_glossary(meta, tname))
        # 用語があることだけ知らせる。定義は describe_table で取りに行かせる
        return line + (f" / 業務用語: {', '.join(terms)}" if terms else "")

    lines = [f"### {head}"]
    if desc:
        lines.append(f"{desc}{draft}")

    # 主キーは「1行が何を表すか（粒度）」の手がかりなので、複合キーは構成順で明示する
    pk_cols, pk_src = effective_pk(profile, meta, tname)
    note = {"override": "（人が指定）", "declared": "", "none": ""}[pk_src]
    if len(pk_cols) > 1:
        lines.append(f"主キー{note}: ({', '.join(pk_cols)}) の複合キー → この組み合わせで1行が一意。"
                     f"結合するときは{len(pk_cols)}列すべてを条件にする。")
    elif len(pk_cols) == 1:
        lines.append(f"主キー{note}: {pk_cols[0]}")
    else:
        lines.append("主キー: なし（宣言が無く、指定もされていない）。"
                     "重複行があり得るので COUNT(DISTINCT ...) の要否に注意する。")

    mcols = tmeta.get("columns") or {}
    lines.append("列:")
    for c in t["columns"]:
        cm = (mcols.get(c["name"])) or {}
        parts = [f"- {c['name']} {c['type']}".rstrip()]
        if c["pk"]:
            parts.append("PK")
        if cm.get("description"):
            parts.append(f": {cm['description']}")
        stat = t.get("col_stats", {}).get(c["name"]) or {}
        if "values" in stat:
            parts.append(f"/ 値: {_fmt_value_list(stat['values'], cm.get('values'))}")
        elif cm.get("values"):
            vv = ", ".join(f"{k}={v}" for k, v in cm["values"].items())
            parts.append(f"/ コード値: {vv}")
        elif "min" in stat:
            parts.append(f"/ 範囲: {stat['min']} 〜 {stat['max']}")
        lines.append(" ".join(parts))
    if t.get("sample_rows"):
        lines.append(f"サンプル行 {t['sample_columns']}:")
        for r in t["sample_rows"][:3]:
            lines.append(f"  {r}")

    tgl = table_glossary(meta, tname)
    if tgl:
        lines.append(f"{tname} の業務用語（質問にこの言葉が出たら必ずこの定義に従う）:")
        lines.extend(glossary_lines(tgl))
    return "\n".join(lines)


def _sibling_groups(by_group: dict) -> list:
    """同じ名前の表（接頭辞を除いた部分）を持つまとまり同士を束ねて返す。

    生産実績__daily と 生産実績_関西工場__daily のような対を見つける。
    名前の一致だけで判定し、意味までは断定しない（文面も事実だけ言う）。
    """
    suffix_owner: dict = {}
    for g, ts in by_group.items():
        for t in ts:
            suffix_owner.setdefault(t.split("__", 1)[1], set()).add(g)
    parent = {g: g for g in by_group}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for gs in suffix_owner.values():
        gs = sorted(gs)
        for other in gs[1:]:
            parent[find(other)] = find(gs[0])
    fams: dict = {}
    for g in by_group:
        fams.setdefault(find(g), []).append(g)
    return sorted(sorted(v) for v in fams.values() if len(v) > 1)


def db_text(alias: str, db_path, tables: list[str] | None, full: bool) -> str:
    """1DB分の説明テキスト（プロファイル＋メタの合成）。"""
    profile = profile_db(db_path)
    meta = load_meta(db_path)
    names = tables or list(profile["tables"].keys())

    shown = set(names)
    limited = tables is not None and len(shown) < len(profile["tables"])

    lines = []
    lines.append("## 使えるデータ")
    if limited:
        # 絞っていることを明示しないと、AIは知識として知っている他データの話を
        # 始め、最後に「使えません」と言う（利用者からは「できないのに答える」に見える）
        lines.append(
            "※ 利用者がいま対象にしているのは、下に挙げる表だけです。"
            "ここに無いデータは存在しないものとして答えてください。"
            "他の表があるかのような案内・前置き・質問返しはしないこと。"
            "対象外の話を求められたら、サイドバーの SQLite3 でその表に"
            "チェックを入れるよう一言で伝えてください。")

    # 表名の接頭辞（まとまり）ごとに、表示中の表を束ねる
    by_group: dict = {}
    for t in names:
        if "__" in t:
            by_group.setdefault(t.split("__", 1)[0], []).append(t)
    gmeta = db_groups(meta)

    # 同じ名前の表を持つまとまり同士は「同じ領域の拠点・区分違い」。
    # スキーマから機械的に分かることは人に書かせない（書くと表の入れ替えで
    # 腐る）。表示中の表だけから導くので、選択外のまとまりの名前は漏れない。
    for fam in _sibling_groups(by_group):
        lines.append(
            "※ " + "・".join(fam)
            + " は同じ構成の表を持つまとまりです（拠点・区分などの分かれ）。"
              "全体・合計を求められたら、該当する表を UNION ALL で合算すること。"
              "どれか1つのまとまりを黙って代表にしない。")

    # まとまりごとのメモ（複数の表にまたがる前提）。表示中のぶんだけ渡す
    for g in sorted(by_group):
        memo = (gmeta.get(g) or {}).get("description")
        if memo:
            lines.append(f"【{g}】" + chr(10) + memo)
    lines.append("")
    if full:
        for tname in names:
            lines.append(table_text(alias, tname, profile, meta, full=True))
            lines.append("")
    else:
        lines.append("テーブル一覧:")
        for tname in names:
            lines.append(table_text(alias, tname, profile, meta, full=False))
        lines.append("")

    # 表を絞っているときは、関連・用語・例文もその表のものだけにする。
    # ここを素通しにすると、載せていない表の名前がSQL例文などから漏れ、
    # AIが「あるはず」と判断してその表を読みに行ってしまう。
    def _mentions_only_shown(text: str) -> bool:
        """その文が触れている表が、すべて表示中の表かどうか。"""
        hit = [t for t in profile["tables"] if re.search(
            r"(?<![\w.])" + re.escape(t) + r"(?![\w])", str(text or ""))]
        return bool(hit) and all(t in shown for t in hit)

    rels = [r for r in (meta.get("relationships") or [])]
    if limited:
        rels = [r for r in rels
                if _mentions_only_shown(f"{r.get('from')} {r.get('to')}")]
    fk_lines = []
    for tname in names:
        for fk in profile["tables"].get(tname, {}).get("fks", []):
            fk_lines.append(f"- {tname}.{fk['from']} = {fk['table']}.{fk['to']} (FK宣言)")
    if rels or fk_lines:
        lines.append("結合キー（JOINにはこれを使う）:")
        lines.extend(fk_lines)
        for r in rels:
            card = f" ({r['cardinality']})" if r.get("cardinality") else ""
            pr = rel_pairs(r, "")
            if pr and len(pr[2]) > 1:
                (fa, ftb), (ta, ttb), pairs = pr
                fh = ftb if not fa else f"{fa}.{ftb}"
                th = ttb if not ta else f"{ta}.{ttb}"
                conds = " AND ".join(f"{fh}.{fc} = {th}.{tc}" for fc, tc in pairs)
                lines.append(f"- {conds}{card}"
                             f" ※複合キー: {len(pairs)}列すべてを同時に結合条件へ。"
                             "片方の列だけで結ばない")
            else:
                lines.append(f"- {r.get('from')} = {r.get('to')}{card}")
        lines.append("")

    def _no_hidden_tables(text: str) -> bool:
        """文中に出てくる表が、すべて表示中か（表名が出てこなければ True）。"""
        hit = [t for t in profile["tables"] if re.search(
            r"(?<![\w.])" + re.escape(t) + r"(?![\w])", str(text or ""))]
        return all(t in shown for t in hit)

    gl = db_glossary(meta)
    if limited and gl:
        # SQL式は表示表しか引かないもの、説明文も表示外の表に触れないものだけ。
        # 説明文を素通しにすると、選択外の表の名前と役割がここから漏れる
        gl = {k: v for k, v in gl.items()
              if (not (v or {}).get("sql") or _mentions_only_shown((v or {}).get("sql")))
              and _no_hidden_tables((v or {}).get("description"))}
    if gl:
        lines.append("テーブルをまたぐ業務用語（質問にこの言葉が出たら必ずこの定義に従う）:")
        lines.extend(glossary_lines(gl))
        lines.append("")

    exs = meta.get("examples") or []
    if limited:
        exs = [e for e in exs if _mentions_only_shown(e.get("sql"))]
    if exs:
        lines.append("正しいと確認済みの質問とSQLの例:")
        for ex in exs:
            lines.append(f"Q: {ex.get('q')}")
            # 説明は「この例をどう読むか」の注意書き。人が書いたときだけ載せる
            if ex.get("description"):
                lines.append(f"補足: {ex['description']}")
            lines.append(f"SQL: {ex.get('sql')}")
        lines.append("")
    return "\n".join(lines)


#: 組み立て済みのカタログ本文。DBが多いと1回あたり数十msかかり、
#: 質問のたび・対象を選び直すたびに作り直すのは無駄なので覚えておく。
_TEXT_CACHE: dict = {}


def _text_key(alias: str, path, tables, full: bool):
    """中身が変わったら別物になるキー。DB・メタ・プロファイルの更新時刻を見る。"""
    p = Path(path)

    def stamp(f: Path) -> int:
        try:
            return f.stat().st_mtime_ns
        except OSError:
            return 0

    return (alias, str(p), tuple(tables or ()), full,
            stamp(p), stamp(meta_path(p)), stamp(_cache_path(p)))


def forget(db_path) -> None:
    """そのDBについて覚えているものを捨てる。DBを消したときに呼ぶ。

    本文のキャッシュは更新時刻で自動的に切り替わるが、プロファイルの
    キャッシュはファイルとして残る。DBが無くなったあとも残っていると、
    同じ名前で作り直したときに古い中身が出てくる。
    """
    p = Path(db_path)
    try:
        _cache_path(p).unlink(missing_ok=True)
    except OSError as e:
        print(f"[catalog] キャッシュを消せませんでした: {e}")
    for key in [k for k in _TEXT_CACHE if k[1] == str(p)]:
        _TEXT_CACHE.pop(key, None)


def db_text_cached(alias: str, path, tables=None, full: bool = True) -> str:
    """db_text の結果を使い回す版。カタログを直せば自動で作り直される。"""
    try:
        key = _text_key(alias, path, tables, full)
    except Exception:
        return db_text(alias, path, tables, full=full)
    hit = _TEXT_CACHE.get(key)
    if hit is None:
        hit = db_text(alias, path, tables, full=full)
        if len(_TEXT_CACHE) > 64:            # 古い世代が溜まりすぎないように
            _TEXT_CACHE.clear()
        _TEXT_CACHE[key] = hit
    return hit


def inline_length(scope: list[dict]) -> int:
    """詳細版カタログの文字数（列名までAIに渡せるかの判断に使う）。"""
    return sum(len(db_text_cached(s["alias"], s["path"], s.get("tables"), full=True))
               for s in (scope or []))


def inline_limit() -> int:
    """カタログを全文のまま入れる上限の天井（モデルを知らない呼び出し向け）。

    実効値は選択中モデルの文脈量から自動で決まる（models.inline_limit_for）ので、
    通常は prompt_for_scope に limit を渡す。ここはモデルが分からない場面の
    フォールバック（天井値）。読めなければ env の初期値に落とす。
    """
    try:
        import models
        return models.prompt_inline_limit()
    except Exception:
        return config.PROMPT_INLINE_LIMIT_CHARS


def prompt_for_scope(scope: list[dict], limit: int | None = None,
                     admin: bool = True) -> str:
    """選択スコープ全体のカタログテキスト。

    全文が上限（limit。省略時は管理者設定/env）以下なら詳細をインライン、
    超えるなら要約のみ（詳細は describe_table ツールで取得させる）。
    limit は「選択中のモデルが一度に読める量」から呼び出し側が渡せる
    （models.inline_limit_for 参照。固定値だと小さいモデルで溢れるため）。
    """
    if not scope:
        # 一般利用者に「取り込み画面で作って」と言わせない。
        # その画面は管理者専用で、メニューにも出ていない
        return ("（対象にできるテーブルがありません。"
                + ("「データ取り込み」でデータを入れるよう案内してください。"
                   if admin else
                   "サイドバーの一覧でチェックを入れるか、"
                   "データが入っていないことを管理者に伝えるよう案内してください。"
                   "取り込み画面は管理者専用なので、利用者には案内しないこと。")
                + "）")
    full = "\n".join(db_text_cached(s["alias"], s["path"], s.get("tables"), full=True)
                     for s in scope)
    if len(full) <= (limit if limit is not None else inline_limit()):
        return full
    compact = "\n".join(db_text_cached(s["alias"], s["path"], s.get("tables"), full=False)
                        for s in scope)
    # ここに載っているのはテーブル単位の説明までで、列名は入っていない。
    # それを言わずに渡すと「その列は無い」と早合点して、できることまで断ってしまう。
    return (compact + "\n"
            "【重要】対象のDBが多いため、上には各テーブルの説明までしか載せていません。"
            "**列名は1つも載っていません。**\n"
            "そのため、上に見当たらないという理由で「その列は無い」「そのテーブルは無い」と"
            "判断してはいけません。必要な列があるかどうかは、必ず describe_table を呼んで"
            "確かめること。名前から中身が推測できるテーブル（商品なら products、"
            "社員なら employees など）は、まず describe_table で列を見てから答えること。\n"
            "ユーザーに「その情報は無い」と答えてよいのは、関係しそうなテーブルを"
            "describe_table で実際に確認した後だけです。")


def describe_table_text(scope: list[dict], db_alias: str, tname: str) -> str:
    """describe_table ツールの実体。alias と テーブル名から詳細テキストを返す。"""
    # "alias.table" 形式で渡された場合に対応。
    # AIは db を指定したうえで table にも "alias.table" を入れてくることがある
    # （カタログには常にその形で載っているため）。db の有無に関係なく、
    # 先頭がいずれかのDBエイリアスに一致するときだけ剥がす。テーブル名そのものに
    # "." が入っている可能性を潰さないよう、一致しないときは触らない。
    if "." in tname:
        head, rest = tname.split(".", 1)
        known = {s["alias"].lower() for s in scope}
        if head.lower() in known and rest:
            if not db_alias or str(db_alias).lower() == head.lower():
                db_alias, tname = head, rest
    if not db_alias and scope:
        entry = scope[0]              # DBは常に1つ。呼ぶ側が名前を知る必要はない
    else:
        entry = next((s for s in scope if s["alias"].lower() == str(db_alias).lower()), None)
    if entry is None:
        aliases = ", ".join(s["alias"] for s in scope)
        return f"エラー: DBエイリアス '{db_alias}' は選択されていません。選択中: {aliases}"
    profile = profile_db(entry["path"])
    meta = load_meta(entry["path"])
    # 「そもそも無い」を先に見る。順番が逆だと、存在しない表に対して
    # 「対象に入っていません。チェックを入れてください」と案内してしまい、
    # 入れようにも一覧に出てこないので堂々巡りになる
    if tname not in profile["tables"]:
        cand = ", ".join(profile["tables"].keys())
        return f"エラー: テーブル '{tname}' は {db_alias} にありません。存在するテーブル: {cand}"
    if entry.get("tables") and tname not in entry["tables"]:
        # 利用者が対象から外した表。説明も見せない（中身と扱いを揃える）
        return (f"エラー: テーブル '{tname}' は実在しますが、いまの対象に入っていません。"
                "サイドバーの一覧でチェックを入れると使えます。")
    return table_text(entry["alias"], tname, profile, meta, full=True)


# ==========================================================================
# ===== 元 verify.py
# 相互検証（検算）。同じ数字を独立した2つの経路で計算して突き合わせる。
#
# text-to-SQL の最大のリスクは「もっともらしいが間違っているSQL」ではなく、
# 「正しいSQLなのに、業務的には別の数字を指している」ことにある。
# 実際、demo_sales の「売上」は明細から数えると1.23億、請求から数えると0.85億で、
# どちらのSQLも正しい。差の3,866万円は未請求の受注339件だった。
# どのSQLを書くかで答えが1.5倍変わるのに、聞いた人にはそれが見えない。
#
# そこで、カタログに「一致するはずの2つの式」を検算ルールとして登録しておき、
# AIがそのテーブルに触れるSQLを実行するたびに突き合わせる。
#
#   data/<DB>.db.meta.yaml:
#     checks:
#       - name: 入金と請求（入金済）の一致
#         left:  {label: 入金の合計,          sql: SELECT SUM(amount) FROM demo_sales.payments}
#         right: {label: 請求のうち入金済み,   sql: SELECT SUM(amount) FROM demo_sales.invoices WHERE paid_flag = 1}
#         tolerance_pct: 0.1        # 許容差（%）。これ以内なら一致とみなす
#         drilldown: SELECT ...     # 不一致のとき、差の実体を見せるSQL（任意）
#         enabled: true
#
# 設計上の約束:
#   * 左右のSQLは「1行1列のスカラ」を返すこと（SUM や COUNT）。
#   * 検算は質問のたびに走るが、結果はデータの版（DBファイルのmtime）で
#     キャッシュするので、実際に実行されるのはデータが変わった後の最初の1回だけ。
#   * 壊れた検算ルール（SQLエラー）は黙って飛ばす。質問への回答を止めないため。
#     ルール自体の点検は、カタログ画面の「検算」から人が行う。
# ==========================================================================
import re
from pathlib import Path

import db

#: 許容差の既定（%）。丸め誤差を拾わない程度に小さく。
DEFAULT_TOLERANCE_PCT = 0.5
#: 不一致時に内訳SQLで見せる行数。
DRILL_ROWS = 8
#: 検算結果のキャッシュ。キーは（ルールの中身, データの版）。
_verify_cache: dict = {}
_CACHE_MAX = 300


# =============================================================================
# ルールの読み出し
# =============================================================================

def normalize(raw) -> list[dict]:
    """meta の checks をあるべき形に揃える。壊れた項目は落とす。"""
    out = []
    for c in (raw or []):
        if not isinstance(c, dict):
            continue
        left, right = c.get("left") or {}, c.get("right") or {}
        lsql = str(left.get("sql") or "").strip()
        rsql = str(right.get("sql") or "").strip()
        if not lsql or not rsql:
            continue
        try:
            tol = float(c.get("tolerance_pct", DEFAULT_TOLERANCE_PCT))
        except (TypeError, ValueError):
            tol = DEFAULT_TOLERANCE_PCT
        out.append({
            "name": str(c.get("name") or "検算").strip(),
            "left": {"label": str(left.get("label") or "左"), "sql": lsql},
            "right": {"label": str(right.get("label") or "右"), "sql": rsql},
            "tolerance_pct": max(0.0, tol),
            "drilldown": str(c.get("drilldown") or "").strip(),
            "enabled": c.get("enabled", True) is not False,
        })
    return out


def checks_for(scope: list[dict]) -> list[dict]:
    """選択中のDB群に登録されている検算ルール（有効なものだけ）。"""
    import catalog

    out = []
    for s in scope or []:
        meta = s.get("meta") or catalog.load_meta(s["path"])
        for c in normalize(meta.get("checks")):
            if c["enabled"]:
                out.append({**c, "owner": s.get("alias") or ""})
    return out


# =============================================================================
# 「このSQLはどのテーブルに触れているか」
# =============================================================================

def tables_in(sql: str, scope: list[dict]) -> set:
    """SQLが触れている (alias, table) の集合。名前の照合だけで判定する。"""
    found = set()
    for s in scope or []:
        alias = str(s.get("alias") or "")
        for t in (s.get("tables") or []):
            name = str(t)
            qualified = alias and re.search(
                r'(?<![\w."])' + re.escape(alias) + r'\s*\.\s*"?' + re.escape(name) + r'"?(?![\w])',
                sql, re.IGNORECASE)
            bare = re.search(r'(?<![\w."])"?' + re.escape(name) + r'"?(?![\w])',
                             sql, re.IGNORECASE)
            if qualified or bare:
                found.add((alias, name))
    return found


# =============================================================================
# 実行
# =============================================================================

def _scalar(sql: str, scope: list[dict]):
    """1行1列のSELECTを実行して数値を返す。数値でなければ ValueError。"""
    columns, rows, _ = db.run_select(sql, scope, max_rows=1)
    v = rows[0][0] if rows else None
    if v is None:
        return 0.0                      # SUMが空のときのNULLは0として扱う
    return float(v)


def _fingerprint(check: dict) -> tuple:
    return (check["name"], check["left"]["sql"], check["right"]["sql"],
            check["tolerance_pct"], check["drilldown"])


def _check_key(check: dict) -> str:
    """同じ名前の検算を見分ける短い識別子（起動しても変わらない）。"""
    return hashlib.md5("||".join(str(x) for x in _fingerprint(check))
                       .encode("utf-8")).hexdigest()[:8]


def _version_key(version: tuple) -> str:
    """データの版を、起動しても変わらない短い文字列にする。

    hash() は文字列に対して起動ごとに違う値を返すので、これを既読の鍵に
    使うと、再起動しただけで同じ警告がまた出る（_check_key と同じ理由で md5）。
    """
    return hashlib.md5("||".join(f"{p}:{m}" for p, m in version)
                       .encode("utf-8")).hexdigest()[:8]


def _data_version(check: dict, scope: list[dict]) -> tuple:
    """検算が読むDBファイルの版。これが変わったら計算し直す。"""
    text = " ".join([check["left"]["sql"], check["right"]["sql"], check["drilldown"]])
    stamps = []
    for s in db.narrow_scope(text, scope):
        try:
            stamps.append((str(s["path"]), Path(s["path"]).stat().st_mtime_ns))
        except OSError:
            stamps.append((str(s["path"]), 0))
    return tuple(sorted(stamps))


def run_check(check: dict, scope: list[dict], use_cache: bool = True) -> dict:
    """検算を1本実行する。

    戻り値:
      {"ok_run": bool, "match": bool, "left": float, "right": float,
       "diff": float, "pct": float|None, "version": str,
       "drill": {"columns", "rows", "truncated"} | None, "error": str|None}
    """
    version = _data_version(check, scope)
    key = (_fingerprint(check), version)
    if use_cache and key in _verify_cache:
        return _verify_cache[key]

    res: dict = {"ok_run": False, "match": True, "left": None, "right": None,
                 "diff": None, "pct": None, "drill": None, "error": None,
                 "version": _version_key(version)}
    try:
        lv = _scalar(check["left"]["sql"], scope)
        rv = _scalar(check["right"]["sql"], scope)
    except Exception as e:
        res["error"] = str(e).splitlines()[0][:200]
        _remember(key, res)
        return res

    diff = lv - rv
    base = max(abs(lv), abs(rv))
    pct = (abs(diff) / base * 100) if base else 0.0
    match = pct <= check["tolerance_pct"]
    res.update({"ok_run": True, "match": match, "left": lv, "right": rv,
                "diff": diff, "pct": round(pct, 2)})

    if not match and check["drilldown"]:
        try:
            columns, rows, truncated = db.run_select(
                check["drilldown"], scope, max_rows=DRILL_ROWS)
            res["drill"] = {"columns": columns,
                            "rows": [list(r) for r in rows],
                            "truncated": truncated}
        except Exception as e:
            res["drill"] = {"error": str(e).splitlines()[0][:160]}

    _remember(key, res)
    return res


def _remember(key, res) -> None:
    if len(_verify_cache) > _CACHE_MAX:
        _verify_cache.clear()
    _verify_cache[key] = res


def clear_cache() -> None:
    """テスト用。"""
    _verify_cache.clear()


# =============================================================================
# 質問への割り込み（ツール実行後に呼ばれる）
# =============================================================================

def alerts_for(sql_texts: list[str], scope: list[dict]) -> list[dict]:
    """実行されたSQL群に関係する検算を走らせ、不一致だけを返す。

    一致した検算・実行できなかった検算は何も言わない
    （毎回「問題ありません」と言われても読まれなくなるだけ）。
    """
    texts = [t for t in (sql_texts or []) if t and t.strip()]
    if not texts or not scope:
        return []
    try:
        checks = checks_for(scope)
    except Exception:
        return []
    if not checks:
        return []

    touched = set()
    for t in texts:
        touched |= tables_in(t, scope)
    if not touched:
        return []

    alerts = []
    for check in checks:
        involved = tables_in(check["left"]["sql"] + " " + check["right"]["sql"], scope)
        if not (involved & touched):
            continue
        res = run_check(check, scope)
        if not res["ok_run"] or res["match"]:
            continue
        alerts.append({
            # 同じ名前の検算が拠点ごとにあるので、SQLまで含めた指紋で区別する。
            # hash() はプロセスごとに変わる（再起動で同じ警告が出直す）ので使わない
            "key": f"verify||{check['owner']}||{check['name']}"
                   f"||{_check_key(check)}||{res['version']}",
            "name": check["name"],
            "left_label": check["left"]["label"], "left": res["left"],
            "right_label": check["right"]["label"], "right": res["right"],
            "diff": res["diff"], "pct": res["pct"],
            "tolerance_pct": check["tolerance_pct"],
            "drill": res["drill"],
        })
    return alerts


def _fmt(v) -> str:
    if v is None:
        return "—"
    return f"{v:,.4f}".rstrip("0").rstrip(".") if v % 1 else f"{int(v):,}"


def llm_note(alert: dict) -> dict:
    """LLMのツール結果に混ぜる、検算の注意書き。"""
    note = {
        "check": alert["name"],
        alert["left_label"]: alert["left"],
        alert["right_label"]: alert["right"],
        "difference": alert["diff"],
        "difference_pct": alert["pct"],
        "instruction": ("この2つの数字は一致するはずですが食い違っています。"
                        "回答では、どちらの数字を使ったのかと、この差異があることを"
                        "必ず注記してください。差異の理由を推測で断定しないこと。"),
    }
    drill = alert.get("drill") or {}
    if drill.get("rows"):
        note["difference_detail_sample"] = {
            "columns": drill["columns"], "rows": drill["rows"][:3]}
    return note


def render_item(alert: dict) -> dict:
    """画面に出す検算カード。分析結果と同じ report の形で描ける。"""
    tables = [{
        "name": "2つの経路の比較",
        "columns": ["経路", "値"],
        "rows": [(alert["left_label"], alert["left"]),
                 (alert["right_label"], alert["right"]),
                 ("差", alert["diff"]),
                 ("差の割合", f"{alert['pct']}%（許容 {alert['tolerance_pct']}%）")],
    }]
    notes = [f"「{alert['left_label']}」と「{alert['right_label']}」は一致するはず"
             f"ですが、{_fmt(abs(alert['diff']))}（{alert['pct']}%）食い違っています。"]
    drill = alert.get("drill") or {}
    if drill.get("rows"):
        tables.append({"name": "差の内訳（先頭のみ）",
                       "columns": drill["columns"], "rows": drill["rows"]})
        notes.append("内訳の表は差の実体の一部です。全体はデータカタログの"
                     "「検算」で確認できます。")
    elif drill.get("error"):
        notes.append(f"内訳SQLは実行できませんでした: {drill['error']}")
    notes.append("この検算ルールはデータカタログの「用語集・例文 → 検算」で"
                 "管理されています。差が正しい業務状態なら、許容差を広げるか"
                 "ルールを無効にしてください。")
    return {"role": "assistant", "kind": "report",
            "title": f"⚠ 検算: {alert['name']}",
            "tables": tables, "notes": notes,
            "verify_key": alert["key"]}


# ==========================================================================
# ===== 元 sqlusage.py
# 過去の分析で「実際に使われた」結合を数える。
#
# ER図が描いているのは宣言された関連で、実際に通った道ではない。
# チャット履歴には実行されたSQLが全部残っているので、そこからJOINを取り出して
# 数えると、次の3つが見えるようになる。
#
#   よく通る道       … 太く描く。分析の主要動線
#   誰も通らない道   … 灰色にする。検算されていない経路でもある
#                      （実際、demo_sales で3,866万円の未請求が見つかったのは
#                        一度も使われていなかった invoices への経路の上だった）
#   登録の無い道     … AIが実際に結合しているのにカタログに無い。
#                      「関連の候補」に実績つきで出す。登録すべきか、
#                      AIが誤った結合をしているかのどちらかで、どちらでも知る価値がある
#
# 解析は正規表現＋カタログのプロファイル（テーブル・列の一覧）で行う。
# SQLパーサは入れない。ここでの用途は「多い・少ない・ゼロ」が分かればよく、
# 多少の取りこぼしで結論が変わらないため。
# ==========================================================================
import json
import re
from pathlib import Path

import catalog
import config
import db

#: エイリアスとして解釈してはいけない語。
_sqlusage_RESERVED = {"on", "using", "where", "group", "order", "left", "right", "inner",
             "outer", "cross", "natural", "join", "as", "select", "from", "limit",
             "having", "union", "all", "and", "or", "not", "set", "by"}

_FROM_RE = re.compile(
    r'\b(?:from|join)\s+("?[\w一-龠ぁ-んァ-ヶ．.]+"?)(?:\s+(?:as\s+)?([A-Za-z_]\w*))?',
    re.IGNORECASE)
_USING_RE = re.compile(
    r'\bjoin\s+("?[\w一-龠ぁ-んァ-ヶ．.]+"?)(?:\s+(?:as\s+)?([A-Za-z_]\w*))?'
    r'\s+using\s*\(\s*"?(\w+)"?\s*\)', re.IGNORECASE)
_ON_RE = re.compile(
    r'\bon\s+("?[\w一-龠ぁ-んァ-ヶ．.]+"?)\s*=\s*("?[\w一-龠ぁ-んァ-ヶ．.]+"?)',
    re.IGNORECASE)


# =============================================================================
# 履歴からSQLを集める
# =============================================================================

def _walk_sql(node, acc: list) -> None:
    if isinstance(node, dict):
        for k, v in node.items():
            if k == "sql" and isinstance(v, str) and v.strip():
                acc.append(v)
            else:
                _walk_sql(v, acc)
    elif isinstance(node, list):
        for v in node:
            _walk_sql(v, acc)


def collect_sqls() -> tuple:
    """全ユーザーのチャット履歴から実行SQLを集める。

    同じSQLが画面用の写しとツール呼び出しの両方に残っているので、
    会話単位で重複を除く。戻り値: (SQLのリスト, 会話数)
    """
    sqls: list[str] = []
    users = Path(config.USER_META_DIR)
    chats = 0
    if not users.exists():
        return sqls, 0
    for f in users.glob("*/chats/*.json"):
        if f.name == "index.json":
            continue
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        chats += 1
        seen: set = set()
        for item in data.get("render_log") or []:
            if item.get("kind") == "sql" and item.get("sql"):
                seen.add(str(item["sql"]).strip())
        buf: list = []
        for m in data.get("messages") or []:
            for tc in (m.get("tool_calls") or []):
                try:
                    args = json.loads((tc.get("function") or {}).get("arguments") or "{}")
                except Exception:
                    continue
                _walk_sql(args, buf)
        seen |= {s.strip() for s in buf}
        sqls.extend(seen)
    return sqls, chats


# =============================================================================
# JOIN の解決
# =============================================================================

def _entries() -> list[dict]:
    """全DBのプロファイル（テーブル・列）。名前解決の台帳になる。"""
    out = []
    for p in db.list_db_files():
        try:
            out.append({"alias": db.alias_for(p), "path": p,
                        "profile": catalog.profile_db(p)})
        except Exception:
            continue
    return out


def _resolve_table(raw: str, entries: list[dict], hint_aliases: set):
    """'demo_sales.orders' や 'orders' を (DBエイリアス, テーブル) にする。"""
    name = raw.strip().strip('"')
    if "." in name:
        prefix, _, rest = name.partition(".")
        rest = rest.strip('"')
        for e in entries:
            if e["alias"].lower() == prefix.lower() and rest in e["profile"]["tables"]:
                return (e["alias"], rest)
        return None
    hits = [e["alias"] for e in entries if name in e["profile"]["tables"]]
    if len(hits) == 1:
        return (hits[0], name)
    if hits:
        # 同名テーブルが複数DBにある。同じSQLに出てきたDBを優先する
        for a in hits:
            if a in hint_aliases:
                return (a, name)
    return None


def _columns_of(entries: list[dict], alias: str, table: str) -> set:
    for e in entries:
        if e["alias"] == alias:
            t = e["profile"]["tables"].get(table) or {}
            return {c["name"] for c in t.get("columns", [])}
    return set()


def _edge_key(a: tuple, b: tuple) -> str:
    x, y = ".".join(a), ".".join(b)
    return f"{x}||{y}" if x <= y else f"{y}||{x}"


def joins_in(sql: str, entries: list[dict]) -> list[tuple]:
    """1本のSQLから、(端点, 端点) のリストを取り出す。端点 = (alias, table, column)。"""
    flat = " ".join(sql.split())

    # 出現順のテーブルと、エイリアス→テーブルの対応
    order: list[tuple] = []
    alias_map: dict = {}
    hint = {e["alias"] for e in entries
            if re.search(r'(?<![\w."])' + re.escape(e["alias"]) + r'\s*\.',
                         flat, re.IGNORECASE)}
    for m in _FROM_RE.finditer(flat):
        raw, al = m.group(1), (m.group(2) or "")
        resolved = _resolve_table(raw, entries, hint)
        if resolved is None:
            continue
        order.append(resolved)
        alias_map[resolved[1].lower()] = resolved          # テーブル名でも引ける
        if al and al.lower() not in _sqlusage_RESERVED:
            alias_map[al.lower()] = resolved

    out: list[tuple] = []

    # JOIN ... USING(col): 相手は「それより前に出た、同じ列を持つテーブル」
    for m in _USING_RE.finditer(flat):
        raw, col = m.group(1), m.group(3)
        right = _resolve_table(raw, entries, hint)
        if right is None:
            continue
        try:
            pos = order.index(right)
        except ValueError:
            continue
        left = next((t for t in reversed(order[:pos])
                     if col in _columns_of(entries, *t)), None)
        if left and col in _columns_of(entries, *right):
            out.append(((*left, col), (*right, col)))

    # JOIN ... ON a.x = b.y
    for m in _ON_RE.finditer(flat):
        ends = []
        for side in (m.group(1), m.group(2)):
            side = side.strip().strip('"')
            if "." not in side:
                break
            qual, _, col = side.rpartition(".")
            qual = qual.strip('"')
            t = None
            if "." in qual:                       # demo_sales.orders.customer_id
                t = _resolve_table(qual, entries, hint)
            else:                                 # o.customer_id / orders.customer_id
                t = alias_map.get(qual.lower())
            if t is None or col not in _columns_of(entries, *t):
                break
            ends.append((*t, col))
        if len(ends) == 2 and ends[0][:2] != ends[1][:2]:
            out.append((ends[0], ends[1]))
    return out


# =============================================================================
# 集計とAPI
# =============================================================================

def usage_counts() -> dict:
    """全履歴のJOINを数える。{edge_key: {"from","to","count"}}"""
    entries = _entries()
    sqls, chats = collect_sqls()
    edges: dict = {}
    tables: dict = {}
    for sql in sqls:
        for a, b in joins_in(sql, entries):
            key = _edge_key(a, b)
            hit = edges.setdefault(key, {"from": list(a), "to": list(b), "count": 0})
            hit["count"] += 1
        low = sql.lower()
        for e in entries:
            for t in e["profile"]["tables"]:
                if re.search(r'(?<![\w."])' + re.escape(t.lower()) + r'(?![\w])', low):
                    tables[f"{e['alias']}.{t}"] = tables.get(f"{e['alias']}.{t}", 0) + 1
    return {"edges": edges, "tables": tables,
            "scanned": {"chats": chats, "sqls": len(sqls)}}


def _declared_pairs(entries: list[dict]) -> set:
    """カタログ/FKに登録済みの結合（端点の組）。"""
    cat_entries = [{"alias": e["alias"], "profile": e["profile"],
                    "meta": catalog.load_meta(e["path"])} for e in entries]
    out = set()
    for edge in catalog.collect_edges(cat_entries):
        fa, ftb, _ = edge["from"]
        ta, ttb, _ = edge["to"]
        for fc, tc in (edge.get("pairs") or [[edge["from"][2], edge["to"][2]]]):
            out.add(_edge_key((fa, ftb, fc), (ta, ttb, tc)))
    return out


def usage_for(alias: str) -> dict:
    """ER図に重ねるためのデータ（このDBのキャンバス向け）。"""
    data = usage_counts()
    return {
        "edges": {k: v["count"] for k, v in data["edges"].items()},
        "tables": {k: n for k, n in data["tables"].items()
                   if k.startswith(alias + ".")},
        "scanned": data["scanned"],
    }


def suggestions_for(alias: str, profile: dict, meta: dict) -> list[dict]:
    """実際に使われているのにカタログに無い結合を「関連の候補」に出す。

    形は catalog.join_suggestions と同じ。from 側は必ずこのDBのテーブルにする
    （関連はそのDBの .meta.yaml に書かれるため）。
    """
    entries = _entries()
    if not entries:
        return []
    declared = _declared_pairs(entries)
    data = usage_counts()

    out = []
    for key, e in sorted(data["edges"].items(), key=lambda kv: -kv[1]["count"]):
        if key in declared:
            continue
        a, b = tuple(e["from"]), tuple(e["to"])
        # from 側をこのDBに揃える。どちらもこのDBでなければ、この画面では出さない
        if a[0] != alias and b[0] != alias:
            continue
        if a[0] != alias:
            a, b = b, a
        frm = f"{a[1]}.{a[2]}"
        to = f"{b[1]}.{b[2]}" if b[0] == alias else f"{b[0]}.{b[1]}.{b[2]}"
        out.append({"from": frm, "to": to, "cardinality": "N:1",
                    "reason": f"過去の分析で{e['count']}回使われています（未登録）"})
    return out[:8]


# ==========================================================================
# ===== 元 importer.py
# Excel / CSV を SQLite に取り込む層。
#
# このアプリで **唯一 DB に書き込む場所**。分析側（db.py）は読み取り専用のまま保つ。
# 書き込みをここに閉じ込めることで、「チャットからDBが書き換わることはない」という
# 保証を壊さずに、DB・テーブルの新規作成を提供する。
#
# 安全のための制約:
#   - 読むファイルは config.IMPORT_DIRS の中にあるものだけ（画面からパスは打たせない）
#   - シンボリックリンクや .. で許可フォルダの外に出ようとしたら拒否
#   - 拡張子・ファイルサイズ・行数の上限あり
#   - 作る .db は config.DATA_DIR の直下のみ。名前も英数字系に正規化する
# ==========================================================================
import re
import sqlite3
import unicodedata
from datetime import datetime
from pathlib import Path

import pandas as pd
import yaml

import config

# SQLiteの予約語のうち、テーブル名・列名に使われがちなもの
_RESERVED = {
    "abort", "action", "add", "all", "alter", "and", "as", "asc", "between", "by", "case",
    "check", "column", "commit", "create", "cross", "default", "delete", "desc", "distinct",
    "drop", "else", "end", "escape", "except", "exists", "for", "from", "full", "group",
    "having", "in", "index", "inner", "insert", "into", "is", "join", "key", "left", "like",
    "limit", "not", "null", "offset", "on", "or", "order", "outer", "primary", "references",
    "right", "select", "set", "table", "then", "to", "transaction", "union", "unique",
    "update", "using", "values", "view", "when", "where", "with",
}


class ImportError_(Exception):
    """取り込みに失敗したときに投げる（画面にそのまま出せる日本語メッセージ）。"""


# =============================================================================
# 取り込み元ファイルの列挙（許可フォルダの中だけ）
# =============================================================================

def _read_extra() -> list[str]:
    p = config.IMPORT_DIRS_FILE
    if not p.exists():
        return []
    try:
        data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    except Exception as e:
        print(f"[importer] 追加フォルダの設定を読めませんでした: {p} ({e})")
        return []
    items = data.get("dirs") if isinstance(data, dict) else data
    return [str(x) for x in (items or []) if str(x).strip()]


def extra_dirs() -> list[Path]:
    """画面から追加されたフォルダ。"""
    return [Path(s).expanduser() for s in _read_extra()]


def configured_dirs() -> list[dict]:
    """許可フォルダの一覧（どこで設定されたかつき）。"""
    out = [{"path": d, "source": "env", "removable": False} for d in config.IMPORT_DIRS]
    for d in extra_dirs():
        out.append({"path": d, "source": "ui", "removable": True})
    return out


def add_dir(raw: str) -> Path:
    """画面からフォルダを追加する。存在と読み取り可否をその場で確かめる。"""
    if not config.IMPORT_DIRS_EDITABLE:
        raise ImportError_("画面からのフォルダ追加は無効化されています（IMPORT_DIRS_EDITABLE）。")
    text = (raw or "").strip().strip('"')
    if not text:
        raise ImportError_("フォルダのパスを入力してください。")
    p = Path(text).expanduser()
    try:
        real = p.resolve(strict=True)
    except OSError:
        raise ImportError_(f"見つかりません: {text}（マウントされているか確認してください）") from None
    if not real.is_dir():
        raise ImportError_(f"フォルダではありません: {real}")
    # ルート直下を丸ごと許可すると、走査が終わらないうえ事故のもとになる
    if real.parent == real:
        raise ImportError_("ドライブ/ファイルシステムのルートは指定できません。"
                           "取り込み用のフォルダを切って指定してください。")
    try:
        next(real.iterdir(), None)
    except PermissionError:
        raise ImportError_(f"読み取り権限がありません: {real}") from None
    except OSError as e:
        raise ImportError_(f"アクセスできません: {real}（{e.strerror or e}）") from None

    current = _read_extra()
    if any(Path(s).expanduser().resolve() == real for s in current
           if Path(s).expanduser().exists()):
        raise ImportError_("そのフォルダは既に登録されています。")
    if any(d.resolve() == real for d in config.IMPORT_DIRS if d.exists()):
        raise ImportError_("env の IMPORT_DIRS に既に入っています。")

    current.append(str(real))
    _write_extra(current)
    return real


def remove_dir(raw: str) -> bool:
    if not config.IMPORT_DIRS_EDITABLE:
        raise ImportError_("画面からのフォルダ変更は無効化されています。")
    current = _read_extra()
    left = [s for s in current if s != raw]
    if len(left) == len(current):
        return False
    _write_extra(left)
    return True


def _write_extra(items: list[str]) -> None:
    p = config.IMPORT_DIRS_FILE
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(yaml.safe_dump({"dirs": items}, allow_unicode=True, sort_keys=False),
                 encoding="utf-8")


def allowed_dirs() -> list[Path]:
    """実際に読み込みを許可するフォルダ（env + 画面から追加した分）。"""
    out, seen = [], set()
    for d in list(config.IMPORT_DIRS) + extra_dirs():
        try:
            real = d.resolve()
        except OSError:
            continue
        if real not in seen:
            seen.add(real)
            out.append(real)
    return out


def dir_status() -> list[dict]:
    """許可フォルダごとの状態。

    本番ではネットワークマウント（/mnt/... など）を指すため、
    「ファイルが無い」のか「マウントされていない・権限がない」のかを
    画面で切り分けられるようにする。
    """
    rows = []
    for entry in configured_dirs():
        d = entry["path"]
        info = {"設定値": str(d), "実際のパス": "", "状態": "", "ok": False,
                "source": entry["source"], "removable": entry["removable"]}
        try:
            real = d.resolve()
            info["実際のパス"] = str(real)
            if not real.exists():
                info["状態"] = "見つかりません（マウントされていない可能性があります）"
            elif not real.is_dir():
                info["状態"] = "フォルダではありません"
            else:
                next(real.iterdir(), None)      # 読めるかどうかを実際に試す
                info["状態"] = "利用できます"
                info["ok"] = True
        except PermissionError:
            info["状態"] = "読み取り権限がありません"
        except OSError as e:
            info["状態"] = f"アクセスできません（{e.strerror or e}）"
        rows.append(info)
    return rows


def _importer_walk(root: Path, depth: int = 0, only_supported: bool = True):
    """root 以下を走査する。depth=0 なら階層の制限なし。

    権限の無いフォルダは黙って飛ばす（共有フォルダには必ずあるため、
    そこで止まると他のファイルまで見えなくなる）。

    only_supported=False にすると拡張子で絞らない。「何が置いてあるか」を
    調べる用で、読み込みの可否は別に判断する。
    """
    stack = [(root, 0)]
    seen_dirs: set = set()
    while stack:
        cur, level = stack.pop()
        try:
            real = cur.resolve()
            if real in seen_dirs:        # リンクの輪でぐるぐる回らないように
                continue
            seen_dirs.add(real)
            entries = list(cur.iterdir())
        except OSError:
            continue
        for p in entries:
            try:
                if p.is_dir():
                    if not depth or level < depth:
                        stack.append((p, level + 1))
                elif is_noise(p.name):
                    continue
                elif not only_supported or p.suffix.lower() in config.IMPORT_EXTENSIONS:
                    yield p
            except OSError:
                continue


def is_noise(name: str) -> bool:
    """Windows共有フォルダに必ず混ざる、開いても意味の無いファイル。

    ~$売上.xlsx … Excelで開いている間だけできるロックファイル（開くと壊れて見える）
    .DS_Store / desktop.ini / Thumbs.db … OSが勝手に作るもの
    """
    low = name.lower()
    return (name.startswith("~$") or name.startswith(".")
            or low in ("desktop.ini", "thumbs.db"))


def is_allowed(path: Path) -> bool:
    """許可フォルダの中にある実ファイルかどうか（.. やリンク経由の脱出を防ぐ）。"""
    try:
        real = path.resolve(strict=True)
    except (OSError, RuntimeError):
        return False
    if not real.is_file() or is_noise(real.name):
        return False
    # 拡張子は大小を無視する（Windows側では .CSV と .csv が混在しうる）
    if real.suffix.lower() not in config.IMPORT_EXTENSIONS:
        return False
    return any(real == d or d in real.parents for d in allowed_dirs())


def is_within_allowed(path: Path) -> bool:
    """許可フォルダの中にある実ファイルか（拡張子は問わない）。

    is_allowed() は「取り込めるファイルか」まで見るので拡張子で弾く。
    こちらは置き場所だけを見る。何が置いてあるかを一覧するためのもので、
    「読んでよいか」は呼び出し側が別に判断すること。
    """
    try:
        real = path.resolve(strict=True)
    except (OSError, RuntimeError):
        return False
    if not real.is_file() or is_noise(real.name):
        return False
    return any(real == d or d in real.parents for d in allowed_dirs())


def list_all_files(depth: int | None = None, limit: int | None = None) -> list[Path]:
    """許可フォルダ配下のファイル（拡張子を問わない）。調査用。

    depth を渡さなければ config.IMPORT_SCAN_DEPTH（既定 0 = 無制限）に従う。
    0 は「無制限」という意味のある値なので、未指定は None で区別する。
    """
    depth = config.IMPORT_SCAN_DEPTH if depth is None else depth
    cap = limit or config.IMPORT_MAX_FILES
    seen: set = set()
    found: list[Path] = []
    for d in allowed_dirs():
        try:
            if not d.is_dir():
                continue
        except OSError:
            continue
        for p in _importer_walk(d, depth, only_supported=False):
            try:
                real = p.resolve()
            except OSError:
                continue
            if real in seen:
                continue
            seen.add(real)
            found.append(real)
            if len(found) >= cap:
                return sorted(found)
    return sorted(found)


def display_name(path: Path) -> str:
    """画面に出す相対パス（許可フォルダからの位置）。"""
    for d in allowed_dirs():
        try:
            return str(path.relative_to(d))
        except ValueError:
            continue
    return path.name


def is_allowed_dir(path: Path) -> bool:
    """許可フォルダ自身か、その配下のフォルダか。"""
    try:
        real = path.resolve(strict=True)
    except (OSError, RuntimeError):
        return False
    if not real.is_dir():
        return False
    return any(real == d or d in real.parents for d in allowed_dirs())


def browse(path: str | None = None) -> dict:
    """フォルダの中身を1階層ぶん返す（エクスプローラ風の画面用）。

    path を省略すると許可フォルダの一覧を返す。
    許可フォルダの外は、パスを直接渡されても開かない。
    """
    roots = allowed_dirs()
    if not path:
        return {
            "path": "", "label": "取り込み元フォルダ", "parent": None,
            "dirs": [{"path": str(d), "name": str(d)} for d in roots if d.is_dir()],
            "files": [], "crumbs": [],
        }

    here = Path(path)
    if not is_allowed_dir(here):
        raise ImportError_("そのフォルダは開けません（許可されたフォルダの外です）。")
    here = here.resolve()

    dirs, files = [], []
    try:
        for p in sorted(here.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower())):
            try:
                if p.is_dir():
                    if not is_noise(p.name):
                        dirs.append({"path": str(p), "name": p.name})
                elif p.suffix.lower() in config.IMPORT_EXTENSIONS and not is_noise(p.name):
                    files.append({"path": str(p), "name": p.name,
                                  "size": p.stat().st_size,
                                  "mtime": datetime.fromtimestamp(
                                      p.stat().st_mtime).strftime("%Y-%m-%d %H:%M")})
            except OSError:
                continue
    except PermissionError:
        raise ImportError_(f"読み取り権限がありません: {here}") from None
    except OSError as e:
        raise ImportError_(f"開けませんでした: {here}（{e.strerror or e}）") from None

    # パンくず。許可フォルダより上には遡らせない
    root = next((d for d in roots if here == d or d in here.parents), None)
    crumbs, cur = [], here
    while root is not None and cur != root:
        crumbs.append({"path": str(cur), "name": cur.name})
        cur = cur.parent
    crumbs.append({"path": str(root), "name": str(root)})
    crumbs.reverse()
    parent = str(here.parent) if (root is not None and here != root) else ""
    return {"path": str(here), "label": here.name or str(here), "parent": parent,
            "dirs": dirs, "files": files, "crumbs": crumbs}


def check_readable(path: Path) -> None:
    if not is_allowed(path):
        raise ImportError_("許可されたフォルダの中のファイルではありません。")
    mb = path.stat().st_size / (1024 * 1024)
    if mb > config.IMPORT_MAX_FILE_MB:
        raise ImportError_(
            f"ファイルが大きすぎます（{mb:.1f}MB / 上限 {config.IMPORT_MAX_FILE_MB}MB）。")


# =============================================================================
# 読み込み
# =============================================================================

def sheet_names(path: Path) -> list[str]:
    """Excelのシート名。CSVなら空リスト。"""
    if path.suffix.lower() not in (".xlsx", ".xlsm"):
        return []
    check_readable(path)
    return _sheet_names_of(path)


def _sheet_names_of(src) -> list[str]:
    try:
        import openpyxl
        wb = openpyxl.load_workbook(src, read_only=True, data_only=True)
        try:
            return list(wb.sheetnames)
        finally:
            wb.close()
    except Exception as e:
        raise ImportError_(f"Excelを開けませんでした: {e}") from e


# CSVの文字コード。上から順に試す。
CSV_ENCODINGS = ["utf-8-sig", "cp932", "utf-8", "shift_jis", "euc_jp"]


# --- アップロードされたファイル（サーバのフォルダには置かない） --------------------

def check_upload(data: bytes, filename: str) -> str:
    """アップロードの受け入れ判定。戻り値は正規化した拡張子。"""
    if not config.IMPORT_ALLOW_UPLOAD:
        raise ImportError_("アップロードからの取り込みは無効化されています（IMPORT_ALLOW_UPLOAD）。")
    ext = Path(filename or "").suffix.lower()
    if ext not in config.IMPORT_EXTENSIONS:
        raise ImportError_(
            f"扱えない形式です（{ext or '拡張子なし'}）。{'、'.join(config.IMPORT_EXTENSIONS)} のみ対応です。")
    mb = len(data) / (1024 * 1024)
    if mb > config.IMPORT_MAX_FILE_MB:
        raise ImportError_(
            f"ファイルが大きすぎます（{mb:.1f}MB / 上限 {config.IMPORT_MAX_FILE_MB}MB）。")
    return ext


def upload_sheet_names(data: bytes, filename: str) -> list[str]:
    if check_upload(data, filename) not in (".xlsx", ".xlsm"):
        return []
    import io
    return _sheet_names_of(io.BytesIO(data))


def read_upload(data: bytes, filename: str, sheet: str | None = None, header_row: int = 0,
                delimiter: str | None = None, nrows: int | None = None) -> pd.DataFrame:
    """アップロードされたバイト列を DataFrame として読む。ディスクには書かない。"""
    import io
    ext = check_upload(data, filename)
    try:
        if ext in (".xlsx", ".xlsm"):
            return pd.read_excel(io.BytesIO(data), sheet_name=sheet or 0,
                                 header=header_row, nrows=nrows, dtype=object)
        sep = delimiter if delimiter else ("\t" if ext == ".tsv" else None)
        last = None
        for enc in CSV_ENCODINGS:
            try:
                return pd.read_csv(io.BytesIO(data), header=header_row, nrows=nrows,
                                   dtype=object, sep=sep, engine="python", encoding=enc)
            except UnicodeDecodeError as e:
                last = e
        raise ImportError_(
            "文字コードを判定できませんでした。UTF-8 か Shift_JIS で保存し直してください。"
            f"（{last}）")
    except ImportError_:
        raise
    except Exception as e:
        raise ImportError_(f"ファイルを読めませんでした: {e}") from e


# 画面に出す区切り文字の選択肢（.txt は区切りがまちまちなので選べるようにする）
DELIMITERS = {
    "自動判定": None,
    "カンマ ( , )": ",",
    "タブ": "\t",
    "パイプ ( | )": "|",
    "セミコロン ( ; )": ";",
    "空白（連続もまとめる）": r"\s+",
}


def _explain_read_error(e: Exception, path: Path, sheet: str | None) -> str:
    """pandas / OS の例外を、管理者がそのまま対処できる日本語にする。

    定期取り込みの失敗はメール・⚠マーク・AIの注記にこの文がそのまま載るので、
    'No columns to parse from file' のような英語のままでは何をすればよいか分からない。
    """
    name = path.name
    if isinstance(e, PermissionError):
        return (f"{name} を開けません。他のプログラム（Excel など）で開かれているか、"
                "読み取り権限がありません。閉じてから、次回の実行を待つか「今すぐ更新」してください。")
    if isinstance(e, FileNotFoundError):
        return f"{name} が見つかりません（移動・削除された可能性）。"
    msg = str(e)
    if "No columns to parse" in msg or isinstance(e, pd.errors.EmptyDataError):
        return f"{name} の中身が空です（0バイト、または見出し行がありません）。"
    if "Worksheet named" in msg or "Worksheet index" in msg:
        try:
            names = _sheet_names_of(path)
            have = "、".join(names) if names else "（なし）"
        except Exception:
            have = "（不明）"
        return (f"シート「{sheet}」が {name} にありません（シート名が変わった可能性）。"
                f"いまあるシート: {have}。設定のシートを直してください。")
    if "BadZipFile" in type(e).__name__ or "not a zip file" in msg.lower() or "File is not a zip file" in msg:
        return (f"{name} を Excel ファイルとして開けません（壊れているか、拡張子だけ .xlsx の別形式）。"
                "Excel で開いて保存し直してください。")
    if isinstance(e, pd.errors.ParserError):
        return f"{name} を表として読めませんでした（行ごとの列数が揃っていない等）: {msg}"
    return f"{name} を読めませんでした: {msg}"


def read_table(path: Path, sheet: str | None = None, header_row: int = 0,
               encoding: str | None = None, nrows: int | None = None,
               delimiter: str | None = None) -> pd.DataFrame:
    """ファイルを DataFrame として読む。

    header_row は0始まり。見出しが2行目にあるなら 1 を渡す。
    delimiter は CSV/TSV/TXT 用。None なら .tsv はタブ、それ以外は自動判定。
    """
    check_readable(path)
    ext = path.suffix.lower()
    try:
        if ext in (".xlsx", ".xlsm"):
            df = pd.read_excel(path, sheet_name=sheet or 0, header=header_row,
                               nrows=nrows, dtype=object)
        else:
            if path.stat().st_size == 0:
                raise ImportError_(f"{path.name} の中身が空です（0バイト）。")
            sep = delimiter if delimiter else ("\t" if ext == ".tsv" else None)
            last = None
            for enc in ([encoding] if encoding else CSV_ENCODINGS):
                try:
                    df = pd.read_csv(path, header=header_row, nrows=nrows, dtype=object,
                                     sep=sep, engine="python", encoding=enc)
                    break
                except UnicodeDecodeError as e:
                    last = e
            else:
                raise ImportError_(
                    f"{path.name} の文字コードを判定できませんでした。テキスト（CSV）ではないか、"
                    "壊れている可能性があります。UTF-8 か Shift_JIS で保存し直してください。"
                    f"（{last}）")
    except ImportError_:
        raise
    except Exception as e:
        raise ImportError_(_explain_read_error(e, path, sheet)) from e

    if df.empty and not len(df.columns):
        raise ImportError_(f"{path.name} の中身が空のようです（見出し行の指定を確認してください）。")
    return df


# =============================================================================
# 名前と型の正規化
# =============================================================================

def safe_name(name: str, fallback: str = "col", *, table: bool = False) -> str:
    """SQLiteで扱いやすい識別子にする（日本語はそのまま残す）。

    記号と空白を _ にし、数字始まり・予約語・空文字を避ける。

    table=True のときは「まとまり__表名」の __ を残す。このアプリは表名の
    接頭辞（__ の手前）でまとまりを作るので、ここで _ に潰してしまうと
    取り込み画面からはまとまりに入る表を1つも作れなくなる。
    """
    s = unicodedata.normalize("NFKC", str(name)).strip()
    s = re.sub(r"[^\w]", "_", s, flags=re.UNICODE)   # \w は日本語も含む
    s = re.sub(r"_{2,}", "__", s) if table else re.sub(r"_+", "_", s)
    s = s.strip("_")
    if not s:
        return fallback
    if s[0].isdigit():
        s = "_" + s
    if s.lower() in _RESERVED:
        s = s + "_"
    return s[:64]


def unique_names(names: list[str]) -> list[str]:
    """列名の重複を _2, _3 … で解消する。"""
    out, used = [], {}
    for i, n in enumerate(names):
        base = safe_name(n, fallback=f"col{i + 1}")
        if base in used:
            used[base] += 1
            base = f"{base}_{used[base]}"
        else:
            used[base] = 1
        out.append(base)
    return out


def _looks_like_code(values: pd.Series) -> bool:
    """数値に見えるが、実際は「コード」なので文字列で持つべきか。

    郵便番号 0123、電話番号 08012345678、製品コード 007 のような列は
    全部が数字なので数値と判定できてしまう。しかし INTEGER にすると
    先頭のゼロが落ち（'0123' → 123）、桁数も同一性も永久に失われる。
    元の文字列に戻せない値が1つでもあれば、その列はコードとみなす。
    """
    for v in values:
        text = str(v).strip()
        if not text:
            continue
        # 先頭ゼロ（"0" 単独は除く）。これだけで数値化は不可逆になる
        if len(text) > 1 and text[0] == "0" and text[1] not in ".,":
            return True
        # 往復して元に戻らないもの（前後の + や桁区切り、全角数字など）
        try:
            if str(int(text)) != text:
                return True
        except (TypeError, ValueError):
            return True
    return False


def infer_type(series: pd.Series) -> str:
    """列の中身から SQLite の型を決める（判断できなければ TEXT）。"""
    s = series.dropna()
    s = s[s.astype(str).str.strip() != ""]
    if s.empty:
        return "TEXT"
    num = pd.to_numeric(s, errors="coerce")
    if num.notna().all():
        # 小数点を含まず整数で表せるなら INTEGER
        if (num == num.round()).all() and num.abs().max() < 2 ** 63:
            # ただし「数字だけのコード」は TEXT のまま持つ（先頭ゼロを守る）
            return "TEXT" if _looks_like_code(s) else "INTEGER"
        return "REAL"
    return "TEXT"


def plan_columns(df: pd.DataFrame) -> list[dict]:
    """列ごとの「元の名前 / 使う名前 / 型」の一覧を作る。"""
    names = unique_names([str(c) for c in df.columns])
    return [{"元の列名": str(orig), "列名": name, "型": infer_type(df[orig])}
            for orig, name in zip(df.columns, names)]


def _cast(series: pd.Series, sqlite_type: str):
    """SQLiteに渡せる素のPython値（int / float / str / None）に揃える。

    numpy の int64 などをそのまま渡すと、sqlite3 がバッファとみなして
    BLOB で保存してしまう（数値として比較も集計もできなくなる）。
    """
    if sqlite_type == "INTEGER":
        num = pd.to_numeric(series, errors="coerce")
        return num.map(lambda v: None if pd.isna(v) else int(v))
    if sqlite_type == "REAL":
        num = pd.to_numeric(series, errors="coerce")
        return num.map(lambda v: None if pd.isna(v) else float(v))
    return series.map(lambda v: None if v is None or pd.isna(v) else str(v))


def _column_of(df: pd.DataFrame, name):
    """元ファイルの列を取り出す。見出しが数値や日付のセルでも引けるようにする。

    下見（plan_columns）は見出しを文字にして画面へ返すが、本番の読み込みでは
    pandas の列名が数値の 2024 のままなので、"2024" では見つからず
    KeyError で 500 になっていた（メッセージも「取り込みに失敗しました: '2024'」）。
    """
    if name in df.columns:
        return df[name]
    key = str(name)
    for col in df.columns:
        if str(col) == key:
            return df[col]
    raise ImportError_(
        f"元のファイルに列 '{name}' がありません。"
        "区切り文字・見出し行・シートの指定が変わっていないか確認してください。"
        f"（いまの見出し: {'、'.join(str(c) for c in list(df.columns)[:10])}）")


def prepare_frame(df: pd.DataFrame, columns: list[dict]):
    """型を当てはめた DataFrame と、型を変えた列の説明の一覧を返す。

    型は先頭数千行から推定するので、後ろの行に想定と違う値が混ざることがある。
    そのまま当てはめると値が黙って変わるので、ここで型の方を広げて必ず知らせる。

      ・数値にできない値がある      → TEXT にする（数値にすると NULL で消える）
      ・整数のはずが小数が混ざる    → REAL にする（int() は 2.7 を 2 に切り捨てる）
    """
    out, degraded = {}, []
    for c in columns:
        src = _column_of(df, c["元の列名"])
        if c["型"] in ("INTEGER", "REAL"):
            num = pd.to_numeric(src, errors="coerce")
            filled = src.notna() & (src.astype(str).str.strip() != "")
            if bool((filled & num.isna()).any()):
                c["型"] = "TEXT"
                degraded.append(f'{c["列名"]}: 文字として保存（数値にできない値があった）')
            elif c["型"] == "INTEGER":
                # 小数を整数の列に入れると int() が切り捨てる。
                # 集計だけがずれて、元ファイルと突き合わせるまで気づけない
                frac = num.notna() & (num != num.round())
                if bool(frac.any()):
                    c["型"] = "REAL"
                    degraded.append(
                        f'{c["列名"]}: 小数として保存（整数の指定だったが小数が {int(frac.sum())} 件あった）')
        out[c["列名"]] = _cast(src, c["型"])
    return pd.DataFrame(out), degraded


# =============================================================================
# 書き込み（このアプリで唯一DBに書く場所）
# =============================================================================

def _importer_qi(name: str) -> str:
    return '"' + str(name).replace('"', '""') + '"'


def existing_tables(db_path: Path) -> list[str]:
    if not db_path.exists():
        return []
    conn = sqlite3.connect(f"file:{db_path.as_posix()}?mode=ro", uri=True)
    try:
        rows = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' "
            "AND name NOT LIKE 'sqlite_%' ORDER BY name").fetchall()
        return [r[0] for r in rows]
    finally:
        conn.close()


def table_columns(db_path: Path, table: str) -> list[str]:
    if not db_path.exists():
        return []
    conn = sqlite3.connect(f"file:{db_path.as_posix()}?mode=ro", uri=True)
    try:
        return [r[1] for r in conn.execute(f"PRAGMA table_info({_importer_qi(table)})")]
    except sqlite3.Error:
        return []
    finally:
        conn.close()


def import_dataframe(db_path: Path, table: str, df: pd.DataFrame, columns: list[dict],
                     mode: str = "create", timestamp_col: str | None = None,
                     timestamp_value: str | None = None):
    """DataFrame を1テーブルとして書き込む。

    mode: create=新規作成 / replace=作り直す / append=既存に追記
    timestamp_col: 指定すると、その名前の列に取り込み日時を入れて一緒に書く。
                   追記を重ねたとき「いつ取り込んだ分か」を後から絞れるようにするため。
    戻り値: (書き込んだ行数, 型をTEXTに落とした列名の一覧)
    """
    if db_path.parent.resolve() != config.DATA_DIR.resolve():
        raise ImportError_("DBファイルは data/ の直下にしか作れません。")
    table = safe_name(table, fallback="", table=True)
    if not table:
        raise ImportError_("テーブル名を入力してください。")
    if len(df) > config.IMPORT_MAX_ROWS:
        raise ImportError_(
            f"行数が多すぎます（{len(df):,}行 / 上限 {config.IMPORT_MAX_ROWS:,}行）。")
    if not columns:
        raise ImportError_("取り込む列がありません。")

    data, degraded = prepare_frame(df, columns)

    write_cols = [{"列名": c["列名"], "型": c["型"]} for c in columns]
    if timestamp_col:
        ts_name = safe_name(timestamp_col, fallback="取得日時")
        if ts_name in {c["列名"] for c in write_cols}:
            raise ImportError_(
                f"取得日時の列名 '{ts_name}' が元データの列名とぶつかっています。別の名前にしてください。")
        stamp = timestamp_value or datetime.now().isoformat(timespec="seconds")
        data[ts_name] = stamp
        write_cols.append({"列名": ts_name, "型": "TEXT"})

    config.DATA_DIR.mkdir(parents=True, exist_ok=True)
    # timeout: 裏のスケジューラと画面からの手動更新が重なっても、即エラーにせず順番待ちする
    conn = sqlite3.connect(db_path, timeout=30)
    try:
        # DROP → CREATE → INSERT を1つのまとまりにする。
        # Python の sqlite3 は既定では DDL の前に BEGIN を張らない（DMLの前だけ）ので、
        # ここで自分で張らないと DROP がその場で確定し、
        # INSERT が落ちても元のデータが戻らない（表が空のまま残る）。
        conn.execute("BEGIN")
        have = table in existing_tables(db_path) if db_path.exists() else False
        if mode == "create" and have:
            raise ImportError_(f"テーブル '{table}' は既にあります。"
                               "「作り直す」か「追記する」を選ぶか、別の名前にしてください。")
        if mode == "replace":
            conn.execute(f"DROP TABLE IF EXISTS {_importer_qi(table)}")
            have = False
        if not have:
            cols_sql = ", ".join(f"{_importer_qi(c['列名'])} {c['型']}" for c in write_cols)
            conn.execute(f"CREATE TABLE {_importer_qi(table)} ({cols_sql})")
        else:
            # 追記先に無い列があると INSERT が落ちるので、先に照合して分かる形で止める。
            # 取得日時だけは後から足せるので ALTER で追加する。
            have_cols = set(table_columns(db_path, table))
            missing = [c["列名"] for c in write_cols if c["列名"] not in have_cols]
            if timestamp_col and safe_name(timestamp_col, "取得日時") in missing:
                ts_name = safe_name(timestamp_col, "取得日時")
                conn.execute(f"ALTER TABLE {_importer_qi(table)} ADD COLUMN {_importer_qi(ts_name)} TEXT")
                missing.remove(ts_name)
            if missing:
                raise ImportError_(
                    f"追記先の '{table}' に無い列があります: {', '.join(missing)}。"
                    "列名を合わせるか、「作り直す」を選んでください。")

        placeholders = ", ".join("?" for _ in write_cols)
        cols_list = ", ".join(_importer_qi(c["列名"]) for c in write_cols)
        rows = list(data[[c["列名"] for c in write_cols]]
                    .itertuples(index=False, name=None))   # _cast で素の値に揃え済み
        conn.executemany(
            f"INSERT INTO {_importer_qi(table)} ({cols_list}) VALUES ({placeholders})", rows)
        conn.commit()
        return len(rows), degraded
    except sqlite3.Error as e:
        conn.rollback()
        raise ImportError_(f"書き込みに失敗しました: {e}") from e
    except BaseException:
        # SQLite以外の失敗（値の変換・中断など）でも、書きかけを残さない
        conn.rollback()
        raise
    finally:
        conn.close()


def prune_runs(db_path: Path, table: str, timestamp_col: str, keep: int) -> int:
    """取得日時の新しい keep 回分だけ残し、それより古い回を削除する。

    「回」は取得日時の値の種類で数える（1回の取り込みで入った行は同じ値を持つ）。
    取得日時が NULL の行 ―― この仕組みを入れる前から入っていた行 ―― は消さない。
    戻り値は削除した行数。
    """
    keep = int(keep)
    if keep < 1 or not timestamp_col:
        return 0
    table, ts = safe_name(table, table=True), safe_name(timestamp_col, "取得日時")
    if ts not in table_columns(db_path, table):
        return 0
    conn = sqlite3.connect(db_path, timeout=30)
    try:
        cur = conn.execute(
            f"DELETE FROM {_importer_qi(table)} "
            f"WHERE {_importer_qi(ts)} IS NOT NULL AND {_importer_qi(ts)} NOT IN "
            f"(SELECT {_importer_qi(ts)} FROM {_importer_qi(table)} WHERE {_importer_qi(ts)} IS NOT NULL "
            f" GROUP BY {_importer_qi(ts)} ORDER BY {_importer_qi(ts)} DESC LIMIT ?)", (keep,))
        removed = cur.rowcount or 0
        conn.commit()
        return removed
    except sqlite3.Error as e:
        conn.rollback()
        raise ImportError_(f"古い取り込み分の削除に失敗しました: {e}") from e
    finally:
        conn.close()


def table_info(db_path: Path, table: str, timestamp_col: str | None = None) -> dict:
    """1テーブルの中身の要約。「DBの管理」画面で状態を確かめるために使う。

    取得日時の列は、ジョブに設定があればそれを、無ければ既定の列名を探す
    （画面から手で取り込んだテーブルにも付いているため）。
    """
    cols = table_columns(db_path, table)
    ts = None
    for cand in (timestamp_col, config.IMPORT_TIMESTAMP_COLUMN):
        if cand and safe_name(cand, "") in cols:
            ts = safe_name(cand, "")
            break

    info = {"name": table, "columns": cols, "column_count": len(cols),
            "rows": 0, "timestamp_column": ts, "runs": None,
            "latest": None, "oldest": None}
    if not db_path.exists():
        return info
    conn = sqlite3.connect(f"file:{db_path.as_posix()}?mode=ro", uri=True)
    try:
        info["rows"] = conn.execute(f"SELECT COUNT(*) FROM {_importer_qi(table)}").fetchone()[0]
        if ts:
            row = conn.execute(
                f"SELECT COUNT(DISTINCT {_importer_qi(ts)}), MIN({_importer_qi(ts)}), MAX({_importer_qi(ts)}) "
                f"FROM {_importer_qi(table)} WHERE {_importer_qi(ts)} IS NOT NULL").fetchone()
            info["runs"], info["oldest"], info["latest"] = row[0], row[1], row[2]
    except sqlite3.Error as e:
        info["error"] = str(e)
    finally:
        conn.close()
    return info


def sample_rows(db_path: Path, table: str, limit: int | None = None,
                timestamp_col: str | None = None) -> dict:
    """テーブルの中身を数行だけ覗く（読み取り専用）。

    取得日時の列があれば新しい順に取る。「さっきの取り込みがちゃんと入ったか」を
    確かめるのが主な用途なので、先頭から取ると古い行しか見えず役に立たない。
    """
    table = safe_name(table, table=True)
    limit = int(limit or config.IMPORT_SAMPLE_ROWS)
    cols = table_columns(db_path, table)
    out = {"table": table, "columns": cols, "rows": [], "order_by": None, "limit": limit}
    if not db_path.exists() or not cols:
        out["error"] = "テーブルが見つかりません。"
        return out

    ts = None
    for cand in (timestamp_col, config.IMPORT_TIMESTAMP_COLUMN):
        if cand and safe_name(cand, "") in cols:
            ts = safe_name(cand, "")
            break
    order = f" ORDER BY {_importer_qi(ts)} DESC" if ts else ""
    out["order_by"] = ts

    conn = sqlite3.connect(f"file:{db_path.as_posix()}?mode=ro", uri=True)
    try:
        cur = conn.execute(f"SELECT * FROM {_importer_qi(table)}{order} LIMIT ?", (limit,))
        out["columns"] = [d[0] for d in cur.description]
        # BLOB はそのままだとJSONに載らないので、見える形に潰しておく
        out["rows"] = [[v.hex()[:32] if isinstance(v, (bytes, bytearray)) else v
                        for v in row] for row in cur.fetchall()]
    except sqlite3.Error as e:
        out["error"] = str(e)
    finally:
        conn.close()
    return out


def run_count(db_path: Path, table: str, timestamp_col: str) -> int:
    """いま何回分の取り込みが入っているか。"""
    ts = safe_name(timestamp_col or "", "")
    if not ts or ts not in table_columns(db_path, safe_name(table, table=True)):
        return 0
    conn = sqlite3.connect(f"file:{db_path.as_posix()}?mode=ro", uri=True)
    try:
        row = conn.execute(
            f"SELECT COUNT(DISTINCT {_importer_qi(ts)}) FROM "
            f"{_importer_qi(safe_name(table, table=True))} "
            f"WHERE {_importer_qi(ts)} IS NOT NULL").fetchone()
        return int(row[0]) if row else 0
    except sqlite3.Error:
        return 0
    finally:
        conn.close()


def drop_table(db_path: Path, table: str) -> str:
    if db_path.parent.resolve() != config.DATA_DIR.resolve():
        raise ImportError_("data/ の外は操作できません。")
    conn = sqlite3.connect(db_path)
    try:
        # ビューと表で必要な文が違う。両方撃つのは誤り: SQLite は種類が違うと
        # IF EXISTS でも例外にする（実テーブルに DROP VIEW IF EXISTS を撃つと
        # 「use DROP TABLE to delete table X」で落ちる）。先に種類を見る。
        # 綴りの大小は SQLite の DROP 側が吸収するので、探すときも合わせる
        # （BINARY で引くと「見つからない→黙って何もしない」になり、
        #   呼び出し元は掃除だけ進めて、表は残るのに知識だけ消える）
        row = conn.execute(
            "SELECT name, type FROM sqlite_master WHERE name = ? COLLATE NOCASE",
            (table,)).fetchone()
        if row is None:
            raise ImportError_(f"'{table}' はこのDBにありません。")
        real, kind = row[0], row[1]
        conn.execute(f"DROP {'VIEW' if kind == 'view' else 'TABLE'} "
                     f"IF EXISTS {_importer_qi(real)}")
        conn.commit()
        return real                      # 掃除には実物の綴りを渡す
    finally:
        conn.close()


def create_view(db_path: Path, name: str, sql: str, replace: bool = False) -> None:
    """ビュー（実体を持たない、名前を付けたSELECT）を作る。

    SQLは SELECT専用ガードを通ったものだけを渡すこと（呼び出し側で検査する）。
    replace=True なら同名のビューを作り直す（表は作り直さない＝取り違え防止）。
    """
    if db_path.parent.resolve() != config.DATA_DIR.resolve():
        raise ImportError_("data/ の外は操作できません。")
    conn = sqlite3.connect(db_path)
    try:
        row = conn.execute(
            "SELECT type FROM sqlite_master WHERE name = ?", (name,)).fetchone()
        if row and row[0] != "view":
            raise ImportError_(f"'{name}' は既にテーブルとして存在します。別の名前にしてください。")
        if row and not replace:
            raise ImportError_(f"ビュー '{name}' は既にあります。別の名前にしてください。")
        if row:
            conn.execute(f"DROP VIEW IF EXISTS {_importer_qi(name)}")
        conn.execute(f"CREATE VIEW {_importer_qi(name)} AS {sql}")
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise ImportError_(f"ビューを作れませんでした: {e}")
    finally:
        conn.close()


def list_views(db_path: Path) -> list:
    """DBにあるビューの名前と定義SQL。"""
    if not Path(db_path).exists():
        return []
    conn = sqlite3.connect(f"file:{Path(db_path).as_posix()}?mode=ro", uri=True)
    try:
        return [{"name": n, "sql": q} for n, q in conn.execute(
            "SELECT name, sql FROM sqlite_master WHERE type='view' "
            "AND name NOT LIKE 'sqlite_%' ORDER BY name")]
    finally:
        conn.close()


def view_body(db_path: Path, name: str) -> str:
    """保存されている「CREATE VIEW ... AS」の後ろ（＝SELECT本体）を取り出す。"""
    for v in list_views(db_path):
        if v["name"] == name:
            m = re.search(r"\bAS\b\s*(.+)$", v["sql"] or "", re.S | re.I)
            return (m.group(1) if m else "").strip()
    return ""


# ==========================================================================
# ===== 元 jobs.py
# 定期取り込み（ジョブ）の定義と実行。
#
# 1ジョブ = 「どのファイルを / どう読んで / どのテーブルへ / どの方式で / どの間隔で」。
# 定義は data/import_jobs.yaml に置く（DBファイル自体が全ユーザー共通なのでジョブも共通）。
#
# 実行の入口は4つ。中身はすべて run_job() に集約してある。
#   - 画面の「▶ 今すぐ更新」
#   - ジョブを登録した直後の初回取り込み（全件入れ替えのときだけ）
#   - アプリ内スケジューラ（config.IMPORT_SCHEDULER・既定60秒ごと） ← 本番はこれ
#   - cron から python core.py refresh（スケジューラを切って運用する場合）
# ==========================================================================
import threading
import os
import uuid
from datetime import datetime, timedelta
from pathlib import Path

import yaml

import config
import history
import importer

# 定義ファイルの書き換えとジョブ実行を直列化する。
# 裏で回るスケジューラと、画面からの「▶ 今すぐ更新」が同時に走りうるため。
_jobs_lock = threading.RLock()

# 画面に出す更新間隔。値は分。0 は「手動のみ」。
INTERVALS = {
    "手動のみ": 0,
    "15分ごと": 15,
    "1時間ごと": 60,
    "3時間ごと": 180,
    "6時間ごと": 360,
    "1日ごと": 1440,
    "1週間ごと": 10080,
}
MODES = {
    "replace": "全件入れ替え（毎回すべて削除して入れ直す）",
    "append": "追記（前回までのデータを残して足す）",
}

# 追記のとき「何回分の取り込みを残すか」。これを超えた古い回は消す。
# 上限を決めておかないと、日次で回すだけでもテーブルが際限なく膨らむ。
MAX_KEEP_RUNS = 800
# 既定値は置かない。何回分残すかは業務ごとに違うので、必ず自分で決めてもらう。
DEFAULT_KEEP_RUNS = None
# 開始日時の判定に使う許容。送信のタイムラグで「今」が過去扱いになるのを防ぐ。
START_GRACE_MINUTES = 2


def parse_dt(value) -> datetime | None:
    """画面から来る日時文字列（'2026-08-10T09:00' など）を datetime に。"""
    text = str(value or "").strip()
    if not text:
        return None
    try:
        return datetime.fromisoformat(text)
    except ValueError:
        return None


def validate_job(job: dict, check_start: bool = True) -> list[str]:
    """保存前の点検。画面にそのまま出せる日本語で返す。

    check_start=False にすると開始日時が過去でも通す（登録済みジョブの
    間隔変更や停止/再開など、開始日時を触らない更新のため）。
    """
    errors = []
    if not (job.get("db_file") and job.get("table")):
        errors.append("取り込み先のDBとテーブルを指定してください。")
    if not job.get("source"):
        errors.append("取り込み元のファイルを選んでください。")

    raw_start = str(job.get("start_at") or "").strip()
    if raw_start:
        start = parse_dt(raw_start)
        if start is None:
            errors.append("開始日時の形式が正しくありません。")
        elif check_start and start < datetime.now() - timedelta(minutes=START_GRACE_MINUTES):
            errors.append(f"開始日時に過去の時刻は指定できません"
                          f"（指定: {start:%Y-%m-%d %H:%M}）。今より後の日時にしてください。")

    # 取得日時列は更新の仕方によらず必須。全件入れ替えでも「いつ時点のデータか」が
    # 分からないと、取り込み後の分析で断面を説明できない。
    if not str(job.get("timestamp_column") or "").strip():
        errors.append("取得日時の列名が必須です。")

    # リアルタイム更新は「全件入れ替え」だけに許す。追記で毎回読み直すと、
    # 取得日時が質問のたびに増えて保存回数の意味が壊れるため。
    if job.get("realtime") and job.get("mode") == "append":
        errors.append("リアルタイム更新は「全件入れ替え」のときだけ使えます"
                      "（追記では、質問のたびに取得日時が増えて保存回数が崩れるため）。")

    # 追記は「時系列で溜める」ための設定なので、いつ溜めるかが決まっていないと
    # 意味をなさない（手動で押したときだけ1回ぶん増える、という中途半端な状態になる）。
    # 逆に全件入れ替えは「ファイルを鏡写しにする」ものなので、間隔は要らない。
    if job.get("mode") == "append" and int(job.get("interval_minutes") or 0) <= 0:
        errors.append("追記のときは更新間隔（定期実行）が必須です"
                      "（何回分を溜めるかを決める設定なので、いつ溜めるかも必要です）。")

    if job.get("mode") == "append":
        keep = job.get("keep_runs")
        if keep in (None, ""):
            errors.append("追記のときは保存回数が必須です。")
        else:
            try:
                keep = int(keep)
            except (TypeError, ValueError):
                errors.append("保存回数は数値で指定してください。")
            else:
                if not (1 <= keep <= MAX_KEEP_RUNS):
                    errors.append(f"保存回数は 1〜{MAX_KEEP_RUNS} の範囲で指定してください。")
    return errors


def manual_run_blocked(job: dict) -> str | None:
    """手で走らせてはいけない設定なら、その理由を返す（問題なければ None）。

    定期実行 × 追記 の組み合わせだけは止める。この2つが重なると、
      ・次回予定が「前回実行＋間隔」で決まるので、手で走らせた分だけ後ろにずれる
      ・保存回数を1回ぶん余計に使い、その回だけ間隔の違うデータが混ざる
    となって、せっかく決めた更新頻度が崩れる。
    全件入れ替えや「手動のみ」の設定は、何度走らせても頻度の意味が変わらないので通す。
    """
    if int(job.get("interval_minutes") or 0) <= 0:
        return None
    if (job.get("mode") or "replace") != "append":
        return None
    label = interval_label(job.get("interval_minutes", 0))
    return (f"「{job.get('name') or 'この設定'}」は定期実行（{label}）＋追記です。"
            "手動で動かすと次回の実行時刻がずれ、保存回数も1回ぶん余計に使うため、"
            "手動実行はできません。どうしても今すぐ入れたいときは、"
            "更新の頻度を「手動のみ」に変えてから実行してください。")


def interval_label(minutes: int) -> str:
    for k, v in INTERVALS.items():
        if v == int(minutes or 0):
            return k
    return f"{minutes}分ごと"


# =============================================================================
# 保存と読み出し
# =============================================================================

def _read() -> list[dict]:
    p = config.IMPORT_JOBS_FILE
    if not p.exists():
        return []
    try:
        data = yaml.safe_load(p.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[jobs] 読めませんでした: {p} ({e})")
        return []
    items = data.get("jobs") if isinstance(data, dict) else data
    return [j for j in (items or []) if isinstance(j, dict) and j.get("id")]


def _write(items: list[dict]) -> None:
    p = config.IMPORT_JOBS_FILE
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(yaml.safe_dump({"jobs": items}, allow_unicode=True, sort_keys=False),
                 encoding="utf-8")


def list_jobs() -> list[dict]:
    return sorted(_read(), key=lambda j: (j.get("name") or ""))


def get_job(job_id: str) -> dict | None:
    return next((j for j in _read() if j.get("id") == job_id), None)


def _same_target(a: dict, b: dict) -> bool:
    """同じ取り込み元（ファイル＋シート）を同じDBの同じテーブルへ入れる設定か。"""
    def norm_path(p):
        return os.path.normcase(os.path.normpath(str(p or "").strip()))
    return (norm_path(a.get("source")) == norm_path(b.get("source"))
            and (a.get("sheet") or None) == (b.get("sheet") or None)
            and (a.get("db_file") or "") == (b.get("db_file") or "")
            and (a.get("table") or "") == (b.get("table") or ""))


def find_duplicate(job: dict) -> dict | None:
    """同じ取り込み元→同じテーブルの設定がすでにあれば、それを返す（自分自身は除く）。

    同じ設定が2つあると、同じ時刻に2回追記されて全行が二重になる
    （「保持N回」は取得日時で数えるので、同時刻の2バッチを1回分とみなして両方残す）。
    登録時に止めるためのもの。
    """
    for j in _read():
        if j.get("id") != job.get("id") and _same_target(j, job):
            return j
    return None


def find_target_clash(job: dict) -> dict | None:
    """同じテーブルを狙う「別の取り込み元」の設定があれば返す（自分自身は除く）。

    find_duplicate は同一ファイル→同一テーブルしか見ないので、
    別のファイルから同じテーブルへの2本目が黙って登録できてしまっていた。
    それを許すと、どちらかのファイルが更新されるたびに表の中身が
    入れ替わる綱引きになり、利用者からは「数字が勝手に変わる」ようにしか
    見えない。1テーブルにつき取り込み設定は1本に限る。
    """
    for j in _read():
        if (j.get("id") != job.get("id")
                and (j.get("db_file") or "") == (job.get("db_file") or "")
                and (j.get("table") or "") == (job.get("table") or "")):
            return j
    return None


def save_job(job: dict) -> dict:
    with _jobs_lock:
        job = dict(job)
        # setdefault では駄目。呼び出し側が id=None を明示的に入れてくることがあり、
        # そのまま保存すると読み出し時に落とされて「保存したのに消える」ことになる。
        if not job.get("id"):
            job["id"] = uuid.uuid4().hex[:12]
        if not job.get("created_at"):
            job["created_at"] = datetime.now().isoformat(timespec="seconds")
        items = [j for j in _read() if j.get("id") != job["id"]]
        items.append(job)
        _write(items)
        return job


def delete_job(job_id: str) -> bool:
    with _jobs_lock:
        items = _read()
        left = [j for j in items if j.get("id") != job_id]
        if len(left) == len(items):
            return False
        _write(left)
        return True


# =============================================================================
# 実行タイミング
# =============================================================================

def next_run_at(job: dict) -> datetime | None:
    """次に動く予定の時刻。手動のみなら None。

    開始日時が設定されていれば、それより前には動かさない。
    """
    minutes = int(job.get("interval_minutes") or 0)
    if minutes <= 0:
        return None
    start = parse_dt(job.get("start_at"))
    last = parse_dt(job.get("last_run"))
    if last is None:
        # 一度も動いていない。開始日時があればその時刻、無ければすぐ対象。
        return start or datetime.now()
    nxt = last + timedelta(minutes=minutes)
    return max(nxt, start) if start else nxt


def is_due(job: dict, now: datetime | None = None) -> bool:
    if not job.get("enabled", True):
        return False
    nxt = next_run_at(job)
    return nxt is not None and nxt <= (now or datetime.now())


def due_jobs(now: datetime | None = None) -> list[dict]:
    return [j for j in list_jobs() if is_due(j, now)]


# =============================================================================
# 「設定どおりに更新できていない」ジョブ
#
# 失敗は履歴を見に行かないと分からず、日次の取り込みが月曜から失敗して金曜まで
# 誰も気づかない、が起こり得る。そこで「いま健全でないジョブ」を1か所で判定し、
#   ・チャットのサイドバー（DB名・テーブル名に警告マーク）
#   ・AIの回答（そのテーブルを使う質問に、データが古い可能性を添える）
#   ・管理者へのメール通知
# の3つが同じ判断を使う。
# =============================================================================

def problems() -> list[dict]:
    """設定どおりに更新できていない定期取り込み。

    3種類ある:
      failed   … 前回の実行が失敗した（ファイルが無い・シート名や列が変わった等）
      degraded … 取り込めたが、数値列に文字が混ざって文字として保存した
                 （合計・平均がずれる。元ファイルの値を直すべき）
      overdue  … 有効な自動実行なのに、予定の2周期ぶん以上動いていない
                 （スケジューラが止まっている・アプリが落ちていた等）
    戻り値: [{id, name, db_file, table, kind, since, message}, ...]
    """
    now = datetime.now()
    out = []
    for j in list_jobs():
        if not j.get("enabled", True):
            continue
        if j.get("last_status") == "error":
            out.append({"id": j.get("id"), "name": j.get("name"),
                        "db_file": j.get("db_file"), "table": j.get("table"),
                        "kind": "failed", "since": j.get("last_run") or "",
                        "message": j.get("last_message") or "前回の実行が失敗しました。"})
            continue
        if j.get("last_degraded"):
            cols = "、".join(str(c) for c in j["last_degraded"])
            out.append({"id": j.get("id"), "name": j.get("name"),
                        "db_file": j.get("db_file"), "table": j.get("table"),
                        "kind": "degraded", "since": j.get("last_run") or "",
                        "message": (f"前回の取り込みで、数値の列（{cols}）に数値でない値が混ざり、"
                                    "文字として保存しました。合計や平均がずれる可能性があります。"
                                    "元ファイルの値を確認してください。")})
            continue
        minutes = int(j.get("interval_minutes") or 0)
        last = parse_dt(j.get("last_run"))
        if minutes > 0 and last and (now - last) > timedelta(minutes=minutes * 2):
            out.append({"id": j.get("id"), "name": j.get("name"),
                        "db_file": j.get("db_file"), "table": j.get("table"),
                        "kind": "overdue", "since": j.get("last_run") or "",
                        "message": (f"{interval_label(minutes)}の予定ですが、"
                                    f"{last:%m/%d %H:%M} から更新されていません。"
                                    "自動実行が止まっている可能性があります。")})
    return out


def problems_by_table() -> dict:
    """{(db_file, table): [problem, ...]}。画面やAIの注記で引きやすい形。"""
    out: dict = {}
    for p in problems():
        out.setdefault((p["db_file"], p["table"]), []).append(p)
    return out


# =============================================================================
# 実行
# =============================================================================

def source_path(job: dict) -> Path:
    return Path(job.get("source", ""))


def _source_stamp(job: dict) -> str:
    """元ファイルの版。更新時刻とサイズを見る（中身を読まずに変化を判定する）。"""
    try:
        st = source_path(job).stat()
        return f"{st.st_mtime_ns}:{st.st_size}"
    except OSError:
        return ""


def run_job(job: dict, kind: str = "auto", user: str | None = None) -> dict:
    """1ジョブを実行して、結果を定義ファイルに書き戻す。

    kind は履歴に残す実行のきっかけ。"auto"=スケジューラ、"job"=画面の「▶ 今すぐ更新」。

    例外は投げず、結果を dict で返す（1本こけても他を止めないため）。
      {"ok": bool, "rows": int, "message": str, "degraded": [...]}
    """
    with _jobs_lock:                       # 同じテーブルへ同時に書かないように直列化する
        return _run_job_locked(job, kind, user)


def _run_job_locked(job: dict, kind: str = "auto", user: str | None = None) -> dict:
    started = datetime.now()
    result = {"ok": False, "rows": 0, "message": "", "degraded": []}
    removed = 0
    kept = None
    try:
        path = source_path(job)
        if not importer.is_allowed(path):
            raise importer.ImportError_(
                "取り込み元のファイルが見つかりません（移動・削除、または許可フォルダの設定変更）。")

        df = importer.read_table(
            path,
            sheet=job.get("sheet") or None,
            header_row=int(job.get("header_row") or 0),
            delimiter=job.get("delimiter") or None,
        )
        cols = [dict(c) for c in (job.get("columns") or [])]
        if not cols:
            cols = importer.plan_columns(df)
        missing = [c["元の列名"] for c in cols if c["元の列名"] not in df.columns]
        if missing:
            if len(missing) == len(cols):
                # 1列も合わない＝列名の変更ではなく、区切り文字か見出し行の位置が変わった
                found = "、".join(str(c) for c in list(df.columns)[:5])
                raise importer.ImportError_(
                    f"設定した列が1つも見つかりません（ファイル側の見出し: {found}"
                    f"{' …' if len(df.columns) > 5 else ''}）。"
                    "区切り文字・見出し行の位置・シートが変わった可能性があります。"
                    "取り込み画面で開き直して設定を作り直してください。")
            raise importer.ImportError_(
                f"ファイル側に無い列があります: {', '.join(missing)}。"
                "列構成が変わった可能性があります。設定を作り直してください。")

        db_path = config.DATA_DIR / job["db_file"]
        mode = job.get("mode") or "replace"
        ts_col = job.get("timestamp_column") or config.IMPORT_TIMESTAMP_COLUMN
        if len(df) == 0:
            # 見出しだけのファイル（上流の出力が失敗した等）で全件入れ替えすると、
            # テーブルが空になり「成功」で終わる。前回の内容を残して止める。
            # 本当に0件にしたいときは、取り込み画面から手で入れ替える。
            raise importer.ImportError_(
                f"{path.name} にデータ行がありません（見出しだけ）。"
                f"{'テーブルを空にしないため、前回の内容を残しました。' if mode != 'append' else '追記する行が無いため何もしていません。'}"
                "本当に0件なら、取り込み画面から手で入れ替えてください。")
        n, degraded = importer.import_dataframe(
            db_path, job["table"], df, cols, mode=mode,
            timestamp_col=ts_col,
            timestamp_value=started.isoformat(timespec="seconds"),
        )
        message = f"{n:,}行を{'追記' if mode == 'append' else '全件入れ替え'}しました。"
        if degraded:
            # 指定した型のままでは値が変わってしまう列。取り込み自体は通るが
            # 集計がずれるので、黙って通さない
            message += (f" ⚠ 型を変えて保存した列: {', '.join(degraded)}"
                        "（元ファイルの値を確認してください）")

        # 追記のときは、保存回数を超えた古い取り込み分を落とす
        if mode == "append" and ts_col and job.get("keep_runs"):
            removed = importer.prune_runs(db_path, job["table"], ts_col, job["keep_runs"])
            kept = importer.run_count(db_path, job["table"], ts_col)
            result["removed"], result["kept"] = removed, kept
            message += f" 保持 {kept}/{job['keep_runs']}回"
            if removed:
                message += f"（古い {removed:,}行を削除）"
        result.update(ok=True, rows=n, degraded=degraded, message=message)
    except importer.ImportError_ as e:
        result["message"] = str(e)
    except Exception as e:                        # 想定外でもジョブ一覧は壊さない
        result["message"] = f"想定外のエラー: {e}"

    saved = get_job(job.get("id", "")) or dict(job)
    saved.update({
        "last_run": started.isoformat(timespec="seconds"),
        "last_status": "ok" if result["ok"] else "error",
        "last_message": result["message"],
        "last_rows": result["rows"],
        "last_degraded": list(result.get("degraded") or []),
    })
    if result["ok"]:
        # 取り込んだ時点の元ファイルの版。リアルタイム更新が
        # 「変わったときだけ動く」ための基準になる（経路によらず記録する）
        saved["source_stamp"] = _source_stamp(job)
    save_job(saved)
    history.add_import_record(job.get("db_file", ""), job.get("table", ""),
                result["ok"], result["message"], kind=kind,
                mode=job.get("mode") or "replace", rows=result["rows"],
                removed=removed, kept=kept, keep=job.get("keep_runs"),
                source=job.get("source", ""), sheet=job.get("sheet"),
                job_id=job.get("id"), job_name=job.get("name"),
                user=user, started=started)
    return result


# =============================================================================
# リアルタイム更新
#
# 「取り込み → SQLite → 質問」の形だと、元ファイルを直したことが次の定期実行まで
# 反映されない。リアルタイムを付けたジョブは、質問を受けた時点で元ファイルの
# 更新時刻を見て、前回の取り込みより新しければその場で取り込み直す。
#
#   ・変わっていなければ何もしない（普段の速さは落ちない）
#   ・読めなければ前回取り込んだ内容のまま答える（途中まで書かれたファイルや、
#     Excel を開いている最中に、壊れた状態で読み込んで上書きしないため）
#   ・全件入れ替えのみ。追記は取得日時の回数管理と衝突するので validate で禁止
# =============================================================================

def realtime_jobs() -> list[dict]:
    """リアルタイム更新が有効なジョブ。停止中のものは含めない。"""
    return [j for j in list_jobs()
            if j.get("realtime") and j.get("enabled", True)
            and (j.get("mode") or "replace") != "append"]


def _note_realtime_failure(job: dict, message: str) -> bool:
    """リアルタイム更新でしか気づけない失敗を、定期実行と同じ形で記録する。

    定期実行のジョブなら、元ファイルが消えても次の実行が失敗して
    last_status="error" になり、problems() の failed として拾われる
    （サイドバーの⚠・AIへの注記・管理者へのメール）。
    ところがリアルタイム専用（更新間隔＝手動のみ）のジョブには、その受け皿が
    無かった。run_job を通らないので last_status は "ok" のまま、
    problems() の overdue も interval が 0 なので対象外。結果、警告がどこにも
    出ないまま、消えたファイルの「前回取り込んだ内容」で答え続けることになる。

    質問のたびに呼ばれるので、状態が変わったときだけ書く
    （毎回書くとジョブ定義と履歴が肥大する）。戻り値は今回新しく記録したか。
    """
    saved = get_job(job.get("id", ""))
    if saved is None:
        return False
    if saved.get("last_status") == "error" and saved.get("last_message") == message:
        return False                       # 既に同じ理由で記録済み。黙って続ける
    saved["last_status"] = "error"
    saved["last_message"] = message
    # last_run は触らない。実行していないので「最後に動いた時刻」は変わらない。
    # source_stamp も残す。ファイルが戻ったとき、版が違えば取り込み直せる。
    save_job(saved)
    history.add_import_record(
        job.get("db_file", ""), job.get("table", ""), False, message,
        kind="realtime", mode=job.get("mode") or "replace", rows=0,
        source=job.get("source", ""), sheet=job.get("sheet"),
        job_id=job.get("id"), job_name=job.get("name"))
    return True


def refresh_realtime(scope: list[dict]) -> list[dict]:
    """スコープ内のテーブルのうち、元ファイルが更新されたものを取り込み直す。

    質問のたびに呼ばれる。戻り値は実際に取り込み直したぶんの記録で、
    呼び出し側が画面やログに出すために使う（何も無ければ空リスト）。
    """
    if not scope:
        return []
    wanted = {str(s.get("name") or Path(s["path"]).name) for s in scope}
    done = []
    for job in realtime_jobs():
        if job.get("db_file") not in wanted:
            continue
        stamp = _source_stamp(job)
        if not stamp:
            # ファイルが見当たらない。前回の内容のまま答える（黙って古いデータにしない
            # ために記録は残す）。ジョブ側にも失敗として残し、定期実行が失敗した
            # ときと同じ経路（サイドバーの⚠・AIへの注記・管理者へのメール）に乗せる。
            msg = ("取り込み元のファイルが見つかりません。"
                   "前回取り込んだ内容で回答します。")
            _note_realtime_failure(job, msg)
            done.append({"job": job.get("name") or job.get("table"), "ok": False,
                         "table": job.get("table"), "db_file": job.get("db_file"),
                         "message": msg})
            continue
        if stamp == str(job.get("failed_stamp") or ""):
            # この版はもう試して駄目だった。質問のたびに読み直しても結果は同じで、
            # 大きなファイルだと1問ごとに数十秒待たせ、履歴も同じ失敗で埋まる。
            # ファイルがさらに変わったら（stamp が違ったら）また試す
            continue
        if stamp == str(job.get("source_stamp") or ""):
            # 変わっていない。ただし「ファイルが無い」で失敗扱いになった後、
            # 同じ内容のまま戻ってきた場合はここに来る。中身は前回取り込んだものと
            # 一致しているので取り込み直しは不要だが、警告だけは下ろす
            # （下ろさないと、ファイルが次に変わるまで⚠が出続ける）。
            if job.get("last_status") == "error":
                saved = get_job(job.get("id", ""))
                if saved is not None:
                    saved["last_status"] = "ok"
                    saved["last_message"] = ("取り込み元のファイルが戻りました"
                                             "（内容は前回取り込んだものと同じ）。")
                    save_job(saved)
                    done.append({"job": job.get("name") or job.get("table"), "ok": True,
                                 "table": job.get("table"), "db_file": job.get("db_file"),
                                 "message": saved["last_message"]})
            continue                       # 変わっていない
        # 版の記録は run_job 側で行う（成功時のみ。失敗したら次の質問で再挑戦）
        res = run_job(job, kind="realtime")
        saved = get_job(job.get("id", ""))
        if saved is not None:
            # 失敗した版を覚える／成功したら忘れる
            if res.get("ok"):
                saved.pop("failed_stamp", None)
            else:
                saved["failed_stamp"] = stamp
            save_job(saved)
        done.append({"job": job.get("name") or job.get("table"), "ok": res.get("ok"),
                     "table": job.get("table"), "db_file": job.get("db_file"),
                     "rows": res.get("rows"),
                     "message": res.get("message") or ""})
    return done


# ==========================================================================
# ===== 元 scheduler.py
# アプリ内スケジューラ。cron や常駐サービスを別に用意せず、Pythonだけで定期実行する。
#
# アプリ起動時にデーモンスレッドを1本立て、一定間隔で「期限が来たジョブ」を実行する。
# 画面を誰も開いていなくても、アプリのプロセスが生きていれば動く。
#
#   create_app() ──start()──▶ [aiagent-import-scheduler スレッド]
#                                 └─ 60秒ごと: jobs.due_jobs() → jobs.run_job()
#
# このスレッドにはリクエストの文脈が無いので、Flask の g や request は使わない。
# 状態は _state に置いて画面側から読む。
# ==========================================================================
import atexit
import threading
import traceback
from datetime import datetime

import config
import jobs

# 名前でスレッドの生存を確認する。モジュールが再読込されてもフラグに頼らず
# 二重起動を防げる（開発中にファイルを保存するとStreamlitが読み直すため）。
_THREAD_NAME = "aiagent-import-scheduler"

# 終了時に眠っているスレッドを起こして片付けるための合図。
# sleep() で寝かせたままプロセスを終わらせると、後始末中に標準出力を掴んだままになり
# 「_enter_buffered_busy ... daemon threads」で異常終了することがある。
_stop = threading.Event()

_state: dict = {
    "started_at": None,
    "last_tick": None,
    "tick_count": 0,
    "last_ran": [],        # 直近に実行したジョブ [{name, ok, message, at}]
    "last_error": None,
}


def is_running() -> bool:
    return any(t.name == _THREAD_NAME and t.is_alive() for t in threading.enumerate())


def scheduler_status() -> dict:
    return {**_state, "running": is_running(),
            "tick_sec": config.IMPORT_SCHEDULER_TICK_SEC,
            "enabled": config.IMPORT_SCHEDULER}


def _scheduler_log(msg: str) -> None:
    if _stop.is_set():                 # 終了処理中は標準出力に触らない
        return
    try:
        print(f"[scheduler {datetime.now():%Y-%m-%d %H:%M:%S}] {msg}", flush=True)
    except (ValueError, OSError):      # 出力先が既に閉じられている
        pass


#: 前回の周回で「設定どおりに更新できていなかった」ジョブ。変化を見るために持つ。
_prev_problems: list = []


def tick() -> list:
    """期限が来たジョブを実行する（スレッドの1周分。テストからも呼べる）。"""
    global _prev_problems
    ran = []
    for job in jobs.due_jobs():
        res = jobs.run_job(job)
        ran.append({"name": job.get("name") or job.get("id"), "ok": res["ok"],
                    "message": res["message"],
                    "at": datetime.now().isoformat(timespec="seconds")})
        _scheduler_log(("OK  " if res["ok"] else "NG  ") + f"{job.get('name')}: {res['message']}")
    _state["last_tick"] = datetime.now().isoformat(timespec="seconds")
    _state["tick_count"] += 1
    if ran:
        _state["last_ran"] = ran[-10:]
    # 「健全→失敗」「失敗→復旧」の変わり目だけ管理者に知らせる
    try:
        import mailer
        cur = jobs.problems()
        if _state["tick_count"] > 1:          # 起動直後の1周目は「変化」ではないので送らない
            r = mailer.alert_import_problems(cur, _prev_problems)
            if r:
                _scheduler_log(f"管理者に通知: {r.get('message', '')}")
        _prev_problems = cur
    except Exception as e:
        _scheduler_log(f"通知の判定に失敗（続行）: {e}")
    return ran


def _loop() -> None:
    _scheduler_log(f"開始（{config.IMPORT_SCHEDULER_TICK_SEC}秒ごとに確認）")
    while not _stop.is_set():
        try:
            tick()
            _state["last_error"] = None
        except Exception as e:
            # 1周こけても止めない。止まると以後ずっと更新されなくなるため。
            _state["last_error"] = f"{e}"
            _scheduler_log("巡回でエラー: " + traceback.format_exc(limit=3).replace("\n", " "))
        # sleep ではなく wait。停止の合図が来たら即座に抜ける。
        _stop.wait(max(5, config.IMPORT_SCHEDULER_TICK_SEC))


def stop(timeout: float = 2.0) -> None:
    """スレッドを止める（プロセス終了時に自動で呼ばれる）。"""
    _stop.set()
    for t in threading.enumerate():
        if t.name == _THREAD_NAME and t.is_alive() and t is not threading.current_thread():
            t.join(timeout=timeout)


def start() -> bool:
    """スケジューラを起動する。何度呼んでも1本しか立たない。"""
    if not config.IMPORT_SCHEDULER:
        return False
    if is_running():
        return False
    _stop.clear()
    t = threading.Thread(target=_loop, name=_THREAD_NAME, daemon=True)
    t.start()
    atexit.register(stop)
    _state["started_at"] = datetime.now().isoformat(timespec="seconds")
    return True


# ==========================================================================
# ===== 元 cleanup.py
# テーブル・DBを消したときの後片付け。
#
# 消すこと自体は DROP TABLE とファイル移動で済む。面倒なのはその後で、
# 参照は方々に散らばっている。
#
#   ・そのDBの .meta.yaml  … 説明・関連・用語・例文・検算ルール・ER図の配置
#   ・他のDBの .meta.yaml  … DBをまたぐ関連、ER図に借りたテーブル
#   ・定期取り込みの設定    … 残すと、消したテーブルが次の実行で復活する
#   ・利用者ごとの選択      … 「対象データ」に消えたDBが残り続ける
#
# 放っておくと、AIには存在しないテーブルの説明が渡り続け、例文の検証は
# 「no such table」で落ちる。掃除をここに集めて、消し忘れが出ないようにする。
#
# 消す前の「何が巻き添えになるか」も同じ規則で数える（table_impact）。
# 数えるだけの関数は何も書き換えない。
# ==========================================================================
import re
from pathlib import Path

import catalog
import config
import db
import jobs
import prefs
import verify


# =============================================================================
# SQLがそのテーブルを触っているか
# =============================================================================

def uses_table(sql: str, table: str, alias: str | None = None) -> bool:
    """SQL文字列がそのテーブル名を参照しているか。

    "orders" と "demo_sales.orders" の両方を見る。素の名前だけを探すと
    DB名で修飾された書き方（例文はたいていこちら）を取りこぼし、
    修飾ありだけを探すと単一DBの例文を取りこぼす。
    構文解析まではしない。掃除の判定なので、取りこぼすより拾いすぎるほうがまし。
    ただし何を消したかは呼び出し側で必ず報告すること。
    """
    if not table:
        return False
    text = str(sql or "")
    t = r'"?' + re.escape(table) + r'"?(?![\w])'
    if re.search(r'(?<![\w."])' + t, text, re.IGNORECASE):
        return True
    if alias and re.search(r'(?<![\w."])' + re.escape(alias) + r'\s*\.\s*' + t,
                           text, re.IGNORECASE):
        return True
    return False


def _rel_text(rel: dict) -> str:
    return f"{rel.get('from', '')} → {rel.get('to', '')}"


def _ep_hits(rel: dict, own_alias: str, alias: str, table: str | None) -> bool:
    """関連の端点が (alias, table) を指しているか。table=None ならDB丸ごと。"""
    for key in ("from", "to"):
        ep = catalog.parse_endpoint_cols(rel.get(key, ""), own_alias)
        if ep and ep[0] == alias and (table is None or ep[1] == table):
            return True
    return False


# =============================================================================
# メタの掃除（1ファイルぶん）
# =============================================================================

def _scrub_meta(meta: dict, own_alias: str, alias: str, table: str | None) -> dict:
    """meta から (alias, table) への参照を落とす。落としたものを返す。

    meta はその場で書き換える。table=None なら、そのDBへの参照すべて。
    自分自身のDB（own_alias == alias）かどうかで消す範囲が変わる:
      自分   … テーブルの説明・用語・例文・検算も消す
      他所   … 関連とER図の置き場所だけ（例文は他DBのテーブルを引くこともある）
    """
    hit: dict = {"relationships": [], "glossary": [], "examples": [],
                 "checks": [], "tables": [], "er_layout": [], "tools": []}
    mine = own_alias == alias

    rels = meta.get("relationships") or []
    keep = [r for r in rels if not _ep_hits(r, own_alias, alias, table)]
    if len(keep) != len(rels):
        hit["relationships"] = [_rel_text(r) for r in rels
                                if _ep_hits(r, own_alias, alias, table)]
        meta["relationships"] = keep
    if not meta.get("relationships"):
        meta.pop("relationships", None)

    # ER図の配置（"alias.table": [x, y]）
    layout = meta.get("er_layout") or {}
    lgone = [k for k in layout
             if str(k).split(".")[0] == alias
             and (table is None or str(k).split(".")[-1] == table)]
    if lgone:
        hit["er_layout"] = lgone
        for k in lgone:
            layout.pop(k, None)
        if not layout:
            meta.pop("er_layout", None)

    if not mine:
        return hit

    # --- ここから先は自分のDBのときだけ -------------------------------------
    if table is None:
        return hit                      # DBごと消えるのでファイルごと処分される

    tables = meta.get("tables") or {}
    if table in tables:
        hit["tables"] = [table]
        tables.pop(table, None)
        if not tables:
            meta.pop("tables", None)

    # DB全体の用語。SQL式がそのテーブルを引いているものだけ消す。
    # 説明文だけの用語は、文中にテーブル名が出てきても残す（文章なので）
    gl = meta.get("glossary") or {}
    gone_terms = [t for t, v in gl.items()
                  if isinstance(v, dict) and uses_table(v.get("sql"), table, alias)]
    if gone_terms:
        hit["glossary"] = gone_terms
        for t in gone_terms:
            gl.pop(t, None)
        if not gl:
            meta.pop("glossary", None)

    exs = meta.get("examples") or []
    left = [e for e in exs if not uses_table(e.get("sql"), table, alias)]
    if len(left) != len(exs):
        hit["examples"] = [str(e.get("q") or e.get("sql") or "")[:60]
                           for e in exs if uses_table(e.get("sql"), table, alias)]
        meta["examples"] = left
        if not left:
            meta.pop("examples", None)

    # ユーザー定義ツールのSQL。ここを見ていなかったので、
    # 消した表を使うツールがカタログに残り、AIに配られ続けていた
    tls = meta.get("tools") or []
    keep_tools = [x for x in tls
                  if not uses_table(str((x or {}).get("sql") or ""), table, alias)]
    if len(keep_tools) != len(tls):
        hit["tools"] = [str((x or {}).get("name") or "")
                        for x in tls if x not in keep_tools]
        meta["tools"] = keep_tools
        if not keep_tools:
            meta.pop("tools", None)

    cks = verify.normalize(meta.get("checks"))
    def ck_hits(c):
        return any(uses_table(s, table, alias) for s in
                   (c["left"]["sql"], c["right"]["sql"], c.get("drilldown") or ""))
    left = [c for c in cks if not ck_hits(c)]
    if len(left) != len(cks):
        hit["checks"] = [c["name"] for c in cks if ck_hits(c)]
        meta["checks"] = left
        if not left:
            meta.pop("checks", None)

    return hit


def _merge(into: dict, where: str, hit: dict) -> None:
    """掃除の結果を「どのDBで何を消したか」の形で積む。"""
    for key, items in hit.items():
        for it in items:
            into.setdefault(key, []).append({"db": where, "text": it})


# =============================================================================
# 下見（消す前に見せる。何も書き換えない）
# =============================================================================

def _cleanup_walk(alias: str, table: str | None, apply: bool, skip: Path | None = None) -> dict:
    """全DBのメタを見て、(alias, table) への参照を数える／消す。

    apply=False なら保存しない。skip はそのDB自身のファイル（消すので触らない）。

    load_meta が返すのは控え（キャッシュ）そのものなので、必ず写しを取ってから
    書き換える。ここを直に触ると、削除前の「巻き添えの下見」（apply=False）が
    控えを先に消してしまい、本番の掃除が「消すものが無い」と判断して
    ファイルを書き換えない ＝ 消したテーブルの説明が残り続ける。
    """
    import copy

    found: dict = {}
    for f in db.list_db_files():
        if skip is not None and f == skip:
            continue
        own = db.alias_for(f)
        meta = copy.deepcopy(catalog.load_meta(f))
        hit = _scrub_meta(meta, own, alias, table)
        if any(hit.values()):
            _merge(found, own, hit)
            if apply:
                catalog.save_meta(f, meta)
    return found


def _jobs_for(db_name: str, table: str | None) -> list[dict]:
    return [j for j in jobs.list_jobs()
            if j.get("db_file") == db_name and (table is None or j.get("table") == table)]


def _job_text(j: dict) -> str:
    """定期取り込みの1行分。何がどの間隔で入ってくる設定かが分かればよい。"""
    label = jobs.interval_label(j.get("interval_minutes"))
    name = j.get("name") or j.get("table") or "（無題）"
    stopped = "・停止中" if j.get("enabled") is False else ""
    return f"{name}（{j.get('table')} / {label}{stopped}）"


def _orphan_terms(path: Path, table: str) -> list[dict]:
    """この表を消すと「置き場を失う」全体用語を探す（数えるだけ・消さない）。

    自動削除は「SQLに表名が書かれているか」で判定するため、
    列名だけで書かれた式（例: minutes >= 60）はどの表を消しても残る。
    残った式は検証も整合性の警告も効かなくなるので、削除の確認画面で
    「この表の列だけで成立している用語」を人に見せて、判断を委ねる。
    """
    prof = catalog.profile_db(path)
    meta = catalog.load_meta(path)
    all_tables = {t: {c["name"].lower() for c in (v.get("columns") or [])}
                  for t, v in prof["tables"].items()}
    target_cols = all_tables.get(table) or set()
    if not target_cols:
        return []
    others = {t: cols for t, cols in all_tables.items() if t != table}

    def _words(sql: str) -> set:
        bare = re.sub(r"'[^']*'|\"[^\"]*\"", " ", str(sql or ""))
        return {w.lower() for w in re.findall(r"\w+", bare)
                if not w.isdigit()} - _SQL_WORDS

    out = []
    for term, v in catalog.db_glossary(meta).items():
        sql = (v or {}).get("sql") or ""
        if not sql or uses_table(sql, table, db.alias_for(path)):
            continue                      # 表名を書いている式は自動削除の側で扱う
        words = _words(sql)
        if not words or not words <= target_cols:
            continue                      # この表では成立していない式
        if any(words <= cols for cols in others.values()):
            continue                      # 他の表でも成立する＝残しても宙に浮かない
        out.append({"db": path.name,
                    "text": f"{term}（式に表名が無く、この表の列だけで成立しています。"
                            "削除しても自動では消えないため、用語集で見直してください）"})
    return out


def views_using(path: Path, table: str) -> list[str]:
    """その名前を定義の中で使っているビューの名前。

    ビューの土台を消すと、そのビューは壊れたままDBに残る。SQLiteは
    壊れたビューが1つでもあると、無関係な表の ALTER TABLE RENAME まで
    失敗させるので、消す前に必ず気づけるようにする。
    """
    pat = re.compile(r'(?<![\w."])"?' + re.escape(table) + r'"?(?![\w])')
    return sorted(v["name"] for v in importer.list_views(path)
                  if v["name"] != table and pat.search(str(v.get("sql") or "")))


def table_impact(path: Path, table: str) -> dict:
    """テーブルを消したときに巻き添えになるもの。数えるだけ。"""
    alias = db.alias_for(path)
    out = _cleanup_walk(alias, table, apply=False)
    # 「壊れて残るビュー」は、カタログのYAMLではなくDBの中にある。
    # ここに出さないと、消した本人が壊したことに気づけない
    vs = views_using(path, table)
    if vs:
        out["broken_views"] = [{"db": path.name, "text": v} for v in vs]
    out["jobs"] = [{"id": j.get("id"), "name": j.get("name") or j.get("table"),
                    "text": _job_text(j)}
                   for j in _jobs_for(path.name, table)]
    orphans = _orphan_terms(path, table)
    if orphans:
        out["orphan_terms"] = orphans
    return out


# =============================================================================
# 実際に消す
# =============================================================================

def clean_table(path: Path, table: str, drop_jobs: bool = True) -> dict:
    """テーブルを消したあとの掃除。DROP TABLE 自体は importer 側で済ませておく。"""
    alias = db.alias_for(path)
    done = _cleanup_walk(alias, table, apply=True)
    done["jobs"] = []
    if drop_jobs:
        for j in _jobs_for(path.name, table):
            if jobs.delete_job(j.get("id")):
                done["jobs"].append({"db": path.name,
                                     "text": j.get("name") or j.get("table")})
    catalog.forget(path)
    # まとまりの最後の表が消えたら、まとまりのメモも片づける
    # （残すと、無いデータの前提だけがAIに渡り続ける）
    if table and "__" in table:
        pref = table.split("__", 1)[0]
        prof = catalog.profile_db(path)
        if not any(t.startswith(pref + "__") for t in prof["tables"]):
            meta = catalog.load_meta_for_edit(path)
            if pref in (meta.get("groups") or {}):
                info = meta["groups"].pop(pref)
                if not meta["groups"]:
                    meta.pop("groups", None)
                catalog.save_meta(path, meta)
                done["groups"] = [{"db": path.name, "text": pref}]
    return done


def _rename_in_text(text: str, old: str, new: str) -> str:
    """文の中のテーブル名を境界つきで置き換える（SQL・散文の両方に使う）。

    境界はUnicodeの語構成文字で見る。日本語のテーブル名では「品質__x」が
    「高品質__x」の一部に一致してしまう事故があり得るため、英数字だけの
    境界では足りない。
    """
    return re.sub(r"(?<!\w)" + re.escape(old) + r"(?!\w)", new, text)


def _fix_view_refs(conn, old: str, new: str) -> int:
    """本文が old を参照しているビューを、new を参照する形で作り直す。

    ビューの改名は DROP+CREATE なので、それを参照している別のビューは
    旧名のまま取り残されて壊れる（ALTER TABLE RENAME なら SQLite が直す）。
    同じ接続の中で直すので、途中で壊れた状態が外から見えることはない。
    """
    pat = re.compile(r'(?<![\w."])"?' + re.escape(old) + r'"?(?![\w])')
    rows = conn.execute(
        "SELECT name, sql FROM sqlite_master WHERE type='view'").fetchall()
    fixed = 0
    for name, sql in rows:
        if name == new or not sql or not pat.search(sql):
            continue
        m = re.search(r"\bAS\b\s*(.+)$", sql, re.S | re.I)
        if not m:
            continue
        body = pat.sub(f'"{new}"', m.group(1).strip())
        conn.execute(f"DROP VIEW {_importer_qi(name)}")
        conn.execute(f"CREATE VIEW {_importer_qi(name)} AS {body}")
        fixed += 1
    return fixed


def _rename_object(conn, path: Path, old: str, new: str) -> None:
    """実体の名前を付け替える。表は ALTER、ビューは作り直し。

    SQLite はビューを ALTER できない（view X may not be altered）ので、
    定義を読み直して DROP → CREATE する。ビューは実体を持たないため、
    これで中身は失われない。
    """
    row = conn.execute("SELECT type FROM sqlite_master WHERE name = ?",
                       (old,)).fetchone()
    if row and row[0] == "view":
        body = view_body(path, old)
        if not body:
            raise ImportError_(f"ビュー '{old}' の定義を読めませんでした。")
        conn.execute(f"DROP VIEW {_importer_qi(old)}")
        conn.execute(f"CREATE VIEW {_importer_qi(new)} AS {body}")
        # ALTER TABLE と違い、DROP+CREATE では他のビューの本文が直らない。
        # そのビューを参照している別のビューを、同じ接続の中で作り直す
        # （放っておくと壊れたビューが残り、次の profile_db が落ちる）。
        _fix_view_refs(conn, old, new)
    else:
        try:
            conn.execute(f"ALTER TABLE {_importer_qi(old)} RENAME TO {_importer_qi(new)}")
        except sqlite3.OperationalError as e:
            # SQLite は「壊れたビュー」が1つでもあると、まったく関係のない表の
            # 改名まで断る。そのままだと、いま触っている表とは無関係な名前が
            # 出てきて原因が分からないので、何をすればよいかまで書く
            if "error in view" in str(e):
                raise ValueError(
                    f"このDBに、定義が壊れたビューが残っているため改名できません（{e}）。"
                    "カタログの「ビュー」タブを開くと、動かないビューに印が付いています。"
                    "そのビューを直すか削除してから、もう一度やり直してください。"
                    "（このテーブルはまだ変更していません）") from e
            raise


def rename_table(path: Path, old: str, new: str) -> dict:
    """テーブルを改名し、カタログ・定期取り込み・利用者の選択を全部付け替える。

    まとまりはテーブル名の接頭辞なので、接頭辞を変えれば「まとまりの移動」になる。
    改名しても説明・関連・用語・例文・検算は失われない（削除→取り込み直しとの違い）。
    失敗したら実表とカタログを元に戻す。
    """
    new = importer.safe_name(new, table=True)
    prof = catalog.profile_db(path)
    if old not in prof["tables"]:
        raise ValueError(f"テーブル '{old}' が見つかりません。")
    if "__" not in new.strip("_"):
        raise ValueError("新しい名前は「まとまり__テーブル名」の形にしてください。")
    if new == old:
        raise ValueError("名前が変わっていません。")
    if new in prof["tables"]:
        raise ValueError(f"'{new}' は既にあります。別の名前にしてください。")

    meta_file = catalog.meta_path(path)
    meta_backup = meta_file.read_text(encoding="utf-8") if meta_file.exists() else None

    conn = sqlite3.connect(path, timeout=30)
    try:
        _rename_object(conn, path, old, new)   # 表でもビューでも通る
        conn.commit()
    finally:
        conn.close()

    try:
        # カタログはYAML全文への境界つき置換で一括更新する。表名は十分に固有なので、
        # 説明・SQL・関連の端点・ER配置キーのどこに現れても同じ置き換えでよい。
        # そのあと一度読み直して save_meta に通し、形を正規化して保存する。
        if meta_backup is not None:
            data = yaml.safe_load(_rename_in_text(meta_backup, old, new)) or {}
        else:
            data = {}

        # まとまり（接頭辞キー）は名前の一部ではないので、別に面倒を見る。
        # 旧まとまりが空になったらメモを引き継ぐか片づける（削除時と同じ考え方）。
        old_g = old.split("__", 1)[0] if "__" in old else None
        new_g = new.split("__", 1)[0]
        moved_memo = kept_memo = None
        if old_g and old_g != new_g:
            rest = [t for t in prof["tables"] if t != old
                    and t.split("__", 1)[0] == old_g]
            groups = data.get("groups") or {}
            if not rest and old_g in groups:
                if new_g not in groups:
                    groups[new_g] = groups.pop(old_g)   # まとまりごと動いた＝メモも一緒に
                    moved_memo = old_g
                else:
                    # 移動先に既にメモがある。前は旧メモを黙って捨てていたが、
                    # 書いた人にしか復元できないので残す。
                    # 表の無いまとまりとして点検に出るので、そこで判断してもらう
                    kept_memo = old_g
                if groups:
                    data["groups"] = groups
                else:
                    data.pop("groups", None)
        catalog.save_meta(path, data)

        # 定期取り込みの設定
        jobs_hit = 0
        items = jobs._read()
        for j in items:
            if j.get("db_file") == path.name and j.get("table") == old:
                j["table"] = new
                if j.get("name"):
                    j["name"] = _rename_in_text(str(j["name"]), old, new)
                jobs_hit += 1
        if jobs_hit:
            jobs._write(items)

        # 利用者ごとの「対象から外した表」
        prefs_hit = 0
        root = Path(config.USER_META_DIR)
        if root.exists():
            for pf in root.glob("*/prefs.yaml"):
                try:
                    d = yaml.safe_load(pf.read_text(encoding="utf-8")) or {}
                except Exception:
                    continue
                off = d.get("tables_off")
                if isinstance(off, list) and old in off:
                    d["tables_off"] = [new if t == old else t for t in off]
                    pf.write_text(yaml.safe_dump(d, allow_unicode=True, sort_keys=False),
                                  encoding="utf-8")
                    prefs_hit += 1
    except Exception:
        # カタログ側で失敗したら、実表とカタログを元に戻す
        conn = sqlite3.connect(path, timeout=30)
        try:
            _rename_object(conn, path, new, old)   # 巻き戻しも同じ扱い
            conn.commit()
        finally:
            conn.close()
        if meta_backup is not None:
            meta_file.write_text(meta_backup, encoding="utf-8")
        catalog.forget(path)
        raise

    catalog.forget(path)
    return {"old": old, "new": new, "jobs": jobs_hit, "prefs": prefs_hit,
            "memo_moved": moved_memo, "memo_kept": kept_memo}


def rename_group(path: Path, old_key: str, new_key: str) -> dict:
    """まとまりのキー（表名の接頭辞）を、配下の全テーブルごと改名する。"""
    # 整形（safe_name）は __ を _ に潰すので、検査は生の入力に対して行う
    if "__" in str(new_key or ""):
        raise ValueError("まとまりのキーには「__」を含められません。")
    # 代わりの名前（既定の "col"）を使わせない。使うと、記号だけの入力が
    # "col" になって次の検査を素通りし、まとまりが col に改名されてしまう
    new_key = importer.safe_name(new_key, "")
    if not new_key:
        raise ValueError("まとまりのキーを入力してください。")
    if new_key == old_key:
        raise ValueError("キーが変わっていません。")
    prof = catalog.profile_db(path)
    members = sorted(t for t in prof["tables"]
                     if t.split("__", 1)[0] == old_key and "__" in t)
    if not members:
        raise ValueError(f"まとまり '{old_key}' の表がありません。")
    # 先に衝突を全部確かめてから始める（途中で止まると半端になるため）
    views = {v["name"] for v in list_views(path)}
    for t in members:
        target = new_key + "__" + t.split("__", 1)[1]
        if target in prof["tables"]:
            raise ValueError(f"'{target}' が既にあるため、まとめて改名できません。")
        # ビューは作り直しで改名する。定義を読めないものが混ざっていたら
        # 手前で止める（1つでも落ちると、まとまりが2つに割れたまま残るため）
        if t in views and not view_body(path, t):
            raise ValueError(f"ビュー '{t}' の定義を読めないため、まとめて改名できません。")
    renamed = []
    for t in members:
        r = rename_table(path, t, new_key + "__" + t.split("__", 1)[1])
        renamed.append({"old": r["old"], "new": r["new"]})
    return {"renamed": renamed, "count": len(renamed)}


#: 画面に出すときの見出し。キーの順にそのまま並べる。
LABELS = {
    "own_tables": "テーブルと中のデータ",
    "tools": "AIに配るツール（SQLがこの表を使っているもの）",
    "tables": "テーブルの説明",
    "relationships": "関連（ER図の線）",
    "glossary": "業務用語",
    "examples": "質問とSQLの例文",
    "checks": "検算ルール",
    "er_layout": "ER図の配置",
    "groups": "まとまりのメモ",
    "jobs": "定期取り込みの設定",
    "orphan_terms": "自動では消えない用語（表名の無いSQL式）",
    "broken_views": "これを使っているビュー（消すと動かなくなります）",
    "removed": "削除したファイル",
}


def summarize(impact: dict) -> list[dict]:
    """{キー: [{db, text}]} を画面用の並びにする。空の項目は落とす。"""
    return [{"key": k, "label": LABELS.get(k, k), "items": impact[k]}
            for k in LABELS if impact.get(k)]


# ==========================================================================
# ===== AI・分析（brain.py）を読み込む
# ==========================================================================
# ここより上が「土台・データ」、ここより下が「画面」。
# その境目で brain.py を読み込む。brain の中の `import db` や
# `catalog.load_meta()` は、上で登録した別名を通ってここへ戻ってくる。
#
# 順番に意味がある。brain より先にデータ層を定義しておかないと、
# brain の読み込み中に「まだ無い名前」を見に行くことになる。
import brain  # noqa: E402,F401

# brain 側にある名前を、このファイルからも裸で使えるようにする。
# （画面のコードが llm.xxx / tools.xxx と書けるのは、brain が自分自身を
#   それらの名前で sys.modules に登録しているため）
import excel  # noqa: E402,F401
import exports  # noqa: E402,F401
import usage  # noqa: E402,F401
from custom_tools import builtin_overrides  # noqa: E402,F401


# ==========================================================================
# ===== 元 web.py（Flask ルーティング・画面）
# ==========================================================================
"""web.py — Flaskアプリ本体と全画面（元: web/ の11モジュール）。

元は以下のファイルに分かれていた。中身は変えずに1つにまとめている:
  web/filestore.py
  web/helpers.py
  web/auth_bp.py
  web/chat_bp.py
  web/catalog_bp.py
  web/import_bp.py
  web/mail_bp.py
  web/models_bp.py
  web/knowledge_bp.py
  web/table_bp.py
  web/api_bp.py
  web/__init__.py

"""

import sys as _sys





from flask import render_template_string

# 元 templates/403.html（1画面だけの部品なのでコードに内蔵）
_TPL_403 = """{% extends "base.html" %}
{% block title %}権限がありません — {{ app_title }}{% endblock %}
{% block heading %}権限がありません{% endblock %}
{% block subheading %}この画面は管理者だけが開けます。{% endblock %}

{% block body %}
<div class="content">
  <div class="card">
    <div class="alert alert--warn">
      データカタログ・データ取り込み・モデル設定・メール設定は、変更すると
      ほかの利用者にも影響するため、管理者のみが開けます。
    </div>
    <div class="card__desc mt">
      必要な場合は管理者に依頼してください。いま
      <b>{{ user.display_name or user.username }}</b>でログインしています。
    </div>
    <div class="row mt">
      <a class="btn btn--primary" href="{{ url_for('chat.index') }}">チャットに戻る</a>
    </div>
  </div>
</div>
{% endblock %}
"""

# ==========================================================================
# ===== 元 web/filestore.py
# 生成ファイル（Excel/CSV/テキスト）の一時置き場。
#
# ツールが作るのはバイト列なので、ブラウザに渡すには一度サーバ側に置いて
# ダウンロードURLを発行する必要がある。ディスクには書かない（Streamlit版と同じ方針）。
# ==========================================================================
import secrets
import threading
from collections import OrderedDict

_MAX_ITEMS = 200          # 保持する本数。古いものから捨てる
_fs_lock = threading.Lock()
_files: OrderedDict[str, dict] = OrderedDict()


def _fs_put(data: bytes, filename: str, mime: str, owner: str) -> str:
    token = secrets.token_urlsafe(16)
    with _fs_lock:
        _files[token] = {"data": data, "filename": filename, "mime": mime, "owner": owner}
        while len(_files) > _MAX_ITEMS:
            _files.popitem(last=False)
    return token


def _fs_get(token: str, owner: str) -> dict | None:
    """本人が作ったファイルだけ返す（URLを推測されても他人のものは渡さない）。"""
    with _fs_lock:
        item = _files.get(token)
    if item is None or item["owner"] != owner:
        return None
    return item


# ==========================================================================
# ===== 元 web/helpers.py
# 画面まわりの共通処理: ログイン状態・スコープ・描画用の変換。
# ==========================================================================
import functools
import json
import re
from pathlib import Path

from flask import g, jsonify, redirect, render_template, request, session, url_for

import auth
import catalog
import config
import db

_USER_KEY = "user"


# --- ログイン -----------------------------------------------------------------

def load_user_into_context():
    """毎リクエストの冒頭でログイン中のユーザーを復元する。"""
    data = session.get(_USER_KEY)
    g.user = auth.User(**data) if data else None


def login_user(user: auth.User) -> None:
    session[_USER_KEY] = {"username": user.username, "display_name": user.display_name,
                          "groups": list(user.groups), "is_admin": user.is_admin}
    session.permanent = False


def logout_user() -> None:
    session.clear()


def login_required(view):
    @functools.wraps(view)
    def wrapped(*a, **kw):
        if g.get("user") is None:
            if request.path.startswith("/api/"):
                return jsonify({"error": "ログインしてください。"}), 401
            return redirect(url_for("auth.login", next=request.path))
        return view(*a, **kw)
    return wrapped


def admin_required(view):
    """管理者だけが通れる。ログインしていなければログイン画面へ。

    データカタログ・データ取り込み・メール設定は、間違えると全員に影響が出る
    （AIの回答の土台、DBの中身、送信先）ので、閲覧も含めて管理者に限る。
    画面側でメニューを隠すだけでは、URLを直に叩かれると素通りしてしまう。
    """
    @functools.wraps(view)
    def wrapped(*a, **kw):
        user = g.get("user")
        if user is None:
            if request.path.startswith("/api/"):
                return jsonify({"error": "ログインしてください。"}), 401
            return redirect(url_for("auth.login", next=request.path))
        if not user.is_admin:
            if request.path.startswith("/api/"):
                return jsonify({"error": "この操作は管理者のみです。"}), 403
            return render_template_string(_TPL_403), 403
        return view(*a, **kw)
    return wrapped


def _body() -> dict:
    """POSTのJSON本文を辞書として受け取る。

    本文がJSONとして読めなければ Flask が先に400を返す。ただし
    "文字列" や [] のような「JSONではあるが辞書ではない」本文は素通りするので、
    そのまま .get を呼ぶと AttributeError になり、英語の500ページが出る。
    ここで空の辞書に均して、以降は「入っていない」と同じ扱いにする。
    """
    b = request.json
    return b if isinstance(b, dict) else {}


def inject_globals() -> dict:
    """全テンプレートで使う値。"""
    return {"user": g.get("user"), "app_title": config.APP_TITLE,
            "nav": request.endpoint or ""}


# --- 分析スコープ（どのDBのどのテーブルを見るか） --------------------------------

def db_files() -> list[Path]:
    return db.list_db_files()


def build_scope(selection: dict) -> list[dict]:
    """{DBファイル名: [テーブル名, ...]} から scope を組み立てる。

    scope は tools/llm がそのまま受け取る形式。
    """
    files = {f.name: f for f in db_files()}
    chosen = [files[n] for n in selection if n in files]
    aliases = db.aliases_for(chosen)
    scope = []
    for f, alias in zip(chosen, aliases):
        prof = catalog.profile_db(f)
        available = list(prof["tables"].keys())
        want = [t for t in (selection.get(f.name) or available) if t in available]
        scope.append({"path": str(f), "alias": alias, "name": f.name,
                      "tables": want or available, "meta": catalog.load_meta(f)})
    return scope


def dbs_in_sql(sql: str, scope: list[dict]) -> list[dict]:
    """SQLが名前を挙げているDBを、SQLに出てくる順で返す。

    例文の保存先を決めるのに使う。例文はDBごとのファイルに残すので、
    複数のDBを選んでいても「このSQLはどのDBのものか」を決める必要がある。
    DBをまたぐSQLでは、主となるFROM句のDB（最初に出てくるもの）が先頭に来る。
    """
    def first_hit(pattern: str) -> int | None:
        m = re.search(pattern, sql, re.IGNORECASE)
        return m.start() if m else None

    # まずは「エイリアス.テーブル」の形で探す
    found = []
    for s in scope:
        alias = s.get("alias") or ""
        pos = first_hit(r'(?<![\w."])' + re.escape(alias) + r'\s*\.') if alias else None
        if pos is not None:
            found.append((pos, s))
    if found:
        found.sort(key=lambda t: t[0])
        return [s for _, s in found]

    # 修飾されていないSQL（DBを1つしか選んでいないときにAIが書く形）。
    # テーブル名で当てにいく。列名と紛れることがあるので、あくまで最後の手段。
    hits = []
    for s in scope:
        for t in (s.get("tables") or []):
            pos = first_hit(r'(?<![\w."])' + re.escape(t) + r'(?![\w"])')
            if pos is not None:
                hits.append((pos, s))
                break
    hits.sort(key=lambda t: t[0])
    out = []
    for _, s in hits:
        if s not in out:
            out.append(s)
    return out


def tables_in_sql(sql: str, scope: list[dict], limit: int = 6) -> list[dict]:
    """SQLが触れているテーブルを {db, table} で返す。

    チャットからデータカタログの該当テーブルへ飛ぶリンクを作るのに使う。
    「この列が何なのか分からない」とAIが言ったときに、その場で説明を
    書きに行けるようにするためのもの。
    """
    flat = str(sql or "").replace('"', "")       # "orders" のような引用符を外して見る
    out, seen = [], set()
    for s in scope:
        alias = str(s.get("alias") or "")
        for t in (s.get("tables") or []):
            name = str(t)
            qualified = (alias and re.search(
                r'(?<![\w.])' + re.escape(alias) + r'\s*\.\s*' + re.escape(name) + r'(?![\w])',
                flat, re.IGNORECASE))
            bare = re.search(r'(?<![\w.])' + re.escape(name) + r'(?![\w])',
                             flat, re.IGNORECASE)
            if not (qualified or bare):
                continue
            key = (s.get("name"), name)
            if key not in seen:
                seen.add(key)
                out.append({"db": s.get("name"), "table": name})
    return out[:limit]

#: 最初の画面に出す例文の上限。多すぎると選べない。
_EXAMPLE_LIMIT = 6


def scope_starters(scope: list[dict]) -> dict:
    """まだ何も話していない画面に出す「取っ掛かり」。

    例文はカタログ（各DBの .meta.yaml の examples）から取る。固定の例文を
    持たないのは、DB構成が変われば必ず嘘になるため。チャットの
    「この質問とSQLを例文として保存」で貯まるので、使うほど増えていく。

    未登録のDBでは代わりに選択中のテーブル名を出す。空のままだと
    「何を聞けるのか」の手がかりが無くなるため。
    """
    examples, tables = [], []
    for s in scope:
        for ex in (s.get("meta", {}).get("examples") or []):
            q = str(ex.get("q") or "").strip()
            if q and q not in examples:
                examples.append(q)
        tables.extend(s.get("tables") or [])
    return {"examples": examples[:_EXAMPLE_LIMIT], "tables": tables[:12]}


# --- 描画用アイテムの変換 --------------------------------------------------------

def jsonable(value):
    """JSONに載らない値（bytes / datetime など）を落として文字列にする。"""
    if isinstance(value, (bytes, bytearray)):
        return f"<{len(value)} bytes>"
    if isinstance(value, dict):
        return {str(k): jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [jsonable(v) for v in value]
    if isinstance(value, float):
        # NaN / inf は JSON に無い（Excel の空セルは pandas で NaN になる）。
        # そのまま dumps すると "NaN" という不正なJSONになり、ブラウザ側で読めない。
        return None if (value != value or value in (float("inf"), float("-inf"))) else value
    if value is None or isinstance(value, (str, int, bool)):
        return value
    return str(value)


def render_item_for_web(item: dict) -> dict:
    """tools.dispatch が返す描画アイテムを、ブラウザに渡せる形へ。

    - グラフは plotly の JSON にしてクライアントで描く
    - ファイルは中身をサーバ側に預け、ダウンロードURLだけ渡す
    """
    import charts

    kind = item.get("kind")
    out = {k: jsonable(v) for k, v in item.items() if k not in ("data", "sheets")}

    if kind in ("chart", "chart_dual"):
        try:
            fig = (charts.build_dual_figure(item) if kind == "chart_dual"
                   else charts.build_figure(item))
            out["figure"] = json.loads(fig.to_json())
            out["kind"] = "chart"
        except Exception as e:
            out["kind"] = "error"
            out["message"] = f"グラフを描けませんでした: {e}"
    elif kind == "report_doc":
        # 節ごとのグラフはここで figure に変換する（画面はそのまま描くだけ）
        out["sections"] = []
        for s in item.get("sections") or []:
            sec = {k: v for k, v in s.items() if k != "chart"}
            if s.get("chart"):
                try:
                    fig = charts.build_figure(s["chart"])
                    sec["figure"] = json.loads(fig.to_json())
                except Exception as e:
                    sec["chart_error"] = f"グラフを描けませんでした: {e}"
            out["sections"].append(jsonable(sec))
    elif kind == "file":
        sheets = item.get("sheets") or []
        out["sheets"] = [{"name": s.get("name"), "columns": jsonable(s.get("columns")),
                          "rows": jsonable((s.get("rows") or [])[:20]),
                          "total": len(s.get("rows") or [])} for s in sheets]
    return out


# ==========================================================================
# ===== 元 web/auth_bp.py
# ログイン / ログアウト。認証の中身は auth.py のプロバイダに任せる。
# ==========================================================================
from flask import Blueprint, flash, g, redirect, render_template, request, url_for

import auth


bp_auth = Blueprint("auth", __name__)


@bp_auth.route("/login", methods=["GET", "POST"])
def login():
    if g.get("user") is not None:
        return redirect(url_for("chat.index"))

    setup_needed = False
    try:
        provider = auth.get_provider()
        # 常設の管理者で入れるなら、ユーザー未登録でも詰まらない
        if (provider.name == "local" and not auth.admin_enabled()
                and not (auth.load_users_file().get("users") or [])):
            setup_needed = True
    except auth.AuthError as e:
        return render_template("login.html", fatal=str(e))

    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""
        if not username or not password:
            flash("ユーザー名とパスワードを入力してください。", "warning")
        else:
            try:
                user = auth.authenticate(username, password)
            except auth.AuthError as e:
                flash(f"認証できませんでした: {e}", "error")
            else:
                if user is None:
                    flash("ユーザー名またはパスワードが違います。", "error")
                else:
                    login_user(user)
                    nxt = request.args.get("next") or url_for("chat.index")
                    return redirect(nxt if nxt.startswith("/") else url_for("chat.index"))

    return render_template("login.html", setup_needed=setup_needed)


@bp_auth.post("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


# ==========================================================================
# ===== 元 web/chat_bp.py
# チャット画面とエージェントループ。
#
# Streamlit 版との違いは状態の置き場所だけで、流れは同じ。
#   質問 → LLM → tool_calls があれば実行 → 結果を返して再度LLM → 最終回答
#
# 会話の実体は chats.py（ユーザーごとのファイル）に置く。
# 使うモデルの選択は prefs.py に置く（ログアウトしても残す）。
# 対象データはユーザーが選ばず、質問ごとに _auto_scope が決める。
# セッションに持つのは「いまどの会話を開いているか」だけ。
# ==========================================================================
import json
from pathlib import Path

from flask import (Blueprint, Response, g, jsonify, render_template, request,
                   session, stream_with_context)

import catalog
import catalog_history
import chats
import config
import custom_tools
import db
import jobs
import llm
import mailer
import models
import rag
import results
import tools
import verify


bp_chat = Blueprint("chat", __name__)

TOOL_LABELS = {
    "run_sql_query": "SQL実行 (SELECT)",
    "search_knowledge_base": "社内文書の検索",
    "plot_chart": "グラフ描画",
    "plot_dual_axis": "2軸グラフ描画 (棒+折れ線)",
    "plot_comparison": "グラフ描画（比較）",
    "plot_trend": "グラフ描画（推移）",
    "plot_composition": "グラフ描画（構成）",
    "plot_distribution": "グラフ描画（分布）",
    "plot_relationship": "グラフ描画（関係）",
    "plot_kpi": "グラフ描画（指標）",
    "pivot_table": "クロス集計",
    "analyze_stats": "統計分析",
    "export_excel": "Excel作成",
    "export_csv": "CSV作成",
    "export_text": "テキスト作成",
    "export_pptx": "PowerPoint作成",
    "export_docx": "Word作成",
    "build_report": "レポート作成",
    "compare_periods": "期間の比較",
    "data_quality": "データ品質チェック",
    "detect_anomalies": "異常検知",
    "funnel_analysis": "ファネル分析",
    "cohort_analysis": "コホート分析",
    "market_basket": "併売分析",
    "survival_analysis": "生存時間分析",
    "explore_import_files": "取り込み元ファイルの調査",
    "describe_table": "テーブル詳細の確認",
    "show_er_diagram": "ER図の表示",
    "open_table": "テーブル全体を開く",
    "hypothesis_test": "仮説検定",
    "regression": "回帰分析",
    "distribution_analysis": "分布の分析",
    "forecast": "予測",
    "timeseries_analysis": "時系列分析",
    "monte_carlo_simulation": "モンテカルロ・シミュレーション",
    "scenario_analysis": "シナリオ分析",
    "bootstrap_estimate": "信頼区間の推定",
    "clustering": "クラスタ分析",
    "abc_analysis": "ABC分析",
    "find_mail_recipients": "宛先の検索",
    "compose_email": "メールの下書き",
    "analyze_usage": "利用状況の分析",
    "propose_glossary_term": "用語登録の提案",
    "propose_example": "例文登録の提案",
}


# =============================================================================
# 画面
# =============================================================================

def table_groups_for(tables: list[dict], groups_meta: dict | None = None) -> tuple[list[dict], bool]:
    """表を「元DB名__表名」の接頭辞でまとめる（サイドバーとカタログ共用）。

    戻り値は (groups, grouped)。grouped=False のときは束ねる意味がない
    （規約に沿う表が2グループ未満）ので、呼び出し側はフラット表示にする。
    見出しは接頭辞そのもの、メモは meta の groups（db_groups の戻り）から引く。
    表は名前順に並んでいる前提で、接頭辞の変わり目で束ねるだけ。
    """
    gmeta = groups_meta or {}
    groups: list[dict] = []
    for t in tables:
        gkey = t["name"].split("__", 1)[0] if "__" in t["name"] else None
        if groups and groups[-1]["key"] == gkey:
            groups[-1]["tables"].append(t)
        else:
            info = gmeta.get(gkey) or {}
            groups.append({"key": gkey,
                           "memo": info.get("description") or "",
                           "tables": [t]})
    grouped = len([g for g in groups if g["key"]]) >= 2
    return groups, grouped


@bp_chat.get("/", endpoint="index")
@login_required
def chat_index():
    # このアプリはDBを常に1つだけ持つ。サイドバーに出すのは
    # 「どんなデータ（テーブル）があるか」だけで、DBという概念は見せない。
    files = db.list_db_files()
    data = None
    if files:
        f = files[0]
        meta = catalog.load_meta(f)
        prof = catalog.profile_db(f)
        tmeta = meta.get("tables") or {}
        # 名前にマウスを乗せたときに出す説明。カタログに書いた内容が
        # そのままAIの理解になるので、見る側にも同じ説明が見えている方がよい。
        off = set(rag.excluded_tables(g.user))
        tables = [{"name": t,
                   "description": (tmeta.get(t) or {}).get("description") or "",
                   "rows": info.get("row_count"),
                   "columns": len(info.get("columns") or []),
                   "on": t not in off}
                  for t, info in prof["tables"].items()]
        # 設定どおりに更新できていない定期取り込み → テーブル名に警告マーク
        problems = jobs.problems_by_table()
        marks = []
        for t in tables:
            ps = problems.get((f.name, t["name"]))
            if ps:
                t["problem"] = "／".join(p["message"] for p in ps)
                marks.append(t["name"])
        groups, grouped = table_groups_for(tables, catalog.db_groups(meta))
        data = {"db": f.name,
                "groups": groups, "grouped": grouped, "total": len(tables),
                "on_count": sum(1 for t in tables if t["on"]),
                "problem": (f"定期取り込みが設定どおりに動いていません: {'、'.join(marks)}"
                            if marks else "")}
    return render_template(
        "chat.html",
        data=data,
        knowledge=knowledge_prefs_payload(),
        chat_id=session.get("chat_id"),
        history=chats.list_chats(g.user),
        starters=scope_starters(build_scope({f.name: [] for f in db.list_db_files()})),
        llm_ready=llm.is_configured(),
        placeholder=config.APP_INPUT_PLACEHOLDER,
        auto_download=config.AUTO_DOWNLOAD,
    )


# =============================================================================
# モデルの選択と画像
# =============================================================================

@bp_chat.get("/api/models")
@login_required
def list_models():
    return jsonify(models.status(g.user,
                                 refresh=request.args.get("refresh") == "1"))


@bp_chat.post("/api/models")
@login_required
def choose_model():
    try:
        models.choose(g.user, _body().get("model", ""))
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    return jsonify({"ok": True, **models.status(g.user)})


@bp_chat.post("/api/chat/image")
@login_required
def upload_image():
    """画像を1枚受け取り、送信待ちとして預かる。

    ここではLLMに送らない。実際に送るのは、その画像を付けて質問したとき。
    """
    f = request.files.get("file")
    if f is None:
        return jsonify({"error": "画像が選ばれていません。"}), 400
    if not models.is_vision(models.current(g.user)):
        return jsonify({"error": "いま選ばれているモデルは画像を扱えません。"
                                 "画像に対応したモデルに切り替えてください。"}), 400
    mime = (f.mimetype or "").lower()
    if mime not in llm.IMAGE_MIMES:
        return jsonify({"error": f"この形式は送れません（{mime or '不明'}）。"
                                 "PNG / JPEG / GIF / WebP を使ってください。"}), 400
    data = f.read()
    limit = int(config.IMAGE_MAX_MB * 1024 * 1024)
    if len(data) > limit:
        return jsonify({"error": f"画像が大きすぎます（{len(data) / 1024 / 1024:.1f}MB）。"
                                 f"{config.IMAGE_MAX_MB:.0f}MB以下にしてください。"}), 400
    if not data:
        return jsonify({"error": "中身が空の画像です。"}), 400

    token = _fs_put(data, f.filename or "image.png", mime, g.user.username)
    return jsonify({"ok": True, "token": token, "filename": f.filename or "image.png",
                    "mime": mime, "size": len(data),
                    "url": f"/api/file/{token}"})


def _images_from(tokens: list) -> tuple[list, list]:
    """預かった画像を、LLMに渡せる形（base64）にする。

    戻り値は (LLM用, 画面表示用)。
    """
    import base64
    send, show = [], []
    for t in (tokens or [])[: config.IMAGE_MAX_COUNT]:
        item = _fs_get(str(t), g.user.username)
        if item is None:
            continue
        send.append({"mime": item["mime"],
                     "b64": base64.b64encode(item["data"]).decode("ascii")})
        show.append({"filename": item["filename"], "mime": item["mime"],
                     "size": len(item["data"]), "url": f"/api/file/{t}"})
    return send, show


# =============================================================================
# 会話の読み書き
# =============================================================================

def _hold_chat(cid) -> None:
    """この会話を、いまの要求が終わるまで自分のものにする。

    読んでから書き戻すまでの間に、同じ会話への別の送信が割り込むと、
    片方のやり取りがまるごと消える。ここで待たせて順番にする。
    離すのは _release_chat（要求の終わりに必ず呼ばれる）。

    待ちきれないときは止めずに進む。ここで断ると、鍵が何かの拍子に
    返らなくなったときに、その会話が二度と使えなくなるため。
    """
    if not cid or getattr(g, "_chat_lock", None) is not None:
        return
    lk = chats.lock_for(g.user, cid)
    if lk.acquire(timeout=config.CHAT_LOCK_WAIT_SEC):
        g._chat_lock = lk
    else:
        print(f"[chat] 会話 {cid} の順番待ちが "
              f"{config.CHAT_LOCK_WAIT_SEC}秒を超えました。そのまま続けます。")


def _release_chat(_exc=None) -> None:
    """要求の終わりに、会話の鍵を返す。"""
    lk = getattr(g, "_chat_lock", None)
    if lk is not None:
        g._chat_lock = None
        try:
            lk.release()
        except RuntimeError:
            pass


def _load_current() -> dict:
    """いま開いている会話。無ければ新規の空会話。

    読んだ時点でこの会話の鍵を取る。書き戻すまで他の送信を待たせるため。
    """
    cid = session.get("chat_id")
    if cid:
        _hold_chat(cid)
        chat = chats.load_chat(g.user, cid)
        if chat:
            return chat
    return {"id": None, "title": "", "created_at": "", "messages": [], "render_log": []}


def _persist(chat: dict) -> dict:
    # 新しい会話は、何か話すまでファイルを作らない。
    # 既にある会話は空になっても保存する（巻き戻しで全部消したときに、
    # 保存済みの古いやり取りが復活してしまうため）。
    if not chat["render_log"] and not chat.get("id"):
        return chat
    if not chat.get("id"):
        chat["id"] = chats.new_id()
        # 新しい会話はここで初めてIDが決まる。以後の書き戻しも直列にする
        _hold_chat(chat["id"])
    # db_names は「この会話で実際にSQLが触ったDB」。開いて続きを聞いたときに
    # 同じDBをスコープへ残すために使う（_auto_scope 参照）。
    used = set(chat.get("db_names") or [])
    for i in chat["render_log"]:
        if i.get("kind") == "sql" and i.get("sql"):
            used |= set(db.dbs_named_in(str(i["sql"])))
    chat["db_names"] = sorted(used)
    # 使った「表」も覚える（"DBファイル名.テーブル名"）。表ルーターで絞るとき、
    # この会話が実際に触った表は選から漏れても残すため（db_names の表版）。
    tabs = set(chat.get("table_names") or [])
    sqls = [str(i["sql"]) for i in chat["render_log"]
            if i.get("kind") == "sql" and i.get("sql")]
    if sqls:
        for name in chat["db_names"]:
            try:
                prof = catalog.profile_db(db.path_for(name))
            except Exception:              # DBが消えた等。表の記録はあきらめてよい
                continue
            for t in prof["tables"].keys():
                pat = r"(?<!\w)" + re.escape(t) + r"(?!\w)"
                if any(re.search(pat, s, re.IGNORECASE) for s in sqls):
                    tabs.add(f"{name}.{t}")
    chat["table_names"] = sorted(tabs)
    saved = chats.save_chat(
        g.user, chat["id"], chat["messages"], chat["render_log"],
        db_names=chat["db_names"], tables={},
        table_names=chat.get("table_names") or [],
        title=chat.get("title") or "", created_at=chat.get("created_at") or "")
    session["chat_id"] = chat["id"]
    chat["title"], chat["created_at"] = saved["title"], saved["created_at"]
    return chat


def _count_turns(render_log: list[dict]) -> int:
    """ユーザーの発言が何回あったか。"""
    return sum(1 for i in render_log
               if i.get("role") == "user" and i.get("kind") == "text")


def _split_at_turn(chat: dict, turn: int) -> tuple[list, list, str]:
    """指定の発言の直前までを切り出す。

    画面(render_log)とLLMの会話(messages)は別物なので、
    「何回目のユーザー発言か」を共通の目盛りにして両方を同じ位置で切る。
    戻り値は (切り詰めた messages, 切り詰めた render_log, もとの発言内容)。
    """
    seen, cut_log, original = 0, None, ""
    for i, item in enumerate(chat.get("render_log") or []):
        if item.get("role") == "user" and item.get("kind") == "text":
            if seen == turn:
                cut_log, original = i, item.get("content", "")
                break
            seen += 1
    if cut_log is None:
        raise ValueError(f"{turn + 1}番目の発言が見つかりません。")

    seen, cut_msg = 0, None
    for i, m in enumerate(chat.get("messages") or []):
        if m.get("role") == "user":
            if seen == turn:
                cut_msg = i
                break
            seen += 1
    if cut_msg is None:
        raise ValueError(f"{turn + 1}番目の発言が会話履歴にありません。")
    return chat["messages"][:cut_msg], chat["render_log"][:cut_log], original


def _web_log(render_log: list[dict], start: int = 0) -> list[dict]:
    """保存形式 → ブラウザ表示用。ファイルはダウンロードURLに差し替える。

    ユーザーの発言には通し番号(turn)を振る。巻き戻しのとき、
    画面のどの吹き出しが messages の何番目に当たるかを、これで対応付ける。
    """
    out = []
    turn = _count_turns(render_log[:start])
    for item in render_log[start:]:
        w = render_item_for_web(item)
        if item.get("role") == "user" and item.get("kind") == "text":
            w["turn"] = turn
            turn += 1
        # 中身(bytes)を持つアイテムは、種類を問わずダウンロードURLに置き換える
        if item.get("data"):
            token = _fs_put(item["data"], item.get("filename", "download"),
                                  item.get("mime", "application/octet-stream"),
                                  g.user.username)
            w["url"] = f"/api/file/{token}"
        if item.get("kind") == "sql":
            w["label"] = TOOL_LABELS.get(item.get("tool"), item.get("tool"))
        out.append(w)
    return out


@bp_chat.get("/api/history", endpoint="history")
@login_required
def chat_history():
    return jsonify({"chats": [{**c, "label": chats.label(c)} for c in chats.list_chats(g.user)],
                    "current": session.get("chat_id")})


@bp_chat.post("/api/chat/open")
@login_required
def open_chat():
    cid = _body().get("id")
    if not cid:
        session.pop("chat_id", None)
        return jsonify({"ok": True, "items": []})
    chat = chats.load_chat(g.user, cid)
    if chat is None:
        return jsonify({"error": "この会話は見つかりませんでした。"}), 404
    session["chat_id"] = cid
    return jsonify({"ok": True, "items": _web_log(chat.get("render_log") or []),
                    "title": chat.get("title", "")})


@bp_chat.post("/api/chat/delete", endpoint="delete_chat")
@login_required
def _w_delete_chat():
    cid = _body().get("id")
    # 自分のフォルダの中しか見ないので、他人のIDを送っても他人のものは消えない。
    # そのとき deleted は false で返る（「消した」と言わない）
    deleted = chats.delete_chat(g.user, cid)
    if session.get("chat_id") == cid:
        session.pop("chat_id", None)
    return jsonify({"ok": True, "deleted": bool(deleted)})


# =============================================================================
# エージェントループ
# =============================================================================

def _msg_to_dict(m) -> dict:
    d = {"role": "assistant", "content": m.content}
    if m.tool_calls:
        d["tool_calls"] = [{"id": tc.id, "type": "function",
                            "function": {"name": tc.function.name,
                                         "arguments": tc.function.arguments}}
                           for tc in m.tool_calls]
    return d


def _extract_calls(m) -> list[dict]:
    if not m.tool_calls:
        return []
    return [{"id": tc.id, "name": tc.function.name, "arguments": tc.function.arguments}
            for tc in m.tool_calls]


def _call_previews(calls: list[dict], scope: list[dict], question: str) -> list[dict]:
    """実行『前』に見せる内容（生成SQLなど）。"""
    out = []
    for c in calls:
        try:
            args = json.loads(c["arguments"]) if c["arguments"] else {}
        except json.JSONDecodeError:
            args = {}
        custom = next((t for t in custom_tools.collect_everywhere(scope)
                       if t.get("name") == c["name"]), None)
        # 触れているテーブルを添える。画面ではカタログの該当テーブルへのリンクになり、
        # 「列の意味が分からない」と言われた場所から、そのまま説明を書きに行ける。
        if c["name"] in tools.SQL_TOOLS and "sql" in args:
            out.append({"role": "assistant", "kind": "sql", "tool": c["name"],
                        "sql": args["sql"], "purpose": args.get("purpose", ""),
                        "explanation": args.get("explanation", ""),
                        "question": question,
                        "tables": tables_in_sql(args["sql"], scope)})
        elif custom is not None:
            binds = ", ".join(f"{k}={v!r}" for k, v in args.items()) or "（引数なし）"
            sql = tools.render_sql(custom)
            out.append({"role": "assistant", "kind": "sql", "tool": c["name"],
                        "sql": sql,
                        "purpose": f"{custom.get('description', '')[:60]} / 引数: {binds}",
                        # SQLは人が登録したものなので、AIの解説ではなく登録時の説明を出す
                        "explanation": custom.get("description", ""),
                        "question": question,
                        "tables": tables_in_sql(sql, scope)})
        elif c["name"] == "describe_table":
            # db は省略できる（DBは常に1つ）。省略時に "None." と出さない
            alias, table = args.get("db"), args.get("table")
            owner = (next((s for s in scope if s.get("alias") == alias), None)
                     if alias else (scope[0] if scope else None))
            out.append({"role": "assistant", "kind": "text",
                        "content": f"🛠 テーブル詳細を確認: `{table}`",
                        "tables": ([{"db": owner["name"], "table": table}]
                                   if owner and table else [])})
    return out


class _Guard:
    """同じ呼び出しを繰り返させないための見張り。

    LLMは、直せない指摘を受けると同じ引数のまま呼び直すことがある。
    そのまま通すと上限まで同じエラーが並び、ユーザーには何も残らない。
    2回目以降は実行せずに「同じ呼び出しです」と返し、
    それでも繰り返すならその質問を打ち切る。

    見張るのは失敗だけではない。**成功した呼び出しも覚えておく。**
    繰り返しやすいモデルは、正しい結果が返っていても同じ検索を何度も呼び、
    steps の上限まで使い切って回答を書かずに終わることがある
    （実測: 同じ文書検索を10回・103秒、毎回正解を得ていたのに無回答）。
    成功も覚えておけば、2回目は実行せず「結果はもう出ている」と差し戻せる。
    """

    LIMIT = 2                     # 同じ呼び出しが何回来たら打ち切るか

    def __init__(self):
        self.failed: dict[tuple, str] = {}    # 失敗した呼び出し -> 理由
        self.done: set[tuple] = set()         # 成功した呼び出し
        self.repeats = 0

    @staticmethod
    def key(call: dict) -> tuple:
        return (call["name"], (call.get("arguments") or "").strip())

    def seen(self, call: dict) -> bool:
        """同じ引数で実行済みか（成功・失敗どちらも）。実行前の判定に使う。"""
        k = self.key(call)
        return k in self.failed or k in self.done

    def note(self, call: dict, res: dict) -> None:
        k = self.key(call)
        if res.get("ok"):
            self.done.add(k)
            return
        try:
            why = json.loads(res["llm_content"]).get("error", "")
        except (ValueError, TypeError):
            why = ""
        self.failed[k] = why or "同じ内容で失敗しました。"

    def repeated(self, call: dict) -> str:
        """2回目以降の同じ呼び出しに返す、LLM向けの差し戻し文。

        前回が成功だったのか失敗だったのかで、言うべきことが違う。
        成功していたなら、直す必要はなく「もう答えを書ける」と伝える。
        """
        self.repeats += 1
        k = self.key(call)
        if k in self.done:
            return json.dumps({
                "error": "この呼び出しは既に実行済みです。もう一度は実行しません。",
                "hint": "前回の結果はこの会話の中に残っている。それを使って、"
                        "いま利用者への回答を書くこと。"
                        "同じツールを同じ引数で呼び直してはいけない。"
                        "本当に別の情報が要るなら、引数を変えて呼ぶこと。",
            }, ensure_ascii=False)
        return json.dumps({
            "error": "同じツールを同じ引数で呼び直しています。実行しませんでした。",
            "previous_error": self.failed.get(k, ""),
            "hint": "引数を直してから呼ぶこと。直せないなら、そのツールは諦めて"
                    "別の方法（表だけで示す・SQLを見直す・ユーザーに確認する）に切り替える。"
                    "同じ呼び出しをもう一度行ってはいけない。",
        }, ensure_ascii=False)

    @property
    def stuck(self) -> bool:
        return self.repeats >= self.LIMIT

    @property
    def stop_reason(self) -> str:
        """打ち切ったときに画面へ出す文言。失敗の連鎖か、堂々巡りかで変える。"""
        return _LOOP_MESSAGE if self.done and not self.failed else _STUCK_MESSAGE


def _stop_note(reason: str) -> dict:
    return {"role": "assistant", "kind": "text", "content": reason}


def _is_admin() -> bool:
    """管理者専用ツールを渡してよい相手か。

    「データ取り込み」画面が管理者専用なので、AI経由でも同じ線を引く。
    そうしないと、画面では見られない中身がチャットからは見える、という
    抜け道ができる。
    """
    return bool(getattr(g.get("user"), "is_admin", False))


#: カタログへの書き込みを断るときの文面（チャットのカードにそのまま出る）
_CATALOG_CONTRIB_DENIED = (
    "カタログ（用語集・例文）への登録は管理者のみです。"
    "全員の回答に効く共有の設定のため、既定では管理者に限っています。"
    "登録したい内容は管理者にお伝えください。")


def _may_contribute_catalog() -> bool:
    """チャットの登録カードからカタログを書き換えてよい相手か。

    カタログは全利用者のシステムプロンプトに毎回そのまま載り、AIには
    用語の定義に「必ず従う」・用語のSQL式を「そのまま使う」と指示している。
    つまりここを開けると、権限の低い利用者が管理者を含む全員の回答を
    左右できてしまう。既定は管理者のみ、env で従来の全員可に戻せる。
    """
    return config.CATALOG_OPEN_CONTRIB or _is_admin()


def _advance(chat: dict, scope: list[dict], question: str) -> None:
    """最終回答が出るまで回す。

    実行するSQLは _call_previews で毎回チャットに出るので、
    何が走ったかは後からでも追える。
    """
    guard = _Guard()
    retried_empty = False
    for _ in range(config.MAX_AGENT_STEPS):
        try:
            defs = tools.build_tools(scope, admin=_is_admin())
            model = models.current(g.user)
            # 文脈に収まらないぶんは、古い質問から落とした控えを送る
            # （chat["messages"] 自体は削らない。削ると巻き戻しの位置がずれる）
            msg = llm.chat(llm.history_for_llm(chat["messages"], model, defs),
                           defs, model=model)
        except Exception as e:
            chat["render_log"].append({"role": "assistant", "kind": "error",
                                       "message": _friendly_llm_error(e)})
            return

        chat["messages"].append(_msg_to_dict(msg))
        if msg.content:
            chat["render_log"].append({"role": "assistant", "kind": "text",
                                       "content": msg.content})

        calls = _extract_calls(msg)
        if not calls:
            if (msg.content or "").strip():
                _note_if_cut(chat, msg)
                return                         # 最終回答
            # 本文もツール呼び出しも無い「空の最終回答」。そのまま受理すると
            # 画面には何も出ず、空のassistant発言が履歴に残って次の質問でも
            # 真似される（一度空になると、そのチャットがずっと無言になる）。
            # 履歴から取り除いて連鎖を断つ。空応答は散発的なことが多いので、
            # まずツール付きのままもう一度だけ聞き直し（ここで大抵は復帰する）、
            # それでも空ならツール無しで書き直させる。
            chat["messages"].pop()
            if not retried_empty:
                retried_empty = True
                continue
            if _append_final_answer(chat) is None:
                chat["render_log"].append(_stop_note(_EMPTY_MESSAGE))
            return

        fresh = [c for c in calls if not guard.seen(c)]
        chat["render_log"].extend(_call_previews(fresh, scope, question))
        _execute(chat, calls, scope, guard)
        if guard.stuck:
            _append_final_answer(chat)
            chat["render_log"].append(_stop_note(guard.stop_reason))
            return

    _append_final_answer(chat)
    chat["render_log"].append(_stop_note(_LIMIT_MESSAGE))


_STUCK_MESSAGE = ("（同じ操作の失敗が続いたため、ここで止めました。"
                  "上のエラーに出ている列名や条件を指定し直すか、"
                  "質問を「まず集計だけ」「次にグラフ」のように分けて試してください。）")

_LOOP_MESSAGE = ("（同じ調べ物を繰り返していたため、ここで止めました。"
                 "必要なデータは上に出ています。）")

_LIMIT_MESSAGE = (f"（ツールの呼び出しが{config.MAX_AGENT_STEPS}回に達したので、"
                  "ここで一区切りにしました。続きが必要なら、"
                  "「続けて」と送るか、質問を分けてください。）")

def _friendly_llm_error(e: Exception) -> str:
    """LLM呼び出しの失敗を、利用者向けの言葉に整える。

    生の例外文をそのまま出すと、プロバイダのエラーJSONやGPUのメモリ事情まで
    画面に並び、利用者は自分のせいだと感じるか、意味が分からず不安になるだけ。
    よくある原因は言い換え、それ以外も詳細は短く切り詰めて添える。
    """
    s = str(e)
    low = s.lower()
    if "error parsing tool call" in low:
        return ("モデルの応答が途中で乱れたため、処理を続けられませんでした。"
                "もう一度送ってください（ローカルのモデルではまれに起きます）。")
    if "out of memory" in low or "cudamalloc" in low:
        return ("ローカルLLMのメモリが足りず、応答を作れませんでした。"
                "少し待ってからもう一度送ってください。")
    if "timed out" in low or "timeout" in low:
        return ("モデルの応答が時間内に返りませんでした。"
                "もう一度送るか、質問を短く分けてください。")
    return f"LLM呼び出しに失敗しました: {s[:160]}"


_EMPTY_MESSAGE = ("（モデルから空の応答が返り、書き直しもできませんでした。"
                  "もう一度送ってみてください。繰り返すようなら、"
                  "新規チャットで質問し直してください。）")

_CUT_MESSAGE = ("（回答がモデルの出力上限で途中まででした。"
                "「続けて」と送ると続きを書きます。）")


def _note_if_cut(chat: dict, msg) -> dict | None:
    """出力が上限で切れていたら、その旨の注意書きを積んで返す。

    どのモデルにも出力上限はあり、達すると本文が文の途中で終わる。
    黙って出すと「完結した回答」に見えてしまうので、切れたことを画面に残す。
    """
    if getattr(msg, "finish_reason", None) != "length":
        return None
    item = _stop_note(_CUT_MESSAGE)
    chat["render_log"].append(item)
    return item


def _append_final_answer(chat: dict) -> dict | None:
    """ツールを渡さずに、最後にもう一度だけ回答を書かせる。

    打ち切りや上限で終わると、材料は揃っているのに回答が1行も無いまま
    終わることがあった（同じ検索を繰り返して steps を使い切る等）。
    ツールを渡さなければモデルは文章で答えるしかないので、
    そこまでに得た結果で締めさせる。ここで失敗しても黙って諦める
    （打ち切りの理由は、この後に別途表示される）。
    """
    try:
        msg = llm.chat(
            llm.history_for_llm(chat["messages"], models.current(g.user)) + [{
                "role": "user",
                "content": "ここまでの会話をふまえて、直前の質問に日本語で答えてください。"
                           "ツールは使えません。すでに得られた結果があれば、それだけを"
                           "根拠に簡潔に答えること。必要な情報が得られていない場合は、"
                           "憶測で埋めず「うまく処理できませんでした。もう一度質問して"
                           "ください」とだけ伝えること。内部の仕組み（ツール名・"
                           "データベースの構成・システムの状態）を説明してはいけない。",
            }], [], model=models.current(g.user))   # [] ＝ ツールを渡さない
    except Exception as e:
        print(f"[chat] 最後の回答をまとめられませんでした: {e}")
        return None
    text = (getattr(msg, "content", "") or "").strip()
    if not text:
        return None
    chat["messages"].append(_msg_to_dict(msg))
    item = {"role": "assistant", "kind": "text", "content": text}
    chat["render_log"].append(item)
    return item


def _merge_alerts(content: str, alerts: list[dict]) -> str:
    """検算の不一致をツール結果に混ぜて、LLMに気づかせる。"""
    notes = [verify.llm_note(a) for a in alerts]
    try:
        data = json.loads(content)
        if isinstance(data, dict):
            data["verification_warnings"] = notes
            return json.dumps(data, ensure_ascii=False, default=str)
    except (ValueError, TypeError):
        pass
    return content + "\n\n【検算の不一致】" + json.dumps(notes, ensure_ascii=False, default=str)


def _fresh_alerts(chat: dict, alerts: list[dict]) -> list[dict]:
    """この会話でまだ見せていない検算だけを残す。

    同じデータ・同じルールの警告を質問のたびに繰り返すと、読まれなくなる。
    データが変わる（=キーの版が変わる）と、また1回だけ出る。
    """
    seen = {i.get("verify_key") for i in chat["render_log"] if i.get("verify_key")}
    return [a for a in alerts if a["key"] not in seen]


def _execute(chat: dict, calls: list[dict], scope: list[dict],
             guard: "_Guard | None" = None) -> None:
    for c in calls:
        if guard is not None and guard.seen(c):
            # 同じ呼び出しの繰り返し。実行せずに差し戻す（時間もお金も使わない）。
            # 前回が成功でも同じ。結果はもう会話に載っているので、
            # 取り直すのではなく、それを使って回答させる。
            chat["messages"].append({"role": "tool", "tool_call_id": c["id"],
                                     "content": guard.repeated(c)})
            continue
        res = tools.dispatch(c["name"], c["arguments"], scope, scope, admin=_is_admin())
        if guard is not None:
            guard.note(c, res)

        # 相互検証。数字が食い違っていたら、回答の前に画面とLLMの両方へ
        content = res["llm_content"]
        alerts = _fresh_alerts(chat, res.get("verify_alerts") or [])
        if alerts:
            content = _merge_alerts(content, alerts)
        chat["messages"].append({"role": "tool", "tool_call_id": c["id"],
                                 "content": content})
        if res.get("render"):
            chat["render_log"].append(dict(res["render"]))
        for a in alerts:
            chat["render_log"].append(verify.render_item(a))


def _reply(chat: dict, before: int, replace: bool = False):
    _persist(chat)
    return jsonify({
        "ok": True,
        # replace=True のときは画面をいったん空にして全部描き直してもらう
        "items": _web_log(chat["render_log"], 0 if replace else before),
        "replace": replace,
        "chat_id": chat.get("id"),
        "title": chat.get("title", ""),
    })


class _TurnError(Exception):
    """送信を始められないときの理由。画面にそのまま出せる文言を持つ。"""

    def __init__(self, message: str, status: int = 400, **extra):
        super().__init__(message)
        self.payload = {"error": message, **extra}
        self.status = status


@bp_chat.errorhandler(_TurnError)
def _turn_error(e: _TurnError):
    return jsonify(e.payload), e.status


def _auto_scope(question: str, chat: dict) -> list[dict]:
    """質問に合わせてAIへ渡すカタログの範囲を決める。利用者は何も選ばない。

    決め方は config.SCOPE_MODE:
      auto   … カタログ全体が「選択中モデルの読める量」に収まるならそのまま直載せ
               （ルーター省略＝選び漏れゼロ・プロンプトが毎回同一でキャッシュ最大）。
               収まらないときだけ表ルーターで絞り、詳細を保つ（既定）。
      router … 常に表ルーターで絞る。
      all    … 常に全部（収まらなければ要約モードに落ちる。旧来の挙動）。

    表で絞るときは、この会話で実際にSQLが触った表を残し続ける（「それをグラフに」の
    ような続き質問はルーターに手がかりが無いため）。判定できないときは絞らない＝
    要約モードに任せる。ルーターの不調で答えられなくなるのがいちばん悪い。

    サイドバーで利用者が外した表は、この一番外側で落とす。以降の判断
    （収まるか・ルーターに何を見せるか）を、外した後の姿で行うため。
    """
    scope = build_scope({f.name: [] for f in db.list_db_files()})
    off = set(rag.excluded_tables(g.user))
    if off:
        for s_ in scope:
            s_["tables"] = [t for t in s_["tables"] if t not in off]
        scope = [s_ for s_ in scope if s_["tables"]]
    if not scope:
        return scope
    if config.SCOPE_MODE == "all":
        return scope
    limit = models.inline_limit_for(models.current(g.user))
    if config.SCOPE_MODE == "auto" and catalog.inline_length(scope) <= limit:
        return scope                       # 全部入りで選び漏れゼロ
    chat_history = [i.get("content") or "" for i in (chat.get("render_log") or [])
               if i.get("role") == "user" and i.get("kind") == "text"]
    picked = llm.route_tables(question, scope, chat_history)
    if picked:
        # この会話で実際にSQLが触った表は選から漏れても残す（続き質問のため）
        for t in (chat.get("table_names") or []):
            # 形式は "DBファイル名.テーブル名"。DBファイル名自体が .db を含むので
            # 最後のドットで割る（先頭で割ると equipment / db.stop_records になる）
            dbn, _, tn = str(t).rpartition(".")
            if dbn in {s["name"] for s in scope}:
                picked.setdefault(dbn, [])
                if tn and tn not in picked[dbn]:
                    picked[dbn] = sorted(set(picked[dbn]) | {tn})
        picked = llm.expand_tables_by_relations(picked, scope)
        for s in scope:
            sel = picked.get(s["name"])
            if sel and off:
                # ピン留め（過去にSQLが触った表）と関連の1ホップ補完は、
                # 利用者が外した表を知らない。ここで落とし直さないと、
                # 会話の続きで除外したはずの表が戻ってきてしまう
                sel = [t for t in sel if t not in off]
            if sel:
                s["tables"] = sel
    return scope


def _realtime_refresh(scope: list[dict]) -> None:
    """質問に入る前に、リアルタイム更新のテーブルを元ファイルに追随させる。

    取り込み直しの成否は履歴（kind=realtime）に残る。ここで失敗しても質問は
    止めない（読めなければ前回取り込んだ内容で答える、が決めごとのため）。
    """
    try:
        for r in jobs.refresh_realtime(scope):
            mark = "OK" if r.get("ok") else "NG"
            print(f"[realtime] {mark} {r.get('db_file')}/{r.get('table')}: "
                  f"{r.get('message')}")
    except Exception as e:
        print(f"[realtime] 更新の確認でエラー（回答は続行）: {e}")


def _begin_turn():
    """/send と /stream に共通する前処理。

    質問を検証し、スコープを確定し、会話にユーザーの発言を積むところまで。
    始められないときは _TurnError を投げる（呼び出し側で分岐を書かずに済む）。
    """
    body = _body()
    text = (body.get("text") or "").strip()
    if not text:
        raise _TurnError("質問を入力してください。")
    if not llm.is_configured():
        raise _TurnError("LLMが未設定です。env の OPENAI_* を設定してください。")

    # ツールの実処理から、この利用者の検索対象と検索設定を引けるようにする。
    # dispatch は引数に利用者を持たないため、処理中のスレッドに置いて渡す。
    rag.set_current_user(g.user)
    # 同じ質問の中で同じSQLを2回実行しないための区切り。
    # ここで新しい質問だと宣言することで、前の質問の結果は使い回されなくなる
    # （データが入れ替わっていても古い数字を返す、という事故を防ぐ）。
    results.new_turn()

    chat = _load_current()

    images, show = _images_from(body.get("images"))
    if images and not models.is_vision(models.current(g.user)):
        raise _TurnError("いま選ばれているモデルは画像を扱えません。")

    # 質問は、重い処理（DBルーターのLLM呼び出し・リアルタイム取り込み）より
    # 先に保存する。保存が後ろだと、送信直後に別のチャットへ切り替えて戻った
    # とき（/api/chat/open は保存ファイルを読む）、質問がまだ無くて消えて見える。
    # ルーターはローカルLLMだと数十秒かかることがあり、その間ずっと消えたままになる。
    chat["messages"].append(llm.user_message(text, images))
    # 古い質問に付いた画像を注記へ差し替える。1枚で数MBの base64 が
    # 以後ずっと毎回送られるのを止める（画面の render_log には残る）。
    n_img = llm.drop_old_images(chat["messages"])
    if n_img:
        print(f"[chat] 古い画像 {n_img} 枚を履歴から外しました（{g.user.username}）")
    chat["render_log"].append({"role": "user", "kind": "text", "content": text,
                               "at": chats.now(),
                               **({"images": show} if show else {})})
    _persist(chat)

    scope = _auto_scope(text, chat)
    # DBが1つも無くても、ナレッジベースがあれば文書には答えられる。
    # 両方無いときだけ止める（この構成では何も調べようがないため）。
    # ※ この時点で質問は保存済みなので、ここで止まると「答えの無い質問」が
    #   1件残る。DBもKBも無い環境だけの稀な話なので、消す処理までは足さない。
    if not scope and not rag.rag_available(g.user):
        raise _TurnError("いま調べられるものがありません。"
                         "サイドバーの SQLite3 か LightRAG で、"
                         "使うものにチェックを入れてください。")
    _realtime_refresh(scope)

    # システムプロンプトはスコープが決まってから。ユーザー発言より後に組むが、
    # 置き場所は必ず先頭（index 0）なので、並び順は崩れない。
    if not chat["messages"] or chat["messages"][0].get("role") != "system":
        chat["messages"].insert(0, {"role": "system", "content": ""})
    chat["messages"][0] = {"role": "system",
                           "content": llm.build_system_prompt(
                               scope, admin=_is_admin(),
                               model=models.current(g.user))}
    return chat, scope, text


@bp_chat.post("/api/chat/send", endpoint="send")
@login_required
def _w_send():
    chat, scope, text = _begin_turn()
    before = len(chat["render_log"]) - 1
    _advance(chat, scope, text)
    return _reply(chat, before)


# =============================================================================
# ストリーミング送信
#
# 通常の /api/chat/send は、ツールを何回か呼んで最終回答が出るまで待ってから
# まとめて返す。待ち時間が長く、届いた瞬間に画面がいちばん下へ飛ぶ。
# こちらは、起きたことをその都度 Server-Sent Events で流す。
# =============================================================================

def _sse(event: str, data) -> str:
    return f"event: {event}\ndata: {json.dumps(data, ensure_ascii=False, default=str)}\n\n"


def _stream_advance(chat: dict, scope: list[dict], question: str):
    """_advance のストリーミング版。起きたことを逐次 yield する。"""
    guard = _Guard()
    retried_empty = False
    for _ in range(config.MAX_AGENT_STEPS):
        msg = None
        try:
            defs = tools.build_tools(scope, admin=_is_admin())
            model = models.current(g.user)
            for kind, payload in llm.chat_stream(
                    llm.history_for_llm(chat["messages"], model, defs),
                    defs, model=model):
                if kind == "text":
                    yield _sse("delta", {"text": payload})
                else:
                    msg = payload
        except Exception as e:
            item = {"role": "assistant", "kind": "error",
                    "message": _friendly_llm_error(e)}
            chat["render_log"].append(item)
            yield _sse("item", _web_log([item])[0])
            return
        if msg is None:
            return

        chat["messages"].append(_msg_to_dict(msg))
        if msg.content:
            chat["render_log"].append({"role": "assistant", "kind": "text",
                                       "content": msg.content})
        calls = _extract_calls(msg)
        if not calls:
            yield _sse("text_end", {})
            if (msg.content or "").strip():
                cut = _note_if_cut(chat, msg)
                if cut:
                    yield _sse("item", _web_log([cut])[0])
                return                              # 最終回答
            # 空の最終回答（_advance 側の同名ブロックと同じ扱い）
            chat["messages"].pop()
            if not retried_empty:
                retried_empty = True
                continue           # まずツール付きのまま、もう一度だけ聞き直す
            answer = _append_final_answer(chat)
            if answer:
                yield _sse("item", _web_log([answer])[0])
            else:
                item = _stop_note(_EMPTY_MESSAGE)
                chat["render_log"].append(item)
                yield _sse("item", _web_log([item])[0])
            return

        yield _sse("text_end", {})
        fresh = [c for c in calls if not guard.seen(c)]
        previews = _call_previews(fresh, scope, question)
        chat["render_log"].extend(previews)
        for p in _web_log(previews):
            yield _sse("item", p)

        for c in calls:
            if guard.seen(c):
                _execute(chat, [c], scope, guard)      # 実行せず差し戻すだけ
                continue
            yield _sse("running", {"name": c["name"],
                                   "label": TOOL_LABELS.get(c["name"], c["name"])})
            before = len(chat["render_log"])
            _execute(chat, [c], scope, guard)
            for item in _web_log(chat["render_log"], before):
                yield _sse("item", item)

        if guard.stuck:
            answer = _append_final_answer(chat)
            if answer:
                yield _sse("item", _web_log([answer])[0])
            item = _stop_note(guard.stop_reason)
            chat["render_log"].append(item)
            yield _sse("item", _web_log([item])[0])
            return

    answer = _append_final_answer(chat)
    if answer:
        yield _sse("item", _web_log([answer])[0])
    item = _stop_note(_LIMIT_MESSAGE)
    chat["render_log"].append(item)
    yield _sse("item", _web_log([item])[0])


@bp_chat.post("/api/chat/stream")
@login_required
def stream():
    """1問1答をSSEで流す。イベントの種類:

        delta     … 回答の文字（少しずつ）
        text_end  … ひとまとまりの回答が終わった
        item      … 表・グラフ・ファイルなどの描画アイテム
        running   … ツールを実行し始めた
        end       … 終わり（保存後の会話ID・タイトルを載せる）
    """
    chat, scope, text = _begin_turn()
    # 会話IDはここで確定させてセッションに入れる。
    # 応答を流し始めるとセッションに書けなくなるので、あとから入れても消える
    # （次の質問が別の会話として始まってしまう）。
    if not chat.get("id"):
        chat["id"] = chats.new_id()
        _hold_chat(chat["id"])       # 以後の書き戻しを直列にする
    session["chat_id"] = chat["id"]
    turn_id = results.current_turn()

    user = g.user

    def generate():
        # 応答を流す処理が別のスレッドで回る構成でも設定を引けるようにする
        # （_begin_turn で入れたものは、そのスレッドには無い）。
        rag.set_current_user(user)
        results.set_turn(turn_id)
        # 利用者が画面を閉じた/更新したときは、次の書き込みで GeneratorExit が飛ぶ。
        # その場合も進んだところまでは保存するが、"end" はもう送れない
        # （切断後に yield すると RuntimeError になり、ログが汚れるだけ）。
        aborted = False
        try:
            yield from _stream_advance(chat, scope, text)
        except GeneratorExit:
            aborted = True
            raise
        except Exception as e:                       # 途中で落ちても接続は閉じる
            yield _sse("item", {"role": "assistant", "kind": "error",
                                "message": _friendly_llm_error(e)})
        finally:
            _persist(chat)
            if not aborted:
                yield _sse("end", {"chat_id": chat.get("id"),
                                   "title": chat.get("title", "")})

    return Response(stream_with_context(generate()),
                    mimetype="text/event-stream",
                    headers={"Cache-Control": "no-cache",
                             "X-Accel-Buffering": "no"})   # nginx等でのバッファ抑止


@bp_chat.post("/api/chat/rewind")
@login_required
def rewind():
    """指定の発言まで巻き戻して、そこからやり直す。

    text を送ると、その発言を書き換えたうえで会話を続ける。
    text が空なら巻き戻すだけ（それ以降を消して、入力欄に戻す）。
    どちらも、その発言より後のやり取りは消える。
    """
    body = _body()
    try:
        turn = int(body.get("turn"))
    except (TypeError, ValueError):
        return jsonify({"error": "巻き戻す位置が指定されていません。"}), 400
    text = (body.get("text") or "").strip()

    # 送信（_begin_turn）と同じ下ごしらえをここでもやる。どちらも
    # 処理中のスレッドに置いて渡す仕組みなので、書き直しだけ抜けていると
    #   ・そのスレッドを直前に使った別の利用者のナレッジベース設定で検索する
    #   ・前の質問で取った結果を使い回して、取り込み直す前の古い数字を返す
    # という、間違いに気づけない事故になる。
    rag.set_current_user(g.user)
    results.new_turn()

    chat = _load_current()
    try:
        messages, render_log, original = _split_at_turn(chat, turn)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    dropped = len(chat["render_log"]) - len(render_log)
    chat["messages"], chat["render_log"] = messages, render_log

    if not text:
        _persist(chat)
        return jsonify({"ok": True, "replace": True,
                        "items": _web_log(chat["render_log"]),
                        "restored": original, "dropped": dropped,
                        "chat_id": chat.get("id"), "title": chat.get("title", "")})

    if not llm.is_configured():
        return jsonify({"error": "LLMが未設定です。env の OPENAI_* を設定してください。"}), 400
    scope = _auto_scope(text, chat)
    # 表を1つも選んでいなくても、文書（LightRAG）が選ばれていれば答えられる。
    # 送信のときと同じ規則にする（ここだけ厳しいと「書き直しだけ通らない」になる）
    if not scope and not rag.rag_available(g.user):
        return jsonify({"error": "いま調べられるものがありません。"
                                 "サイドバーの SQLite3 か LightRAG で、"
                                 "使うものにチェックを入れてください。"}), 400
    _realtime_refresh(scope)

    # やり直しなので、カタログの現状に合わせてシステムプロンプトも入れ直す
    if not chat["messages"] or chat["messages"][0].get("role") != "system":
        chat["messages"].insert(0, {"role": "system", "content": ""})
    chat["messages"][0] = {"role": "system",
                           "content": llm.build_system_prompt(
                               scope, admin=_is_admin(),
                               model=models.current(g.user))}
    chat["messages"].append({"role": "user", "content": text})
    llm.drop_old_images(chat["messages"])     # 送信と同じ扱いにする
    chat["render_log"].append({"role": "user", "kind": "text", "content": text,
                               "at": chats.now()})

    _advance(chat, scope, text)
    return _reply(chat, 0, replace=True)


# =============================================================================
# メール送信
#
# 送信はここだけ。LLMは compose_email で下書きを作るところまでしかできず、
# 実際に外へ出るのはユーザーが画面の「送信」を押したときだけにしてある。
# 宛先の間違いは取り消せないため、AIの判断だけで外部に何かを出さない。
# =============================================================================

def _attachments_for(chat: dict, names: list) -> tuple[list, list]:
    """この会話で作ったファイルから、名前が一致する添付を集める。

    'all' が指定されたら直近に作ったものを全部付ける。
    戻り値は (添付, 見つからなかった名前)。
    """
    made = [i for i in (chat.get("render_log") or [])
            if i.get("kind") == "file" and i.get("data")]
    wanted = [str(n) for n in (names or [])]
    if not wanted:
        return [], []
    if any(w.lower() == "all" for w in wanted):
        picked = made[-5:]
        return [{"filename": i.get("filename"), "mime": i.get("mime"),
                 "data": i["data"]} for i in picked], []

    out, missing = [], []
    for w in wanted:
        hit = next((i for i in reversed(made)
                    if (i.get("filename") or "").lower() == w.lower()), None)
        if hit is None:                      # 部分一致でも拾う（拡張子の付け忘れなど）
            hit = next((i for i in reversed(made)
                        if w.lower() in (i.get("filename") or "").lower()), None)
        if hit is None:
            missing.append(w)
        else:
            out.append({"filename": hit.get("filename"), "mime": hit.get("mime"),
                        "data": hit["data"]})
    return out, missing


@bp_chat.post("/api/mail/send")
@login_required
def mail_send():
    """実際に送る。押したのがユーザー本人であることが唯一の前提。"""
    body = _body()
    draft = body.get("draft") or {}
    if not body.get("confirm"):
        return jsonify({"error": "確認されていません。"}), 400
    chat = _load_current()
    files, missing = _attachments_for(chat, draft.get("attach_filenames"))
    if missing:
        return jsonify({"error": f"添付ファイルが見つかりません: {', '.join(missing)}"}), 400
    try:
        record = mailer.send(draft, files, user=g.user.username)
    except mailer.MailError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"送信に失敗しました: {e}"}), 500

    chat["render_log"].append({
        "role": "assistant", "kind": "text",
        "content": ("📤 " + record["message"]
                    + f"（件名: {record['subject']} / 宛先: {', '.join(record['to'])}"
                    + (f" / 添付: {', '.join(record['attachments'])}"
                       if record["attachments"] else "") + "）")})
    _persist(chat)
    return jsonify({"ok": True, "record": record})


@bp_chat.post("/api/mail/test")
@admin_required
def mail_test():
    """SMTPの疎通確認だけ（メールは送らない）。"""
    return jsonify(mailer.test_connection())


@bp_chat.post("/api/chat/glossary-save")
@login_required
def glossary_save():
    """チャットの登録カードから、用語をカタログの用語集へ保存する。

    AIは propose_glossary_term でカードを出すところまで。書き込みはこの
    エンドポイントだけで、カードのボタンを押したときに起こる。
    誰がいつ何を変えたかは catalog_history に必ず残す。

    既定では管理者のみ。用語集は全利用者のシステムプロンプトに載り、AIには
    「必ずその定義に従う」と指示しているため、ここを開けると権限の低い利用者が
    全員の回答を左右できる。皆で育てる運用に戻すなら CATALOG_OPEN_CONTRIB。
    """
    if not _may_contribute_catalog():
        return jsonify({"error": _CATALOG_CONTRIB_DENIED}), 403
    body = _body()
    term = (body.get("term") or "").strip()
    desc = (body.get("description") or "").strip()
    sql = (body.get("sql") or "").strip()
    table = (body.get("table") or "").strip()
    if not term or not desc:
        return jsonify({"error": "用語と説明が必要です。"}), 400
    try:
        path = db.path_for(body.get("db") or "")
    except FileNotFoundError as e:
        return jsonify({"error": str(e)}), 400

    meta = catalog.load_meta_for_edit(path)
    entry = {"description": desc, "sql": sql}
    if table:
        gl = catalog.table_glossary(meta, table)      # 既存の用語を消さずに足す
        old = gl.get(term)
        gl[term] = entry
        catalog.set_table_glossary(meta, table, gl)
    else:
        gl = catalog.db_glossary(meta)
        old = gl.get(term)
        gl[term] = entry
        meta["glossary"] = gl
    catalog.save_meta(path, meta)
    catalog_history.add_catalog_change("glossary", "update" if old else "add", path.name, term,
                        user=g.user.username, table=table or None,
                        before=old, after=entry, source="chat")
    where = table if table else "全体"
    return jsonify({"ok": True,
                    "message": f"「{term}」を {where} の用語集に"
                               f"{'上書き登録' if old else '登録'}しました。"
                               "次の質問からAIがこの定義に従います。"})


@bp_chat.post("/api/chat/save-example")
@login_required
def save_example():
    """チャットの登録カードから、例文をカタログへ保存する。

    誰がいつ何を変えたかは catalog_history に必ず残す。同じSQLの例文が既にあれば、
    質問文と説明を更新する。既定では管理者のみ（glossary_save と同じ理由。
    例文もシステムプロンプトに「正しいと確認済みの例」として載るため）。
    """
    if not _may_contribute_catalog():
        return jsonify({"error": _CATALOG_CONTRIB_DENIED}), 403
    scope = build_scope({f.name: [] for f in db.list_db_files()})
    body = _body()
    q = (body.get("question") or "").strip()
    sql = (body.get("sql") or "").strip()
    desc = (body.get("description") or "").strip()
    if not q or not sql:
        return jsonify({"error": "質問とSQLの両方が必要です。"}), 400

    # 例文はDBごとのファイルに残すので、保存先を1つに決める必要がある。
    # 複数のDBを選んでいても、SQLがどのDBを見ているかで決められる。
    # DBをまたぐ例文（人事の勤怠 × マスタの社員、など）は珍しくないため、
    # 「1つだけ選んでいるとき」に限ると保存できる場面が狭くなりすぎる。
    hits = dbs_in_sql(sql, scope)
    # 登録カード（propose_example）は置き場のDBを持っている。あればそれを使う。
    # SQLに DB名 が無い（単一DBの略記など）ときも、カードの db で決められる。
    asked = (body.get("db") or "").strip()
    target = next((s for s in scope if s["name"] == asked or s.get("alias") == asked), None) if asked else None
    if target is None:
        target = hits[0] if hits else (scope[0] if len(scope) == 1 else None)
    if target is None:
        return jsonify({"error": "このSQLがどのデータの例文か判断できませんでした。"
                                 "db を指定してください。"}), 400

    p = Path(target["path"])
    meta = catalog.load_meta_for_edit(p)
    examples = meta.get("examples") or []

    # 同じSQLが既にあれば、増やさずにその1件の質問文・説明を更新する。
    # 例文は毎回プロンプトに載るので、言い回し違いで同じSQLが並ぶと
    # トークンを食うだけで精度は上がらない。
    same = catalog.find_example(examples, sql)
    if same is not None:
        before = dict(same)
        same["q"] = q
        if desc:
            same["description"] = desc
        meta["examples"] = catalog.dedupe_examples(examples)
        catalog.save_meta(p, meta)
        catalog_history.add_catalog_change("example", "update", p.name, q,
                            user=g.user.username, before=before,
                            after={k: same.get(k) for k in ("q", "description", "sql")},
                            source="chat")
        return jsonify({"ok": True, "added": False, "updated": True,
                        "message": f"同じSQLの例文があったため、"
                                   f"質問文を「{q}」に更新しました。"})
    if len(examples) >= catalog.EXAMPLES_MAX:
        return jsonify({"error": f"例文は{catalog.EXAMPLES_MAX}件までです。"
                                 "データカタログの「質問とSQLの例文」で古いものを"
                                 "整理してください。"}), 400

    new_entry = {"q": q, "sql": sql}
    if desc:
        new_entry["description"] = desc
    meta["examples"] = catalog.dedupe_examples([*examples, new_entry])
    catalog.save_meta(p, meta)
    catalog_history.add_catalog_change("example", "add", p.name, q, user=g.user.username,
                        after=new_entry, source="chat")
    return jsonify({"ok": True, "added": True, "message": "例文に追加しました。"})


# ==========================================================================
# ===== 元 web/catalog_bp.py
# データカタログ画面。テーブル/列の説明・用語集・結合(ER)・ツールを編集する。
# ==========================================================================
import inspect
import re
from pathlib import Path

from flask import Blueprint, g, jsonify, render_template, request

import advanced
import catalog
import catalog_history
import charts
import custom_tools
import db
import jobs
import llm
import sqlusage
import tools
import verify


bp_catalog = Blueprint("catalog", __name__)


@bp_catalog.errorhandler(FileNotFoundError)
def _db_missing(e: FileNotFoundError):
    """db.path_for が見つけられなかったとき。存在しないDB名を投げられても500にしない。"""
    return jsonify({"error": str(e)}), 400


@bp_catalog.errorhandler(catalog.MetaUnreadable)
def _meta_broken(e):
    """カタログのファイルが壊れているとき。保存させると全部消えるので断る。"""
    return jsonify({"error": str(e), "meta_broken": True}), 409


def _pick(name: str | None) -> Path | None:
    files = db.list_db_files()
    if not files:
        return None
    return next((f for f in files if f.name == name), files[0])


def _builtin_view(tool: dict) -> dict:
    """組み込みツールを画面で見られる形にする。

    AIに渡しているのは JSON Schema そのものなので、説明もパラメータも
    切らずに全部見せる。「AIがこのツールをどう理解しているか」が
    そのまま分かるようにするのが目的（説明の上書きを決める材料になる）。
    """
    fn = tool["function"]
    params = fn.get("parameters") or {}
    required = set(params.get("required") or [])
    return {
        "name": fn["name"],
        "description": fn.get("description") or "",
        # SQLを受け取るツールか（実行したSQLがチャットに表示される対象）
        "is_sql": fn["name"] in tools.SQL_TOOLS,
        "params": [{"name": k,
                    "type": (v or {}).get("type") or "",
                    "required": k in required,
                    "description": (v or {}).get("description") or "",
                    # 選択肢が決まっている引数は、そのまま候補を見せる
                    "enum": (v or {}).get("enum") or []}
                   for k, v in (params.get("properties") or {}).items()],
    }


def _tool_source(name: str) -> list[dict]:
    """組み込みツールが実際に何をしているかを、コードそのもので見せる。

    チャットで生成SQLを見せているのと同じ考え方で、「AIがこのツールを呼ぶと
    データに何が起きるか」を確かめられるようにする。
    統計系のツールは共通の入れ物でくるまれているので、中の呼び出しと
    その先の実装（advanced.py）まで辿って出す。
    """
    fn = tools._HANDLERS.get(name)
    if fn is None:
        return []

    out: list[dict] = []

    def add(target, label):
        try:
            src = inspect.getsource(target)
            where = f"{Path(inspect.getsourcefile(target)).name}:{inspect.getsourcelines(target)[1]}"
        except (OSError, TypeError):
            return
        out.append({"label": label, "where": where, "code": src})

    # _analysis_tool でくるまれたものは、中の呼び出し（どの分析を呼ぶか）を出す
    inner = None
    if fn.__name__ == "run" and fn.__closure__:
        cand = fn.__closure__[0].cell_contents
        if callable(cand):
            inner = cand
    add(inner or fn, "ツールの処理")

    # くるまれていた（＝短い委譲）ときだけ、委譲先の本体も見せる。
    # ふつうの関数まで辿ると、エラー処理で AnalysisError に触れているだけで
    # 例外クラスの定義を「実際の計算」と表示してしまう。
    if out and inner is not None:
        m = re.search(r"\b(advanced|business)\.(\w+)\(", out[0]["code"])
        if m:
            target = getattr(advanced, m.group(2), None)
            if inspect.isfunction(target):
                add(target, f"実際の計算 {m.group(1)}.{m.group(2)}()")
    return out


@bp_catalog.get("/api/catalog/builtin/source")
@admin_required
def builtin_source():
    """組み込みツールのコード。開いたときだけ取りに行く（全部で65KBあるため）。"""
    name = request.args.get("name") or ""
    if name not in tools._HANDLERS:
        return jsonify({"error": f"未知のツールです: {name}"}), 404
    return jsonify({"name": name, "parts": _tool_source(name)})


def _overview(path: Path) -> dict:
    profile = catalog.profile_db(path)
    meta = catalog.load_meta(path)
    cov = catalog.coverage(profile, meta)
    return {"profile": profile, "meta": meta, "coverage": cov,
            "drift": catalog.drift_warnings(profile, meta)}


@bp_catalog.get("/catalog", endpoint="index")
@admin_required
def catalog_index():
    target = _pick(request.args.get("db"))
    if target is None:
        return render_template("catalog.html", target=None)
    ov = _overview(target)
    profile, meta = ov["profile"], ov["meta"]

    tables = []
    for tname, t in profile["tables"].items():
        tmeta = (meta.get("tables") or {}).get(tname) or {}
        mcols = tmeta.get("columns") or {}
        pk_cols, pk_src = catalog.effective_pk(profile, meta, tname)
        cols = []
        for c in t["columns"]:
            cm = mcols.get(c["name"]) or {}
            stat = (t.get("col_stats") or {}).get(c["name"]) or {}
            if "values" in stat:
                actual = ", ".join(str(v) for v in stat["values"][:12])
            elif "min" in stat:
                actual = f"{stat['min']} 〜 {stat['max']}"
            else:
                actual = ""
            cols.append({"name": c["name"], "type": c["type"], "pk": c["name"] in set(pk_cols),
                         "description": cm.get("description", ""),
                         "codes": cm.get("values") or {}, "actual": actual})
        tables.append({
            "name": tname, "rows": t.get("row_count"),
            "is_view": t.get("type") == "view",
            "description": tmeta.get("description", ""),
            "ai_draft": bool(tmeta.get("ai_draft")),
            "pk": pk_cols, "pk_src": pk_src,
            "columns": cols,
            "glossary": catalog.table_glossary(meta, tname),
            "sample_columns": t.get("sample_columns") or [],
            "sample_rows": (t.get("sample_rows") or [])[:5],
        })

    table_groups, grouped = table_groups_for(tables, catalog.db_groups(meta))

    return render_template(
        "catalog.html",
        target=target.name,
        coverage=ov["coverage"], drift=ov["drift"], tables=tables,
        table_groups=table_groups, grouped=grouped,
        examples_max=catalog.EXAMPLES_MAX,
        # 画面はこの3つを丸ごと置き換えて保存するので、開いたときの中身の印を
        # 渡しておく。保存時に送り返してもらい、変わっていたら断る
        stamps={k: catalog.section_stamp(meta, k)
                for k in ("glossary", "examples", "checks")},
        db_glossary=catalog.db_glossary(meta),
        examples=meta.get("examples") or [],
        checks=verify.normalize(meta.get("checks")),
        suggestions=(catalog.join_suggestions(profile, meta, target)
                     + sqlusage.suggestions_for(db.alias_for(target), profile, meta)),
        er=_er_payload(target, profile, meta),
        # ツールはDBに紐づけずに作るので、一覧も全DB分を出す（組み込みと同じ扱い）
        custom=custom_tools.collect_everywhere(),
        builtin=[_builtin_view(t) for t in tools.BUILTIN_TOOLS],
        chart_fields={t: list(charts.required_fields(t)) for t in charts.CHART_TYPES},
        builtin_overrides=meta.get("builtin_tools") or {},
        intervals=list(jobs.INTERVALS.keys()),
        llm_ready=llm.is_configured(),
        views=_views_payload(target),
    )


# =============================================================================
# ER図（キャンバス用のデータ）
# =============================================================================

def _er_payload(path: Path, profile: dict, meta: dict) -> dict:
    """ERキャンバス用ペイロード。実体は catalog.er_payload（チャットのツールと共用）。"""
    return catalog.er_payload(path, profile, meta)


def _alias_lookup(own_alias: str, own_profile: dict, own_meta: dict):
    """エイリアス → (profile, meta)。DBまたぎの関連を扱うのに要る。"""
    cache = {own_alias: (own_profile, own_meta)}

    def get(alias: str):
        if alias not in cache:
            p = next((f for f in db.list_db_files() if db.alias_for(f) == alias), None)
            cache[alias] = ((catalog.profile_db(p), catalog.load_meta(p)) if p
                            else (None, None))
        return cache[alias]
    return get


def _endpoint_error(ep: tuple, lookup) -> str | None:
    """関連の端点が実在するかを確かめる。DB名を含む3要素も受ける。"""
    alias, table, column = ep
    profile, _ = lookup(alias)
    if profile is None:
        return f"DB '{alias}' が見つかりません。"
    t = (profile.get("tables") or {}).get(table)
    if t is None:
        return f"{alias} にテーブル '{table}' がありません。"
    if column not in {c["name"] for c in t.get("columns", [])}:
        return f"{alias}.{table} に列 '{column}' がありません。"
    return None


def _ref(ep: tuple, own_alias: str) -> str:
    """保存する文字列。自DBなら 'table.col'、他DBなら 'alias.table.col'。"""
    return f"{ep[1]}.{ep[2]}" if ep[0] == own_alias else f"{ep[0]}.{ep[1]}.{ep[2]}"


@bp_catalog.get("/api/catalog/suggestions")
@admin_required
def catalog_suggestions():
    """結合候補（列名からの推測）。関連を足したり消したりするたびに
    画面が取り直す（読み込み時の一覧のままだと、消した関連が候補に
    戻らず、引いた関連の候補線が残って二重になる）。"""
    path = db.path_for(request.args.get("db") or "")
    profile = catalog.profile_db(path)
    meta = catalog.load_meta(path)
    return jsonify({"suggestions": catalog.join_suggestions(profile, meta, path)
                                   + sqlusage.suggestions_for(db.alias_for(path), profile, meta)})


@bp_catalog.post("/api/catalog/rename-table")
@admin_required
def api_rename_table():
    """テーブルの改名（まとまりの移動も同じ口）。カタログの記述は全部ついてくる。"""
    body = _body()
    path = db.path_for(body.get("db"))
    try:
        r = cleanup.rename_table(path, str(body.get("table") or ""),
                                 str(body.get("new_table") or ""))
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"改名に失敗しました（元に戻しました）: {e}"}), 500
    print(f"[rename] {path.name}: {r['old']} → {r['new']}（{g.user.username}）")
    return jsonify({"ok": True, **r})


@bp_catalog.post("/api/catalog/rename-group")
@admin_required
def api_rename_group():
    """まとまりのキーを、配下の全テーブルごと改名する。"""
    body = _body()
    path = db.path_for(body.get("db"))
    try:
        r = cleanup.rename_group(path, str(body.get("group") or ""),
                                 str(body.get("new_group") or ""))
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"改名に失敗しました: {e}"}), 500
    print(f"[rename] {path.name}: まとまり {body.get('group')} → "
          f"{body.get('new_group')}（{r['count']}表・{g.user.username}）")
    return jsonify({"ok": True, **r})


@bp_catalog.post("/api/catalog/relationship")
@admin_required
def relationship():
    """関連の追加・多重度変更・削除。ER図キャンバスから呼ばれる。"""
    body = _body()
    path = db.path_for(body.get("db"))
    meta = catalog.load_meta_for_edit(path)
    rels = meta.setdefault("relationships", [])
    action = body.get("action")
    alias = db.alias_for(path)

    # 関連の指定は2通り。ドラッグ直後は from_table/from_column、
    # 「元に戻す／やり直す」は保存済みの文字列 from/to（'table.col' や 'db.table.col'）で来る
    def _ep(side):
        if body.get(side):
            return catalog.parse_endpoint(str(body[side]), alias)
        return catalog.parse_endpoint(f"{body.get(side + '_table')}.{body.get(side + '_column')}", alias)

    if action == "add":
        lookup = _alias_lookup(alias, catalog.profile_db(path), meta)
        # テーブル名は 'table' でも 'otherdb.table' でもよい（DBまたぎ）
        a, b = _ep("from"), _ep("to")
        if not a or not b:
            return jsonify({"error": "関連の指定が正しくありません。"}), 400
        for ep in (a, b):
            err = _endpoint_error(ep, lookup)
            if err:
                return jsonify({"error": err}), 400
        if a == b:
            return jsonify({"error": "同じ列同士は関連にできません。"}), 400
        if a[0] != alias and b[0] != alias:
            return jsonify({"error": "どちらか一方は、いま開いているDBのテーブルにしてください。"}), 400

        # 向きを「子（外部キー側）→ 親（主キー側）」に揃えてから保存する。
        # ER図は矢印を描かないので、人はどちら向きにもドラッグする。
        # from/to は描画順ではなく参照の向きで、整合性チェックがこれに依存する。
        a, b, card = catalog.normalize_direction(a, b, body.get("cardinality"), lookup)

        # 同じ表ペアの既存の関連（複合キーとして合流できる相手）。向きが逆でも拾い、
        # 逆なら既存の向きに合わせる（1つの関連の中で向きが混ざらないように）
        same = []
        for i, r in enumerate(rels):
            pr = catalog.rel_pairs(r, alias)
            if not pr:
                continue
            if (pr[0], pr[1]) == ((a[0], a[1]), (b[0], b[1])):
                same.append((i, r))
            elif (pr[0], pr[1]) == ((b[0], b[1]), (a[0], a[1])):
                a, b = b, a
                card = catalog._CARD_FLIP.get(card, card)
                same.append((i, r))

        if a[0] != alias:
            # 子（from側）が他DBになった。その関連は相手のDBが持つべき
            return jsonify({"error":
                            f"この向きの関連は {a[0]} 側で登録してください"
                            f"（外部キーを持つのは {a[0]}.{a[1]} です）。"
                            "DBを切り替えてから、同じようにつないでください。"}), 400

        for _i, r in same:
            if (a[2], b[2]) in catalog.rel_pairs(r, alias)[2]:
                return jsonify({"error": "この関連はすでに登録されています。"}), 400

        mode = body.get("mode")
        if same and mode not in ("merge", "new"):
            # 既存の線に列を足して複合キーにするのか、独立した別の関連なのかは
            # 人にしか決められない。一度返して画面に選ばせる
            return jsonify({"ok": False, "ask": "merge_or_new",
                            "from": _ref(a, alias), "to": _ref(b, alias),
                            "cardinality": card,
                            "existing": [{"from": r.get("from"), "to": r.get("to"),
                                          "cardinality": r.get("cardinality") or "N:1",
                                          "pairs": [[fc, tc] for fc, tc
                                                    in catalog.rel_pairs(r, alias)[2]]}
                                         for _i, r in same]})

        # 結んでよい列か、実データを見て確かめる。
        #   block … 保存しない（値が全く重ならない等。JOINが成立しない線をAIに教えない）
        #   warn  … 理由を返して止める。人が確認して force=true で送り直せば保存する
        def _path_of(al):
            return next((f for f in db.list_db_files() if db.alias_for(f) == al), path)
        check = catalog.link_check(a, b, lookup, _path_of)
        if mode == "merge" and same:
            # 複合キーへの合流では「親が単独では一意でない」警告が的外れになり得る。
            # 合流後の列の組で一意なら、その警告を情報の行に置き換える
            tgt_pairs = catalog.rel_pairs(same[0][1], alias)[2] + [(a[2], b[2])]
            parent_cols = [p_[1] for p_ in tgt_pairs]
            if catalog.tuple_unique(_path_of(b[0]), b[1], parent_cols):
                kept = [i_ for i_ in check["issues"]
                        if "一意ではありません" not in str(i_.get("title", ""))]
                if len(kept) != len(check["issues"]):
                    kept.append({"level": "info", "title": "複合キーとして一意です",
                                 "detail": f"{b[1]} は ({', '.join(parent_cols)}) の組み合わせで"
                                           "1行が一意になるため、単独列の重複は問題ありません。"})
                check = {"level": ("block" if any(i_["level"] == "block" for i_ in kept)
                                   else "warn" if any(i_["level"] == "warn" for i_ in kept)
                                   else "ok"),
                         "issues": kept}
        if check["level"] == "block" or (check["level"] == "warn" and not body.get("force")):
            # 200 で返す: 画面の api() は非2xxだと本文を捨てて例外にするため
            return jsonify({"ok": False, "check": check,
                            "from": _ref(a, alias), "to": _ref(b, alias),
                            "cardinality": card, "mode": mode or ""})

        if mode == "merge" and same:
            tgt_i, tgt = same[0]
            if body.get("merge_from") and body.get("merge_to"):
                tgt_i, tgt = next(((i, r) for i, r in same
                                   if r.get("from") == body["merge_from"]
                                   and r.get("to") == body["merge_to"]), same[0])
            pr = catalog.rel_pairs(tgt, alias)
            pairs = pr[2] + [(a[2], b[2])]
            tgt["from"] = catalog.format_endpoint(a[0], a[1], [p_[0] for p_ in pairs], alias)
            tgt["to"] = catalog.format_endpoint(b[0], b[1], [p_[1] for p_ in pairs], alias)
            extra = {"merged": {"from": tgt["from"], "to": tgt["to"],
                                "cardinality": tgt.get("cardinality") or "N:1",
                                "pair": [a[2], b[2]],
                                # 画面の「元に戻す／やり直す」が同じ列ペアを付け外し
                                # できるよう、addで送り直せる形も返す
                                "add_body": {
                                    "from_table": a[1] if a[0] == alias else f"{a[0]}.{a[1]}",
                                    "from_column": a[2],
                                    "to_table": b[1] if b[0] == alias else f"{b[0]}.{b[1]}",
                                    "to_column": b[2]}}}
        else:
            new = {"from": _ref(a, alias), "to": _ref(b, alias), "cardinality": card}
            rels.append(new)
            extra = {"added": new}
    elif action in ("update", "delete"):
        # 位置（index）でも、保存済みの from/to 文字列でも指せる。
        # 「元に戻す」は index がずれるので from/to で来る
        if body.get("from") and body.get("to"):
            i = next((k for k, r in enumerate(rels)
                      if r.get("from") == body["from"] and r.get("to") == body["to"]), -1)
        else:
            i = int(body.get("index", -1))
        if not (0 <= i < len(rels)):
            return jsonify({"error": "この関連は既に削除されています。"}), 400
        if action == "delete":
            extra = {"removed": rels.pop(i)}
        else:
            prev = rels[i].get("cardinality")
            rels[i]["cardinality"] = body.get("cardinality") or prev
            extra = {"updated": {**rels[i], "previous": prev}}
    elif action == "remove_pair":
        # 複合キーの関連から列ペアを1つ外す。残り1ペアなら単独形式へ、0なら関連ごと削除。
        # 探すのは「表の組が同じで、その列ペアを含む関連」。from/to の文字列は
        # 列を足し引きするたびに変わるので、文字列の完全一致では「元に戻す／やり直す」で
        # 見失う（同じ表ペアに複数の関連があっても、列ペアで一意に決まる）
        pair = [str(x) for x in (body.get("pair") or [])]
        fep = catalog.parse_endpoint_cols(body.get("from", ""), alias)
        tep = catalog.parse_endpoint_cols(body.get("to", ""), alias)
        if not fep or not tep or len(pair) != 2:
            return jsonify({"error": "列ペアの指定が正しくありません。"}), 400
        i, pr = -1, None
        for k, r in enumerate(rels):
            cand = catalog.rel_pairs(r, alias)
            if (cand and cand[0] == (fep[0], fep[1]) and cand[1] == (tep[0], tep[1])
                    and (pair[0], pair[1]) in cand[2]):
                i, pr = k, cand
                break
        if i < 0:
            return jsonify({"error": "この関連は既に変更されています。ページを更新してください。"}), 400
        pairs = [p_ for p_ in pr[2] if [p_[0], p_[1]] != pair]
        if pairs:
            (fa, ftb), (ta, ttb) = pr[0], pr[1]
            rels[i]["from"] = catalog.format_endpoint(fa, ftb, [p_[0] for p_ in pairs], alias)
            rels[i]["to"] = catalog.format_endpoint(ta, ttb, [p_[1] for p_ in pairs], alias)
            (fa2, ftb2), (ta2, ttb2) = pr[0], pr[1]
            extra = {"pair_removed": {"from": rels[i]["from"], "to": rels[i]["to"],
                                      "cardinality": rels[i].get("cardinality") or "N:1",
                                      "pair": pair,
                                      "add_body": {
                                          "from_table": ftb2 if fa2 == alias else f"{fa2}.{ftb2}",
                                          "from_column": pair[0],
                                          "to_table": ttb2 if ta2 == alias else f"{ta2}.{ttb2}",
                                          "to_column": pair[1]}}}
        else:
            extra = {"removed": rels.pop(i)}
    else:
        return jsonify({"error": "不正な操作です。"}), 400

    catalog.save_meta(path, meta)
    profile = catalog.profile_db(path)
    return jsonify({"ok": True, "er": _er_payload(path, profile, catalog.load_meta(path)), **extra})


@bp_catalog.get("/api/catalog/table-info", endpoint="table_info")
@login_required
def _w_table_info():
    """ER図でテーブルをクリックしたときの中身（概要・列・実値・サンプル行）。

    描画用のペイロードには入れていない（全テーブル分を持つと重い）ので、
    開いたときに取りに来る。チャットの読み取り専用ER図からも使うので、
    管理者に限らずログイン済みなら見られる（describe_table でAIに渡している
    情報と同じ範囲）。
    """
    alias = request.args.get("db") or ""
    tname = request.args.get("table") or ""
    path = next((f for f in db.list_db_files() if db.alias_for(f) == alias), None)
    if path is None:
        return jsonify({"error": f"DB '{alias}' が見つかりません。"}), 404
    profile, meta = catalog.profile_db(path), catalog.load_meta(path)
    t = (profile.get("tables") or {}).get(tname)
    if t is None:
        return jsonify({"error": f"テーブル '{tname}' が見つかりません。"}), 404
    tmeta = (meta.get("tables") or {}).get(tname) or {}
    mcols = tmeta.get("columns") or {}
    pk = set(catalog.effective_pk(profile, meta, tname)[0])
    cols = []
    for c in t.get("columns") or []:
        cm = mcols.get(c["name"]) or {}
        stat = (t.get("col_stats") or {}).get(c["name"]) or {}
        if "values" in stat:
            actual = ", ".join(str(v[0]) if isinstance(v, (list, tuple)) else str(v)
                               for v in stat["values"][:8])
        elif "min" in stat:
            actual = f"{stat['min']} 〜 {stat['max']}"
        else:
            actual = ""
        cols.append({"name": c["name"], "type": c.get("type") or "",
                     "pk": c["name"] in pk,
                     "description": cm.get("description") or "",
                     "codes": cm.get("values") or {}, "actual": actual})
    return jsonify({
        "db": path.name, "alias": alias, "table": tname,
        "rows": t.get("row_count"),
        "description": tmeta.get("description") or "",
        "ai_draft": bool(tmeta.get("ai_draft")),
        "columns": cols,
        "glossary": catalog.table_glossary(meta, tname),
        "sample_columns": t.get("sample_columns") or [],
        "sample_rows": jsonable((t.get("sample_rows") or [])[:5]),
    })


# --- ビュー（実体を持たない、名前を付けたSELECT）--------------------------------
#
# 「よく使う結合や絞り込み」に名前を付けて置いておく口。表と同じ規約（まとまり__名前）
# で作るので、登録するとテーブル一覧・ER図・チャットの表選択にそのまま出る。
# 説明や用語も表と同じように付けられる（カタログ側は名前で引くので追加実装が要らない）。

VIEW_PREVIEW_ROWS = 20


def _view_check_sql(sql: str) -> str:
    """ビューの定義として受け付けてよいSQLか。通らなければ ValueError。"""
    sql = str(sql or "").strip().rstrip(";").strip()
    if not sql:
        raise ValueError("SQLが空です。")
    db.validate_select(sql)          # SELECT専用ガード（書き込み・複数文を弾く）
    return sql


def _view_run(path, sql: str, limit: int = VIEW_PREVIEW_ROWS) -> dict:
    """定義SQLを実データで動かして、列と先頭数行と件数を返す。"""
    scope = [{"path": str(path), "alias": db.alias_for(path), "name": path.name}]
    cols, rows, _tr = db.run_select(sql, scope, max_rows=limit)
    total = None
    try:
        _c, crows, _t = db.run_select(
            f"SELECT COUNT(*) FROM ({sql})", scope, max_rows=1)
        total = crows[0][0] if crows else None
    except Exception:
        pass                          # 件数は付けられなくても本体は見せる
    return {"columns": cols, "rows": jsonable(rows), "total": total}


@bp_catalog.post("/api/catalog/view/preview")
@admin_required
def view_preview():
    """定義SQLを実データで動かして確かめる（保存はしない）。"""
    body = _body()
    try:
        path = db.path_for(body.get("db") or "")
        sql = _view_check_sql(body.get("sql"))
        return jsonify({"ok": True, "sql": sql, **_view_run(path, sql)})
    except FileNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@bp_catalog.post("/api/catalog/view/draft")
@admin_required
def view_draft():
    """日本語の「欲しい一覧」から、AIにビューの下書きを起こさせる。

    起こしたらその場で実データに当て、失敗したらエラーを添えて1回だけ書き直させる。
    """
    body = _body()
    purpose = str(body.get("purpose") or "").strip()
    if not purpose:
        return jsonify({"error": "どんな一覧が欲しいかを書いてください。"}), 400
    if not llm.is_configured():
        return jsonify({"error": "AIが未設定です。「モデル設定」画面で接続先とAPIキーを設定してください。"}), 400
    try:
        path = db.path_for(body.get("db") or "")
    except FileNotFoundError as e:
        return jsonify({"error": str(e)}), 404

    draft, last_err = None, None
    for _attempt in range(2):
        try:
            draft = llm.draft_view(path, purpose, previous=draft, error=last_err)
        except Exception as e:
            return jsonify({"error": f"AIの下書きに失敗しました: {e}"}), 400
        # 「作らない方がよい」判断は、エラーではなく理由として画面へ返す
        if draft.get("ok") is False:
            return jsonify({"ok": False, "reason": draft.get("reason", "")})
        try:
            sql = _view_check_sql(draft.get("sql"))
            preview = _view_run(path, sql)
        except Exception as e:
            last_err = str(e)
            continue
        return jsonify({**draft, "ok": True, "sql": sql, **preview})
    return jsonify({"error": f"AIが書いたSQLが実データで通りませんでした: {last_err}",
                    "sql": (draft or {}).get("sql", "")}), 400


@bp_catalog.post("/api/catalog/view")
@admin_required
def view_save():
    """ビューの新規作成・作り直し。説明もカタログに書く。"""
    body = _body()
    try:
        path = db.path_for(body.get("db") or "")
    except FileNotFoundError as e:
        return jsonify({"error": str(e)}), 404

    name = importer.safe_name(str(body.get("name") or ""), table=True)
    old = str(body.get("old_name") or "").strip()
    if "__" not in name.strip("_"):
        return jsonify({"error": "名前は「まとまり__名前」の形にしてください。"}), 400
    try:
        sql = _view_check_sql(body.get("sql"))
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    profile = catalog.profile_db(path)
    existing = profile.get("tables", {}).get(name)
    if existing and existing.get("type") != "view" and name != old:
        return jsonify({"error": f"'{name}' は既にテーブルとして存在します。"}), 400

    # 改名は「旧名が本当にビューのとき」だけ許す。ここを通さないと
    # old に実テーブル名を入れられて、実表を改名・削除できてしまう
    if old and old != name and old not in {v["name"] for v in importer.list_views(path)}:
        return jsonify({"error": f"'{old}' はビューではありません。改名できるのはビューだけです。"}), 400

    # 新規作成のつもりで既存ビューの名前を入れたときは、黙って差し替えない。
    # 画面が overwrite を明示したときだけ上書きする（実テーブルとの衝突は上で拒否済み）。
    if existing and name != old and not body.get("overwrite"):
        return jsonify({"error": f"ビュー '{name}' は既にあります。"
                                 f"作り直すときは、そのビューを開いてから保存してください。",
                        "exists": True}), 409

    try:
        _view_run(path, sql, limit=1)     # 保存前に必ず動かす
    except Exception as e:
        return jsonify({"error": f"このSQLは実データで動きませんでした: {e}"}), 400

    try:
        # 改名は表と同じ経路に通す。説明だけでなく、関連・ER配置・例文・用語・
        # 検算・まとまりメモ・利用者の「対象から外した表」まで一緒に付け替わる。
        # （ここを自前で書いていたときは、説明以外が旧名のまま取り残されていた）
        if old and old != name:
            cleanup.rename_table(path, old, name)
        importer.create_view(path, name, sql,
                             replace=bool(old) or bool(existing))
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    # 説明はカタログ（表と同じ置き場）に書く。旧名からの引き継ぎは
    # rename_table が済ませているので、ここでは書き足すだけ
    meta = catalog.load_meta_for_edit(path)
    tmeta = meta.setdefault("tables", {})
    desc = str(body.get("description") or "").strip()
    entry = tmeta.setdefault(name, {})
    if desc:
        entry["description"] = desc
        entry.pop("ai_draft", None)
    catalog.save_meta(path, meta)
    catalog.forget(path)

    print(f"[view] {path.name} のビュー {name} を保存しました（{g.user.username}）")
    return jsonify({"ok": True, "name": name, "views": _views_payload(path)})


@bp_catalog.post("/api/catalog/view/delete")
@admin_required
def view_delete():
    """ビューを消して、カタログに残る参照も片づける（表の削除と同じ扱い）。"""
    body = _body()
    try:
        path = db.path_for(body.get("db") or "")
    except FileNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    name = str(body.get("name") or "").strip()
    if not name:
        return jsonify({"error": "ビュー名がありません。"}), 400
    if name not in {v["name"] for v in importer.list_views(path)}:
        return jsonify({"error": f"ビュー '{name}' が見つかりません。"}), 404
    using = cleanup.views_using(path, name)
    if using and not body.get("force"):
        return jsonify({
            "error": f"ビュー '{name}' を次のビューが使っています: {'、'.join(using)}。"
                     "このまま消すとそれらは動かなくなり、"
                     "さらにこのDBでは表の改名が一切できなくなります。"
                     "先にそちらを直すか削除してください。",
            "broken_views": using}), 409
    importer.drop_table(path, name)
    done = cleanup.clean_table(path, name, drop_jobs=False)
    catalog.forget(path)
    print(f"[view] {path.name} のビュー {name} を削除しました（{g.user.username}）")
    # 掃除で用語集・例文・検算が変わっていることがある。新しい印を返さないと、
    # 開いたままの画面からの次の保存が「別の場所で変わりました」で拒まれる
    return jsonify({"ok": True, "groups": cleanup.summarize(done),
                    "stamps": _stamps_of(path),
                    "views": _views_payload(path)})


def _views_payload(path) -> list:
    """画面に渡すビューの一覧（定義SQL・説明・列数・行数つき）。"""
    profile = catalog.profile_db(path)
    meta = catalog.load_meta(path)
    tmeta = meta.get("tables") or {}
    out = []
    for v in importer.list_views(path):
        t = (profile.get("tables") or {}).get(v["name"]) or {}
        out.append({
            "name": v["name"],
            "sql": importer.view_body(path, v["name"]),
            "description": (tmeta.get(v["name"]) or {}).get("description", ""),
            "columns": [c["name"] for c in t.get("columns", [])],
            "rows": t.get("row_count"),
            "error": t.get("error") or "",
        })
    return out


@bp_catalog.post("/api/catalog/layout")
@admin_required
def save_layout():
    body = _body()
    path = db.path_for(body.get("db"))
    meta = catalog.load_meta_for_edit(path)
    incoming = body.get("layout") or {}
    if not isinstance(incoming, dict):
        return jsonify({"error": "配置の形式が正しくありません。"}), 400
    clean = {}
    for k, v in incoming.items():
        # 1ノード = [x, y] の数値2つ。それ以外は受け付けない（保存すると以後ER図が読めなくなる）
        if not isinstance(v, (list, tuple)) or len(v) != 2:
            return jsonify({"error": f"配置の形式が正しくありません（{k}）。"}), 400
        try:
            clean[str(k)] = [int(round(float(v[0]))), int(round(float(v[1])))]
        except (TypeError, ValueError):
            return jsonify({"error": f"配置の座標が数値ではありません（{k}）。"}), 400
    meta["er_layout"] = {**(meta.get("er_layout") or {}), **clean}
    catalog.save_meta(path, meta)
    return jsonify({"ok": True})


@bp_catalog.post("/api/catalog/primary-key")
@admin_required
def primary_key():
    body = _body()
    path = db.path_for(body.get("db"))
    # 書き換えるので load_meta_for_edit（控え）を使う。load_meta は共有キャッシュ
    # そのものなので、書き換えると保存前に他の画面・プロンプトへ漏れる
    table = str(body.get("table") or "").strip()
    if not table:
        return jsonify({"error": "テーブルが指定されていません。"}), 400
    profile, meta = catalog.profile_db(path), catalog.load_meta_for_edit(path)
    tm = meta.setdefault("tables", {}).setdefault(table, {})
    declared = catalog.declared_pk(profile, table)
    cols = body.get("columns") or []
    if cols and cols != declared:
        tm["primary_key"] = cols
    else:
        tm.pop("primary_key", None)
    catalog.save_meta(path, meta)
    return jsonify({"ok": True, "er": _er_payload(path, profile, catalog.load_meta(path))})


# =============================================================================
# 保存系
# =============================================================================

@bp_catalog.post("/api/catalog/table")
@admin_required
def save_table():
    body = _body()
    path = db.path_for(body.get("db"))
    table = str(body.get("table") or "").strip()
    if not table:
        return jsonify({"error": "テーブルが指定されていません。"}), 400
    cols_in = body.get("columns") or {}
    if not isinstance(cols_in, dict):
        return jsonify({"error": "列の形式が正しくありません。"}), 400
    meta = catalog.load_meta_for_edit(path)
    tables = meta.setdefault("tables", {})
    tm = tables.setdefault(table, {})
    tm["description"] = (body.get("description") or "").strip()
    cols = {}
    for name, c in cols_in.items():
        if not isinstance(c, dict):
            return jsonify({"error": f"列 '{name}' の形式が正しくありません。"}), 400
        entry = {}
        if (c.get("description") or "").strip():
            entry["description"] = c["description"].strip()
        if c.get("values"):
            entry["values"] = c["values"]
        if entry:
            cols[name] = entry
    if cols:
        tm["columns"] = cols
    else:
        tm.pop("columns", None)
    tm.pop("ai_draft", None)
    if not any(tm.get(k) for k in ("description", "columns", "primary_key", "glossary")):
        tables.pop(table, None)
    catalog.save_meta(path, meta)
    return jsonify({"ok": True})


def _rows(body: dict, key: str):
    """本文の一覧（用語・例文・検算）を「辞書の並び」として受け取る。

    画面は必ずこの形で送るが、本文を手で作られると並びでないものが来る。
    そのまま回すと .get で落ちて英語の500ページになる。

    形が違うときは None を返す（空の並びとは区別する）。
    一覧の保存は全置換なので、形の違いを「空」として通すと、
    登録済みのものがまるごと消えてしまう。
    """
    v = body.get(key)
    if v is None:
        return []
    if not isinstance(v, list) or any(not isinstance(r, dict) for r in v):
        return None
    return v


def _stamps_of(path) -> dict:
    """いまの用語集・例文・検算の印。削除などで一覧が変わったとき、
    開いたままの画面に渡し直すために使う（渡さないと次の保存が409になる）。"""
    meta = catalog.load_meta(path)
    return {k: catalog.section_stamp(meta, k)
            for k in ("glossary", "examples", "checks")}


def _stale(body: dict, meta: dict, kind: str, label: str):
    """画面が持っていた印と、いまの中身がずれていたら 409 を返す。

    印が送られてこないとき（チャットからの登録など、一覧を置き換えない経路）は
    素通しする。置き換える画面だけが印を送る。
    """
    stamp = str(body.get("stamp") or "")
    if not stamp or stamp == catalog.section_stamp(meta, kind):
        return None
    return jsonify({
        "error": f"この画面を開いたあとに、別の場所で{label}が変わりました。"
                 f"画面を読み直してから保存してください"
                 f"（このまま保存すると、あとから足されたものが消えます）。",
        "stale": True}), 409


@bp_catalog.post("/api/catalog/glossary")
@admin_required
def save_glossary():
    body = _body()
    path = db.path_for(body.get("db"))
    meta = catalog.load_meta_for_edit(path)
    conflict = _stale(body, meta, "glossary", "用語集")
    if conflict:
        return conflict
    rows = _rows(body, "terms")
    if rows is None:
        return jsonify({"error": "用語の形式が正しくありません。"}), 400
    gl = {}
    for row in rows:
        term = (row.get("term") or "").strip()
        desc = (row.get("description") or "").strip()
        sql = (row.get("sql") or "").strip()
        if term and (desc or sql):
            gl[term] = {"description": desc, "sql": sql}
    # 誰が何を変えたかを残す（チャットからの登録と同じ記録に揃える）
    before_gl = (catalog.table_glossary(meta, body["table"]) if body.get("table")
                 else catalog.db_glossary(meta))
    _log_glossary_diff(path.name, body.get("table") or None, before_gl, gl)
    if body.get("table"):
        catalog.set_table_glossary(meta, body["table"], gl)
    elif gl:
        meta["glossary"] = gl
    else:
        meta.pop("glossary", None)
    catalog.save_meta(path, meta)
    # 続けて保存できるよう、新しい印を返す（画面は次の保存でこれを送る）
    return jsonify({"ok": True, "stamp": catalog.section_stamp(meta, "glossary")})


def _sql_scope(sql: str, path: Path) -> list[dict]:
    """このSQLを実行するのに繋ぐべきDBを決める。

    例文も用語のSQL式も、チャットと同じように別DBのテーブルへ
    「demo_master.employees」の形で入ることがある（人事DBに社員の氏名は無く、
    マスタDB側にある、など）。編集中のDBだけを繋いで検証すると、
    実際には通るSQLが "no such table" で落ちてしまうので、
    式が名前を挙げているDBは一緒に繋ぐ。
    """
    alias = db.alias_for(path)
    scope = [{"path": str(path), "alias": alias}]
    for p in db.list_db_files():
        if p == path or len(scope) >= db.MAX_ATTACHED:
            continue
        a = db.alias_for(p)
        if a.lower() == alias.lower():
            continue
        if re.search(r'(?<![\w."])' + re.escape(a) + r'\s*\.', sql, re.IGNORECASE):
            scope.append({"path": str(p), "alias": a})
    return scope


def _entries_for(scope: list[dict], cache: dict) -> list[dict]:
    """結合定義を引くための材料（各DBのプロファイルとメタ）を揃える。

    「すべて検証」では同じDBを何度も見るので、1リクエストの間だけ控えておく。
    """
    entries = []
    for s in scope:
        if s["alias"] not in cache:
            p = Path(s["path"])
            cache[s["alias"]] = {"alias": s["alias"], "profile": catalog.profile_db(p),
                                 "meta": catalog.load_meta(p)}
        entries.append(cache[s["alias"]])
    return entries


def _tables_having_columns(sql: str, entries: list[dict]) -> list[tuple]:
    """テーブル名を書いていない式（例: minutes >= 60）から、使えるテーブルを探す。

    DB全体の用語は「どのテーブルの話か」を書かずに列名だけで書かれることが多い
    （統合前は置き場所のテーブルが自明だったため）。式に出てくる語を列名として
    持っているテーブルを探し、見つかればそれを土台に検証する。
    候補が複数あれば、列数が少ない＝より限定的なものを選ぶ。
    """
    # 'A' のような文字列リテラルの中身は列名ではない。先に伏せてから語を拾う
    bare = re.sub(r"'[^']*'|\"[^\"]*\"", " ", sql)
    words = {w.lower() for w in re.findall(r"\w+", bare)   # \w は日本語の列名も拾う
             if not w.isdigit()}
    words -= _SQL_WORDS
    if not words:
        return []
    hits = []
    for e in entries:
        for t, info in (e["profile"].get("tables") or {}).items():
            cols = {c["name"].lower() for c in (info.get("columns") or [])}
            if words <= cols:
                hits.append((len(cols), e["alias"], t))
    hits.sort()
    return [(a, t) for _, a, t in hits[:1]]


#: 列名と間違えやすいSQLの予約語。テーブル探しのときに無視する。
#: CAST(... AS REAL) の型名も列名ではないので入れておく（入れないと
#: 「real という列を持つ表」を探しに行き、表の自動推定が必ず外れる）
_SQL_WORDS = {"select", "from", "where", "and", "or", "not", "null", "is", "in",
              "like", "between", "case", "when", "then", "else", "end", "as",
              "count", "sum", "avg", "min", "max", "round", "cast", "distinct",
              "coalesce", "ifnull", "nullif", "strftime", "date", "julianday",
              "substr", "length", "trim", "upper", "lower", "replace", "abs",
              "integer", "int", "real", "float", "double", "numeric", "decimal",
              "text", "blob", "char", "varchar", "boolean", "datetime"}


def _referenced_tables(sql: str, entries: list[dict], own_alias: str) -> list[tuple]:
    """SQL式の中に出てくるテーブルを (エイリアス, テーブル名) で拾う。

    自DBの "attendances.overtime_min" という書き方と、DBをまたぐ
    "demo_master.employees.employee_id" という書き方の両方を見つける。
    長い名前から先に照合する（"emp" が "employees" に化けるのを防ぐ）。
    """
    found = []
    for e in entries:
        a = e["alias"]
        for t in sorted(e["profile"].get("tables") or {}, key=len, reverse=True):
            qualified = (r'(?<![\w."])' + re.escape(a) + r'\s*\.\s*'
                         + re.escape(t) + r'\s*\.')
            if re.search(qualified, sql, re.IGNORECASE):
                found.append((a, t))
            elif a == own_alias and re.search(
                    r'(?<![\w."])' + re.escape(t) + r'\s*\.', sql, re.IGNORECASE):
                found.append((a, t))
    return found


def _table_label(at: tuple, own_alias: str) -> str:
    """画面に出すテーブル名。別DBのものはどのDBか分かるようにする。"""
    return at[1] if at[0] == own_alias else f"{at[0]}.{at[1]}"


def _from_clause(tables: list[tuple], entries: list[dict]) -> tuple[str, bool]:
    """複数テーブルをつなぐ FROM句を組み立てる。

    tables: [(エイリアス, テーブル名), ...]
    カタログに結合定義があればそれで JOIN する。無ければ素直に並べる
    （直積になるが、SELECT専用・タイムアウトつきなので暴走はしない）。
    戻り値の2つ目は「全部つなげたか」。直積のときは件数の割合に意味が無いので、
    呼び出し側でその旨を添える。
    """
    def q(at):
        return f'{at[0]}."{at[1]}"'

    if len(tables) <= 1:
        return q(tables[0]), True

    edges = catalog.collect_edges(entries)
    joined, sql, all_linked = [tables[0]], q(tables[0]), True
    for t in tables[1:]:
        cond = None
        for e in edges:
            (fa, ft, fc), (ta, tt, tc) = e["from"], e["to"]
            pair = {(fa, ft), (ta, tt)}
            if t in pair and pair & set(joined) and (fa, ft) != (ta, tt):
                cond = f'{fa}."{ft}"."{fc}" = {ta}."{tt}"."{tc}"'
                break
        if cond:
            sql += f" JOIN {q(t)} ON {cond}"
        else:
            sql += f", {q(t)}"
            all_linked = False
        joined.append(t)
    return sql, all_linked


@bp_catalog.post("/api/catalog/glossary/verify")
@admin_required
def verify_glossary():
    """用語のSQL式を実データに当てて確かめる。

    テーブルを1つ選んでいればそのテーブルで、DB全体の用語なら式が触れている
    テーブルを式から読み取って組み立てる。結合定義があればJOINでつなぐ。
    """
    body = _body()
    path = db.path_for(body.get("db"))
    alias = db.alias_for(path)
    picked = body.get("table")
    cache: dict = {}

    out = []
    rows = _rows(body, "terms")
    if rows is None:
        return jsonify({"error": "用語の形式が正しくありません。"}), 400
    for row in rows:
        sql = (row.get("sql") or "").strip()
        term = row.get("term") or ""
        if not sql:
            out.append({"term": term, "verdict": "－", "detail": "SQL式が未入力"})
            continue

        # 式が別DBの名前を出していれば、そのDBも繋いだ上で確かめる
        scope = _sql_scope(sql, path)
        entries = _entries_for(scope, cache)
        # 置き場所のテーブルを土台にしつつ、式が名前を挙げているテーブルも足す。
        # 「MTBF = 稼働時間 ÷ アラーム件数」のように、1つの用語が
        # 隣のテーブルを見に行くことがあるため（置き場所だけでは列が足りない）。
        used = _referenced_tables(sql, entries, alias)
        if picked and (alias, picked) not in used:
            used.insert(0, (alias, picked))
        if not used:
            # テーブル名を書いていない式（DB全体の用語に多い）。
            # 列名を持つテーブルが見つかれば、それを土台に検証する
            used = _tables_having_columns(sql, entries)
        if not used:
            # どのテーブルにも触れていない式。定数などはそのまま評価できる
            try:
                _, rows, _ = db.run_select(f"SELECT {sql} AS v", scope, max_rows=1)
                out.append({"term": term, "verdict": "計算式",
                            "detail": f"計算結果: {rows[0][0]}",
                            "columns": ["計算結果"], "rows": [[str(rows[0][0])]]})
            except Exception as e:
                out.append({"term": term, "verdict": "エラー",
                            "detail": "テーブル名が見つかりません。"
                                      "「売上.金額」のようにテーブル名から書いてください。"
                                      f"（{str(e).splitlines()[0][:70]}）"})
            continue

        src, linked = _from_clause(used, entries)
        labels = [_table_label(t, alias) for t in used]
        note = f"／ 対象: {'、'.join(labels)}" if len(used) > 1 or not picked else ""
        if not linked:
            note += "（結合定義が無いため総当たりで数えています。"
            note += "「結合・ER図」で関連を登録すると正確になります）"
        try:
            _, rows, _ = db.run_select(
                f"SELECT COUNT(*) AS n, (SELECT COUNT(*) FROM {src}) AS total "
                f"FROM {src} WHERE {sql}", scope, max_rows=1)
            n, total = rows[0]
            pct = f"（{n / total * 100:.1f}%）" if total else ""
            hit = {"term": term, "verdict": "条件式",
                   "detail": f"該当 {n:,} 行 / 全 {total:,} 行{pct}{note}"}
            # 該当行の例も見せる（条件が意図どおりかは、行を見るのが一番早い）
            try:
                cols2, rows2, _ = db.run_select(
                    f"SELECT * FROM {src} WHERE {sql}", scope, max_rows=3)
                hit["columns"] = cols2
                hit["rows"] = [[None if v is None else str(v) for v in r] for r in rows2]
            except Exception:
                pass
            out.append(hit)
            continue
        except Exception as first:
            err = str(first).splitlines()[0][:120]
        try:
            _, rows, _ = db.run_select(f"SELECT {sql} AS v FROM {src}", scope, max_rows=1)
            out.append({"term": term, "verdict": "計算式",
                        "detail": f"計算結果の例: {rows[0][0]}{note}",
                        "columns": ["計算結果の例"], "rows": [[str(rows[0][0])]]})
        except Exception:
            out.append({"term": term, "verdict": "エラー", "detail": err})
    return jsonify({"results": out})


@bp_catalog.post("/api/catalog/examples/verify")
@admin_required
def verify_examples():
    """例文のSQLが実際に通るか確かめる。

    例文は「正しいと確認済みの例」としてAIに渡すので、通らないSQLが混ざると
    そのまま間違いを教えることになる。保存前にここで気づけるようにする。
    """
    body = _body()
    path = db.path_for(body.get("db"))
    out = []
    rows = _rows(body, "examples")
    if rows is None:
        return jsonify({"error": "例文の形式が正しくありません。"}), 400
    for row in rows:
        sql = (row.get("sql") or "").strip()
        q = (row.get("q") or "").strip()
        if not sql:
            out.append({"q": q, "verdict": "－", "detail": "SQLが未入力"})
            continue
        # 例文はDBをまたぐことがある（人事の勤怠 × マスタの社員、など）。
        # チャットと同じように、式が名前を挙げているDBを全部繋いで確かめる。
        scope = _sql_scope(sql, path)
        others = [s["alias"] for s in scope[1:]]
        cross = (f"／ {'、'.join(others)} も参照しています"
                 "（チャットではこれらのDBも一緒に選ぶ必要があります）") if others else ""
        try:
            columns, rows, truncated = db.run_select(sql, scope, max_rows=5)
        except Exception as e:
            out.append({"q": q, "verdict": "エラー",
                        "detail": str(e).splitlines()[0][:160]})
            continue
        if not rows:
            out.append({"q": q, "verdict": "0行",
                        "detail": f"実行できましたが0行でした（列: {'、'.join(columns)}）。"
                                  f"抽出条件が厳しすぎないか確認してください。{cross}",
                        "columns": columns, "rows": []})
        else:
            more = "以上" if truncated else ""
            out.append({"q": q, "verdict": "OK",
                        "detail": f"{len(rows)}{more}行 取得（列: {'、'.join(columns)}）{cross}",
                        "columns": columns,
                        "rows": [[None if v is None else str(v) for v in r] for r in rows]})
    return jsonify({"results": out})


def _home_db(sql: str, preferred: Path | None = None) -> str:
    """このツール定義を置くDBファイルを決める。

    ツールはDBを選ばずに作るが、定義の置き場（どの .meta.yaml か）は
    1つに決めないといけない。SQLが最初に名指ししているDB＝主に見ているDBに置く。
    そのDBを消せばツールも一緒に片づく（cleanup.py の巻き添え掃除に乗る）。
    """
    if preferred is not None:
        return Path(preferred).name
    allscope = [{"path": str(p), "alias": db.alias_for(p), "name": p.name,
                 "tables": list((catalog.profile_db(p).get("tables") or {}).keys())}
                for p in db.list_db_files()]
    hits = dbs_in_sql(sql, allscope)
    if hits:
        return hits[0]["name"]
    files = db.list_db_files()
    return files[0].name if files else ""


def _sample_params(tool: dict, given: dict | None = None) -> dict:
    """試し実行に使う値。画面で入れた値 → AIが添えた例 → 型ごとの既定値、の順に採る。

    例を使うのは、日本語だけで作ったツールを人が確かめられるようにするため。
    空の値で流すと 0行 になり、「SQLが通った」ことしか分からない。実在する値を
    入れて実際の行を見せれば、SQLを読まなくても正しさを判断できる。

    それでも0行になることはある（条件が厳しいだけかもしれない）ので、
    0行は失敗にせず、そのことを画面に出す。
    """
    out = {}
    for p in (tool.get("parameters") or []):
        name = str(p.get("name") or "").strip()
        if not name:
            continue
        for v in ((given or {}).get(name), p.get("example")):
            if v not in (None, ""):
                out[name] = v
                break
        else:
            t = p.get("type") or "string"
            out[name] = 0 if t in ("integer", "number", "boolean") else ""
    return out


@bp_catalog.post("/api/catalog/tool/try")
@admin_required
def try_tool():
    """ツールのSQLを実データで動かして、出てくる列と先頭の行を返す。

    SQLを読めない人にも「何が出るか」で正しさを判断してもらうための口。
    実行は run_select を通すので SELECT 以外は動かない。
    """
    body = _body()
    path = db.path_for(body.get("db"))
    tool = body.get("tool") or {}
    errs = [e for e in custom_tools.validate_custom_tool(tool) if not e.startswith("'")]
    sql = str(tool.get("sql") or "").strip()
    if not sql:
        return jsonify({"ok": False, "error": "SQLがありません。"})
    try:
        params = custom_tools.coerce_params(tool, _sample_params(tool, body.get("values")))
    except ValueError as e:
        return jsonify({"ok": False, "error": str(e)})

    scope = _sql_scope(sql, path)
    try:
        columns, rows, truncated = db.run_select(sql, scope, max_rows=8, params=params)
    except Exception as e:
        return jsonify({"ok": False, "error": str(e).splitlines()[0][:200]})
    return jsonify({
        "ok": True, "columns": columns,
        "rows": [[jsonable(v) for v in r] for r in rows],
        "truncated": truncated, "problems": errs,
        "note": ("実行できましたが0行でした。抽出条件やパラメータの値を見直してください。"
                 if not rows else ""),
    })


@bp_catalog.post("/api/catalog/tool/draft", endpoint="draft_tool")
@admin_required
def _w_draft_tool():
    """日本語の「やりたいこと」から、ツールの下書きをAIに起こさせる。

    起こしたらその場で実データに当てて確かめ、失敗したらエラーを添えて
    もう一度だけ書き直させる。通らないSQLをそのまま画面に出さないため。
    """
    body = _body()
    # DBは指定させない。どのDBを使うかは、やりたいことを読んだAIが決める。
    # 特定のDBに限りたいときだけ db を渡せる。
    path = db.path_for(body.get("db")) if body.get("db") else None
    purpose = str(body.get("purpose") or "").strip()
    if not purpose:
        return jsonify({"error": "何をするツールかを書いてください。"}), 400
    if not llm.is_configured():
        return jsonify({"error": "LLMが未設定です。env の OPENAI_* を設定してください。"}), 400

    wanted = [str(x).strip() for x in (body.get("params") or []) if str(x).strip()]
    render = body.get("render") or "table"
    # AIが付けた名前が不正・重複でも、保存で突き返されるのはユーザーには
    # 意味不明（名前を入力していないので）。ここで必ず有効な名前に直す。
    taken = [t.get("name") for t in custom_tools.collect_everywhere()]
    tried = []
    draft, last_err = None, None
    for attempt in range(2):          # 1回目でだめならエラーを見せて書き直させる
        try:
            draft = llm.draft_tool(path, purpose, wanted, render,
                                   previous=draft, error=last_err)
        except Exception as e:
            return jsonify({"error": f"下書きに失敗しました: {e}"}), 500
        # 「作れない」判断は、エラーではなく理由として画面へ返す。
        # ただし1回目だけ。実行に失敗したあとの ok:false は、作れない判断ではなく
        # 技術的な失敗の言い換えなので、従来どおりの失敗として扱う
        if draft.get("ok") is False:
            if last_err is None:
                return jsonify({"ok": False, "refused": True,
                                "reason": draft.get("reason", "")})
            # 拒否オブジェクトには sql も name も無い。そのまま下書きとして
            # 返すと画面の編集欄が壊れるので、理由だけを残して下書きは捨てる
            last_err = str(draft.get("reason") or "")[:200]
            tried.append(last_err)
            draft = None
            break
        draft["name"] = custom_tools.custom_tool_safe_name(draft.get("name") or purpose, taken)
        sql = draft.get("sql") or ""
        if not sql:
            last_err = "SQLが空でした。"
            tried.append(last_err)
            continue
        try:
            params = custom_tools.coerce_params(draft, _sample_params(draft))
            if path:
                scope = _sql_scope(sql, path)
            else:
                # SQLがDB名を書いていれば、そのDBだけを繋ぐ。書いていなければ
                # （DBが1つの環境では素の表名で書くのが自然）全DBを繋いで試す。
                # 繋ぐDBが1つも決まらないと必ず「対象のDBがありません」で落ちるため。
                scope = db.widen_scope(sql, []) or [
                    {"path": str(p), "alias": db.alias_for(p), "name": p.name, "tables": None}
                    for p in db.list_db_files()[:db.MAX_ATTACHED]]
            columns, rows, _ = db.run_select(sql, scope, max_rows=8, params=params)
        except Exception as e:
            last_err = str(e).splitlines()[0][:200]
            tried.append(last_err)
            continue
        return jsonify({"ok": True, "tool": draft, "columns": columns,
                        "rows": [[jsonable(v) for v in r] for r in rows],
                        "home_db": _home_db(sql, path),
                        "attempts": attempt + 1, "tried": tried})

    # 2回とも通らなかった。下書きがあれば返す（人が直せるように）
    return jsonify({"ok": False, "tool": draft, "error": last_err, "tried": tried})


@bp_catalog.post("/api/catalog/glossary/draft")
@admin_required
def draft_glossary():
    body = _body()
    path = db.path_for(body.get("db"))
    rows = _rows(body, "terms")
    if rows is None:
        return jsonify({"error": "用語の形式が正しくありません。"}), 400
    terms = [{"term": r["term"], "description": r.get("description", "")}
             for r in rows if r.get("term") and r.get("description")]
    try:
        result = llm.draft_glossary_sql(path, body.get("table"), terms)
    except Exception as e:
        return jsonify({"error": f"下書きに失敗しました: {e}"}), 500
    # drafted は従来どおり {用語: SQL式}。解説と理由は別に返す
    return jsonify({
        "ok": True,
        "drafted": {k: v["sql"] for k, v in result.items() if v.get("ok")},
        "explanations": {k: v.get("explanation", "") for k, v in result.items() if v.get("ok")},
        "reasons": {k: v["reason"] for k, v in result.items() if not v.get("ok")},
    })


@bp_catalog.post("/api/catalog/draft-table")
@admin_required
def draft_table():
    body = _body()
    path = db.path_for(body.get("db"))
    table = str(body.get("table") or "").strip()
    if not table:
        # 「入力が足りない」を AI の失敗（500）に混ぜない
        return jsonify({"error": "テーブルが指定されていません。"}), 400
    try:
        draft = llm.draft_table_meta(path, table)
    except Exception as e:
        return jsonify({"error": f"AI下書きに失敗しました: {e}"}), 500
    return jsonify({"ok": True, "draft": draft})


@bp_catalog.post("/api/catalog/checks")
@admin_required
def save_checks():
    """検算ルールの保存。空になったらキーごと消す。"""
    body = _body()
    path = db.path_for(body.get("db"))
    # 同じ名前は許す。DB統一後は「同じ検算を拠点ごとに持つ」のが普通で、
    # 名前で弾くと画面から一切保存できなくなる（中身は SQL で区別する）。
    # ただし名前もSQLも完全に同じものは、同じ計算を何度もするだけなので1件にする。
    if _rows(body, "checks") is None:
        return jsonify({"error": "検算の形式が正しくありません。"}), 400
    incoming = verify.normalize(body.get("checks"))
    checks, seen = [], set()
    for ck in incoming:
        key = verify._check_key(ck)
        if key in seen:
            continue
        seen.add(key)
        checks.append(ck)
    dropped = len(incoming) - len(checks)
    meta = catalog.load_meta_for_edit(path)
    conflict = _stale(body, meta, "checks", "検算ルール")
    if conflict:
        return conflict
    if checks:
        meta["checks"] = checks
    else:
        meta.pop("checks", None)
    catalog.save_meta(path, meta)
    verify.clear_cache()          # ルールが変わったので、古い検算結果は捨てる
    return jsonify({"ok": True, "checks": checks,
                    "stamp": catalog.section_stamp(meta, "checks"),
                    **({"dropped": dropped} if dropped else {})})


@bp_catalog.post("/api/catalog/checks/verify")
@admin_required
def verify_checks():
    """検算ルールをその場で実行して、左右の値と差を返す（保存前の内容でよい）。"""
    body = _body()
    path = db.path_for(body.get("db"))
    out = []
    rows = _rows(body, "checks")
    if rows is None:
        return jsonify({"error": "検算の形式が正しくありません。"}), 400
    for raw in rows:
        lsql = str((raw.get("left") or {}).get("sql") or "").strip()
        rsql = str((raw.get("right") or {}).get("sql") or "").strip()
        if not lsql or not rsql:
            out.append({"ok_run": False, "error": "左右の両方にSQLが必要です。"})
            continue
        check = verify.normalize([raw])
        if not check:
            out.append({"ok_run": False, "error": "ルールの形が正しくありません。"})
            continue
        # 検算のSQLは別DBを参照できる。名前を挙げているDBも繋いで実行する
        combined = " ".join([lsql, rsql, str(raw.get("drilldown") or "")])
        scope = _sql_scope(combined, path)
        res = verify.run_check(check[0], scope, use_cache=False)
        out.append({k: res[k] for k in
                    ("ok_run", "match", "left", "right", "diff", "pct", "error", "drill")})
    return jsonify({"results": out})


@bp_catalog.get("/api/catalog/usage")
@admin_required
def er_usage():
    """過去の分析で実際に使われた結合の回数（ER図に重ねる）。"""
    path = db.path_for(request.args.get("db") or "")
    return jsonify(sqlusage.usage_for(db.alias_for(path)))


def _log_glossary_diff(db_file: str, table, before: dict, after: dict) -> None:
    """用語集の一括保存を、用語ごとの差分にして履歴へ。"""
    user = getattr(g.user, "username", None)
    for term in after:
        if term not in before:
            catalog_history.add_catalog_change("glossary", "add", db_file, term, user=user,
                                table=table, after=after[term], source="catalog")
        elif before[term] != after[term]:
            catalog_history.add_catalog_change("glossary", "update", db_file, term, user=user,
                                table=table, before=before[term],
                                after=after[term], source="catalog")
    for term in before:
        if term not in after:
            catalog_history.add_catalog_change("glossary", "remove", db_file, term, user=user,
                                table=table, before=before[term], source="catalog")


@bp_catalog.post("/api/catalog/examples")
@admin_required
def save_examples():
    body = _body()
    path = db.path_for(body.get("db"))
    meta = catalog.load_meta_for_edit(path)
    conflict = _stale(body, meta, "examples", "例文")
    if conflict:
        return conflict
    rows = _rows(body, "examples")
    if rows is None:
        return jsonify({"error": "例文の形式が正しくありません。"}), 400
    incoming = [e for e in rows
                if str(e.get("q", "")).strip() and str(e.get("sql", "")).strip()]
    deduped = catalog.dedupe_examples(incoming)
    # 上限は「黙って捨てる」のではなく、何件入らなかったかを応答で知らせる
    over = max(0, len(deduped) - catalog.EXAMPLES_MAX)
    new = deduped[:catalog.EXAMPLES_MAX]

    # 差分をSQLをキーに取り、誰が何を変えたかを残す
    user = getattr(g.user, "username", None)
    old_by_sql = {e.get("sql"): e for e in (meta.get("examples") or [])}
    new_by_sql = {e.get("sql"): e for e in new}
    for s_, e_ in new_by_sql.items():
        if s_ not in old_by_sql:
            catalog_history.add_catalog_change("example", "add", path.name, e_.get("q", ""),
                                user=user, after=e_, source="catalog")
        elif old_by_sql[s_] != e_:
            catalog_history.add_catalog_change("example", "update", path.name, e_.get("q", ""),
                                user=user, before=old_by_sql[s_], after=e_,
                                source="catalog")
    for s_, e_ in old_by_sql.items():
        if s_ not in new_by_sql:
            catalog_history.add_catalog_change("example", "remove", path.name, e_.get("q", ""),
                                user=user, before=e_, source="catalog")

    meta["examples"] = new
    catalog.save_meta(path, meta)
    dropped = len(incoming) - len(deduped)          # 純粋な重複だけを数える
    # 続けて保存できるよう、新しい印を返す（画面は次の保存でこれを送る）
    return jsonify({"ok": True, "dropped": dropped,
                    "stamp": catalog.section_stamp(meta, "examples"),
                    **({"warning": f"例文が上限{catalog.EXAMPLES_MAX}件を超えたため、"
                                   f"超過分 {over} 件は保存されませんでした。"}
                       if over else {}),
                    "examples": meta["examples"]})


@bp_catalog.post("/api/catalog/group")
@admin_required
def save_group():
    """まとまり（表名の接頭辞）のメモを保存する。

    「データ全体の説明」欄は無い。複数の表にまたがる前提はここに書き、
    そのまとまりの表を選んでいるときだけAIに渡る（選択・削除に追随する）。
    """
    body = _body()
    path = db.path_for(body.get("db"))
    gkey = str(body.get("group") or "").strip()
    prof = catalog.profile_db(path)
    desc = (body.get("description") or "").strip()
    alive = any(t.startswith(gkey + "__") for t in prof["tables"])
    # 表が無いまとまりへの「書き込み」は拒む。ただし「消す」（空文字）は通す。
    # 表を全部消したあとメモだけ残ると、乖離警告が出るのに直す手段が無くなる。
    if not gkey or (not alive and desc):
        return jsonify({"error": "そのまとまりの表がありません。"}), 400
    meta = catalog.load_meta_for_edit(path)
    groups = meta.setdefault("groups", {})
    if desc:
        groups[gkey] = {"description": desc}
    else:
        groups.pop(gkey, None)
    if not groups:
        meta.pop("groups", None)
    catalog.save_meta(path, meta)
    return jsonify({"ok": True})


@bp_catalog.post("/api/catalog/group/check")
@admin_required
def check_group():
    """まとまりのメモを点検する。書き換えはしない（指摘を返すだけ）。

    機械で分かるぶん（存在しない表・まとまりへの参照）はカタログ画面の上に
    自動で出ているので、ここではAIの目に頼るぶんだけを返す。
    """
    if not llm.is_configured():
        return jsonify({"error": "AIが未設定です。「モデル設定」画面で接続先とAPIキーを設定してください。"}), 400
    body = _body()
    path = db.path_for(body.get("db"))
    group = str(body.get("group") or "").strip()
    try:
        findings = llm.review_group_memo(path, group, str(body.get("description") or ""))
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"点検に失敗しました: {e}"}), 500
    return jsonify({"ok": True, "findings": findings})


@bp_catalog.post("/api/catalog/tool")
@admin_required
def save_tool():
    """ユーザー定義ツールの追加・更新・削除。"""
    body = _body()
    path = db.path_for(body.get("db"))
    meta = catalog.load_meta_for_edit(path)
    items = list(meta.get("tools") or [])
    name = body.get("name")

    if body.get("action") == "delete":
        items = [t for t in items if t.get("name") != name]
    else:
        tool = body.get("tool") or {}
        # 既存の名前も見て検証する。見ていないと、新規作成で同名を付けたとき
        # 既存のツールを黙って上書きしてしまう（更新は original の名前だけ除く）。
        original = body.get("original") or ""
        others = {t.get("name") for t in items if t.get("name") != original}
        errors = custom_tools.validate_custom_tool(tool, others)
        if errors:
            return jsonify({"error": " / ".join(errors)}), 400
        items = [t for t in items if t.get("name") != (original or name)]
        items.append(tool)
    if items:
        meta["tools"] = items
    else:
        meta.pop("tools", None)
    catalog.save_meta(path, meta)
    return jsonify({"ok": True})


@bp_catalog.post("/api/catalog/builtin")
@admin_required
def save_builtin():
    body = _body()
    path = db.path_for(body.get("db"))
    name = str(body.get("name") or "").strip()
    if not name:
        return jsonify({"error": "ツールが指定されていません。"}), 400
    meta = catalog.load_meta_for_edit(path)
    over = dict(meta.get("builtin_tools") or {})
    over[name] = {"enabled": bool(body.get("enabled", True)),
                  "description": (body.get("description") or "").strip()}
    if not over[name]["description"] and over[name]["enabled"]:
        over.pop(name)
    meta["builtin_tools"] = over
    catalog.save_meta(path, meta)
    return jsonify({"ok": True})


# ==========================================================================
# ===== 元 web/import_bp.py
# データ取り込み画面。Excel / CSV / TXT から DB・テーブルを作り、定期更新も設定する。
# ==========================================================================
from datetime import datetime
from pathlib import Path

from flask import Blueprint, g, jsonify, render_template, request

import catalog
import cleanup
import config
import db
import history
import importer
import jobs
import scheduler


bp_import = Blueprint("imp", __name__)


@bp_import.get("/import", endpoint="index")
@admin_required
def import_index():
    return render_template(
        "import.html",
        dirs=importer.dir_status(),
        extensions=", ".join(config.IMPORT_EXTENSIONS),
        delimiters=list(importer.DELIMITERS),
        db_files=[f.name for f in db.list_db_files()],
        existing={f.name: importer.existing_tables(f) for f in db.list_db_files()},
        groups=_group_choices(),
        manage=_manage_view(),
        intervals=list(jobs.INTERVALS),
        modes=jobs.MODES,
        default_ts=config.IMPORT_TIMESTAMP_COLUMN,
        max_keep=jobs.MAX_KEEP_RUNS,
        default_keep=jobs.DEFAULT_KEEP_RUNS,
        dirs_editable=config.IMPORT_DIRS_EDITABLE,
        allow_upload=config.IMPORT_ALLOW_UPLOAD,
    )


def _group_choices() -> list[dict]:
    """取り込み先で選べる「まとまり」。いま表があるものだけを出す。

    まとまりは表名の接頭辞（まとまり__表名）で決まる。この規約を利用者に
    手入力させると、綴りを1文字違えただけで新しいまとまりができてしまう。
    """
    out = []
    for f in db.list_db_files():
        prof = catalog.profile_db(f)
        keys = sorted({t.split("__", 1)[0] for t in prof["tables"] if "__" in t})
        out.extend({"key": k} for k in keys)
    return out


def _manage_view() -> dict:
    """「DBの管理」タブが必要とするもの一式。

    定期取り込みは対象テーブルに紐づけて見せるので、DB→テーブル→そのテーブルを
    更新するジョブ、という並びにまとめる。テーブルが消えた・まだ作られていない
    ジョブは宙に浮くので orphans に分けて、画面から必ず触れるようにする。
    """
    by_target: dict[tuple, list[dict]] = {}
    for j in jobs.list_jobs():
        by_target.setdefault((j.get("db_file"), j.get("table")), []).append(j)

    used: set[tuple] = set()
    dbs = []
    for f in db.list_db_files():
        try:
            names = importer.existing_tables(f)
        except Exception as e:
            dbs.append({"name": f.name, "error": str(e), "tables": []})
            continue
        tables = []
        for t in names:
            js = by_target.get((f.name, t), [])
            if js:
                used.add((f.name, t))
            info = importer.table_info(f, t, js[0].get("timestamp_column") if js else None)
            tables.append({**info, "jobs": [_job_row(j) for j in js]})
        st = f.stat()
        dbs.append({"name": f.name, "size": st.st_size,
                    "mtime": datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M"),
                    "tables": tables})

    orphans = [_job_row(j) for key, js in by_target.items() if key not in used for j in js]
    return {"dbs": dbs, "orphans": orphans, "locked": _locked_tables(),
            "sched": scheduler.scheduler_status()}


def _locked_tables() -> dict:
    """手で更新してはいけないテーブル。{DBファイル: {テーブル: 理由}}

    定期実行＋追記のテーブルは、画面からの1回きりの取り込みでも
    余計な取得日時が1回ぶん増えて更新間隔が崩れるので、そちらも止める。
    """
    out: dict[str, dict] = {}
    for j in jobs.list_jobs():
        why = jobs.manual_run_blocked(j)
        if why:
            out.setdefault(j.get("db_file", ""), {})[j.get("table", "")] = why
    return out


def _job_row(j: dict) -> dict:
    nxt = jobs.next_run_at(j)
    kept = None
    if j.get("timestamp_column"):
        try:
            kept = importer.run_count(config.DATA_DIR / j["db_file"], j["table"],
                                      j["timestamp_column"])
        except Exception:
            kept = None
    # 画面はこれらのキーを必ず読むので、古い定義や手書きのジョブでも欠けないよう埋める
    defaults = {"sheet": None, "delimiter": None, "header_row": 0, "start_at": "",
                "realtime": False,
                "timestamp_column": None, "keep_runs": None, "enabled": True,
                "last_run": "", "last_status": "", "last_message": "", "columns": [],
                "last_degraded": []}
    return {**defaults, **j,
            "interval_label": jobs.interval_label(j.get("interval_minutes", 0)),
            "mode_label": "追記" if j.get("mode") == "append" else "全件入れ替え",
            "source_label": importer.display_name(Path(j.get("source", ""))),
            "kept": kept,
            "manual_blocked": jobs.manual_run_blocked(j),
            "next_label": nxt.strftime("%m-%d %H:%M") if nxt else "手動のみ"}


# =============================================================================
# 取り込み元フォルダの管理とファイル選択
# =============================================================================

@bp_import.get("/api/import/dirs")
@admin_required
def dirs_list():
    return jsonify({"dirs": [{k: (str(v) if k == "path" else v) for k, v in d.items()}
                             for d in importer.dir_status()],
                    "editable": config.IMPORT_DIRS_EDITABLE and bool(g.user.is_admin)})


@bp_import.post("/api/import/dirs")
@admin_required
def dirs_edit():
    """取り込み元フォルダの追加・削除。読める範囲が広がる操作なので管理者だけ。"""
    if not g.user.is_admin:
        return jsonify({"error": "取り込み元フォルダの変更は管理者のみです。"}), 403
    body = _body()
    try:
        if body.get("action") == "remove":
            importer.remove_dir(body.get("path", ""))
        else:
            importer.add_dir(body.get("path", ""))
    except importer.ImportError_ as e:
        return jsonify({"error": str(e)}), 400
    return jsonify({"ok": True, "dirs": importer.dir_status()})


@bp_import.post("/api/import/browse", endpoint="browse")
@admin_required
def _w_browse():
    """フォルダを1階層ぶん開く（エクスプローラ風の選択画面用）。"""
    try:
        return jsonify(importer.browse(_body().get("path") or None))
    except importer.ImportError_ as e:
        return jsonify({"error": str(e)}), 400


# =============================================================================
# プレビューと取り込み
# =============================================================================

def _read_source(body: dict, nrows=None):
    """サーバのフォルダ / アップロード のどちらからでも DataFrame を返す。"""
    delim = importer.DELIMITERS.get(body.get("delimiter") or "自動判定")
    header = int(body.get("header_row") or 0)
    sheet = body.get("sheet") or None
    token = body.get("upload")
    if token:
        item = _fs_get(token, g.user.username)
        if item is None:
            raise importer.ImportError_(
                "アップロードしたファイルが見つかりません。もう一度選び直してください。")
        return importer.read_upload(item["data"], item["filename"], sheet=sheet,
                                    header_row=header, delimiter=delim, nrows=nrows)
    return importer.read_table(Path(body.get("path", "")), sheet=sheet, header_row=header,
                               delimiter=delim, nrows=nrows)


@bp_import.post("/api/import/upload")
@admin_required
def upload():
    """手元のPCから選んだファイルを受け取る。ディスクには書かず、メモリに預かる。"""
    f = request.files.get("file")
    if f is None:
        return jsonify({"error": "ファイルが選ばれていません。"}), 400
    data = f.read()
    try:
        importer.check_upload(data, f.filename or "")
    except importer.ImportError_ as e:
        return jsonify({"error": str(e)}), 400
    token = _fs_put(data, f.filename or "upload", "application/octet-stream",
                          g.user.username)
    try:
        sheets = importer.upload_sheet_names(data, f.filename or "")
    except importer.ImportError_ as e:
        return jsonify({"error": str(e)}), 400
    return jsonify({"ok": True, "upload": token, "name": f.filename,
                    "size": len(data), "sheets": sheets})


@bp_import.post("/api/import/preview", endpoint="preview")
@admin_required
def _w_preview():
    body = _body()
    token = body.get("upload")
    try:
        if token:
            item = _fs_get(token, g.user.username)
            if item is None:
                raise importer.ImportError_(
                    "アップロードしたファイルが見つかりません。もう一度選び直してください。")
            stem = Path(item["filename"]).stem
            sheets = importer.upload_sheet_names(item["data"], item["filename"])
        else:
            path = Path(body.get("path", ""))
            stem = path.stem
            sheets = importer.sheet_names(path)
        df = _read_source(body, nrows=2000)
    except importer.ImportError_ as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"読み込みに失敗しました: {e}"}), 400

    plan = importer.plan_columns(df)
    head = df.head(config.IMPORT_PREVIEW_ROWS)
    return jsonify({
        "ok": True, "sheets": sheets,
        "columns": [str(c) for c in df.columns],
        "rows": jsonable(head.values.tolist()),
        "scanned": len(df),
        "plan": [{**p, "include": True} for p in plan],
        "suggest_table": importer.safe_name(stem, table=True),
        "suggest_db": stem,
    })


def _log_manual(db_path, body: dict, mode: str, ok: bool, message: str,
                started, **kw) -> None:
    """画面からの1回きりの取り込みを履歴に残す（成功も失敗も）。"""
    upload = body.get("upload")
    source = "（自分のPCからアップロード）" if upload else body.get("path", "")
    history.add_import_record(db_path.name if db_path else (body.get("db_file") or ""),
                importer.safe_name(body.get("table", ""), table=True), ok, message,
                kind="manual", mode=mode, source=source,
                sheet=body.get("sheet") or None,
                user=getattr(g.user, "username", None), started=started, **kw)


@bp_import.post("/api/import/run")
@admin_required
def run():
    body = _body()
    cols = [{"元の列名": c["source"], "列名": importer.safe_name(c["name"], c["source"]),
             "型": c["type"]} for c in (body.get("columns") or []) if c.get("include")]
    if not cols:
        return jsonify({"error": "取り込む列が選ばれていません。"}), 400
    # 表は必ずどれかのまとまりに入れる（まとまり__表名）。画面でも選ばせているが、
    # ここを通さないと、まとまりに属さない表がカタログに紛れ込む。
    # 代わりの名前は使わせない（空のまま "col" になると、足りないのが
    # まとまりなのか表名なのか分からない案内になる）
    tname = importer.safe_name(body.get("table", ""), "", table=True)
    if not tname:
        return jsonify({"error": "テーブル名を入力してください。"}), 400
    if "__" not in tname.strip("_"):
        return jsonify({"error": "まとまりを選んでください"
                                 "（テーブルは「まとまり__テーブル名」の形で作ります）。"}), 400

    mode = body.get("mode") or "replace"
    ts_col = (body.get("timestamp_column") or "").strip() or None
    keep = body.get("keep_runs")
    # 追記は「決めた間隔で1回ぶんずつ溜める」ための設定なので、手で1回だけ取り込む
    # 道は用意しない。押せてしまうと1回ぶん余計に増え、保存回数の数え方が崩れる。
    # （画面でもボタンを無効にしているが、APIを直接叩かれても同じ扱いにする）
    if mode == "append":
        return jsonify({"error":
                        "追記では「いま取り込む」は使えません。"
                        "更新間隔を決めて定期取り込みに登録してください"
                        "（手で取り込むと1回ぶん余計に増えて、"
                        "保存回数の数え方が崩れるため）。"}), 400
    # 1回きりの取り込みでも、定期取り込みと同じ条件を課す。
    # 後から定期化したときに「取得日時が無い古い行」が残らないようにするため。
    # 間隔は「1回きり」の話なので、ここでは判定に含めない。
    errors = jobs.validate_job({"db_file": "x", "table": "x", "source": "x", "mode": mode,
                            "timestamp_column": ts_col, "keep_runs": keep,
                            "interval_minutes": 1})
    if errors:
        return jsonify({"error": " / ".join(errors)}), 400
    if mode == "append":
        keep = int(keep)

    # 取り込み先は常に唯一のDB。クライアントが何を送ってきても選ばせない
    # （このアプリはDBを1つだけ持つ設計。空DBは起動時に自動で用意される）。
    sole = db.list_db_files()
    if not sole:
        return jsonify({"error": "データの保存先が見つかりません。アプリを再起動してください。"}), 500

    # 定期実行＋追記のテーブルは、手で足すと取得日時が1回ぶん余計に増えて
    # 更新間隔が崩れる。定期取り込みの「▶ 今すぐ更新」と同じ理由で止める。
    target_db = sole[0].name
    locked = _locked_tables().get(target_db, {}).get(
        importer.safe_name(body.get("table", ""), table=True))
    if locked:
        return jsonify({"error": locked}), 400

    started = datetime.now()
    db_path = None
    try:
        db_path = sole[0]
        full = _read_source(body)
        n, degraded = importer.import_dataframe(
            db_path, body["table"], full, cols, mode=mode, timestamp_col=ts_col)
        removed = (importer.prune_runs(db_path, body["table"], ts_col, keep)
                   if mode == "append" else 0)
        kept = importer.run_count(db_path, body["table"], ts_col)
    except importer.ImportError_ as e:
        _log_manual(db_path, body, mode, False, str(e), started, keep=keep)
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        _log_manual(db_path, body, mode, False, f"取り込みに失敗しました: {e}",
                    started, keep=keep)
        return jsonify({"error": f"取り込みに失敗しました: {e}"}), 500

    message = f"{n:,}行を{'追記' if mode == 'append' else '全件入れ替え'}しました。"
    if mode == "append":
        message += f" 保持 {kept}/{keep}回"
        if removed:
            message += f"（古い {removed:,}行を削除）"
    _log_manual(db_path, body, mode, True, message, started,
                rows=n, removed=removed, kept=kept, keep=keep)

    catalog.profile_db(db_path, force=True)
    return jsonify({"ok": True, "rows": n, "degraded": degraded, "removed": removed,
                    "kept": kept, "keep": keep if mode == "append" else None,
                    "timestamp_column": importer.safe_name(ts_col, "取得日時"),
                    "db": db_path.name,
                    "table": importer.safe_name(body["table"], table=True)})


@bp_import.get("/api/import/manage")
@admin_required
def manage_view():
    return jsonify(_manage_view())


@bp_import.get("/api/import/table")
@admin_required
def table_detail():
    """テーブルを開いたときに読む中身（サンプル行と更新履歴）。

    一覧を出すたびに全テーブルを走査すると重いので、開いたものだけ取りに来る。
    """
    db_file = request.args.get("db", "")
    table = request.args.get("table", "")
    path = config.DATA_DIR / db_file
    if path.parent.resolve() != config.DATA_DIR.resolve() or not path.exists():
        return jsonify({"error": "DBが見つかりません。"}), 404
    ts = next((j.get("timestamp_column") for j in jobs.list_jobs()
               if j.get("db_file") == db_file and j.get("table") == table), None)
    return jsonify({
        "sample": jsonable(importer.sample_rows(path, table, timestamp_col=ts)),
        "history": history.for_table(db_file, table, limit=50),
        "kinds": history.IMPORT_RECORD_KINDS,
    })


@bp_import.get("/api/import/impact")
@admin_required
def impact():
    """消す前の下見。何が巻き添えになるかを返す（何も書き換えない）。

    どのテーブルを消すかは table で指定する。
    """
    try:
        path = db.path_for(request.args.get("db") or "")
    except FileNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    table = request.args.get("table") or ""
    if not table:
        return jsonify({"error": "テーブルを指定してください。"}), 400
    found = cleanup.table_impact(path, table)
    return jsonify({"db": path.name, "table": table,
                    "groups": cleanup.summarize(found)})


@bp_import.post("/api/import/drop-table", endpoint="drop_table")
@admin_required
def _w_drop_table():
    """テーブルを消して、カタログに残る参照も一緒に片づける。

    掃除をしないと、存在しないテーブルの説明がAIに渡り続け、
    例文の検証は no such table で落ちる。
    """
    body = _body()
    try:
        path = db.path_for(body.get("db") or "")
    except FileNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    table = str(body.get("table") or "").strip()
    if not table:
        return jsonify({"error": "テーブル名がありません。"}), 400
    # このテーブル／ビューを使っているビューがあると、消したあとそれが壊れて残り、
    # そのDBの改名が全部できなくなる（SQLiteが無関係な表の ALTER まで断るため）。
    # 黙って消さず、一度確認する
    using = cleanup.views_using(path, table)
    if using and not body.get("force"):
        return jsonify({
            "error": f"'{table}' は次のビューが使っています: {'、'.join(using)}。"
                     "このまま消すと、それらのビューは動かなくなり、"
                     "さらにこのDBでは表の改名が一切できなくなります。"
                     "先にビューを直すか削除してください。",
            "broken_views": using}), 409
    try:
        table = importer.drop_table(path, table)   # 実物の綴りで掃除する
    except ImportError_ as e:
        return jsonify({"error": str(e)}), 404
    done = cleanup.clean_table(path, table,
                              drop_jobs=body.get("drop_jobs", True) is not False)
    print(f"[import] {path.name} の {table} を削除しました（{g.user.username}）")
    # 掃除で用語集・例文・検算が変わる。新しい印を返さないと、開いたままの
    # 画面からの次の保存が「別の場所で変わりました」で拒まれ、
    # 読み直しで書きかけが失われる
    return jsonify({"ok": True, "groups": cleanup.summarize(done),
                    "stamps": _stamps_of(path)})


# =============================================================================
# 定期取り込み
# =============================================================================

@bp_import.post("/api/jobs/save")
@admin_required
def job_save():
    body = _body()
    if body.get("upload") or not body.get("path"):
        return jsonify({"error": "アップロードしたファイルは定期取り込みに登録できません"
                                 "（サーバ上に置かれていないため、次回以降読み直せません）。"
                                 "取り込み元フォルダに置いたファイルを選んでください。"}), 400
    cols = [{"元の列名": c["source"], "列名": importer.safe_name(c["name"], c["source"]),
             "型": c["type"]} for c in (body.get("columns") or []) if c.get("include")]
    # 取り込み先は常に唯一のDB（クライアントの指定は使わない）
    sole = db.list_db_files()
    if not sole:
        return jsonify({"error": "データの保存先が見つかりません。アプリを再起動してください。"}), 500
    db_file = sole[0].name
    draft = {
        "id": body.get("id"),
        "name": (body.get("name") or "").strip() or Path(body.get("path", "")).stem,
        "source": body.get("path"), "sheet": body.get("sheet") or None,
        "header_row": int(body.get("header_row") or 0),
        "delimiter": importer.DELIMITERS.get(body.get("delimiter") or "自動判定"),
        # table=True でないと「まとまり__表名」の __ が _ に潰され、
        # 手動取り込みで作った表と定期取り込みの書き込み先が食い違う
        # 代わりの名前は使わせない。空のまま "col" になると、
        # validate_job の「テーブルを指定してください」が効かなくなる
        "db_file": db_file, "table": importer.safe_name(body.get("table", ""), "", table=True),
        "mode": body.get("mode") or "replace",
        "timestamp_column": (body.get("timestamp_column") or "").strip() or None,
        # 取得日時は全件入れ替えでも付ける（いつ時点のデータかを残すため）
        "keep_runs": body.get("keep_runs"),
        "start_at": (body.get("start_at") or "").strip(),
        "columns": cols,
        "interval_minutes": jobs.INTERVALS.get(body.get("interval") or "手動のみ", 0),
        # リアルタイム更新（質問のたびに元ファイルの更新を確認して取り込み直す）
        "realtime": bool(body.get("realtime")),
        "enabled": True,
    }
    # 取り込み方は2通りしかない。画面もこの形で聞くが、APIを直接叩かれても
    # 同じ形に寄せる（中途半端な組み合わせを保存させない）。
    #   全件入れ替え … ファイルの鏡写し。登録時に1回取り込み、以降は質問のたびに追随。
    #                   定期実行は使わない（間隔＝手動のみ・リアルタイム＝ON）
    #   追記         … 時系列で溜める。定期実行が必須で、リアルタイムは使えない
    if draft["mode"] == "append":
        draft["realtime"] = False
    else:
        draft["realtime"] = True
        draft["interval_minutes"] = 0
    errors = jobs.validate_job(draft)
    if errors:
        return jsonify({"error": " / ".join(errors)}), 400
    # 同じ取り込み元→同じテーブルは1つだけ。2つあると同時刻に2回追記されて全行が二重になる
    dup = jobs.find_duplicate(draft)
    if dup:
        return jsonify({"error":
                        f"この取り込み元と保存先の定期取り込み「{dup.get('name')}」はすでに登録されています"
                        f"（{jobs.interval_label(dup.get('interval_minutes') or 0)}）。"
                        "頻度や停止はデータカタログの各テーブルの「管理」で変更できます。"}), 400
    # 別のファイルから同じテーブルへの2本目も止める。許すと、どちらかの
    # ファイルが更新されるたびに表の中身が入れ替わる綱引きになる。
    clash = jobs.find_target_clash(draft)
    if clash:
        src = Path(str(clash.get("source") or "")).name or "別のファイル"
        return jsonify({"error":
                        f"このテーブルには、別の取り込み元「{src}」の設定"
                        f"「{clash.get('name')}」がすでにあります。"
                        "1つのテーブルに複数の取り込みを重ねると、内容がどちらの"
                        "ファイルとも一致しなくなります。既存の設定を削除するか、"
                        "別のテーブル名を指定してください。"}), 400
    if draft["mode"] == "append":
        draft["keep_runs"] = int(draft["keep_runs"])
    saved = jobs.save_job(draft)

    # 全件入れ替えは登録した時点で1回取り込む。以降はリアルタイム更新が
    # 面倒を見るので、これをやらないと「登録したのに中身が空」のまま、
    # 最初の質問が来るまでテーブルができない。
    first = None
    if saved.get("mode") != "append":
        res = jobs.run_job(saved, kind="job", user=getattr(g.user, "username", None))
        if res.get("ok"):
            catalog.profile_db(config.DATA_DIR / saved["db_file"], force=True)
        else:
            print(f"[import] 登録直後の取り込みに失敗: {res.get('message')}")
        first = {"ok": res.get("ok"), "rows": res.get("rows"),
                 "message": res.get("message")}
        saved = jobs.get_job(saved.get("id", "")) or saved

    return jsonify({"ok": True, "job": _job_row(saved), "first_run": first})


@bp_import.post("/api/jobs/run")
@admin_required
def job_run():
    body = _body()
    # 画面から押した実行は、裏のスケジューラと区別できるように印を付けて履歴に残す
    who = getattr(g.user, "username", None)
    job = jobs.get_job(body.get("id", ""))
    if job is None:
        return jsonify({"error": "ジョブが見つかりません。"}), 404
    blocked = jobs.manual_run_blocked(job)
    if blocked:
        return jsonify({"error": blocked}), 400
    results = [(job, jobs.run_job(job, kind="job", user=who))]
    for j, r in results:
        if r["ok"]:
            catalog.profile_db(config.DATA_DIR / j["db_file"], force=True)
    return jsonify({"ok": True,
                    "results": [{"name": j.get("name"), **r} for j, r in results],
                    "jobs": [_job_row(x) for x in jobs.list_jobs()]})


@bp_import.post("/api/jobs/update")
@admin_required
def job_update():
    body = _body()
    job = jobs.get_job(body.get("id", ""))
    if job is None:
        return jsonify({"error": "ジョブが見つかりません。"}), 404
    if "enabled" in body:
        job["enabled"] = bool(body["enabled"])
    if body.get("interval"):
        job["interval_minutes"] = jobs.INTERVALS.get(body["interval"], 0)
    if "realtime" in body:
        job["realtime"] = bool(body["realtime"])
    # 開始日時は触らないので過去チェックはしない（登録時に済んでいる）
    errors = jobs.validate_job(job, check_start=False)
    if errors:
        return jsonify({"error": " / ".join(errors)}), 400
    jobs.save_job(job)
    return jsonify({"ok": True, "jobs": [_job_row(x) for x in jobs.list_jobs()]})


@bp_import.post("/api/jobs/delete")
@admin_required
def job_delete():
    jobs.delete_job(_body().get("id", ""))
    return jsonify({"ok": True, "jobs": [_job_row(x) for x in jobs.list_jobs()]})



# ==========================================================================
# ===== 元 web/mail_bp.py
# メール設定の画面。
#
# 送信サーバ（ホスト・ポート・タイムアウト）と、誰から誰に送ってよいかを決める。
# env の値は初期値として使い、画面から保存したものが優先される。
#
# 暗号化と認証は社内リレー前提（なし）なので画面には出さない。必要な環境では
# env の SMTP_SECURITY / SMTP_USER / SMTP_PASSWORD で指定する。
# 閲覧・変更ともに管理者のみ。
# ==========================================================================
from flask import Blueprint, g, jsonify, render_template, request

import mailer


bp_mail = Blueprint("mail", __name__)


@bp_mail.get("/mail", endpoint="index")
@admin_required
def mail_index():
    return render_template("mail.html", status=mailer.mail_status(),
                           log=mailer.sent_log(20))


@bp_mail.get("/api/mail/settings")
@admin_required
def get_settings():
    return jsonify({**mailer.mail_status(), "editable": True,
                    "log": mailer.sent_log(20)})


@bp_mail.post("/api/mail/settings")
@admin_required
def post_settings():
    """送信サーバ・差出人・宛先の許可リストを保存する。"""
    try:
        mailer.save_settings(_body(), user=g.user.username)
    except mailer.MailError as e:
        return jsonify({"error": str(e)}), 400
    return jsonify({"ok": True, **mailer.mail_status()})


# ==========================================================================
# ===== 元 web/models_bp.py
# モデル設定の画面（管理者のみ）。
#
# チャット画面のプルダウンに出す候補・既定のモデル・画像を扱えるモデルの
# 判定キーワードを決める。ここで候補から外したモデルは、既にそれを選んで
# いた利用者も使えなくなり、既定のモデルに戻る。
# ==========================================================================
from flask import Blueprint, g, jsonify, render_template, request

import db
import models


bp_models = Blueprint("models", __name__)


def _scope():
    """文脈の使用量を測るための基準。

    上限は全員に効くので、見せる数字は「いちばん重いとき」＝全DBを選んだ場合に
    そろえる。管理者本人の選択で測ると、人によって見える数字が変わってしまう。
    """
    return build_scope({f.name: [] for f in db.list_db_files()})


@bp_models.get("/models", endpoint="index")
@admin_required
def models_index():
    return render_template("models.html", status=models.admin_status(scope=_scope()))


@bp_models.get("/api/models/admin")
@admin_required
def get_admin():
    return jsonify(models.admin_status(refresh=request.args.get("refresh") == "1",
                                       scope=_scope()))


@bp_models.post("/api/models/admin")
@admin_required
def post_admin():
    try:
        models.save_admin(_body(), user=g.user.username)
        return jsonify({"ok": True, **models.admin_status(scope=_scope())})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


# ==========================================================================
# ===== 元 web/knowledge_bp.py
# ナレッジベース（LightRAG環境）の管理画面と、利用者ごとの検索設定。
#
# 画面は2か所に分かれている。
#   「ナレッジベース」画面（管理者）… どの環境を登録するか。全員に効く
#   チャットのサイドバー（各自）    … そのうちどれを検索するか・検索の効き方
#
# 管理者が無効にした環境は、チャットの一覧にそもそも出ない。
# 逆に、利用者が外しただけの環境は他の人の検索対象には残る。
# ==========================================================================
from flask import Blueprint, g, jsonify, render_template, request

import prefs
import rag


bp_knowledge = Blueprint("knowledge", __name__)


# =============================================================================
# 管理画面（登録・接続テスト）
# =============================================================================

@bp_knowledge.get("/knowledge", endpoint="index")
@admin_required
def knowledge_index():
    return render_template("knowledge.html", bases=rag.kb_list(),
                           defaults=rag.rag_defaults(),
                           fields=rag.rag_form_fields())


@bp_knowledge.post("/api/knowledge")
@admin_required
def knowledge_add():
    d = _body()
    try:
        rag.kb_add(name=d.get("name"), base_url=d.get("base_url"),
                   api_key=d.get("api_key") or "",
                   description=d.get("description") or "",
                   enabled=bool(d.get("enabled", True)))
    except rag.RegistryError as e:
        return jsonify({"error": str(e)}), 400
    return jsonify({"ok": True, "bases": rag.kb_list()})


@bp_knowledge.post("/api/knowledge/<kb_id>")
@admin_required
def knowledge_update(kb_id):
    d = _body()
    fields = {k: d[k] for k in ("name", "base_url", "description", "enabled", "api_key")
              if k in d}
    try:
        rag.kb_update(kb_id, **fields)
    except rag.RegistryError as e:
        return jsonify({"error": str(e)}), 400
    return jsonify({"ok": True, "bases": rag.kb_list()})


@bp_knowledge.post("/api/knowledge/<kb_id>/delete")
@admin_required
def knowledge_delete(kb_id):
    if not rag.kb_delete(kb_id):
        return jsonify({"error": "対象のナレッジベースが見つかりません。"}), 404
    return jsonify({"ok": True, "bases": rag.kb_list()})


@bp_knowledge.post("/api/knowledge/<kb_id>/test")
@admin_required
def knowledge_test(kb_id):
    """接続テスト。

    つながらないのは「この画面で確かめたい結果」であってAPIの失敗ではないので、
    200 に ok:false を載せて返す。500 にすると、画面側はネットワークの不調と
    区別できず、原因の文面も出せない。
    """
    try:
        return jsonify(rag.kb_test(kb_id))
    except rag.RegistryError as e:
        return jsonify({"error": str(e)}), 404
    except rag.RagError as e:
        return jsonify({"ok": False, "error": str(e)})
    except Exception as e:                       # 想定外でも画面には理由を出す
        return jsonify({"ok": False, "error": f"接続テストでエラー: {e}"})


@bp_knowledge.get("/api/knowledge/<kb_id>/key")
@admin_required
def knowledge_key(kb_id):
    """APIキーの実値を返す（「表示」ボタン）。

    一覧に埋め込まないのは、管理画面を開くたびにキーがHTMLとして流れ、
    キャッシュやソース表示に残るため。押されたときだけ取りに行く。
    """
    env = rag.kb_get(kb_id, include_secrets=True)
    if env is None:
        return jsonify({"error": "対象のナレッジベースが見つかりません。"}), 404
    return jsonify({"ok": True, "api_key": env.get("api_key") or ""})


# =============================================================================
# 利用者ごとの検索対象と検索設定（チャットのサイドバー）
# =============================================================================

def knowledge_prefs_payload() -> dict:
    """チャット画面のサイドバーに渡す一式。"""
    off = set(rag.rag_excluded_ids(g.user))
    return {
        "bases": [{"id": e["id"], "name": e["name"],
                   "description": e.get("description") or "",
                   "on": e["id"] not in off}
                  for e in rag.kb_enabled()],
        "settings": rag.rag_user_settings(g.user),
        "defaults": rag.rag_defaults(),
        "fields": rag.rag_form_fields(),
    }


@bp_chat.post("/api/tables/prefs")
@login_required
def tables_prefs_save():
    """分析の対象から外した表を保存する（利用者ごと）。"""
    d = _body()
    known = set()
    for f in db.list_db_files():
        known |= set(catalog.profile_db(f)["tables"].keys())
    # いま実在する表だけ残す。消えた表の名前を持ち続けても意味がない
    off = d.get("off") or []
    if not isinstance(off, (list, tuple)):
        return jsonify({"error": "外す表の指定が正しくありません。"}), 400
    prefs.set_value(g.user, "tables_off",
                    [str(t) for t in off if str(t) in known])
    return jsonify({"ok": True, "off": rag.excluded_tables(g.user)})


@bp_knowledge.post("/api/knowledge/prefs")
@login_required
def knowledge_prefs_save():
    d = _body()
    if "off" in d:
        # 実在するidだけ残す。消えた環境のidを持ち続けても意味がなく、
        # 同じidが再利用されることもない。
        known = {e["id"] for e in rag.kb_list()}
        off = d.get("off") or []
        if not isinstance(off, (list, tuple)):
            return jsonify({"error": "外す文書の指定が正しくありません。"}), 400
        prefs.set_value(g.user, "rag_off",
                        [str(i) for i in off if str(i) in known])
    if "settings" in d:
        try:
            cleaned = rag.rag_validate_settings(d.get("settings") or {})
        except (ValueError, TypeError) as e:
            return jsonify({"error": str(e)}), 400
        # 初期値と同じ項目は保存しない。管理者が env の既定を変えたとき、
        # 明示的に設定を変えていない利用者はその新しい既定に追随する。
        base = rag.rag_defaults()
        prefs.set_value(g.user, "rag_settings",
                        {k: v for k, v in cleaned.items() if v != base.get(k)})
    return jsonify({"ok": True, **knowledge_prefs_payload()})


# ==========================================================================
# ===== 元 web/table_bp.py
# テーブル全体を見る画面。
#
# サンプル行（先頭数行）だけでは「本当にこのテーブルでよいか」が分からないので、
# 中身を1ページずつ辿れる読み取り専用のビューアを別タブで開けるようにする。
#
# ・読むのは db.connect_ro（読み取り専用接続）だけ。書き込みの経路は持たない。
# ・行数が多いテーブルでも落ちないよう、常にサーバ側で LIMIT/OFFSET を付けて返す。
# ・絞り込みは全列を文字として LIKE する素朴なもの。値はプレースホルダで渡す
#   （列名は実在する列名と照合してからでないと SQL に入れない）。
# ==========================================================================
import json

from flask import Blueprint, jsonify, render_template, request

import catalog
import db


# =============================================================================
# ===== 利用状況（管理者のみ）
# 「誰が・何を・どれだけ・どう使ったか」を見る画面。
#
# 集計そのものは既にある（元 usage.py の analyze）。この節が足すのは
#   - その結果を表とグラフで見せる画面
#   - 全利用者のチャット履歴を読む口
#   - 見ているものをそのまま Excel に出す口
# だけで、数え方は増やさない（チャットの analyze_usage と同じ数字が出る）。
#
# 他人の質問文がそのまま見えるので、入口は管理者だけに開ける。
# =============================================================================

bp_usage = Blueprint("usage", __name__)

#: 画面のタブ。キーは usage.METHODS のもの＋imports。
USAGE_VIEWS = [
    {"key": "summary",   "label": "全体像"},
    {"key": "users",     "label": "利用者"},
    {"key": "trend",     "label": "推移"},
    {"key": "tools",     "label": "使われた機能"},
    {"key": "databases", "label": "使われたデータ"},
    {"key": "errors",    "label": "失敗"},
    # 取り込みの記録はカタログ画面の「更新履歴」で見られるので、ここには出さない
    # （集計そのものは残してあり、チャットの analyze_usage からは今も呼べる）。
    # 質問は「チャット履歴」と1つのタブにまとめている（質問→その会話を開く）。
    # 集計としては残す（Excel出力もこのキーで作る）が、単独のタブは出さない。
    {"key": "questions", "label": "質問・履歴", "merged": True},
]

#: 期間の選択肢。None は全期間。
USAGE_RANGES = [{"days": 7, "label": "直近7日"}, {"days": 30, "label": "直近30日"},
                {"days": 90, "label": "直近90日"}, {"days": 0, "label": "全期間"}]


def usage_users() -> list[str]:
    """会話ファイルを持っている利用者の一覧。"""
    root = Path(config.USER_META_DIR)
    if not root.exists():
        return []
    return sorted(d.name for d in root.iterdir()
                  if d.is_dir() and (d / "chats").exists())


def _usage_result(method: str, days, user):
    """集計を1つ実行して、画面が使う形に整える。"""
    res = usage.analyze(method, days=days or None, user=user or None)
    return {"title": res.get("title") or "", "notes": res.get("notes") or [],
            "tables": [{"title": t.get("title") or "",
                        "columns": list(t.get("columns") or []),
                        "rows": [list(r) for r in (t.get("rows") or [])]}
                       for t in (res.get("tables") or [])]}


@bp_usage.get("/usage", endpoint="index")
@admin_required
def usage_index():
    return render_template("usage.html", views=USAGE_VIEWS,
                           ranges=USAGE_RANGES, users=usage_users())


@bp_usage.get("/api/usage/report")
@admin_required
def usage_report():
    method = (request.args.get("method") or "summary").strip()
    if method not in {v["key"] for v in USAGE_VIEWS}:
        return jsonify({"error": "その集計はありません。"}), 400
    try:
        days = int(request.args.get("days") or 0)
    except ValueError:
        days = 0
    try:
        return jsonify(_usage_result(method, days, (request.args.get("user") or "").strip()))
    except Exception as e:
        return jsonify({"error": f"集計に失敗しました: {e}"}), 500


def _qa_pairs(log: list, created: str) -> list[dict]:
    """会話の表示物から「質問と、その回答」の対を作る。

    回答は、その質問の後・次の質問の前に出た AI の文章をつなげたもの。
    表・グラフ・ファイルは本文を持たないので、種類だけを [表] のように残す
    （何をして答えたのかが1行で分かるようにするため）。
    """
    marks = {"table": "［表］", "chart": "［グラフ］", "sql": "［SQL］",
             "file": "［ファイル］", "error": "［失敗］"}
    out: list[dict] = []
    cur: dict | None = None
    for x in log:
        role, kind = x.get("role") or "", x.get("kind") or ""
        if role == "user" and kind == "text":
            if cur:
                out.append(cur)
            cur = {"at": str(x.get("at") or created)[:16].replace("T", " "),
                   "text": str(x.get("content") or "")[:500], "answer": "", "marks": []}
            continue
        if cur is None:
            continue                       # 最初の質問より前のものは、誰の答えでもない
        if role == "assistant" and kind == "text" and x.get("content"):
            cur["answer"] = (cur["answer"] + " " + str(x["content"])).strip()[:1000]
        elif kind in marks and marks[kind] not in cur["marks"]:
            cur["marks"].append(marks[kind])
    if cur:
        out.append(cur)
    return out


@bp_usage.get("/api/usage/chats")
@admin_required
def usage_chats():
    """全利用者の会話一覧（質問と回答つき）。"""
    try:
        days = int(request.args.get("days") or 0)
    except ValueError:
        days = 0
    out = _chat_rows(days, (request.args.get("user") or "").strip())
    return jsonify({"chats": out[:500], "total": len(out)})


_QA_COLUMNS = ["日時", "利用者", "会話ID", "会話", "質問", "回答"]


def _qa_rows(days: int, who: str) -> list[list]:
    """「質問と回答」1行ぶんの配列（_QA_COLUMNS と同じ並び）。Excelの2箇所で使う。"""
    return [[q["at"], c["user"], c["id"], c["title"] or "（無題）", q["text"],
             (" ".join(q["marks"]) + " " + q["answer"]).strip()]
            for c in _chat_rows(days, who)
            for q in c["questions"]]


def _chat_rows(days: int, who: str) -> list[dict]:
    """会話1本を1レコードに畳む（質問と回答の対つき）。画面とExcelで共用。"""
    limit = datetime.now() - timedelta(days=days) if days else None
    out = []
    root = Path(config.USER_META_DIR)
    for f in sorted(root.glob("*/chats/*.json"), reverse=True):
        if f.name == "index.json":
            continue
        owner = f.parent.parent.name
        if who and owner != who:
            continue
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue                       # 壊れた1本で一覧を止めない
        created = str(data.get("created_at") or "")
        if limit and created and created[:19] < limit.strftime("%Y-%m-%dT%H:%M:%S"):
            continue
        log = data.get("render_log") or []
        title = data.get("title") or ""
        asked = [x for x in log if x.get("role") == "user" and x.get("kind") == "text"]
        out.append({
            "id": data.get("id") or f.stem, "user": owner, "title": title,
            "created_at": created[:16].replace("T", " "),
            "turns": len(asked),
            "errors": sum(1 for x in log if x.get("kind") == "error"),
            "last_at": str((log[-1].get("at") if log else "") or "")[:16].replace("T", " "),
            # 質問と、その質問に対する回答の対。画面はこれを1行として表に出す。
            "questions": _qa_pairs(log, created)[:50],
        })
    return out


@bp_usage.post("/api/usage/export")
@admin_required
def usage_export():
    """いま見ている条件のまま Excel にする。1つの集計＝1シート。"""
    body = _body()
    methods = [m for m in (body.get("methods") or [])
               if m in {v["key"] for v in USAGE_VIEWS}]
    if not methods:
        return jsonify({"error": "出力する集計が選ばれていません。"}), 400
    try:
        days = int(body.get("days") or 0)
    except (TypeError, ValueError):
        days = 0
    who = (body.get("user") or "").strip()
    labels = {v["key"]: v["label"] for v in USAGE_VIEWS}

    sheets = []
    for m in methods:
        # 「質問・履歴」タブは画面が質問と回答の表なので、その表をそのまま出す
        try:
            res = _usage_result(m, days, who)
        except Exception as e:
            return jsonify({"error": f"{labels[m]} の集計に失敗しました: {e}"}), 500
        if m == "questions":
            # 画面と同じもの（質問と回答の表）だけを出す。集計側の
            # 「直近の質問（最大40件）」はこの表に含まれるので重ねない
            sheets.append({"name": "質問と回答",
                           "columns": _QA_COLUMNS, "rows": _qa_rows(days, who),
                           "note": "／".join(res["notes"][:2])})
            continue
        for i, t in enumerate(res["tables"]):
            name = labels[m] + (f"-{i + 1}" if len(res["tables"]) > 1 else "")
            sheets.append({"name": name, "columns": t["columns"], "rows": t["rows"],
                           "note": "／".join(res["notes"][:2])})
    # 元データ（明細）も一緒に出す。集計の根拠をExcel側でも辿れるように、
    # どのタブの出力にも「質問と回答」と「会話」の明細を付ける
    # （質問・履歴タブでは質問と回答が本体なので、会話の明細だけ足す）。
    if "questions" not in methods:
        sheets.append({"name": "明細（質問と回答）",
                       "columns": _QA_COLUMNS, "rows": _qa_rows(days, who),
                       "note": "1行 = 1つの質問と、その回答。集計の元になった記録です。"})
    recs = usage.collect(days=days or None, user=who or None)
    conv_rows = [[(f"{r['created']:%Y-%m-%d %H:%M}" if r["created"] else ""),
                  r["user"], r["id"], r["title"] or "（無題）",
                  len(r["questions"]), r["sqls"], r["charts"], r["files"],
                  len(r["errors"]) + len(r["orphan_errors"]),
                  "、".join(sorted(set(r["tools"])))]
                 for r in recs]
    sheets.append({"name": "明細（会話）",
                   "columns": ["開始日時", "利用者", "会話ID", "会話", "質問数",
                               "SQL実行", "グラフ", "ファイル", "失敗", "使ったツール"],
                   "rows": conv_rows,
                   "note": "1行 = 1つの会話。集計はこの明細から数えています。"})

    if not sheets:
        return jsonify({"error": "出せる表がありませんでした。"}), 400

    cond = [labels[m] for m in methods]
    span = next((r["label"] for r in USAGE_RANGES if r["days"] == days), "全期間")
    try:
        data = excel.build_excel(sheets, title="利用状況 " + "・".join(cond))
    except Exception as e:
        return jsonify({"error": f"Excelの作成に失敗しました: {e}"}), 500
    fname = exports.safe_filename(f"利用状況_{span}" + (f"_{who}" if who else ""), "xlsx")
    token = _fs_put(data, fname, exports.XLSX_MIME, g.user.username)
    return jsonify({"ok": True, "url": f"/api/file/{token}", "filename": fname,
                    "sheets": len(sheets)})


bp_help = Blueprint("help", __name__)


@bp_help.get("/help", endpoint="index")
@login_required
def help_index():
    """全機能の説明書と、システム構成の説明。文章は TEMPLATES の help.html に全部書いてある。

    サーバ一覧（管理者向け）・「まとまりとテーブルの一覧」・「ツール一覧」は、
    いまの登録簿・DB・カタログから動的に描く。手で書くと、足した・改名した・
    無効化したときにヘルプが古いままになるため。"""
    groups_now = []
    total_tables = 0
    metas = []
    for f in db.list_db_files():
        prof = catalog.profile_db(f)
        meta = catalog.load_meta(f)
        metas.append(meta)
        gmeta = catalog.db_groups(meta)
        by_g: dict = {}
        for t in sorted(prof["tables"]):
            if "__" not in t:
                continue
            gkey, _, rest = t.partition("__")
            by_g.setdefault(gkey, []).append(
                {"suffix": rest, "rows": (prof["tables"][t] or {}).get("row_count")})
            total_tables += 1
        for gkey in sorted(by_g):
            groups_now.append({"key": gkey, "tables": by_g[gkey],
                               "memo": bool((gmeta.get(gkey) or {}).get("description"))})

    # ツール一覧: 実行時と同じ合成（管理者の無効化・説明の差し替え・ユーザー定義追加が映る）
    def _first_sentence(text: str, limit: int = 90) -> str:
        s = str(text or "").strip().splitlines()[0] if text else ""
        s = s.split("。")[0]
        return (s[:limit] + "…") if len(s) > limit else (s + "。" if s else "")

    over = builtin_overrides([{"meta": m} for m in metas])
    tools_now = []
    for t in tools.BUILTIN_TOOLS:
        name = t["function"]["name"]
        if name in tools.ADMIN_TOOLS and not g.user.is_admin:
            continue                       # AIに渡らないツールは一覧にも出さない
        ov = over.get(name) or {}
        tools_now.append({
            "kind": "組み込み", "name": name, "label": TOOL_LABELS.get(name, ""),
            "desc": _first_sentence(ov.get("description")
                                    or t["function"].get("description")),
            "enabled": ov.get("enabled") is not False})
    for m in metas:
        for t in (m.get("tools") or []):
            if isinstance(t, dict) and str(t.get("name") or "").strip():
                tools_now.append({
                    "kind": "ユーザー定義", "name": str(t["name"]), "label": "",
                    "desc": _first_sentence(t.get("description")),
                    "enabled": t.get("enabled") is not False})

    return render_template("help.html",
                           bases=rag.kb_list() if g.user.is_admin else [],
                           groups_now=groups_now, total_tables=total_tables,
                           tools_now=tools_now)


bp_table = Blueprint("tableview", __name__)

PAGE_SIZES = (50, 100, 200, 500)
MAX_LIMIT = 500


def _w_qi(name: str) -> str:
    return '"' + str(name).replace('"', '""') + '"'


def _resolve(db_name: str, table: str):
    """DBファイルとテーブル名を確かめる。

    db は 'sales.db'（ファイル名）でも 'sales'（エイリアス）でも受ける。
    ER図やチャットからはエイリアスで来るため。
    """
    files = db.list_db_files()
    path = next((f for f in files if f.name == db_name), None)
    if path is None:
        path = next((f for f in files if db.alias_for(f) == db_name), None)
    if path is None:
        return None, None, f"DB '{db_name}' が見つかりません。"
    names = list((catalog.profile_db(path).get("tables") or {}).keys())
    if table not in names:
        return path, None, f"テーブル '{table}' が {path.name} にありません。"
    return path, table, None


@bp_table.get("/table", endpoint="index")
@login_required
def table_index():
    """別タブで開くビューア本体。中身は table.js が API から取ってくる。"""
    db_name = request.args.get("db") or ""
    table = request.args.get("table") or ""
    path, tname, err = _resolve(db_name, table)
    meta = catalog.load_meta(path) if path else {}
    tmeta = ((meta.get("tables") or {}).get(tname) or {}) if tname else {}
    return render_template(
        "table.html",
        nav="tableview",
        db_file=path.name if path else db_name,
        db_title=meta.get("title") or "",
        table=tname or table,
        description=tmeta.get("description") or "",
        error=err or "",
        page_sizes=list(PAGE_SIZES),
    )


def _like(text: str) -> str:
    """LIKE のワイルドカードを打ち消して、入力された文字そのものを探す。"""
    return "%" + text.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_") + "%"


def _filters_sql(raw: str, cols: list[str]) -> tuple:
    """列ごとの絞り込み（Excelのフィルターに相当）を WHERE 句にする。

    raw は画面から来るJSON:
      {"店舗コード": {"values": ["S01", null]},        … 選んだ値だけ（null は NULL 行）
       "売上金額":   {"op": ">=", "value": "100000"},  … 数の比較
       "顧客名":     {"op": "contains", "value": "商事"}}
    列名は実在するものだけを通し、値は必ずプレースホルダで渡す。
    """
    try:
        spec = json.loads(raw) if raw else {}
    except (TypeError, ValueError):
        return "", [], {}
    if not isinstance(spec, dict):
        return "", [], {}

    OPS = {"=": "=", "!=": "<>", ">": ">", ">=": ">=", "<": "<", "<=": "<="}
    clauses, params, used = [], [], {}
    for col, f in spec.items():
        if col not in cols or not isinstance(f, dict):
            continue
        q = _w_qi(col)
        vals = f.get("values")
        if isinstance(vals, list) and vals:
            # 値の選択。NULL は IN で拾えないので別に足す
            plain = [v for v in vals if v is not None]
            parts = []
            if plain:
                parts.append(f"CAST({q} AS TEXT) IN ({', '.join('?' for _ in plain)})")
                params.extend(str(v) for v in plain)
            if any(v is None for v in vals):
                parts.append(f"{q} IS NULL")
            if parts:
                clauses.append("(" + " OR ".join(parts) + ")")
                used[col] = f
            continue
        op, value = str(f.get("op") or ""), f.get("value")
        if op in ("contains", "not_contains") and str(value or "") != "":
            neg = "NOT " if op == "not_contains" else ""
            clauses.append(f"CAST({q} AS TEXT) {neg}LIKE ? ESCAPE '\\'")
            params.append(_like(str(value)))
            used[col] = f
        elif op in OPS and str(value or "") != "":
            # 数として比較できるなら数で、無理なら文字で比べる
            try:
                num = float(value)
                clauses.append(f"CAST({q} AS REAL) {OPS[op]} ?")
                params.append(num)
            except (TypeError, ValueError):
                clauses.append(f"CAST({q} AS TEXT) {OPS[op]} ?")
                params.append(str(value))
            used[col] = f
        elif op == "empty":
            clauses.append(f"({q} IS NULL OR CAST({q} AS TEXT) = '')")
            used[col] = f
        elif op == "not_empty":
            clauses.append(f"({q} IS NOT NULL AND CAST({q} AS TEXT) <> '')")
            used[col] = f
    return (" AND ".join(clauses), params, used)


@bp_table.get("/api/table/rows")
@login_required
def rows():
    """1ページぶんの行。offset/limit・絞り込み・並べ替えはすべてサーバ側で行う。"""
    path, table, err = _resolve(request.args.get("db") or "", request.args.get("table") or "")
    if err:
        return jsonify({"error": err}), 404

    try:
        offset = max(0, int(request.args.get("offset") or 0))
        limit = int(request.args.get("limit") or 100)
    except ValueError:
        return jsonify({"error": "表示位置の指定が正しくありません。"}), 400
    limit = max(1, min(MAX_LIMIT, limit))
    q = (request.args.get("q") or "").strip()
    sort = request.args.get("sort") or ""
    desc = (request.args.get("dir") or "asc").lower() == "desc"

    conn = db.connect_ro(path)
    try:
        cols = [r[1] for r in conn.execute(f"PRAGMA table_info({_w_qi(table)})")]
        if sort and sort not in cols:        # 実在しない列名は SQL に入れない
            sort = ""
        conds, params = [], []
        if q:
            # 全列を文字として見て部分一致。数値列も CAST して同じ扱いにする
            conds.append("(" + " OR ".join(
                f"CAST({_w_qi(c)} AS TEXT) LIKE ? ESCAPE '\\'" for c in cols) + ")")
            params.extend([_like(q)] * len(cols))
        fsql, fparams, used = _filters_sql(request.args.get("filters") or "", cols)
        if fsql:
            conds.append(fsql)
            params.extend(fparams)
        where = (" WHERE " + " AND ".join(conds)) if conds else ""

        total = conn.execute(f"SELECT COUNT(*) FROM {_w_qi(table)}").fetchone()[0]
        matched = (conn.execute(f"SELECT COUNT(*) FROM {_w_qi(table)}{where}", params).fetchone()[0]
                   if where else total)
        order = f" ORDER BY {_w_qi(sort)} {'DESC' if desc else 'ASC'}" if sort else ""
        cur = conn.execute(
            f"SELECT * FROM {_w_qi(table)}{where}{order} LIMIT ? OFFSET ?", [*params, limit, offset])
        data = [list(r) for r in cur.fetchall()]
    except Exception as e:                   # 壊れたDB・読めないテーブルでも画面は保つ
        return jsonify({"error": f"読み取りに失敗しました: {e}"}), 400
    finally:
        conn.close()

    return jsonify({"ok": True, "columns": cols, "rows": jsonable(data),
                    "total": total, "matched": matched,
                    "offset": offset, "limit": limit,
                    "sort": sort, "dir": "desc" if desc else "asc",
                    "filters": used})


@bp_table.get("/api/table/values")
@login_required
def values():
    """1列の値の一覧（Excelのフィルターで出る候補）。多い順に返す。

    種類が多すぎる列（IDなど）は全部返しても選べないので、上限で切って
    「絞り込んで探す」に誘導する（truncated で画面に伝える）。
    """
    path, table, err = _resolve(request.args.get("db") or "", request.args.get("table") or "")
    if err:
        return jsonify({"error": err}), 404
    column = request.args.get("column") or ""
    q = (request.args.get("q") or "").strip()
    limit = 300

    conn = db.connect_ro(path)
    try:
        cols = [r[1] for r in conn.execute(f"PRAGMA table_info({_w_qi(table)})")]
        if column not in cols:
            return jsonify({"error": f"列 '{column}' がありません。"}), 404
        c = _w_qi(column)
        where, params = "", []
        if q:
            where = f" WHERE CAST({c} AS TEXT) LIKE ? ESCAPE '\\'"
            params = [_like(q)]
        kinds = conn.execute(f"SELECT COUNT(DISTINCT {c}) FROM {_w_qi(table)}").fetchone()[0]
        cur = conn.execute(
            f"SELECT {c} AS v, COUNT(*) AS n FROM {_w_qi(table)}{where} "
            f"GROUP BY v ORDER BY n DESC, v LIMIT ?", [*params, limit + 1])
        rows_ = cur.fetchall()
    except Exception as e:
        return jsonify({"error": f"値を読めませんでした: {e}"}), 400
    finally:
        conn.close()

    truncated = len(rows_) > limit
    return jsonify({"ok": True, "column": column, "kinds": kinds, "truncated": truncated,
                    "values": [{"value": jsonable(v), "count": n} for v, n in rows_[:limit]]})


# ==========================================================================
# ===== 元 web/api_bp.py
# 細々したAPI: 生成ファイルのダウンロードと plotly.js の配信。
# ==========================================================================
from pathlib import Path

from flask import Blueprint, Response, abort, g, send_file


bp_api = Blueprint("api", __name__)


@bp_api.get("/api/file/<token>")
@login_required
def download(token: str):
    item = _fs_get(token, g.user.username)
    if item is None:
        abort(404)
    from io import BytesIO
    return send_file(BytesIO(item["data"]), mimetype=item["mime"],
                     as_attachment=True, download_name=item["filename"])


@bp_api.get("/vendor/plotly.min.js")
def plotly_js():
    """plotly パッケージ同梱のJSをそのまま配る（CDNに出ない・オフラインで動く）。"""
    import plotly
    p = Path(plotly.__file__).parent / "package_data" / "plotly.min.js"
    if not p.exists():
        abort(404)
    return Response(p.read_bytes(), mimetype="application/javascript",
                    headers={"Cache-Control": "public, max-age=604800"})


# ==========================================================================
# ===== 元 web/__init__.py
# Flask アプリ本体（アプリファクトリ）。
#
# 画面まわりだけをここに置き、業務ロジックは既存モジュールをそのまま使う。
#   db / catalog / llm / tools / custom_tools / charts / exports / excel / analysis
#   auth / chats / importer / jobs / scheduler
#
# Streamlit 版との違いは「状態の持ち方」だけ。
#   Streamlit: st.session_state（プロセス内）
#   Flask    : サーバ側セッション + 会話の実体は chats.py（ファイル）
# ==========================================================================
import os
import secrets

from flask import Flask
from jinja2 import DictLoader

import auth
import config
import scheduler

_SECRET_FILE = config.BASE_DIR / ".flask_secret"


def _secret_key() -> str:
    """セッション署名鍵。再起動でログアウトさせないためファイルに保持する。"""
    env = os.getenv("FLASK_SECRET_KEY", "").strip()
    if env:
        return env
    if _SECRET_FILE.exists():
        return _SECRET_FILE.read_text(encoding="utf-8").strip()
    key = secrets.token_urlsafe(48)
    _SECRET_FILE.write_text(key, encoding="utf-8")
    try:
        os.chmod(_SECRET_FILE, 0o600)
    except OSError:
        pass
    return key


def _ensure_default_db() -> None:
    """data/ に .db が無ければ、空のデータベースを用意する。

    このアプリはDBを常に1つだけ持つ設計で、利用者がDBを作る・選ぶという
    操作は存在しない。初回起動のここで受け皿を作っておけば、
    最初から「取り込む→テーブルが増える」だけの世界になる。
    """
    if db.list_db_files():
        return
    path = config.DATA_DIR / "データ.db"
    sqlite3.connect(path).close()          # 空ファイル＝SQLiteとして有効な空DB
    catalog.save_meta(path, {"title": "データ"})
    print(f"[app] 初回起動: 空のデータベースを用意しました（data/{path.name}）")


def _warn_if_no_admin() -> None:
    """管理者が1人も居ない設定なら、起動時に知らせる。

    認証APIがグループを返さない構成では、管理者になれるのは auth.py の ADMIN_PASS で
    入る admin だけになる。これを設定し忘れると、カタログ・取り込み・モデル・メールの
    画面に誰も入れないまま動き続ける。気づけるのは「設定を直したいとき」なので、
    起動時に言う。
    """
    if auth.admin_enabled():
        return
    try:
        provider = auth.get_provider()
    except auth.AuthError:
        return
    if provider.name == "local":
        has_admin = any(auth.AUTH_ADMIN_GROUP in (u.get("groups") or [])
                        for u in (auth.load_users_file().get("users") or []))
        if has_admin:
            return
        how = "python core.py users add <ユーザー名> --admin で管理者を作るか、"
    else:
        # 認証APIがグループを返さないなら、ここに来た時点で管理者は現れない
        how = f"認証APIが '{auth.AUTH_ADMIN_GROUP}' グループを返すようにするか、"
    print(f"[auth] 警告: 管理者が1人も居ません。{how}"
          "auth.py の ADMIN_PASS を設定してください。"
          "このままではデータカタログ・データ取り込み・モデル設定・メール設定を"
          "誰も開けません（チャットは使えます）。")


def create_app() -> Flask:
    # 画面ファイル（HTML/CSS/JS）はファイルではなく本ファイル末尾の
    # TEMPLATES / STATIC_FILES から配る
    app = Flask(__name__, static_folder=None)
    app.jinja_loader = DictLoader(TEMPLATES)
    app.add_url_rule("/static/<path:filename>", endpoint="static",
                     view_func=_static_file)
    app.config.update(
        SECRET_KEY=_secret_key(),
        MAX_CONTENT_LENGTH=64 * 1024 * 1024,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        JSON_AS_ASCII=False,
    )

    app.register_blueprint(bp_auth)
    app.register_blueprint(bp_chat)
    app.register_blueprint(bp_catalog)
    app.register_blueprint(bp_import)
    app.register_blueprint(bp_mail)
    app.register_blueprint(bp_models)
    app.register_blueprint(bp_knowledge)
    app.register_blueprint(bp_usage)
    app.register_blueprint(bp_help)
    app.register_blueprint(bp_table)
    app.register_blueprint(bp_api)

    app.before_request(load_user_into_context)
    app.teardown_request(_release_chat)      # 会話の鍵を必ず返す
    app.context_processor(inject_globals)

    _warn_if_no_admin()
    _ensure_default_db()

    @app.after_request
    def _no_html_cache(res):
        """画面のHTMLはキャッシュさせない。

        中身はログイン中の人・選択中のDB・カタログの現状で毎回変わるので、
        取っておいても正しくない。既定ではキャッシュ指定が付かず、ブラウザが
        独自の判断で古い画面を出すため、直したはずの表示が変わらないことがある。
        静的ファイル（CSS/JS）は ETag で更新を見ているのでそのまま。
        """
        if res.mimetype == "text/html":
            res.headers["Cache-Control"] = "no-store"
        return res

    # 定期取り込みの裏スレッド。Streamlit版と同じく cron 不要。
    # Flask では起動時に1回通るので、誰かがページを開くのを待たずに動き出す。
    scheduler.start()
    return app


# ==========================================================================
# ===== 元 manage_users.py（CLI: python core.py users …）
# ==========================================================================
"""ローカル認証のユーザー管理（LDAP導入までの暫定アカウント用）。

  python core.py users list
  python core.py users add onoke --admin
  python core.py users passwd onoke
  python core.py users remove onoke

パスワードはプロンプトで入力する（画面に表示されない）。
保存されるのは PBKDF2-SHA256 のハッシュで、平文は保存しない。

社内LDAP認証APIに切り替えた後は、このファイルと auth_users.yaml は不要になる。
"""

import argparse
import getpass
import sys

import auth
import config


def _mu_find(users: list, username: str):
    for i, u in enumerate(users):
        if str(u.get("username", "")).lower() == username.lower():
            return i
    return -1


def _mu_ask_password(password: str | None) -> str:
    if password:
        print("警告: コマンドラインで渡したパスワードは履歴に残ります。", file=sys.stderr)
        return password
    p1 = getpass.getpass("パスワード: ")
    if not p1:
        sys.exit("パスワードが空です。")
    if p1 != getpass.getpass("パスワード（確認）: "):
        sys.exit("パスワードが一致しません。")
    return p1


def _mu_cmd_list(_args):
    users = auth.load_users_file().get("users") or []
    if not users:
        print("ユーザーは登録されていません。")
        return
    print(f"{'ユーザー名':<20} {'表示名':<20} グループ")
    for u in users:
        print(f"{u.get('username',''):<20} {u.get('display_name',''):<20} "
              f"{', '.join(u.get('groups') or []) or '-'}")


def _mu_cmd_add(args):
    data = auth.load_users_file()
    users = data.setdefault("users", [])
    if _mu_find(users, args.username) >= 0:
        sys.exit(f"'{args.username}' は既に存在します。パスワード変更は passwd を使ってください。")
    groups = [g.strip() for g in (args.groups or "").split(",") if g.strip()]
    if args.admin and auth.AUTH_ADMIN_GROUP not in groups:
        groups.append(auth.AUTH_ADMIN_GROUP)
    users.append({
        "username": args.username,
        "display_name": args.display_name or args.username,
        "password_hash": auth.hash_password(_mu_ask_password(args.password)),
        "groups": groups,
    })
    auth.save_users_file(data)
    print(f"追加しました: {args.username}"
          + (f"（{', '.join(groups)}）" if groups else ""))
    print(f"保存先: {auth.AUTH_USERS_FILE}")


def _mu_cmd_passwd(args):
    data = auth.load_users_file()
    users = data.get("users") or []
    i = _mu_find(users, args.username)
    if i < 0:
        sys.exit(f"'{args.username}' は存在しません。")
    users[i]["password_hash"] = auth.hash_password(_mu_ask_password(args.password))
    auth.save_users_file(data)
    print(f"パスワードを変更しました: {args.username}")


def _mu_cmd_remove(args):
    data = auth.load_users_file()
    users = data.get("users") or []
    i = _mu_find(users, args.username)
    if i < 0:
        sys.exit(f"'{args.username}' は存在しません。")
    users.pop(i)
    auth.save_users_file(data)
    print(f"削除しました: {args.username}")
    print("※ 個人カタログ（data/users/配下）は残ります。不要なら手動で削除してください。")


def users_cli(argv=None):
    ap = argparse.ArgumentParser(description="ローカル認証のユーザー管理")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list", help="一覧").set_defaults(func=_mu_cmd_list)

    a = sub.add_parser("add", help="追加")
    a.add_argument("username")
    a.add_argument("--display-name", default="")
    a.add_argument("--groups", default="", help="カンマ区切り")
    a.add_argument("--admin", action="store_true",
                   help=f"管理者グループ({auth.AUTH_ADMIN_GROUP})に入れる")
    a.add_argument("--password", help="非対話で渡す（履歴に残るので非推奨）")
    a.set_defaults(func=_mu_cmd_add)

    p = sub.add_parser("passwd", help="パスワード変更")
    p.add_argument("username")
    p.add_argument("--password")
    p.set_defaults(func=_mu_cmd_passwd)

    r = sub.add_parser("remove", help="削除")
    r.add_argument("username")
    r.set_defaults(func=_mu_cmd_remove)

    args = ap.parse_args(argv)
    args.func(args)
    return 0


# ==========================================================================
# ===== 元 refresh.py（CLI: python core.py refresh …）
# ==========================================================================
"""定期取り込みをコマンドから実行する（cron / タスクスケジューラ用）。

  python core.py refresh              期限が来たジョブだけ実行
  python core.py refresh --all        期限に関係なく全部実行（手動のみのジョブも含む）
  python core.py refresh --job <ID>   1本だけ実行
  python core.py refresh --list       ジョブの一覧を表示するだけ

Linuxサーバでの設定例（15分おきに期限チェック）:
  */15 * * * * cd /opt/aiagent && .venv/bin/python core.py refresh >> /var/log/aiagent-refresh.log 2>&1

ジョブごとの間隔は画面（🗄 データ取り込み → 🔁 定期取り込み）で設定する。
cron は「期限が来ているか」を見に行くだけなので、cron 側は細かく回しておけばよい。

終了コード: 0=全部成功（または対象なし） / 1=1本でも失敗
"""

import argparse
import sys
from datetime import datetime


import jobs


def _rf_stamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _rf_show(job: dict) -> str:
    nxt = jobs.next_run_at(job)
    return (f"{job.get('name') or job['id']}"
            f" [{job.get('db_file')} / {job.get('table')}"
            f" / {jobs.MODES.get(job.get('mode'), job.get('mode'))}"
            f" / {jobs.interval_label(job.get('interval_minutes', 0))}]"
            + ("" if job.get("enabled", True) else " (停止中)")
            + (f" 次回 {nxt:%Y-%m-%d %H:%M}" if nxt else ""))


def refresh_cli(argv=None) -> int:
    ap = argparse.ArgumentParser(description="定期取り込みの実行")
    ap.add_argument("--all", action="store_true", help="期限に関係なく全ジョブを実行")
    ap.add_argument("--job", help="指定したIDのジョブだけ実行")
    ap.add_argument("--list", action="store_true", help="一覧表示のみ")
    args = ap.parse_args(argv)

    all_jobs = jobs.list_jobs()
    if args.list:
        if not all_jobs:
            print("ジョブは登録されていません。")
        for j in all_jobs:
            print(" ", j["id"], _rf_show(j))
        return 0

    if args.job:
        target = jobs.get_job(args.job)
        if target is None:
            print(f"ジョブが見つかりません: {args.job}", file=sys.stderr)
            return 1
        targets = [target]
    elif args.all:
        targets = [j for j in all_jobs if j.get("enabled", True)]
    else:
        targets = jobs.due_jobs()

    if not targets:
        print(f"[{_rf_stamp()}] 実行対象はありません。")
        return 0

    failed = 0
    for j in targets:
        res = jobs.run_job(j)
        mark = "OK " if res["ok"] else "NG "
        print(f"[{_rf_stamp()}] {mark}{_rf_show(j)} -> {res['message']}")
        if res["degraded"]:
            print(f"        ※ TEXTに落とした列: {', '.join(res['degraded'])}")
        if not res["ok"]:
            failed += 1
    print(f"[{_rf_stamp()}] {len(targets)}件中 {len(targets) - failed}件成功 / {failed}件失敗")
    return 1 if failed else 0


# ==========================================================================
# ===== 画面ファイル（元 templates/*.html と static/css・js）
# ==========================================================================
# 画面のHTML（Jinja2テンプレート）とCSS・JSの実体。別ファイルにせず
# ここに文字列で持ち、create_app() が DictLoader と /static ルートで配る。
# 編集したらサーバを再起動して反映（Pythonコードと同じ扱い）。
# 各項目は「# --- ファイル名 ---」のコメント行で区切ってある。

_STATIC_CACHE: dict = {}
#: 拡張子と Content-Type の対応。werkzeug が text/* には charset=utf-8 を足す
_STATIC_MIME = {".css": "text/css", ".js": "text/javascript"}


def _static_file(filename: str):
    """/static/<filename> の配信。ETag 付きで、変わっていなければ 304 を返す。"""
    ent = _STATIC_CACHE.get(filename)
    if ent is None:
        body = STATIC_FILES.get(filename)
        if body is None:
            abort(404)
        data = body.encode("utf-8")
        mime = _STATIC_MIME.get(os.path.splitext(filename)[1].lower(),
                                "application/octet-stream")
        ent = _STATIC_CACHE[filename] = (data, mime, hashlib.md5(data).hexdigest())
    data, mime, etag = ent
    res = Response(data, mimetype=mime)
    res.set_etag(etag)
    return res.make_conditional(request)




# ==========================================================================
# ===== 起動（元 run.py）
# ==========================================================================
# 起動の設定はここだけで完結している（下の HOST / PORT / DEBUG）。
# env や環境変数は見ない。「ここに書いた値がそのまま使われる」ようにするため。
# 特に PORT は他のソフトが環境変数として設定していることがあり、それを読むと
# ここに 8000 と書いてあるのに違うポートで起動する、という事故が起きる。
#
# 待ち受けは waitress（1プロセス・マルチスレッドの本番用サーバ）。
# つまり開発も本番も同じ「python core.py」で起動できる。
# DEBUG = True にしたときだけ、エラー詳細が見える Flask 開発サーバに切り替わる。
#
# コマンドから直接起動したい場合は、下記も同等に使える（任意）。
# その場合 HOST / PORT はコマンド側で指定するので、ここの値は使われない。
#
#   waitress-serve --host=0.0.0.0 --port=8000 --threads=8 --call core:create_app
#   gunicorn -w 1 -b 0.0.0.0:8000 'core:create_app()'
#
# ワーカー（プロセス）は必ず 1 にすること。定期取り込みのスレッド（scheduler）が
# ワーカーの数だけ立ち、同じジョブを多重に実行してしまうため。
# 同時アクセス数を稼ぎたいときは、スレッド数（下の THREADS）で増やす。
#
# 回答の逐次表示（Server-Sent Events）を使うので、前段に nginx などを置く場合は
# そのパスだけバッファリングを切ること（proxy_buffering off;）。
# 切らないと、回答がまとめて届いて逐次表示にならない。

# --- 待ち受け先 -------------------------------------------------------------
# ここを書き換えれば起動先が変わる。
#
#   HOST = "0.0.0.0"    社内の他のPCからも開ける（本番はこちら）
#                       起動後は「サーバのIP:PORT」でアクセスする
#   HOST = "127.0.0.1"  起動したPCからだけ開ける（手元で試すとき）
#
# ポートが他のアプリと重なると起動に失敗する。その場合は PORT を変える。
HOST = "0.0.0.0"
PORT = 8000
# 同時にさばくリクエスト数（waitressのスレッド数）
THREADS = 8

# エラー画面に詳細を出すか。本番では必ず False のままにすること。
# True にすると、ブラウザからサーバ上で任意のコードを実行できてしまう。
DEBUG = False

if __name__ == "__main__":
    # --- CLI（サーバは起動しない） ------------------------------------------
    if len(sys.argv) > 1:
        _cmd, _rest = sys.argv[1], sys.argv[2:]
        if _cmd == "users":
            sys.exit(users_cli(_rest))
        if _cmd == "refresh":
            sys.exit(refresh_cli(_rest))
        if _cmd == "selftest":
            sys.exit(_sql_guard_selftest())
        sys.exit(f"不明なコマンド: {_cmd}（users / refresh / selftest のどれか。"
                 "サーバ起動は引数なしの python core.py）")

    app = create_app()
    if DEBUG:
        # デバッグ時だけ Flask 開発サーバ（エラー画面に詳細が出る）。
        # reloader を切っているのは、二重起動でスケジューラのスレッドが増えるのを避けるため
        app.run(host=HOST, port=PORT, debug=True,
                use_reloader=False, threaded=True)
    else:
        # 通常運転。waitress（本番用サーバ）で待ち受ける
        try:
            from waitress import serve
        except ImportError:
            print("[app] waitress が見つからないため、Flask開発サーバで起動します"
                  "（pip install -r requirements.txt で本番用サーバが入ります）")
            app.run(host=HOST, port=PORT, debug=False,
                    use_reloader=False, threaded=True)
        else:
            # flush: リダイレクト先がファイルだと serve() が先にブロックして
            # このメッセージがいつまでも書き出されないため
            print(f"[app] http://{HOST}:{PORT} で起動しました"
                  f"（waitress / threads={THREADS}）", flush=True)
            serve(app, host=HOST, port=PORT, threads=THREADS)
