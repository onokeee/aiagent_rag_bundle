"""アプリ全体の設定値。環境変数（env ファイル）から読み込む。

設定は プロジェクト直下の env ファイルに書く（ドット無し）。
中身は shell と同じ書き方でよい:

    export OPENAI_API_KEY="sk-..."
    export DATA_DIR="/home/user/data"

`export ` は python-dotenv が読み飛ばすので、
`source env` で shell に読ませることもできる。
"""
import os
import re
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
# カレントディレクトリがどこでも読めるように、まず実行位置の ./env、
# 次にこのファイルと同じ場所の env を見る（どちらか一方があればよい）。
load_dotenv("./env")
load_dotenv(BASE_DIR / "env")

# --- パス設定 ---------------------------------------------------------------
# 分析対象の .db ファイルを置くフォルダ。サイドカーの .meta.yaml も同居する。
DATA_DIR = Path(os.getenv("DATA_DIR", str(BASE_DIR / "data")))
# 自動プロファイルのキャッシュ置き場（自動生成・編集不可）
PROFILE_CACHE_DIR = DATA_DIR / ".profile_cache"

# --- 取り込み（Excel/CSV → SQLite） -----------------------------------------
# 取り込み元として「許可する」フォルダ。ここに置かれたファイルしか読まない。
# 画面からパスを打たせない・許可フォルダの外へ出さないための土台なので、
# 広いフォルダ（C:\ や / やユーザーフォルダ直下など）を指定しないこと。
#
# 開発はWindows・本番はLinuxのマウント先、といった使い分けを想定して、
# 区切りは環境によらず ";" と改行。Linux では ":" も使える
# （Windowsで ":" を区切りにすると "C:\..." のドライブレターと衝突するため使わない）。
#   Windows: IMPORT_DIRS=C:\shared\取込用;D:\data\csv
#   Linux  : IMPORT_DIRS=/mnt/real/real2;/mnt/real/real3
def _split_dirs(raw: str) -> list:
    parts = re.split(r"[;\n]" if os.name == "nt" else r"[;:\n]", raw)
    return [Path(p.strip()).expanduser() for p in parts if p.strip()]


IMPORT_DIRS = _split_dirs(os.getenv("IMPORT_DIRS") or str(BASE_DIR / "import"))
# 画面から追加したフォルダの保存先。env の IMPORT_DIRS と合わせたものが許可リストになる。
# env 側は画面から消せない（管理者が決めた土台として残す）。
IMPORT_DIRS_FILE = Path(os.getenv("IMPORT_DIRS_FILE",
                                  str(DATA_DIR / "import_dirs.yaml"))).expanduser()
# 画面からフォルダを追加できるようにするか。false なら env の指定だけになる。
IMPORT_DIRS_EDITABLE = (os.getenv("IMPORT_DIRS_EDITABLE", "true").strip().lower()
                        in ("1", "true", "yes", "on"))
# 手元のPCからファイルをアップロードして取り込めるようにするか。
# 既定は無効。取り込み元は「サーバの許可フォルダ」に一本化しておくほうが、
# 誰がどのファイルを入れたか追いやすく、定期取り込みにもそのまま載せられる。
IMPORT_ALLOW_UPLOAD = (os.getenv("IMPORT_ALLOW_UPLOAD", "false").strip().lower()
                       in ("1", "true", "yes", "on"))
IMPORT_EXTENSIONS = (".csv", ".tsv", ".txt", ".xlsx", ".xlsm")
IMPORT_MAX_FILE_MB = int(os.getenv("IMPORT_MAX_FILE_MB", "100") or 100)
IMPORT_MAX_ROWS = int(os.getenv("IMPORT_MAX_ROWS", "1000000") or 1000000)
IMPORT_PREVIEW_ROWS = 30         # 取り込み前に画面で見せる行数
# 探索の深さ。0 = 無制限（既定）。指定フォルダより下は全部見る。
IMPORT_SCAN_DEPTH = int(os.getenv("IMPORT_SCAN_DEPTH", "0") or 0)
# ネットワーク共有で件数が膨らんだときに画面が固まらないための上限。
IMPORT_MAX_FILES = int(os.getenv("IMPORT_MAX_FILES", "2000") or 2000)

# --- 定期取り込み -----------------------------------------------------------
# 取り込み設定（ジョブ）の保存先。全ユーザー共通（DBファイル自体が共通のため）。
# cron から refresh.py を動かすときは、アプリと同じ場所を指すこと。
IMPORT_JOBS_FILE = Path(os.getenv("IMPORT_JOBS_FILE",
                                  str(DATA_DIR / "import_jobs.yaml"))).expanduser()
# アプリ内スケジューラ。アプリを起動している間、裏で定期取り込みを回す。
# cron や常駐サービスを別に用意しなくてよい（画面を誰も開いていなくても動く）。
IMPORT_SCHEDULER = (os.getenv("IMPORT_SCHEDULER", "true").strip().lower()
                    in ("1", "true", "yes", "on"))
# 何秒おきに「期限が来たジョブがあるか」を見に行くか。
IMPORT_SCHEDULER_TICK_SEC = int(os.getenv("IMPORT_SCHEDULER_TICK_SEC", "60") or 60)
# 追記(append)時に付ける取得日時の列名
IMPORT_TIMESTAMP_COLUMN = os.getenv("IMPORT_TIMESTAMP_COLUMN", "取得日時").strip() or "取得日時"

# --- 更新履歴 ---------------------------------------------------------------
# 「いつ・どこから・何行入ったか」の記録。ジョブ定義側は直前の1回しか持たないので、
# さかのぼって追えるように別ファイルに追記していく（1行1件のJSON）。
IMPORT_HISTORY_FILE = Path(os.getenv("IMPORT_HISTORY_FILE",
                                     str(DATA_DIR / "import_history.jsonl"))).expanduser()
# 残す件数の上限。超えたら古いものから捨てる。
IMPORT_HISTORY_MAX = int(os.getenv("IMPORT_HISTORY_MAX", "5000") or 5000)
# 画面のテーブル詳細に出すサンプル行数
IMPORT_SAMPLE_ROWS = int(os.getenv("IMPORT_SAMPLE_ROWS", "20") or 20)

# --- カタログの変更履歴 -------------------------------------------------------
# 用語集・例文を誰がいつ変えたかの記録（チャットからの登録・カタログ画面の編集の両方）。
CATALOG_HISTORY_FILE = Path(os.getenv("CATALOG_HISTORY_FILE",
                                      str(DATA_DIR / "catalog_history.jsonl"))).expanduser()
CATALOG_HISTORY_MAX = int(os.getenv("CATALOG_HISTORY_MAX", "2000") or 2000)

# チャットの登録カード（用語・例文）から、一般利用者もカタログを書けるようにするか。
#
# カタログは全利用者のシステムプロンプトに毎回そのまま載る。用語の定義は
# 「必ずその定義に従う」、用語のSQL式は「そのまま使う」とAIに指示しているので、
# ここを開けると、権限の低い利用者が管理者を含む全員の回答を左右できてしまう
# （書けるのは読み取り専用のSELECTだけだが、答えの中身は歪められる）。
# 既定は管理者のみ。皆でカタログを育てる運用に戻すなら env で true にする。
# なお、どちらの設定でも「誰がいつ何を変えたか」は catalog_history に残る。
CATALOG_OPEN_CONTRIB = (os.getenv("CATALOG_OPEN_CONTRIB", "false").strip().lower()
                        in ("1", "true", "yes", "on"))

# --- メール送信（SMTP） -------------------------------------------------------
# ここの値は「初期値」で、画面（メール設定）から保存すると上書きされる。
#
# 社内リレー（ポート25・暗号化なし・認証なし）が前提。実運用のスクリプトが
# この型で動いているため、画面に出すのはホスト・ポート・タイムアウトだけ。
# 外部のSMTP（Gmail等）を使う環境では、暗号化と認証をここで指定する。
#   SMTP_HOST=relay.example.co.jp
#   SMTP_PORT=25
#   SMTP_SECURITY=none          # none / starttls / ssl（画面には出さない）
#   SMTP_USER=... / SMTP_PASSWORD=...   ← 認証が要るサーバのときだけ
#   SMTP_SENDER=bi-report@example.co.jp
# 画面から保存した設定の置き場。
SMTP_SETTINGS_FILE = Path(os.getenv("SMTP_SETTINGS_FILE",
                                    str(DATA_DIR / "mail_settings.yaml"))).expanduser()
SMTP_HOST = os.getenv("SMTP_HOST", "").strip()
SMTP_PORT = int(os.getenv("SMTP_PORT", "25") or 25)
SMTP_SECURITY = (os.getenv("SMTP_SECURITY", "none").strip().lower() or "none")
SMTP_USER = os.getenv("SMTP_USER", "").strip()
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SMTP_SENDER = os.getenv("SMTP_SENDER", "").strip()
SMTP_SENDER_NAME = os.getenv("SMTP_SENDER_NAME", "DB分析アシスタント").strip()
SMTP_TIMEOUT = int(os.getenv("SMTP_TIMEOUT", "20") or 20)
# 「メール設定」画面で宛先として登録してよいドメインの【初期値】（env では設定しない）。
# 管理者が「メール設定」画面の「登録してよいドメイン」で変更でき、画面で保存した値が
# こちらより優先される（data/mail_settings.yaml の ok_domains）。
# ここに書いたドメイン以外のアドレスは、そもそも許可リストに追加できない。
#   "@example.co.jp"    先頭の @ は付けても付けなくてもよい
#   "a.co.jp;b.co.jp"   複数なら ; か , で区切る
#   ""                  空にすると、この制限だけが外れる
#                       （宛先の許可リスト自体は必要なまま）
# 既定は空（制限なし）。本番でメールを使うときは、メール設定画面の
# 「登録してよいドメイン」で社内ドメインを設定してから宛先を登録すること。
_SEND_OK_MAIL_DOMAIN = ""
SEND_OK_MAIL_DOMAIN = [d.strip().lstrip("@").lower() for d
                       in re.split(r"[;,]", _SEND_OK_MAIL_DOMAIN)
                       if d.strip()]

# 一度に送れる宛先の上限。誤って一斉送信するのを防ぐ。
SMTP_MAX_RECIPIENTS = int(os.getenv("SMTP_MAX_RECIPIENTS", "20") or 20)
# true のあいだは実際に送らず、組み立てた内容だけ返す（既定）。
# 本番のSMTPを設定して動作を確かめてから false にすること。
SMTP_DRY_RUN = (os.getenv("SMTP_DRY_RUN", "true").strip().lower()
                in ("1", "true", "yes", "on"))

# --- OpenAI / OpenAI互換API の設定 -----------------------------------------
# OpenAI SDK は base_url の末尾に "/chat/completions" を付けて呼ぶ。
# 公式OpenAIなら base_url は .../v1。/v1 以外のパスのOpenAI互換エンドポイントを使う
# 場合は、そのパスまで（末尾の /chat/completions は付けない）で設定する。
# 管理者が「モデル設定」画面で接続先URL（チャット用・モデル一覧用のフルパス2本）を
# 保存した場合はそちらが優先され、この値は初期値になる
# （実際の参照は models.llm_chat_url / llm_models_url）。
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "").strip()
# APIキー。管理者が「モデル設定」画面で保存したキー（model_settings.yaml の api_key）が
# あればそちらが優先され、この env の値は初期値になる（実際の参照は models.llm_api_key）。
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
# 既定のモデル。ここで直接指定する（env では設定しない）。
# 使われるのは次の2通り:
#   1. 「モデル設定」画面で既定を決めていないときの、チャットの既定モデル
#   2. 裏方の処理（DBルーター・用語集やツールのAI下書き）。こちらは画面での
#      選択に関係なく常にこのモデルを使う。安く速いものを指定しておくとよい
OPENAI_MODEL = "gpt-5.6-sol"
# ※ gpt-5.6-sol は、ツールを使うとき reasoning_effort='none' が必須。
#    この作法は llm.py の _fix_for が1回目の400応答から自動で学習するので、
#    ここでモデル名を変えるだけでよい（設定を書き足す必要はない）。
# 画面のプルダウンに出すモデル。空ならAPIの /models から取りに行く。
#   export OPENAI_MODELS="gpt-4o-mini;gpt-4o;5.6sol"
OPENAI_MODELS = [m.strip() for m in re.split(r"[;,]", os.getenv("OPENAI_MODELS", ""))
                 if m.strip()]
# 画像を送れるモデル（マルチモーダル）。名前の一部でよい。
#   export OPENAI_VISION_MODELS="gpt-4o;sol;vision"
OPENAI_VISION_MODELS = [m.strip().lower() for m
                        in re.split(r"[;,]", os.getenv("OPENAI_VISION_MODELS",
                                                       "gpt-4o;gpt-4.1;gpt-5;o4;sol;vision"))
                        if m.strip()]
# 利用者が選んだモデルは data/users/<ユーザー>/prefs.yaml に入る（prefs.py 参照）
# 管理者が「モデル設定」画面から保存した内容の置き場。
# 上の OPENAI_MODEL / OPENAI_MODELS / OPENAI_VISION_MODELS より優先される。
MODEL_SETTINGS_FILE = Path(os.getenv("MODEL_SETTINGS_FILE",
                                     str(DATA_DIR / "model_settings.yaml"))).expanduser()
# 画像1枚あたりの上限（MB）と、1メッセージに付けられる枚数
IMAGE_MAX_MB = float(os.getenv("IMAGE_MAX_MB", "8") or 8)
IMAGE_MAX_COUNT = int(os.getenv("IMAGE_MAX_COUNT", "4") or 4)

# 生成パラメータ（いずれも任意）。SQL生成の安定のため temperature は既定0。
OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0") or 0)
_top_p = os.getenv("OPENAI_TOP_P")
OPENAI_TOP_P = float(_top_p) if _top_p else None
_max_tokens = os.getenv("OPENAI_MAX_TOKENS")
OPENAI_MAX_TOKENS = int(_max_tokens) if _max_tokens else None

# --- レポート（PowerPoint / Word） -------------------------------------------
# 文書に使う日本語フォント。開く側のPCに入っているものを指定すること。
# Windows なら Meiryo / 游ゴシック / MS Pゴシック あたりが確実。
REPORT_FONT_JA = os.getenv("REPORT_FONT_JA", "Meiryo").strip() or "Meiryo"
# 文書に貼るグラフ画像の大きさ（px）と倍率。倍率を上げると精細だが重くなる。
REPORT_IMAGE_WIDTH = int(os.getenv("REPORT_IMAGE_WIDTH", "1200") or 1200)
REPORT_IMAGE_HEIGHT = int(os.getenv("REPORT_IMAGE_HEIGHT", "650") or 650)
REPORT_IMAGE_SCALE = float(os.getenv("REPORT_IMAGE_SCALE", "2") or 2)
# 表紙などに入れる組織名（空なら出さない）
REPORT_ORG = os.getenv("REPORT_ORG", "").strip()

# --- 対象データの決め方 -------------------------------------------------------
# 質問ごとに、どのDBのカタログをAIに渡すか。
#   auto   … カタログ全体が「選択中モデルの上限」に収まるなら全DBを直載せ
#            （ルーター省略・選び漏れゼロ・キャッシュ最大）。超えたらルーターで
#            関係するDBだけに絞り、詳細を保ったままにする（既定）
#   router … 常にルーターで絞る（無関係なDBを本番プロンプトに一切入れない）
#   all    … 常に全DB。上限を超えると要約モード（列名が渡らない）に落ちる
SCOPE_MODE = (os.getenv("SCOPE_MODE", "auto").strip().lower() or "auto")
if SCOPE_MODE not in ("auto", "router", "all"):
    SCOPE_MODE = "auto"

# --- エージェント動作 -------------------------------------------------------
# 1質問あたり、AIが「考えてツールを呼ぶ」を何往復まで許すか。
# 1往復で複数のツールをまとめて呼べるので、実際に使えるツールの数はこれより多い。
# 暴走（同じ検索を延々と繰り返す等）を止めるための安全弁で、
# 分析→グラフ→レポートのような多段の作業では10前後が目安。
MAX_AGENT_STEPS = int(os.getenv("MAX_AGENT_STEPS", "10") or 10)
MAX_RESULT_ROWS = 2000     # 1クエリで取得・表示する最大行数
QUERY_TIMEOUT_SEC = 10     # ユーザークエリのタイムアウト(秒)
SAMPLE_ROWS_FOR_LLM = 40   # LLMへ返すサンプル行数(トークン節約)

# ファイル出力(Excel / CSV / テキスト)が1回に書き出せる最大行数。
# 画面とLLM向けの MAX_RESULT_ROWS(2,000) とは別枠。画面の表は2,000行で充分だが、
# 「CSVでください」はファイルとして全行欲しいのが普通なので、こちらの上限で取り直す。
# 既定100万行は取り込み側の上限(IMPORT_MAX_ROWS)と揃えた値。ファイルはメモリ上で
# 組み立てるので、行数×列数が大きいとその分メモリを使う。
# なお Excel のシートは仕様上 1,048,576 行までしか持てない(こちらは自動で丸める)。
EXPORT_MAX_ROWS = int(os.getenv("EXPORT_MAX_ROWS", "1000000") or 1000000)

# --- 自動プロファイリング ---------------------------------------------------
PROFILE_SAMPLE_ROWS = 5          # プロファイルに保存するサンプル行数
PROFILE_LOW_CARDINALITY = 20     # 実値一覧を保持する distinct 数の上限
PROFILE_TIMEOUT_SEC = 30         # プロファイリング中の1クエリのタイムアウト(秒)
PROFILE_STATS_MAX_ROWS = 2_000_000  # これ以上の行数のテーブルは列統計をスキップ

# --- プロンプト組み立て -----------------------------------------------------
# 選択スコープのカタログ全文がこの文字数以下なら、すべて system prompt にインライン。
# 超える場合はテーブル一覧などの要約のみ入れ、詳細は describe_table ツールで取得させる。
#
# 既定の80,000字は実測に基づく。全DB選択（11DB・58,000字）で gpt-4o-mini に渡すと
# 入力52,000トークン・初回3秒、2回目以降はプロンプトキャッシュがほぼ全体に効いて
# 1.7秒・費用は1問1円未満だった。カタログはシステムプロンプトの先頭側にあり、
# 内容を変えない限り毎回同一なので、キャッシュに乗る。
# 逆に、要約に落ちると列名がAIに渡らず「その列は無い」と誤答する原因になる。
# 上限は「渡らない」を防ぐためではなく、モデルのコンテキストを守るための安全弁。
#
# ここは初期値で、「モデル設定」画面で決めた値があればそちらが優先される
# （models.prompt_inline_limit() を参照）。
# ※ 現在は「選択中モデルの文脈量」から自動で決めるため、この値は使っていない。
#   古い env との互換のために読むだけ（models.inline_limit_for を参照）。
PROMPT_INLINE_LIMIT_CHARS = int(os.getenv("PROMPT_INLINE_LIMIT_CHARS", "80000") or 80000)

# モデルが一度に読める量（トークン）。OpenAI公式リファレンス（developers.openai.com/api/docs/models）
# の Context window の値。名前の部分一致で当てる（長い名前から見る）ので、
# "gpt-4o-mini-2024-07-18" のような日付つきスナップショットも "gpt-4o-mini" に当たる。
#
# ここに無いモデル（ゲートウェイ独自の名前や他社モデル）は MODEL_CONTEXT_DEFAULT を仮の値に
# 使い、画面に「推定」と出す。正しい値は「モデル設定」画面で管理者が登録できる
# （models.py の context_overrides）。ここは既定値であって上書きの土台。
MODEL_CONTEXT_WINDOWS = {
    # GPT-5.6（2026）
    "gpt-5.6": 1_050_000,
    # GPT-5 系（2025-08）: 400K。mini / nano も同じ
    "gpt-5-mini": 400_000,
    "gpt-5-nano": 400_000,
    "gpt-5": 400_000,
    # GPT-4.1 系（2025-04）: 1,047,576。mini / nano も同じ
    "gpt-4.1-mini": 1_047_576,
    "gpt-4.1-nano": 1_047_576,
    "gpt-4.1": 1_047_576,
    # GPT-4o 系: 128K
    "gpt-4o-mini": 128_000,
    "gpt-4o": 128_000,
    "chatgpt-4o": 128_000,
    # o シリーズ（推論）: 200K
    "o4-mini": 200_000,
    "o4": 200_000,
    "o3-mini": 200_000,
    "o3": 200_000,
    "o1-mini": 128_000,
    "o1": 200_000,
    # 旧世代
    "gpt-4-turbo": 128_000,
    "gpt-4-32k": 32_768,
    "gpt-4": 8_192,
    "gpt-3.5-turbo-16k": 16_385,
    "gpt-3.5-turbo": 16_385,
}
MODEL_CONTEXT_DEFAULT = int(os.getenv("MODEL_CONTEXT_DEFAULT", "128000") or 128000)

# --- レート制限（429）への対応 -------------------------------------------------
# OpenAI は短時間に問い合わせが集中すると 429 を返す。多くは数秒待てば通る。
#
# SDK自体も2回までは自動で投げ直すが、それでも足りないことがある。
# 足りなかったときにその場で終わらせず、アプリ側でも待って投げ直す。
# エラー文の「Please try again in 300ms」や retry-after ヘッダに従うので、
# 実際の待ちはたいてい1秒未満で済む。
#
# 0 にするとこの再試行を行わない（SDKの2回だけになる）。
LLM_RATE_LIMIT_RETRIES = int(os.getenv("LLM_RATE_LIMIT_RETRIES", "3") or 3)
# 1回あたりの待ち時間の上限（秒）。サーバが「60秒待て」と言ってきても、
# 利用者を待たせすぎないためここで頭打ちにする。
LLM_RATE_LIMIT_MAX_WAIT = float(os.getenv("LLM_RATE_LIMIT_MAX_WAIT", "20") or 20)

# --- ナレッジベース（LightRAG連携） -------------------------------------------
# 社内文書の検索は、別に立てた LightRAG サーバへHTTPで問い合わせる。
# このアプリは索引を持たない（索引作成は重く、GPUのある別サーバで動かすため）。
#
# 接続先は env でもコードでもなく「ナレッジベース」画面から登録する。
# IT部門から払い出されるのが URL と APIキー の2つだけ、という前提のため。
# 登録が1件も無ければ、AIにナレッジ検索ツールを渡さない（他の機能はそのまま動く）。
KNOWLEDGE_BASES_FILE = Path(os.getenv("KNOWLEDGE_BASES_FILE",
                                      str(DATA_DIR / "knowledge_bases.json"))).expanduser()

# 各ナレッジベースへの検索タイムアウト（秒）。
# 文書の取り込み中は LightRAG 側が抽出処理で埋まり、検索の応答が遅くなる。
# 短すぎると取り込み中は毎回タイムアウトするので余裕を持たせている。
RAG_RETRIEVE_TIMEOUT = int(os.getenv("RAG_RETRIEVE_TIMEOUT", "180") or 180)
# 複数のナレッジベースへ同時に投げる数。登録が増えても待ち時間が伸びないようにする。
RAG_FANOUT_WORKERS = int(os.getenv("RAG_FANOUT_WORKERS", "8") or 8)

# --- 検索の効き方の初期値 ---
# 利用者はチャット画面のサイドバーから個別に変えられる（rag/settings.py）。
# ここの値は「初期値に戻す」の戻り先になるので、全体の既定を変えたいときはここを直す。
# 明示的に設定を変えていない利用者は、ここを変えれば新しい既定に追随する。
RAG_RETRIEVE_MODE = os.getenv("RAG_RETRIEVE_MODE", "mix").strip() or "mix"
# 1つのナレッジベースから取る文章の数
RAG_CHUNK_TOP_K = int(os.getenv("RAG_CHUNK_TOP_K", "10") or 10)
# ナレッジグラフから取るエンティティ／関係の数
RAG_TOP_K = int(os.getenv("RAG_TOP_K", "40") or 40)
# 統合後、AIに渡す参考情報の最大文字数。
# ツール1回ぶんの戻り値なので、モデルの文脈量に対して控えめにしておく
# （1つの質問でナレッジ検索を何度も呼ぶことがあり、そのたびに積み上がるため）。
RAG_MAX_CONTEXT_CHARS = int(os.getenv("RAG_MAX_CONTEXT_CHARS", "12000") or 12000)

# --- 認証 -------------------------------------------------------------------
# ログイン関係の設定（認証方式・常設管理者・認証APIの項目名）は、env でも
# ここでもなく **auth.py の冒頭にすべて集約** してある。LDAP切替や管理者
# パスワードの変更は auth.py を編集する（触るファイルを1つに閉じるため）。

# ユーザーごとのカタログ／チャット履歴の置き場所（data/users/<ユーザー名>/）
USER_META_DIR = DATA_DIR / "users"

# --- チャット履歴 -----------------------------------------------------------
# 1人あたり保持する会話の本数。超えた分は古い順に自動削除する。
CHAT_HISTORY_LIMIT = 100
# 保存期間（日）。最後に使った日からこれを過ぎた会話は自動削除する。
# 既定は3か月。0 にすると期限で消さない（本数の上限だけが効く）。
CHAT_HISTORY_DAYS = int(os.getenv("CHAT_HISTORY_DAYS", "90") or 0)
# 作成したファイル(Excel/CSV等)を履歴に埋め込む上限。超えるものは本体を保存せず、
# 過去の会話を開いたときは「再ダウンロードできない」旨だけ表示する。
CHAT_EMBED_FILE_MAX_BYTES = 2 * 1024 * 1024

# --- ファイル出力 -----------------------------------------------------------
# True にすると、ファイル作成後にボタンを押さなくてもブラウザの保存が始まる
# （Excel / CSV / テキスト / ZIP 共通）。ブラウザ側の設定（自動ダウンロードの
# ブロック等）で止められることがあるため、退避用のダウンロードボタンは
# 折りたたんで残す。
AUTO_DOWNLOAD = True

# --- アプリ表示 -------------------------------------------------------------
APP_TITLE = "DB分析アシスタント"

# チャット入力欄のプレースホルダ
# 画像を扱えるモデルのときは、貼り付け・ドロップの案内を chat.js が末尾に足す
APP_INPUT_PLACEHOLDER = "データについて質問してください…"

# 初期表示するサンプル質問ボタン（空リストにすると非表示）。
# 同梱の sample_db.py で作れる5つのデモDB向け。DB横断の質問を含む。
# 起動時にデータ用フォルダを用意
DATA_DIR.mkdir(parents=True, exist_ok=True)
