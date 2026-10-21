# Codex跨设备配置仓库

本仓库用于在macOS与Windows之间同步个人技能、共享规则和插件安装清单。Windows安装脚本执行前会建立备份，并将Mac绝对路径转换为当前Windows用户目录。

## Windows一键安装

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\windows-sync\install.ps1
```

详细说明见 [windows-sync/README.md](windows-sync/README.md)。

## 同步内容

- `skills/`：个人技能、PPT版式参考库及共享规则文件。
- `global-rules/`：跨设备AGENTS规则模板。
- `windows-sync/manifest.json`：技能、共享文件和插件清单。
- `windows-sync/install.ps1`：Windows安装、备份、路径转换和插件恢复脚本。
- `windows-sync/verify.ps1`：Windows端独立核验脚本。

## 安全边界

仓库不保存Codex登录凭据、API密钥、聊天记录、插件缓存、运行时缓存、项目授权路径及Mac专用MCP配置。远程插件在Windows端首次使用时按界面提示完成账户授权。
