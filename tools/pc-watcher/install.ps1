# PC 감시 설치: config.json 생성(비밀 키 자동 생성) + 로그인 시 자동 실행 등록
#   powershell -ExecutionPolicy Bypass -File .\install.ps1
#   제거: powershell -ExecutionPolicy Bypass -File .\install.ps1 -Remove
param([switch]$Remove)
$TaskName = 'AmsaWYD 사이트 감시'
if ($Remove) { Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false; Write-Host '제거했습니다.'; exit 0 }

$Here = $PSScriptRoot
$Utf8 = New-Object System.Text.UTF8Encoding($false)
$cfgPath = Join-Path $Here 'config.json'
if (-not (Test-Path $cfgPath)) {
  $req = [IO.File]::ReadAllText((Join-Path $Here '..\..\functions\api\request.js'), $Utf8)
  $url = [regex]::Match($req, 'INTAKE_URL\s*=\s*"([^"]+)"').Groups[1].Value
  $chars = [char[]]'ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnpqrstuvwxyz23456789'
  $rng = [Security.Cryptography.RandomNumberGenerator]::Create(); $b = New-Object byte[] 40; $rng.GetBytes($b)
  $key = -join ($b | ForEach-Object { $chars[$_ % $chars.Length] })
  $cfg = [ordered]@{ url = $url; key = $key; interval = 60; claude = '' }
  [IO.File]::WriteAllText($cfgPath, ($cfg | ConvertTo-Json), $Utf8)
  Write-Host ''
  Write-Host 'config.json 을 만들었습니다. 아래 키를 Apps Script 스크립트 속성 WATCH_KEY 에 넣으세요:' -ForegroundColor Yellow
  Write-Host "  $key" -ForegroundColor Cyan
  Write-Host ''
}

$ps = (Get-Command powershell.exe).Source
$action = New-ScheduledTaskAction -Execute $ps -Argument "-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$(Join-Path $Here 'watch.ps1')`""
$trigger = New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME
$settings = New-ScheduledTaskSettingsSet -ExecutionTimeLimit ([TimeSpan]::Zero) -RestartCount 99 -RestartInterval (New-TimeSpan -Minutes 5) `
  -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -MultipleInstances IgnoreNew
Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger -Settings $settings -Force | Out-Null
Write-Host "작업 스케줄러에 '$TaskName' 을 등록했습니다 (로그인할 때 자동 시작)."
Write-Host '키를 Apps Script 에 넣은 뒤:  .\watch.ps1 -Test  로 연결을 확인하고,  Start-ScheduledTask -TaskName ''AmsaWYD 사이트 감시''  로 바로 시작하세요.'
