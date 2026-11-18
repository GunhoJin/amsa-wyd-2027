# 암사동성당 WYD 사이트 — PC 감시 스크립트 (Windows PowerShell 5.1 / 7)
# 1분마다 접수 웹 앱에 최신 ID만 물어보고, 새 수정요청·문의가 있으면 바로 Claude Code로 처리 → push → 결과 메일.
#   .\watch.ps1          계속 감시 (작업 스케줄러가 로그인 때 숨김 실행)
#   .\watch.ps1 -Test    연결 확인만 하고 끝
#   .\watch.ps1 -Once    지금 한 번 처리 (새 글 여부와 관계없이)
param([switch]$Test, [switch]$Once)

$ErrorActionPreference = 'Continue'
$Here = $PSScriptRoot
$Repo = (Resolve-Path (Join-Path $Here '..\..')).Path
$Work = Join-Path $Repo '.watch'
$Out  = Join-Path $Work 'out'
New-Item -ItemType Directory -Force -Path $Out | Out-Null
$Utf8 = New-Object System.Text.UTF8Encoding($false)

$cfgPath = Join-Path $Here 'config.json'
if (-not (Test-Path $cfgPath)) { Write-Host 'config.json 이 없습니다. install.ps1 을 먼저 실행하세요.'; exit 1 }
$Cfg = [IO.File]::ReadAllText($cfgPath, $Utf8) | ConvertFrom-Json
$Interval = if ($Cfg.interval) { [int]$Cfg.interval } else { 60 }
$Claude = $Cfg.claude
if (-not $Claude) {
  $c = Get-Command claude -ErrorAction SilentlyContinue
  $Claude = if ($c) { $c.Source } else { Join-Path $env:USERPROFILE '.local\bin\claude.exe' }
}

$AllowedFiles = '^((index|about|plan|pilgrim|program|join|market|homestay|rosary|donate|contact|request|inquiry)\.html|rss\.xml|tools/edit-requests/(processed|inquiries)\.json)$'

function Log($m) {
  $line = (Get-Date -Format 'yyyy-MM-dd HH:mm:ss') + '  ' + $m
  [IO.File]::AppendAllText((Join-Path $Work 'watch.log'), $line + "`r`n", $Utf8)
  if ($Test -or $Once) { Write-Host $line }
}

function Api($fields) {
  $fields.kind = 'watch'; $fields.key = $Cfg.key
  $body = ($fields.GetEnumerator() | ForEach-Object { [Uri]::EscapeDataString($_.Key) + '=' + [Uri]::EscapeDataString([string]$_.Value) }) -join '&'
  $r = Invoke-WebRequest -Uri $Cfg.url -Method Post -Body $body -ContentType 'application/x-www-form-urlencoded' -UseBasicParsing -TimeoutSec 90
  $text = $Utf8.GetString($r.RawContentStream.ToArray())
  return @{ text = $text; json = ($text | ConvertFrom-Json) }
}

function B64($s) { [Convert]::ToBase64String($Utf8.GetBytes($s)) }

function Mail($subject, $body) {
  try { $r = Api @{ op = 'report'; subject = (B64 $subject); body = (B64 $body) }; Log ("메일: $subject → " + $r.json.ok) }
  catch { Log "메일 실패: $_" }
}

function GitRun {
  $o = & git -C $Repo @args 2>&1
  $script:GitOk = ($LASTEXITCODE -eq 0)
  foreach ($l in $o) { Log "git $($args[0]): $l" }
  return $o
}

function Seoul { [TimeZoneInfo]::ConvertTimeBySystemTimeZoneId([DateTime]::UtcNow, 'Korea Standard Time') }

function Changed {
  $o = & git -C $Repo status --porcelain --untracked-files=all 2>$null
  return @($o | Where-Object { $_ } | ForEach-Object { $_.Substring(3).Trim('"') })
}

function RunOnce {
  if ((Changed).Count -gt 0) { Log '저장소에 커밋 안 된 변경이 있어 건너뜀 (직접 정리 필요)'; return $false }
  GitRun checkout main | Out-Null
  GitRun pull --ff-only origin main | Out-Null
  if (-not $GitOk) { Log 'git pull 실패'; return $false }

  $rowsPath = Join-Path $Work 'rows.json'
  try {
    $rows = Api @{ op = 'rows' }
    if (-not $rows.json.ok) { Log "rows 실패: $($rows.text)"; return $false }
    [IO.File]::WriteAllText($rowsPath, $rows.text, $Utf8)
    $now = Seoul
    [IO.File]::WriteAllText((Join-Path $Work 'now.txt'), $now.ToString('yyyy-MM-dd HH:mm') + "`n" + $now.ToString('MMddHHmm') + "`n", $Utf8)
    Get-ChildItem $Out -File | Remove-Item -Force

    Log 'Claude 실행'
    Push-Location $Repo
    & $Claude -p 'Read tools/pc-watcher/PROMPT.md and follow it exactly. Do not ask questions.' `
      --allowedTools 'Read,Edit,Write,Glob,Grep' --disallowedTools 'Bash,WebFetch,WebSearch' --max-turns 80 2>&1 |
      ForEach-Object { Log "claude: $_" }
    $code = $LASTEXITCODE
    Pop-Location
    if ($code -ne 0) { Log "Claude 종료 코드 $code"; GitRun checkout -- . | Out-Null; return $false }
  } finally {
    if (Test-Path $rowsPath) { Remove-Item $rowsPath -Force }    # 개인 정보는 남기지 않음
  }

  # 허용된 파일 외 변경은 전부 되돌림
  $files = Changed
  $bad = @($files | Where-Object { $_ -notmatch $AllowedFiles })
  if ($bad.Count -gt 0) {
    GitRun checkout -- . | Out-Null; GitRun clean -fd | Out-Null
    Log ('허용되지 않은 파일 변경 → 되돌림: ' + ($bad -join ', '))
    Mail '[암사동성당 WYD] 자동 처리 중단 (확인 필요)' ("허용되지 않은 파일이 바뀌어 모두 되돌렸습니다.`n" + ($bad -join "`n") + "`n`n시트의 새 글을 직접 확인하거나 Claude에게 처리를 요청하세요.")
    return $true                                                  # 같은 글로 반복하지 않음
  }

  $commitUrl = '(커밋 없음)'
  if ($files.Count -gt 0) {
    $msgFile = Join-Path $Out 'commit_msg.txt'
    $msg = if (Test-Path $msgFile) { ([IO.File]::ReadAllText($msgFile, $Utf8) -split "`n")[0].Trim() } else { '' }
    if (-not $msg) { $msg = '수정요청 반영' }
    $tmp = Join-Path $Work 'msg.txt'; [IO.File]::WriteAllText($tmp, $msg + "`n", $Utf8)
    GitRun add -A | Out-Null
    GitRun -c user.name=GunhoJin -c user.email=redangeljin@gmail.com commit -F $tmp | Out-Null
    GitRun push origin main | Out-Null
    if (-not $GitOk) { GitRun pull --rebase origin main | Out-Null; GitRun push origin main | Out-Null }
    if (-not $GitOk) { Log 'push 실패'; Mail '[암사동성당 WYD] 자동 처리 push 실패' 'PC의 저장소에 커밋은 됐지만 push 하지 못했습니다. watch.log 를 확인하세요.'; return $false }
    $sha = (& git -C $Repo rev-parse HEAD).Trim()
    $commitUrl = "https://github.com/GunhoJin/amsa-wyd-2027/commit/$sha"
    Log "push 완료 $sha"
  }

  foreach ($f in @('mail_request.txt', 'mail_inquiry.txt')) {
    $p = Join-Path $Out $f
    if (-not (Test-Path $p)) { continue }
    $t = [IO.File]::ReadAllText($p, $Utf8).Replace('{{COMMIT_URL}}', $commitUrl).Replace("`r", '')
    $i = $t.IndexOf("`n")
    if ($i -lt 1) { continue }
    Mail $t.Substring(0, $i).Trim() $t.Substring($i + 1).Trim()
    Remove-Item $p -Force
  }
  return $true
}

# ── 실행 ────────────────────────────────────────────────
if ($Test) {
  try { $l = Api @{ op = 'latest' }; Write-Host "연결 확인: $($l.text)" } catch { Write-Host "연결 실패: $_" }
  Write-Host "저장소: $Repo"; Write-Host "Claude: $Claude (존재: $(Test-Path $Claude))"
  exit 0
}
if ($Once) { RunOnce | Out-Null; exit 0 }

$mutex = New-Object System.Threading.Mutex($false, 'Global\AmsaWydWatcher')
if (-not $mutex.WaitOne(0)) { exit 0 }                             # 이미 실행 중

$statePath = Join-Path $Work 'state.txt'
$last = if (Test-Path $statePath) { [IO.File]::ReadAllText($statePath, $Utf8).Trim() } else { '' }
$retryAt = [DateTime]::MinValue
Log '감시 시작'
while ($true) {
  try {
    $l = (Api @{ op = 'latest' }).json
    if ($l.ok) {
      $sig = "$($l.r)|$($l.rn)|$($l.q)|$($l.qn)"
      if ($sig -ne $last -and (Get-Date) -ge $retryAt) {
        Log "새 글 감지: $sig"
        if (@(RunOnce)[-1] -eq $true) { $last = $sig; [IO.File]::WriteAllText($statePath, $sig, $Utf8) }
        else { $retryAt = (Get-Date).AddMinutes(30); Log '실패 → 30분 뒤 다시 시도' }
      }
    } else { Log "latest 거부: key 확인 필요" }
  } catch { Log "오류: $_" }
  Start-Sleep -Seconds $Interval
}
