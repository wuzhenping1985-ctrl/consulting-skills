param(
    [string]$RepoRoot = (Split-Path -Parent $PSScriptRoot),
    [switch]$SkipPluginInstall,
    [switch]$SkipDependencyInstall
)

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

function Write-Stage([string]$Message) {
    Write-Host "`n== $Message ==" -ForegroundColor Cyan
}

function Write-Utf8NoBom([string]$Path, [string]$Content) {
    $utf8 = [System.Text.UTF8Encoding]::new($false)
    [System.IO.File]::WriteAllText($Path, $Content, $utf8)
}

function Backup-Path([string]$Path, [string]$BackupRoot) {
    if (-not (Test-Path -LiteralPath $Path)) {
        return
    }
    $leaf = Split-Path -Leaf $Path
    $target = Join-Path $BackupRoot $leaf
    Copy-Item -LiteralPath $Path -Destination $target -Recurse -Force
}

function Set-PluginEnabled([string]$ConfigPath, [string]$PluginId) {
    if (Test-Path -LiteralPath $ConfigPath) {
        $content = [System.IO.File]::ReadAllText($ConfigPath)
    } else {
        $content = ""
    }

    $escaped = [Regex]::Escape($PluginId)
    $sectionPattern = '(?ms)^\[plugins\."' + $escaped + '"\]\s*(?<body>.*?)(?=^\[|\z)'
    $match = [Regex]::Match($content, $sectionPattern)

    if ($match.Success) {
        $block = $match.Value
        if ($block -match "(?m)^enabled\s*=") {
            $updated = [Regex]::Replace($block, "(?m)^enabled\s*=.*$", "enabled = true")
        } else {
            $updated = $block.TrimEnd() + "`r`nenabled = true`r`n`r`n"
        }
        $content = $content.Substring(0, $match.Index) + $updated + $content.Substring($match.Index + $match.Length)
    } else {
        $content = $content.TrimEnd() + "`r`n`r`n[plugins.`"$PluginId`"]`r`nenabled = true`r`n"
    }

    Write-Utf8NoBom -Path $ConfigPath -Content $content
}

function Convert-PathsForWindows([string]$Root, [string]$HomePosix, [string]$CodexHomePosix) {
    $extensions = @(
        ".md", ".txt", ".json", ".jsonl", ".yaml", ".yml", ".toml",
        ".py", ".js", ".mjs", ".cjs", ".ts", ".tsx", ".jsx",
        ".ps1", ".sh", ".html", ".css", ".xml", ".csv"
    )
    $files = Get-ChildItem -LiteralPath $Root -Recurse -File | Where-Object {
        $extensions -contains $_.Extension.ToLowerInvariant()
    }

    foreach ($file in $files) {
        $content = [System.IO.File]::ReadAllText($file.FullName)
        $updated = $content.Replace("/Users/shampwu/.codex", $CodexHomePosix)
        $updated = $updated.Replace("/Users/shampwu/.agents", "$HomePosix/.agents")
        $updated = $updated.Replace("/Users/shampwu", $HomePosix)
        if ($updated -ne $content) {
            Write-Utf8NoBom -Path $file.FullName -Content $updated
        }
    }
}

$RepoRoot = (Resolve-Path -LiteralPath $RepoRoot).Path
$ManifestPath = Join-Path $PSScriptRoot "manifest.json"
if (-not (Test-Path -LiteralPath $ManifestPath)) {
    throw "未找到同步清单：$ManifestPath"
}

$manifest = Get-Content -LiteralPath $ManifestPath -Raw -Encoding UTF8 | ConvertFrom-Json
$codexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $env:USERPROFILE ".codex" }
$skillsHome = Join-Path $codexHome "skills"
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$backupRoot = Join-Path $codexHome "sync-backups\$timestamp"
$reportRoot = Join-Path $codexHome "sync-reports"
$homePosix = $env:USERPROFILE.Replace("\", "/")
$codexHomePosix = $codexHome.Replace("\", "/")

New-Item -ItemType Directory -Force -Path $skillsHome, $backupRoot, $reportRoot | Out-Null

Write-Stage "备份Windows端现有配置"
Backup-Path -Path (Join-Path $codexHome "AGENTS.md") -BackupRoot $backupRoot
Backup-Path -Path (Join-Path $codexHome "config.toml") -BackupRoot $backupRoot
foreach ($skill in $manifest.skills) {
    Backup-Path -Path (Join-Path $skillsHome $skill.name) -BackupRoot $backupRoot
}
foreach ($file in $manifest.sharedFiles) {
    Backup-Path -Path (Join-Path $skillsHome $file) -BackupRoot $backupRoot
}

Write-Stage "安装个人技能和共享规则"
foreach ($skill in $manifest.skills) {
    $source = Join-Path $RepoRoot "skills\$($skill.name)"
    $target = Join-Path $skillsHome $skill.name
    if (-not (Test-Path -LiteralPath $source)) {
        throw "同步仓库缺少技能目录：$($skill.name)"
    }
    if (Test-Path -LiteralPath $target) {
        Remove-Item -LiteralPath $target -Recurse -Force
    }
    Copy-Item -LiteralPath $source -Destination $target -Recurse -Force
    Convert-PathsForWindows -Root $target -HomePosix $homePosix -CodexHomePosix $codexHomePosix
}

foreach ($file in $manifest.sharedFiles) {
    $source = Join-Path $RepoRoot "skills\$file"
    $target = Join-Path $skillsHome $file
    Copy-Item -LiteralPath $source -Destination $target -Force
    Convert-PathsForWindows -Root $target -HomePosix $homePosix -CodexHomePosix $codexHomePosix
}

$agentsTemplate = Join-Path $RepoRoot "global-rules\AGENTS.template.md"
$agentsTarget = Join-Path $codexHome "AGENTS.md"
$agentsContent = [System.IO.File]::ReadAllText($agentsTemplate).Replace("__CODEX_HOME_POSIX__", $codexHomePosix)
Write-Utf8NoBom -Path $agentsTarget -Content $agentsContent

Write-Stage "安装并启用插件"
$pluginResults = @()
$codexCommand = Get-Command codex -ErrorAction SilentlyContinue
$installedPluginIds = @()
if ($codexCommand) {
    try {
        $installedState = (& codex plugin list --json 2>$null | Out-String) | ConvertFrom-Json
        $installedPluginIds = @($installedState.installed | ForEach-Object { $_.pluginId })
    } catch {
        $installedPluginIds = @()
    }
}
foreach ($plugin in $manifest.plugins) {
    $status = "enabled-in-config"
    $detail = ""
    if ($installedPluginIds -contains $plugin.pluginId) {
        $status = "already-installed"
    } elseif (-not $SkipPluginInstall -and $codexCommand) {
        try {
            $output = & codex plugin add $plugin.pluginId --json 2>&1
            if ($LASTEXITCODE -eq 0) {
                $status = "installed"
                $detail = ($output | Out-String).Trim()
            } else {
                $status = "install-failed"
                $detail = ($output | Out-String).Trim()
            }
        } catch {
            $status = "install-failed"
            $detail = $_.Exception.Message
        }
    } elseif (-not $codexCommand) {
        $status = "codex-cli-unavailable"
        $detail = "已写入启用配置；请在Codex插件目录完成安装。"
    }

    Set-PluginEnabled -ConfigPath (Join-Path $codexHome "config.toml") -PluginId $plugin.pluginId
    $pluginResults += [PSCustomObject]@{
        pluginId = $plugin.pluginId
        status = $status
        detail = $detail
    }
}

if (-not $SkipDependencyInstall) {
    Write-Stage "安装可移植运行依赖"
    $npm = Get-Command npm -ErrorAction SilentlyContinue
    $nodeSkill = Join-Path $skillsHome "slide-image-dual-render"
    if ($npm -and (Test-Path -LiteralPath (Join-Path $nodeSkill "package-lock.json"))) {
        Push-Location $nodeSkill
        try {
            & $npm.Source "ci" "--omit=dev"
            if ($LASTEXITCODE -ne 0) {
                Write-Warning "Node依赖安装未完成，请在$nodeSkill执行npm ci。"
            }
        } finally {
            Pop-Location
        }
    } else {
        Write-Warning "未检测到npm，slide-image-dual-render的Node依赖将在具备npm后安装。"
    }
}

Write-Stage "核验同步结果"
$skillResults = foreach ($skill in $manifest.skills) {
    $path = Join-Path $skillsHome $skill.name
    [PSCustomObject]@{
        name = $skill.name
        exists = Test-Path -LiteralPath $path
        entryFile = $skill.entryFile
        entryExists = Test-Path -LiteralPath (Join-Path $path $skill.entryFile)
    }
}

$report = [PSCustomObject]@{
    completedAt = (Get-Date).ToString("o")
    codexHome = $codexHome
    backupRoot = $backupRoot
    sourceRevision = $manifest.sourceRevision
    skills = $skillResults
    plugins = $pluginResults
    restartRequired = $true
}

$reportPath = Join-Path $reportRoot "windows-sync-$timestamp.json"
Write-Utf8NoBom -Path $reportPath -Content ($report | ConvertTo-Json -Depth 8)

$failedSkills = @($skillResults | Where-Object { -not $_.exists -or -not $_.entryExists })
$failedPlugins = @($pluginResults | Where-Object { $_.status -eq "install-failed" })

Write-Host "`n技能：$($skillResults.Count - $failedSkills.Count)/$($skillResults.Count) 项通过核验"
Write-Host "插件：$($pluginResults.Count - $failedPlugins.Count)/$($pluginResults.Count) 项已安装或写入启用配置"
Write-Host "备份目录：$backupRoot"
Write-Host "核验报告：$reportPath"
Write-Host "请关闭并重新启动Codex。首次调用远程插件时，按界面提示完成账户授权。" -ForegroundColor Green

if ($failedSkills.Count -gt 0) {
    throw "有 $($failedSkills.Count) 个技能未通过文件核验。"
}
