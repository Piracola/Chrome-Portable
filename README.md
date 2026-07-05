# Chrome 便携版

> 全自动构建的谷歌浏览器便携版，集成 Chrome++ 增强组件，提供纯净、高效的浏览体验。

[![Build Status](https://github.com/Piracola/Chrome-Portable/actions/workflows/build.yml/badge.svg)](https://github.com/Piracola/Chrome-Portable/actions/workflows/build.yml)

> 想了解构建系统或新增浏览器？见 [ChromiumPortable](https://github.com/Piracola/ChromiumPortable)——本仓库仅是其构建配置之一。

## 仓库导航

- [ChromiumPortable（主仓库/构建核心）](https://github.com/Piracola/ChromiumPortable)：通用构建核心仓库。
- [Edge_Portable](https://github.com/betacola/Edge_Portable)：同系列 Microsoft Edge 便携版项目。
- [Helium_Portable](https://github.com/Piracola/Helium_Portable)：同系列 Helium 便携版项目。

## 项目简介

本项目由 GitHub Actions 每日自动检查 Google 官方是否有最新 Chrome 离线安装包更新，集成 Chrome++ 组件并封装为便携版。项目同时构建 Stable 与 Beta 两个渠道，发布在同一个 GitHub Release 下。增强功能默认配置见 `chrome++.ini`。

## 功能特性

以下功能均已默认启用，可在 `chrome++.ini` 中调整或关闭：

- 用户数据及缓存均存储于程序同级目录的 `Data` 和 `Cache` 文件夹
- 双击关闭标签页、保留最后一个标签页
- 悬停标签栏时滚轮切换标签页
- 新建前台标签页打开地址栏内容或书签
- 免验证系统登录密码即可查看已保存密码
- 支持右键关闭标签、老板键、翻译快捷键、按键映射、启动/退出钩子等扩展（默认未启用，详见 `chrome++.ini`）
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
2. 备份旧版 `Chrome` 文件夹中的 `Data` 目录（复制到安全位置）。
3. 删除旧版 `Chrome` 文件夹（或重命名为 `Chrome old` 以便回退版本）。
4. 解压新版 `Chrome` 文件夹到同级目录。
5. 把备份的 `Data` 放回新版 `Chrome` 文件夹。

> 想保留旧版以便回退：把旧文件夹改名为 `Chrome old`，新版解压到同级即可；回退时同理。

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
