# 4台の状態を確認する。
#
#   powershell -ExecutionPolicy Bypass -File check-servers.ps1
#
# /health は認証不要で、APIキーが誤っていても 200 を返す（構成の詳細が伏せられるだけ）。
# そのため、キーが効いているかは保護されたエンドポイントで別に確かめる。
# アプリの「接続テスト」ボタンも同じ2段構えになっている。

$servers = @(
    @{ Name = "設備マニュアル"; Port = 9621; Key = "key-manual-9621" },
    @{ Name = "トラブル事例";   Port = 9622; Key = "key-trouble-9622" },
    @{ Name = "改善事例";       Port = 9623; Key = "key-kaizen-9623" },
    @{ Name = "作業標準";       Port = 9624; Key = "key-standard-9624" },
    @{ Name = "社内規程";       Port = 9625; Key = "key-kitei-9625" },
    @{ Name = "営業ナレッジ";   Port = 9626; Key = "key-sales-9626" },
    @{ Name = "ITサポート";     Port = 9627; Key = "key-itsupport-9627" },
    @{ Name = "設備マニュアル（関西工場）"; Port = 9628; Key = "key-manual-kansai-9628" },
    @{ Name = "設備マニュアル（九州工場）"; Port = 9629; Key = "key-manual-kyushu-9629" },
    @{ Name = "トラブル事例（関西工場）"; Port = 9630; Key = "key-trouble-kansai-9630" },
    @{ Name = "トラブル事例（九州工場）"; Port = 9631; Key = "key-trouble-kyushu-9631" },
    @{ Name = "改善事例（関西工場）"; Port = 9632; Key = "key-kaizen-kansai-9632" },
    @{ Name = "作業標準（関西工場）"; Port = 9633; Key = "key-standard-kansai-9633" },
    @{ Name = "品質基準（関西工場）"; Port = 9634; Key = "key-quality-kansai-9634" },
    @{ Name = "社内規程（海外赴任）"; Port = 9635; Key = "key-kitei-overseas-9635" },
    @{ Name = "社内規程（契約社員）"; Port = 9636; Key = "key-kitei-parttime-9636" },
    @{ Name = "営業ナレッジ（海外）"; Port = 9637; Key = "key-sales-overseas-9637" },
    @{ Name = "営業ナレッジ（代理店）"; Port = 9638; Key = "key-sales-agency-9638" },
    @{ Name = "ITサポート（工場側）"; Port = 9639; Key = "key-itsupport-factory-9639" },
    @{ Name = "ITサポート（海外拠点）"; Port = 9640; Key = "key-itsupport-overseas-9640" },
    @{ Name = "安全衛生"; Port = 9641; Key = "key-safety-9641" }
    @{ Name = "社内Webリンク集"; Port = 9642; Key = "key-weblinks-9642" }
)

foreach ($srv in $servers) {
    $url = "http://127.0.0.1:$($srv.Port)"
    $line = "{0,-14} {1}" -f $srv.Name, $url

    try {
        $h = Invoke-RestMethod -Uri "$url/health" -TimeoutSec 10
    } catch {
        Write-Host "$line  応答なし（起動中か、落ちています）" -ForegroundColor Red
        continue
    }

    try {
        $null = Invoke-RestMethod -Uri "$url/documents/pipeline_status" `
            -Headers @{ "X-API-Key" = $srv.Key } -TimeoutSec 10
        $keyOk = "キーOK"
    } catch {
        $keyOk = "キーNG"
    }

    $docs = ""
    try {
        $d = Invoke-RestMethod -Uri "$url/documents" -Headers @{ "X-API-Key" = $srv.Key } -TimeoutSec 10
        $n = ($d.statuses.PSObject.Properties | ForEach-Object { $_.Value.Count } | Measure-Object -Sum).Sum
        $docs = "  文書 $n 件"
    } catch { }

    $color = if ($keyOk -eq "キーOK") { "Green" } else { "Yellow" }
    Write-Host "$line  $($h.status)  $keyOk$docs" -ForegroundColor $color
}
