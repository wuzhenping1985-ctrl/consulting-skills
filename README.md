# Consulting Skills

Portable Codex skills for management consulting work. These skills use Markdown-only instructions and relative references so they can be used on macOS and Windows.

## Skills

- `financial-diagnosis`: financial performance diagnosis, metrics, bridges, peer gaps, and management actions.
- `industry-research`: market sizing, value chain, competition, policy, trends, and industry outlook.
- `ppt-storyline`: consulting-style deck storylines, slide messages, evidence chains, and executive summaries.
- `strategy-analysis`: strategic options, growth paths, where-to-play/how-to-win choices, and roadmaps.
- `management-consulting-methods`: issue trees, MECE structures, hypotheses, workplans, and synthesis.
- `proposal-sow`: consulting proposals, SOWs, workstreams, deliverables, and governance.

## Install By Copying

Copy each skill folder into the Codex skills directory.

macOS:

```bash
mkdir -p ~/.codex/skills
cp -R skills/* ~/.codex/skills/
```

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\skills"
Copy-Item -Recurse -Force .\skills\* "$env:USERPROFILE\.codex\skills\"
```

Restart Codex after copying.

## Install From GitHub

After pushing this repository to GitHub, install individual skills with the Codex skill installer:

```text
帮我从这个 GitHub 地址安装 skill：
https://github.com/<owner>/<repo>/tree/main/skills/financial-diagnosis
```

Repeat for any other skill folder, or ask Codex to install several paths from the same repository.
