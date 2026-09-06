# LightRAG サーバ4台の一括起動。
#
#   powershell -ExecutionPolicy Bypass -File start-servers.ps1
#
# 4台とも同じ .env（OpenAIの設定）を共有し、違うのは次の3つだけ。
#   ポート        … 接続先
#   ワークスペース … 保存先の分離。文書が混ざらないようにする
#   APIキー        … 環境ごとに別のキーにする（1台漏れても他は無事）
#
# 設定ファイルが ".env"（ドット付き）なのは LightRAG 本体の流儀に合わせたもの。
# 読み先はソースにハードコードされていて変えられず、さらに「起動フォルダに
# .env が無い」と対話プロンプトを出して止まる（utils_api.py の check_env_file）。
# aiagent 側の env（ドット無し）とは別物なので、混同しないこと。
#
# APIキーは .env に書かない。書くと4台とも同じキーになってしまうため、
# 起動時に --key で1台ずつ渡す。
#
# 実運用では、URLとAPIキーをIT部門が決めて払い出す。
# アプリ側は受け取った2つを管理画面に入れるだけでよい。

$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$exe  = Join-Path $here "venv\Scripts\lightrag-server.exe"

if (-not (Test-Path $exe)) {
    Write-Host "lightrag-server が見つかりません: $exe" -ForegroundColor Red
    Write-Host "  venv を作り直す場合:" -ForegroundColor Yellow
    Write-Host "    py -3.13 -m venv venv"
    Write-Host "    venv\Scripts\python.exe -m pip install `"lightrag-hku[api]`""
    exit 1
}
if (-not (Test-Path (Join-Path $here ".env"))) {
    Write-Host "設定ファイル .env がありません。これが無いとサーバは起動しません。" -ForegroundColor Red
    exit 1
}

$servers = @(
    @{ Name = "設備マニュアル"; Port = 9621; Workspace = "manual";   Key = "key-manual-9621" },
    @{ Name = "トラブル事例";   Port = 9622; Workspace = "trouble";  Key = "key-trouble-9622" },
    @{ Name = "改善事例";       Port = 9623; Workspace = "kaizen";   Key = "key-kaizen-9623" },
    @{ Name = "作業標準";       Port = 9624; Workspace = "standard"; Key = "key-standard-9624" },
    @{ Name = "社内規程";       Port = 9625; Workspace = "kitei";     Key = "key-kitei-9625" },
    @{ Name = "営業ナレッジ";   Port = 9626; Workspace = "sales";     Key = "key-sales-9626" },
    @{ Name = "ITサポート";     Port = 9627; Workspace = "itsupport"; Key = "key-itsupport-9627" },
    @{ Name = "設備マニュアル（関西工場）"; Port = 9628; Workspace = "manual_kansai"; Key = "key-manual-kansai-9628" },
    @{ Name = "設備マニュアル（九州工場）"; Port = 9629; Workspace = "manual_kyushu"; Key = "key-manual-kyushu-9629" },
    @{ Name = "トラブル事例（関西工場）"; Port = 9630; Workspace = "trouble_kansai"; Key = "key-trouble-kansai-9630" },
    @{ Name = "トラブル事例（九州工場）"; Port = 9631; Workspace = "trouble_kyushu"; Key = "key-trouble-kyushu-9631" },
    @{ Name = "改善事例（関西工場）"; Port = 9632; Workspace = "kaizen_kansai"; Key = "key-kaizen-kansai-9632" },
    @{ Name = "作業標準（関西工場）"; Port = 9633; Workspace = "standard_kansai"; Key = "key-standard-kansai-9633" },
    @{ Name = "品質基準（関西工場）"; Port = 9634; Workspace = "quality_kansai"; Key = "key-quality-kansai-9634" },
    @{ Name = "社内規程（海外赴任）"; Port = 9635; Workspace = "kitei_overseas"; Key = "key-kitei-overseas-9635" },
    @{ Name = "社内規程（契約社員）"; Port = 9636; Workspace = "kitei_parttime"; Key = "key-kitei-parttime-9636" },
    @{ Name = "営業ナレッジ（海外）"; Port = 9637; Workspace = "sales_overseas"; Key = "key-sales-overseas-9637" },
    @{ Name = "営業ナレッジ（代理店）"; Port = 9638; Workspace = "sales_agency"; Key = "key-sales-agency-9638" },
    @{ Name = "ITサポート（工場側）"; Port = 9639; Workspace = "itsupport_factory"; Key = "key-itsupport-factory-9639" },
    @{ Name = "ITサポート（海外拠点）"; Port = 9640; Workspace = "itsupport_overseas"; Key = "key-itsupport-overseas-9640" },
    @{ Name = "安全衛生"; Port = 9641; Workspace = "safety"; Key = "key-safety-9641" }
    @{ Name = "社内Webリンク集"; Port = 9642; Workspace = "weblinks"; Key = "key-weblinks-9642" }
)

foreach ($srv in $servers) {
    $running = Get-NetTCPConnection -LocalPort $srv.Port -State Listen -ErrorAction SilentlyContinue
    if ($running) {
        Write-Host ("port {0}: 既に動いています（{1}）" -f $srv.Port, $srv.Name) -ForegroundColor Yellow
        continue
    }
    $params = @("--port", $srv.Port, "--workspace", $srv.Workspace, "--key", $srv.Key)
    Start-Process -FilePath $exe -ArgumentList $params -WorkingDirectory $here -WindowStyle Minimized
    Write-Host ("port {0}: 起動中  {1}  (workspace={2})" -f $srv.Port, $srv.Name, $srv.Workspace)
}

Write-Host ""
Write-Host "起動には20〜40秒かかります（モデルの初期化）。" -ForegroundColor Cyan
Write-Host "確認:  powershell -ExecutionPolicy Bypass -File check-servers.ps1"
Write-Host ""
Write-Host "アプリの「ナレッジベース」画面に登録する値:" -ForegroundColor Cyan
foreach ($srv in $servers) {
    Write-Host ("  {0,-14} http://127.0.0.1:{1}   {2}" -f $srv.Name, $srv.Port, $srv.Key)
}
