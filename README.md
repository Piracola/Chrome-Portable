<div align="center">

# Chrome 便携版

集成 Chrome++ 的 Google Chrome 便携版，由 GitHub Actions 自动构建，提供 Stable 与 Beta 渠道。

[![最新版本][badge-release]][link-release]
[![总下载量][badge-downloads]][link-release]
[![构建状态][badge-build]][link-actions]
[![许可证][badge-license]][link-license]

**语言 / Language:** **简体中文** · [English](README.en.md)

**[⬇ 下载最新版本][link-release]** · **[📖 使用说明与常见问题][link-site]**

</div>

## 项目简介

本项目由 GitHub Actions 每日检查 Google 官方 Chrome 离线安装包更新，集成 Chrome++ 并封装为便携版。Stable 与 Beta 两个渠道分别提供 Windows x64 与 ARM64 压缩包，发布在同一个 GitHub Release 下。

构建系统由 [ChromiumPortable](https://github.com/Piracola/ChromiumPortable) 提供，本仓库只保存构建配置；本地构建步骤见核心仓的[开发文档](https://github.com/Piracola/ChromiumPortable/blob/main/docs/DEVELOPMENT.md)。

## 快速开始

1. 从 [Releases](https://github.com/Piracola/Chrome-Portable/releases/latest) 下载压缩包（`Chrome++_stable_...7z` 为正式版，`Chrome++_beta_...7z` 为测试版），解压到任意位置。
2. 运行 `开始.bat` 在解压根目录生成 `Chrome.lnk` 快捷方式，之后从快捷方式启动。

Stable 与 Beta 不建议交替切换，可能导致数据读取错误、闪退或无法启动。

## 压缩包与架构

| 系统架构 | Stable 正式版 | Beta 测试版 |
| --- | --- | --- |
| Windows x64 | `Chrome++_stable_<版本>_<日期>.7z` | `Chrome++_beta_<版本>_<日期>.7z` |
| Windows ARM64（Windows 11 on Arm） | `Chrome++_stable_arm64_<版本>_<日期>.7z` | `Chrome++_beta_arm64_<版本>_<日期>.7z` |

ARM64 包用的是 Google 官方 ARM64 浏览器和同架构的 Chrome++ 组件。引擎在 x64 机器上用 x64 的 `setdll` 改写 ARM64 PE，verify 阶段校验导入表以及 `chrome.exe`、`version.dll` 的 `Machine = 0xAA64`；真实启动测试得在 ARM64 Windows 上做。

## 更新

1. 关闭浏览器。
2. 删除 `Chrome` 文件夹或重命名为 `Chrome old` 以便回退版本。
3. 解压新版压缩包内的 `Chrome` 文件夹，`Data`、`Cache` 保持不动。

## 功能特性

以下增强均已集成，除注明外默认启用，可在 `chrome++.ini` 中调整或关闭：

- 用户数据及缓存均存储于与 `Chrome` 文件夹同级的 `Data` 和 `Cache` 文件夹（解压根目录下）
- 双击关闭标签页、保留最后一个标签页
- 悬停标签栏时滚轮切换标签页
- 新建前台标签页打开地址栏内容或书签
- 免验证系统登录密码即可查看已保存密码
- 支持右键关闭标签、老板键、翻译快捷键、按键映射、启动/退出钩子等扩展（默认未启用，详见 `chrome++.ini`）
- 发布包不携带 Google Update / Google Updater，因此不会自行替换整套浏览器；扩展和安全组件更新保持可用
- 更多增强功能请查看 `chrome++.ini`

## 更改数据目录位置

数据目录的位置由 `Chrome\chrome++.ini` 里的 `data_dir` 和 `cache_dir` 两行决定，默认值是 `%app%\..\Data` 和 `%app%\..\Cache`（`%app%` 代表 `chrome.exe` 所在目录，所以默认落在 `Chrome` 文件夹旁边）。值支持绝对路径，目录会自动创建。注意这个文件是 **UTF-16 编码**（记事本另存时选「Unicode」）。

默认路径相对于主程序目录，移动整个文件夹不需要修改。需要将数据存放到程序目录之外时，可改用绝对路径。

## 卸载

删除解压根目录即可，便携版不写注册表。

## 相关项目

- [ChromiumPortable](https://github.com/Piracola/ChromiumPortable)：通用构建核心，Chrome++ 组件随引擎包从它的 `setdll/` 目录发布，上游同步也在那里完成
- [Edge_Portable](https://github.com/Piracola/Edge_Portable)：同系列 Microsoft Edge 便携版
- [Helium_Portable](https://github.com/Piracola/Helium_Portable)：同系列 Helium 便携版

## 致谢

本项目使用以下开源项目与上游服务：

| 项目 | 说明 |
| --- | --- |
| [Bush2021/chrome\_plus](https://github.com/Bush2021/chrome_plus) | 提供核心便携化组件（Chrome++ / version.dll / setdll） |
| Google Omaha update2 API | Chrome 官方版本查询与安装包下载 |

## 许可证

本项目源码遵循 MIT 许可证。

- Google Chrome 浏览器版权归 Google 所有

---

<div align="center">

<sub>Built and maintained by</sub>

**Piracola**

</div>

<!-- 徽标定义：中文标签需 percent-encode，否则 shields.io 无法解析。 -->
<!-- 修改标签文字时请一并更新编码，例如 最新版本 -> %E6%9C%80%E6%96%B0%E7%89%88%E6%9C%AC -->
[badge-release]: https://img.shields.io/github/v/release/Piracola/Chrome-Portable?display_name=tag&style=flat-square&color=d8653f&label=%E6%9C%80%E6%96%B0%E7%89%88%E6%9C%AC
[badge-downloads]: https://img.shields.io/github/downloads/Piracola/Chrome-Portable/total?style=flat-square&color=2ea043&label=%E6%80%BB%E4%B8%8B%E8%BD%BD%E9%87%8F
[badge-build]: https://img.shields.io/github/actions/workflow/status/Piracola/Chrome-Portable/build.yml?branch=main&style=flat-square&label=%E6%9E%84%E5%BB%BA%E7%8A%B6%E6%80%81
[badge-license]: https://img.shields.io/github/license/Piracola/Chrome-Portable?style=flat-square&color=6e7681&label=%E8%AE%B8%E5%8F%AF%E8%AF%81

[link-release]: https://github.com/Piracola/Chrome-Portable/releases/latest
[link-site]: https://piracola.github.io/ChromiumPortable/chrome/
[link-actions]: https://github.com/Piracola/Chrome-Portable/actions/workflows/build.yml
[link-license]: https://github.com/Piracola/Chrome-Portable/blob/main/LICENSE
