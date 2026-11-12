<div align="center">

# Chrome Portable

Portable Google Chrome with Chrome++ integrated, built automatically by GitHub Actions, in both Stable and Beta channels.

[![Latest release][badge-release]][link-release]
[![Total downloads][badge-downloads]][link-release]
[![Build status][badge-build]][link-actions]
[![License][badge-license]][link-license]

**Language / 语言:** [简体中文](README.md) · **English**

**[⬇ Download the latest release][link-release]** · **[📖 Usage guide & FAQ][link-site]**

</div>

## About

GitHub Actions checks Google's official Chrome offline installers every day, integrates Chrome++, and repackages the result as a portable build. The Stable and Beta channels each ship both a Windows x64 and an ARM64 archive, published under one shared GitHub Release.

The build system is provided by [ChromiumPortable](https://github.com/Piracola/ChromiumPortable); this repository only holds the build configuration. For a local build, see the core repository's [development docs](https://github.com/Piracola/ChromiumPortable/blob/main/docs/DEVELOPMENT.md).

## Quick start

1. Download an archive from [Releases](https://github.com/Piracola/Chrome-Portable/releases/latest) — `Chrome++_stable_...7z` is the stable channel, `Chrome++_beta_...7z` is beta — and extract it anywhere.
2. Run `开始.bat` to create the `Chrome.lnk` shortcut inside the extraction folder, then launch from that shortcut.

Avoid switching back and forth between Stable and Beta: it can cause profile read errors, crashes, or a browser that refuses to start.

<details>
<summary>Archives and architectures</summary>

| Architecture | Stable channel | Beta channel |
| --- | --- | --- |
| Windows x64 | `Chrome++_stable_<version>_<date>.7z` | `Chrome++_beta_<version>_<date>.7z` |
| Windows ARM64 (Windows 11 on Arm) | `Chrome++_stable_arm64_<version>_<date>.7z` | `Chrome++_beta_arm64_<version>_<date>.7z` |

The ARM64 archive pairs Google's official ARM64 browser with a matching-architecture Chrome++ component. The engine rewrites the ARM64 PE on an x64 machine using the x64 `setdll`, and the verify stage checks the import table plus `Machine = 0xAA64` on both `chrome.exe` and `version.dll`; an actual launch test has to happen on ARM64 Windows.

</details>

## Updating

1. Close the browser.
2. Delete the `Chrome` folder, or rename it to `Chrome old` if you want a rollback option.
3. Extract the `Chrome` folder from the new archive and leave `Data` and `Cache` alone.

## Features

Everything below is included and enabled by default unless noted; adjust or switch it off in `chrome++.ini`:

- Profile data and cache live in the `Data` and `Cache` folders next to `Chrome` (at the extraction root)
- Double-click a tab to close it; the last tab stays open
- Scroll the mouse wheel over the tab strip to switch tabs
- Open whatever sits in the address bar, or a bookmark, in a new foreground tab
- View saved passwords without going through the Windows sign-in prompt
- Optional extras: close tabs with the right mouse button, boss key, translate shortcut, key remapping, start/exit hooks and more (off by default; see `chrome++.ini`)
- The release carries no Google Update / Google Updater, so the browser never replaces itself with a full install; extension and security component updates keep working
- More enhancements are documented in `chrome++.ini`

<details>
<summary>Changing the data directory</summary>

The location is set by the `data_dir` and `cache_dir` lines in `Chrome\chrome++.ini`. Defaults are `%app%\..\Data` and `%app%\..\Cache`, where `%app%` is the folder holding `chrome.exe`, so data lands next to `Chrome`. Absolute paths are accepted and directories are created as needed. Note that the file is **UTF-16 encoded** (pick "Unicode" when saving from Notepad).

Because the defaults are relative to the program folder, moving the whole tree needs no edits. Switch to an absolute path if you want data stored outside the program folder.

</details>

## Uninstalling

Delete the extraction root. The portable build writes nothing to the registry.

## Related projects

- [ChromiumPortable](https://github.com/Piracola/ChromiumPortable): shared build core — the Chrome++ component ships with the engine bundle from its `setdll/` folder, and upstream syncing happens there too
- [Edge_Portable](https://github.com/Piracola/Edge_Portable): the Microsoft Edge portable build
- [Helium_Portable](https://github.com/Piracola/Helium_Portable): the Helium portable build

<details>
<summary>Credits</summary>

| Project | Role |
| --- | --- |
| [Bush2021/chrome\_plus](https://github.com/Bush2021/chrome_plus) | Core portability components (Chrome++ / version.dll / setdll) |
| Google Omaha update2 API | Official version lookup and installer download |

</details>

## License

Source in this repository is MIT licensed.

- Google Chrome is copyright Google

---

<div align="center">

<sub>Built and maintained by</sub>

**Piracola**

</div>

<!-- Badge labels: percent-encode spaces, otherwise shields.io cannot parse the URL. -->
[badge-release]: https://img.shields.io/github/v/release/Piracola/Chrome-Portable?display_name=tag&style=flat-square&color=d8653f&label=latest%20release
[badge-downloads]: https://img.shields.io/github/downloads/Piracola/Chrome-Portable/total?style=flat-square&color=2ea043&label=total%20downloads
[badge-build]: https://img.shields.io/github/actions/workflow/status/Piracola/Chrome-Portable/build.yml?branch=main&style=flat-square&label=build%20status
[badge-license]: https://img.shields.io/github/license/Piracola/Chrome-Portable?style=flat-square&color=6e7681&label=license

[link-release]: https://github.com/Piracola/Chrome-Portable/releases/latest
[link-site]: https://piracola.github.io/ChromiumPortable/en/chrome/
[link-actions]: https://github.com/Piracola/Chrome-Portable/actions/workflows/build.yml
[link-license]: https://github.com/Piracola/Chrome-Portable/blob/main/LICENSE
