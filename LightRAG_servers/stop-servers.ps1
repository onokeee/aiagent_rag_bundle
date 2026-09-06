# 4台をまとめて止める。
#
#   powershell -ExecutionPolicy Bypass -File stop-servers.ps1
#
# ポートを握っているプロセスを見て止める。他のアプリまで巻き込まないよう、
# 対象は 9621〜9624 の4つに限定している。
#
# 変数名に $pid は使えない（PowerShell の予約変数で書き込めない）。

$ports = 9621, 9622, 9623, 9624, 9625, 9626, 9627, 9628, 9629, 9630, 9631, 9632, 9633, 9634, 9635, 9636, 9637, 9638, 9639, 9640, 9641, 9642

foreach ($port in $ports) {
    $conn = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
    if (-not $conn) {
        Write-Host "port ${port}: 動いていません" -ForegroundColor Yellow
        continue
    }
    foreach ($procId in ($conn.OwningProcess | Select-Object -Unique)) {
        try {
            $p = Get-Process -Id $procId -ErrorAction Stop
            Stop-Process -Id $procId -Force
            Write-Host "port ${port}: 停止しました（$($p.ProcessName) PID $procId）"
        } catch {
            Write-Host "port ${port}: 停止できませんでした（PID $procId）" -ForegroundColor Red
        }
    }
}
