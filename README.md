# Chrome 便携版

> 全自动构建的谷歌浏览器便携版，集成 Chrome++ 增强组件，提供纯净、高效的浏览体验。

[![Build Status](https://github.com/Piracola/Chrome-Portable/actions/workflows/build.yml/badge.svg)](https://github.com/Piracola/Chrome-Portable/actions/workflows/build.yml)

## 项目简介

本项目为全自动无人值守构建脚本，每周定时从 Google 官方获取最新 Chrome 离线安装包，集成 Chrome++ 组件并封装为便携版。

## 功能特性

- **便携化设计**
  - 数据隔离：所有用户数据及缓存均存储于程序同级目录的 `Data` 和 `Cache` 文件夹
  - 零侵入：不在系统或注册表中残留，仅需移动文件夹即可保留全部数据

- **功能增强**
  - 标签页管理：支持双击关闭标签页、保留最后一个标签页
  - 鼠标手势：悬停标签栏时滚轮切换标签页，按住右键时滚轮滚动标签栏
  - 便捷操作：支持新建前台标签页打开书签或地址栏内容

- **纯净体验**
  - 移除便携化导致的自动更新错误警告
  - 精简非必要界面元素

## 安装与配置

### 安装步骤

1. 下载：访问 [Releases](https://github.com/Piracola/Chrome-Portable/releases/latest) 下载最新版本
2. 解压：将压缩包解压至任意位置（建议非系统盘）
3. 运行：双击 `Chrome.exe` 启动

### 配置指南

编辑 `chrome++.ini` 调整功能：

- `double_click_close=1`：开启双击关闭标签页
- `keep_last_tab=1`：开启保留最后一个标签页
- 更多配置项请参考文件内注释

## 使用指南

### 更新

1. 下载新版压缩包
2. 保留原目录下的 `Data` 文件夹
3. 解压新版文件覆盖

### 卸载

直接删除整个 Chrome 文件夹即可。

### 本地构建

```bash
pip install -r requirements.txt
python run.py
```

## 许可证

本项目源码遵循 MIT 许可证。

- Google Chrome 浏览器版权归 Google 所有
- Chrome++ 组件版权归原作者所有

## 致谢

- [Bush2021/chrome_plus](https://github.com/Bush2021/chrome_plus)：提供核心便携化组件
- [rnamoy/chrome_installer](https://github.com/rnamoy/chrome_installer)：提供安装包解析

## 更新日志

本项目采用 GitHub Actions 每日自动检查更新，版本号与 Chrome 官方 Stable/Beta 分支保持一致。

查看 [Releases](https://github.com/Piracola/Chrome-Portable/releases) 获取历史版本。
