# Windows端安装说明

## 执行方法

1. 在Windows端安装并登录最新版Codex。
2. 克隆本仓库或下载仓库ZIP并解压。
3. 关闭正在运行的Codex任务。
4. 在仓库根目录打开PowerShell，执行：

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\windows-sync\install.ps1
```

5. 安装完成后重新启动Codex。
6. 首次调用Gmail、Google Drive、GitHub、Notion、Google Calendar等远程插件时，按界面提示完成账户授权。

## 安装范围

- Mac端个人技能及其引用文件、模板、脚本和资源。
- 全局AGENTS规则与两份PPT共享规则。
- Mac端已安装插件清单及启用状态。
- `slide-image-dual-render`所需Node依赖；Windows已安装npm时自动执行。

## 保留范围

- Windows端原有技能和配置在安装前写入时间戳备份目录。
- Windows端项目授权目录、MCP本机路径、桌面偏好和登录状态保持原值。
- Mac端令牌、认证文件、聊天记录、插件缓存和运行时缓存不进入仓库。

## 独立核验

```powershell
.\windows-sync\verify.ps1
```

核验结果同时保存在 `%USERPROFILE%\.codex\sync-reports`。
