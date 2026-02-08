# Chrome 便携版

> 全自动构建的谷歌浏览器便携版，集成 Chrome++ 增强组件，提供纯净、高效的浏览体验。

[![Build Status](https://github.com/Piracola/Chrome-Portable/actions/workflows/build.yml/badge.svg)](https://github.com/Piracola/Chrome-Portable/actions/workflows/build.yml)

## 项目简介

本项目为全自动无人值守构建脚本，每周定时从 Google 官方获取最新 Chrome 离线安装包，集成 Chrome++ 组件并封装为便携版。旨在解决官方版本数据路径固定、无法便携移动以及缺乏部分实用功能的问题。

## 功能特性

以下功能均可在`chrome++.ini`中修改：
- 所有用户数据及缓存均存储于程序同级目录的 `Data` 和 `Cache` 文件夹
- 双击关闭标签页、保留最后一个标签页
- 悬停标签栏时滚轮切换标签页，按住右键时滚轮滚动标签栏
- 支持新建前台标签页打开书签或地址栏内容

## 快速开始

**安装**

1. 下载：访问 [Releases](https://github.com/Piracola/Chrome-Portable/releases/latest) 获取最新版本
2. 解压：将压缩包解压至任意位置
3. 运行`开始.bat`文件创建快捷方式


**更新**
1. 把旧版chrome文件夹重命名为 chrome old 以便于回退版本。
2. 解压新版chrome文件夹到同级目录。


**本地构建**

```bash
pip install -r requirements.txt
python run.py
```

## 致谢

本项目基于以下优秀开源项目构建：

| 项目 | 说明 |
|------|------|
| [Bush2021/chrome_plus](https://github.com/Bush2021/chrome_plus) | 提供核心便携化组件 |
| [rnamoy/chrome_installer](https://github.com/rnamoy/chrome_installer) | 提供安装包解析 |

## 许可证

本项目源码遵循 MIT 许可证。

- Google Chrome 浏览器版权归 Google 所有
- Chrome++ 组件版权归原作者所有

---

本项目采用 GitHub Actions 每日自动检查更新，版本号与 Chrome 官方 Stable/Beta 分支保持一致。查看 [Releases](https://github.com/Piracola/Chrome-Portable/releases) 获取历史版本。
