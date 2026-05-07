import argparse
import glob
import re
import subprocess
import tempfile
from pathlib import Path


ABSOLUTE_VERSION_DLL = re.compile(rb"[A-Za-z]:\\[^\x00]*version\.dll", re.IGNORECASE)


def check_exe(path):
    data = Path(path).read_bytes()
    matches = sorted(set(match.group(0).decode("ascii", errors="replace") for match in ABSOLUTE_VERSION_DLL.finditer(data)))
    if matches:
        raise RuntimeError(f"{path} contains non-portable version.dll import: {matches[0]}")


def extract_and_check_archive(seven_zip, archive):
    with tempfile.TemporaryDirectory(prefix="chrome_portable_verify_") as temp_dir:
        temp_path = Path(temp_dir)
        cmd = [str(seven_zip), "x", str(archive), "-y", f"-o{temp_path}", "Chrome\\chrome.exe"]
        result = subprocess.run(cmd, capture_output=True, text=True)
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
    parser.add_argument("--seven-zip", default="7zr.exe")
    args = parser.parse_args()

    seven_zip = Path(args.seven_zip)
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
