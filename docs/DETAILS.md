# Chrome 便携版：设置与构建细节

本文收录压缩包命名、构建校验与仓库关系说明。安装、更新、功能配置见仓库根目录的 [README](../README.md)，使用说明与常见问题见 [下载页面](https://piracola.github.io/ChromiumPortable/chrome/)。

## 压缩包与架构

| 系统架构 | Stable 正式版 | Beta 测试版 |
| --- | --- | --- |
| Windows x64 | `Chrome++_stable_<版本>_<日期>.7z` | `Chrome++_beta_<版本>_<日期>.7z` |
| Windows ARM64（Windows 11 on Arm） | `Chrome++_stable_arm64_<版本>_<日期>.7z` | `Chrome++_beta_arm64_<版本>_<日期>.7z` |

ARM64 包使用 Google 官方 ARM64 浏览器和同架构 Chrome++ DLL。引擎在 x64 runner 上用 x64 `setdll` 修改 ARM64 PE，并在 verify 阶段校验导入表与 `chrome.exe`、`version.dll` 的 `Machine = 0xAA64`；ARM64 包的实际启动测试应在 ARM64 Windows 上进行。

Chrome++ 组件随引擎包从 [ChromiumPortable](https://github.com/Piracola/ChromiumPortable) 的 `setdll/` 目录发布，由引擎的每日同步工作流跟进上游。ARM64 Omaha 请求显式声明 Windows 11 完整系统版本和渠道参数，避免 API 回退到 x86 安装包。

## 本地构建

本地构建由 [ChromiumPortable](https://github.com/Piracola/ChromiumPortable) 的图形构建器完成，操作步骤见其 [开发文档](https://github.com/Piracola/ChromiumPortable/blob/main/docs/DEVELOPMENT.md)。

## 相关仓库

- [ChromiumPortable](https://github.com/Piracola/ChromiumPortable)：通用构建核心
- [Edge_Portable](https://github.com/Piracola/Edge_Portable)：同系列 Microsoft Edge 便携版
- [Helium_Portable](https://github.com/Piracola/Helium_Portable)：同系列 Helium 便携版
