param(
    [string]$RepoRoot = (Split-Path -Parent $PSScriptRoot)
)

$ErrorActionPreference = "Stop"
$manifest = Get-Content -LiteralPath (Join-Path $PSScriptRoot "manifest.json") -Raw -Encoding UTF8 | ConvertFrom-Json
$codexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $env:USERPROFILE ".codex" }
$skillsHome = Join-Path $codexHome "skills"

$rows = foreach ($skill in $manifest.skills) {
    $root = Join-Path $skillsHome $skill.name
    $entry = Join-Path $root $skill.entryFile
    [PSCustomObject]@{
        Skill = $skill.name
        Directory = Test-Path -LiteralPath $root
        EntryFile = Test-Path -LiteralPath $entry
    }
}

$rows | Format-Table -AutoSize

$missing = @($rows | Where-Object { -not $_.Directory -or -not $_.EntryFile })
if ($missing.Count -gt 0) {
    throw "有 $($missing.Count) 个技能未通过核验。"
}

if (Get-Command codex -ErrorAction SilentlyContinue) {
    codex plugin list --json
} else {
    Write-Warning "未检测到codex命令，无法执行插件清单核验。"
}

Write-Host "技能文件核验完成。" -ForegroundColor Green
