# Windows兼容性说明

## 一、已完成跨平台处理的内容

- Windows安装脚本按照当前用户目录写入 `.codex\skills` 和 `.codex\AGENTS.md`。
- 个人技能中的 `/Users/shampwu` 绝对路径在安装时转换为Windows用户目录。
- 官方插件通过Windows端Codex插件命令重新安装，插件缓存和运行时文件不跨系统复制。
- `slide-image-dual-render`不携带macOS生成的`node_modules`，Windows已具备npm时执行`npm ci`重建依赖。

## 二、需要Windows本机依赖的功能

- `slide-maker`和`slide-visual-polish-qa`包含LibreOffice、PowerPoint及浏览器渲染能力，实际调用时需要Windows端安装相应应用并配置可执行文件路径。
- `slide-editable-deck-orchestrator`保留macOS检查脚本作为源文件；Windows端不得调用`macos_env.sh`和`verify_macos.sh`。
- 党政公文及中文PPT排版依赖仿宋_GB2312、方正小标宋简体、微软雅黑等字体，Windows端应确认字体已安装。

## 三、需要重新授权的账户连接

- Gmail、Google Drive、Google Calendar、GitHub、Notion等远程插件在首次使用时执行账户授权。
- 同步包不保存令牌、Cookie、API密钥和Codex登录文件。
- 远程插件能否安装取决于Windows端Codex版本、账户权限及工作区插件政策；安装脚本将失败信息写入核验报告。
