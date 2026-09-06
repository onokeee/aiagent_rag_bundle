"""docs/ の文書を、対応する LightRAG サーバへ投入する。

    venv\\Scripts\\python.exe ingest.py            全部入れる
    venv\\Scripts\\python.exe ingest.py manual     1つだけ入れる

投入すると LightRAG がエンティティと関係を抽出して索引を作る。
ここで OpenAI（.env の LLM_MODEL / EMBEDDING_MODEL）を使うので、
文書の量に応じて費用がかかる。

同じ名前の文書が既に入っている場合、LightRAG は 409 を返す（上書きはしない）。
このスクリプトはそれを「済み」として飛ばすので、何度実行しても
新しい文書だけが入る。文書を入れ替えたいときは、サーバの管理画面
（http://127.0.0.1:962x）から先に削除すること。

索引作成は非同期で進む。投入した直後は検索しても0件で返るため、
このスクリプトは全ての文書が processed になるまで待ってから終了する。
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parent

# (ワークスペース名, ポート, APIキー, 表示名)
SERVERS = [
    ("manual",   9621, "key-manual-9621",   "設備マニュアル"),
    ("trouble",  9622, "key-trouble-9622",  "トラブル事例"),
    ("kaizen",   9623, "key-kaizen-9623",   "改善事例"),
    ("standard", 9624, "key-standard-9624", "作業標準"),
    # --- 製造部以外。毛色の違う領域を混ぜて、AIの選び分けを試せるようにしている ---
    ("kitei",     9625, "key-kitei-9625",     "社内規程"),
    ("sales",     9626, "key-sales-9626",     "営業ナレッジ"),
    ("itsupport", 9627, "key-itsupport-9627", "ITサポート"),
    # --- 拠点・部門展開ぶん（本社の7KBと同じ役割を、拠点ごとに持つ）---
    ("manual_kansai", 9628, "key-manual-kansai-9628", "設備マニュアル（関西工場）"),
    ("manual_kyushu", 9629, "key-manual-kyushu-9629", "設備マニュアル（九州工場）"),
    ("trouble_kansai", 9630, "key-trouble-kansai-9630", "トラブル事例（関西工場）"),
    ("trouble_kyushu", 9631, "key-trouble-kyushu-9631", "トラブル事例（九州工場）"),
    ("kaizen_kansai", 9632, "key-kaizen-kansai-9632", "改善事例（関西工場）"),
    ("standard_kansai", 9633, "key-standard-kansai-9633", "作業標準（関西工場）"),
    ("quality_kansai", 9634, "key-quality-kansai-9634", "品質基準（関西工場）"),
    ("kitei_overseas", 9635, "key-kitei-overseas-9635", "社内規程（海外赴任）"),
    ("kitei_parttime", 9636, "key-kitei-parttime-9636", "社内規程（契約社員）"),
    ("sales_overseas", 9637, "key-sales-overseas-9637", "営業ナレッジ（海外）"),
    ("sales_agency", 9638, "key-sales-agency-9638", "営業ナレッジ（代理店）"),
    ("itsupport_factory", 9639, "key-itsupport-factory-9639", "ITサポート（工場側）"),
    ("itsupport_overseas", 9640, "key-itsupport-overseas-9640", "ITサポート（海外拠点）"),
    ("safety", 9641, "key-safety-9641", "安全衛生"),
    ("weblinks", 9642, "key-weblinks-9642", "社内Webリンク集"),
]

#: 索引作成が「終わった」と言える状態。これ以外は途中とみなす。
#: LightRAG は pending / parsing / analyzing / processing … と段階が細かく、
#: 待機側で列挙すると必ず取りこぼす（実際 parsing と analyzing を見落として
#: 途中で抜けていた）。終わりの状態だけを数えるほうが確実。
DONE_STATES = {"processed", "failed"}


def headers(key: str) -> dict:
    return {"X-API-Key": key, "Content-Type": "application/json"}


def insert(port: int, key: str, path: Path) -> str:
    """1ファイルを本文として投入する。戻り値は "ok" / "skip" / "ng"。

    /documents/upload（ファイルアップロード）ではなく /documents/text を使う。
    アップロードはサーバ側の inputs フォルダを経由するため、文字コードや
    拡張子の扱いがサーバの設定に左右される。本文をそのまま渡すほうが確実。
    """
    body = {
        "text": path.read_text(encoding="utf-8"),
        # file_source は検索結果の file_path として返り、アプリ側では出典の
        # ファイル名として表示される。ここを空にすると出典が「どの文書か」を失う。
        "file_source": path.name,
    }
    r = requests.post(f"http://127.0.0.1:{port}/documents/text",
                      json=body, headers=headers(key), timeout=120)
    if r.status_code == 409:
        # 同じ名前の文書が既に入っている。エラーではなく「済み」として扱う
        # （入れ直しても二重にならないための、LightRAG 側の作法）。
        return "skip"
    if r.status_code >= 400:
        print(f"    NG   {path.name}: HTTP {r.status_code} {r.text[:160]}")
        return "ng"
    return "ok"


def statuses(port: int, key: str) -> dict:
    try:
        r = requests.get(f"http://127.0.0.1:{port}/documents",
                         headers=headers(key), timeout=30)
        if r.status_code >= 400:
            return {}
        return {k: len(v) for k, v in (r.json().get("statuses") or {}).items()}
    except requests.RequestException:
        return {}


def wait_done(port: int, key: str, timeout: int = 1800) -> None:
    """全ての文書が pending / processing でなくなるまで待つ。

    pipeline_status の busy だけを見ると、投入した直後はまだ処理が
    始まっておらず busy=False のため、その場で抜けてしまう。
    文書の状態そのものを見るほうが確実。
    """
    started = time.time()
    last = ""
    while time.time() - started < timeout:
        st = statuses(port, key)
        left = sum(n for k, n in st.items() if k.lower() not in DONE_STATES)
        line = "／".join(f"{k}:{n}" for k, n in sorted(st.items()))
        if line != last:
            print(f"    {line}")
            last = line
        if st and left == 0:
            return
        time.sleep(5)
    print("    （時間内に終わりませんでした。check-servers.ps1 で件数を確認してください）")


def main() -> int:
    only = sys.argv[1] if len(sys.argv) > 1 else ""
    targets = [s for s in SERVERS if not only or s[0] == only]
    if not targets:
        print(f"そのワークスペースはありません: {only}")
        print("使えるのは:", "、".join(s[0] for s in SERVERS))
        return 2

    for ws, port, key, label in targets:
        folder = HERE / "docs" / ws
        files = sorted(folder.glob("*.md"))
        print(f"\n■ {label}（port {port} / workspace {ws}）— 文書 {len(files)} 件")
        if not files:
            print("    文書がありません:", folder)
            continue
        try:
            requests.get(f"http://127.0.0.1:{port}/health", timeout=10)
        except requests.RequestException:
            print("    サーバが応答しません。start-servers.ps1 で起動してください。")
            continue

        result = [insert(port, key, f) for f in files]
        new = result.count("ok")
        print(f"    新規 {new} 件 / 済み {result.count('skip')} 件"
              f" / 失敗 {result.count('ng')} 件")
        if new:
            print("    索引作成を待ちます…")
            wait_done(port, key)
        print(f"    完了: {'／'.join(f'{k}:{n}' for k, n in sorted(statuses(port, key).items()))}")

    print("\n全て終わりました。アプリの「ナレッジベース」画面から接続テストを行ってください。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
