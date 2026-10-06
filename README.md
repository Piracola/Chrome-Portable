<div align="center">

# Chrome 便携版

全自动构建的谷歌浏览器便携版，集成 Chrome++ 增强组件，提供纯净、高效的浏览体验。

[![最新版本][badge-release]][link-release]
[![总下载量][badge-downloads]][link-release]
[![构建状态][badge-build]][link-actions]
[![许可证][badge-license]][link-license]

**[⬇ 下载最新版本][link-release]** · **[📖 使用说明与常见问题][link-site]**

</div>

> 想了解构建系统或新增浏览器？见 [ChromiumPortable](https://github.com/Piracola/ChromiumPortable)——本仓库仅是其构建配置之一。

## 仓库导航

- [Chrome 便携版下载页](https://piracola.github.io/ChromiumPortable/chrome/)：安装、更新、校验与常见问题的完整说明。
- [ChromiumPortable（主仓库/构建核心）](https://github.com/Piracola/ChromiumPortable)：通用构建核心仓库。
- [Edge_Portable](https://github.com/Piracola/Edge_Portable)：同系列 Microsoft Edge 便携版项目。
- [Helium_Portable](https://github.com/Piracola/Helium_Portable)：同系列 Helium 便携版项目。

## 项目简介

本项目由 GitHub Actions 每日自动检查 Google 官方是否有最新 Chrome 离线安装包更新，集成 Chrome++ 组件并封装为便携版。项目同时构建 Stable 与 Beta 两个渠道，发布在同一个 GitHub Release 下。增强功能默认配置见 `chrome++.ini`。

## 功能特性

以下功能均已默认启用，可在 `chrome++.ini` 中调整或关闭：

- 用户数据及缓存均存储于与 `Chrome` 文件夹同级的 `Data` 和 `Cache` 文件夹（解压根目录下）
- 双击关闭标签页、保留最后一个标签页
- 悬停标签栏时滚轮切换标签页
- 新建前台标签页打开地址栏内容或书签
- 免验证系统登录密码即可查看已保存密码
- 支持右键关闭标签、老板键、翻译快捷键、按键映射、启动/退出钩子等扩展（默认未启用，详见 `chrome++.ini`）
- 发布包不携带 Google Update / Google Updater，因此不会自行替换整套浏览器；扩展和安全组件更新保持可用
- 更多增强功能请查看 `chrome++.ini`

## 快速开始

**安装**

1. 下载：访问 [Releases](https://github.com/Piracola/Chrome-Portable/releases/latest) 获取最新版本
2. 选择渠道：`Chrome++_stable_...7z` 为正式版（推荐），`Chrome++_beta_...7z` 为测试版
3. 解压：将压缩包解压至任意位置
4. 运行 `开始.bat` 文件创建快捷方式

> ⚠️ Stable 与 Beta 不建议交替切换，可能导致数据读取错误、闪退或无法启动。

**更新**

1. 关闭浏览器。
2. 备份与旧版 `Chrome` 文件夹同级的 `Data` 目录（复制到安全位置）。
3. 删除旧版 `Chrome` 文件夹（或重命名为 `Chrome old` 以便回退版本）。
4. 解压新版 `Chrome` 文件夹到同级目录。
5. 把备份的 `Data` 放回新版 `Chrome` 文件夹旁边。

> 想保留旧版以便回退：把旧文件夹改名为 `Chrome old`，新版解压到同级即可；回退时同理。

**更改数据目录位置**

数据目录的位置由 `Chrome\chrome++.ini` 里的 `data_dir` 和 `cache_dir` 两行决定，默认值是 `%app%\..\Data` 和 `%app%\..\Cache`（`%app%` 代表 `chrome.exe` 所在目录，所以默认落在 `Chrome` 文件夹旁边）。想放到别的位置，改这两行后重启浏览器即可，目录会自动创建。

值既可以写绝对路径（如 `data_dir=D:\BrowserData`），也可以用 `%app%` 加相对层数。要注意这个文件是 **UTF-16 编码**，用记事本编辑后另存时请把编码选成「Unicode」，否则浏览器读不到配置、设置会静默失效。

默认路径本来就会跟着程序走，整个文件夹一起搬动不需要改这里；只有想把数据放到程序外面（比如放在空间更大的分区）时才需要改。

**卸载**

删除 `Chrome` 文件夹即可完成卸载（便携，不写注册表）。

**本地构建**（Windows + Python 3，需将 `ChromiumPortable` 检出到同级目录）

```powershell
python -m pip install requests
$env:PYTHONPATH="..\ChromiumPortable"
python -m portable_builder --config browser.json --target chrome_stable --workdir . build
# 构建 Beta 版：将 --target 改为 chrome_beta
```

## 致谢

本项目基于以下优秀开源项目构建：

| 项目                                                               | 说明                                         |
| ---------------------------------------------------------------- | ------------------------------------------ |
| [Bush2021/chrome\_plus](https://github.com/Bush2021/chrome_plus) | 提供核心便携化组件（Chrome++ / version.dll / setdll） |
| Google Omaha update2 API                                         | Chrome 官方版本查询与安装包下载                        |

## 许可证

本项目源码遵循 MIT 许可证。

- Google Chrome 浏览器版权归 Google 所有
- Chrome++ 组件版权归原作者所有

本项目采用 GitHub Actions 每日自动检查更新，版本号与 Chrome 官方 Stable/Beta 分支保持一致。查看 [Releases](https://github.com/Piracola/Chrome-Portable/releases) 获取历史版本。

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
