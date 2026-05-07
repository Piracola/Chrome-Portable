import argparse
import glob
import re
import subprocess
import shutil
import tempfile
from pathlib import Path


ABSOLUTE_VERSION_DLL = re.compile(rb"[A-Za-z]:\\[^\x00]*version\.dll", re.IGNORECASE)


def check_exe(path):
    data = Path(path).read_bytes()
    matches = sorted(set(match.group(0).decode("ascii", errors="replace") for match in ABSOLUTE_VERSION_DLL.finditer(data)))
    if matches:
        raise RuntimeError(f"{path} contains non-portable version.dll import: {matches[0]}")


def resolve_seven_zip(preferred):
    candidates = []
    if preferred:
        candidates.append(preferred)

    candidates.extend(
        [
            "7zr.exe",
            "7zr",
            "7z.exe",
            "7z",
            "7za.exe",
            "7za",
            str(Path("7zr.exe").resolve()),
            str(Path("7z.exe").resolve()),
            r"C:\Program Files\7-Zip\7z.exe",
            r"C:\Program Files\7-Zip\7zr.exe",
        ]
    )

    checked = []
    for candidate in candidates:
        if not candidate:
            continue
        checked.append(candidate)
        candidate_path = Path(candidate)
        if candidate_path.exists():
            return str(candidate_path.resolve())
        from_path = shutil.which(candidate)
        if from_path:
            return from_path

    portable_builder_root = Path("_portable_builder")
    if portable_builder_root.exists():
        for tool_name in ("7zr.exe", "7z.exe", "7za.exe"):
            for found in portable_builder_root.rglob(tool_name):
                checked.append(str(found))
                if found.exists():
                    return str(found.resolve())

    raise RuntimeError(
        "No usable 7z executable found. "
        f"Checked: {', '.join(checked)}"
    )


def extract_and_check_archive(seven_zip, archive):
    with tempfile.TemporaryDirectory(prefix="chrome_portable_verify_") as temp_dir:
        temp_path = Path(temp_dir)
        cmd = [str(seven_zip), "x", str(archive), "-y", f"-o{temp_path}", "Chrome\\chrome.exe"]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
        except FileNotFoundError as exc:
            raise RuntimeError(f"7z executable not found: {seven_zip}") from exc
        if result.returncode != 0:
            raise RuntimeError(result.stderr or result.stdout or f"Failed to extract {archive}")

        exes = list(temp_path.rglob("chrome.exe"))
        if not exes:
            raise RuntimeError(f"chrome.exe not found in {archive}")
        for exe in exes:
            check_exe(exe)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", help="chrome.exe files or .7z archives to verify")
    parser.add_argument("--seven-zip", default=None)
    args = parser.parse_args()

    seven_zip = resolve_seven_zip(args.seven_zip)
    print(f"[INFO] Using 7z executable: {seven_zip}")
    paths = []
    for raw_path in args.paths:
        matches = glob.glob(raw_path)
        paths.extend(matches or [raw_path])

    for raw_path in paths:
        path = Path(raw_path)
        if path.suffix.lower() == ".7z":
            extract_and_check_archive(seven_zip, path)
        else:
            check_exe(path)
        print(f"[INFO] Portable import check passed: {path}")


if __name__ == "__main__":
    main()
