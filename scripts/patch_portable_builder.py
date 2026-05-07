import sys
from pathlib import Path


OLD = '''    if target.get("version_dll_location") == "version_dir":
        dll_arg = "/d:version.dll"
        cwd = target_exe.parent
    else:
        dll_arg = f"/d:{version_dll.resolve()}"
        cwd = staged["app_root"]
'''

NEW = '''    version_dll_path = version_dll.resolve()
    target_exe_path = target_exe.resolve()
    if version_dll_path.parent == target_exe_path.parent:
        dll_arg = "/d:version.dll"
        cwd = target_exe_path.parent
    elif target.get("version_dll_location") == "version_dir":
        dll_arg = "/d:version.dll"
        cwd = target_exe.parent
    else:
        dll_arg = f"/d:{version_dll_path}"
        cwd = staged["app_root"]
'''


def main():
    builder_path = Path(sys.argv[1] if len(sys.argv) > 1 else "_portable_builder/portable_builder/builder.py")
    text = builder_path.read_text(encoding="utf-8")

    if OLD not in text:
        if "version_dll_path = version_dll.resolve()" in text:
            print(f"[INFO] Portable builder already patched: {builder_path}")
            return 0
        raise RuntimeError(f"Expected injection block not found in {builder_path}")

    builder_path.write_text(text.replace(OLD, NEW), encoding="utf-8")
    print(f"[INFO] Patched portable builder DLL injection: {builder_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
