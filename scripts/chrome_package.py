import argparse
import json
import sys
import xml.etree.ElementTree as tree

import requests


UPDATE_URL = "https://tools.google.com/service/update2"
CHANNELS = {
    "stable": {
        "os": 'platform="win" version="10.0" sp="" arch="x64"',
        "app": 'appid="{8A69D345-D564-463C-AFF1-A69D9E530F96}" version="" nextversion="" lang="en" brand="" installage="-1" installdate="-1" iid="{11111111-1111-1111-1111-111111111111}"',
    },
    "beta": {
        "os": 'platform="win" version="10.0" arch="x64"',
        "app": 'appid="{8A69D345-D564-463C-AFF1-A69D9E530F96}" ap="x64-beta-multi-chrome"',
    },
    "dev": {
        "os": 'platform="win" version="10.0" arch="x64"',
        "app": 'appid="{8A69D345-D564-463C-AFF1-A69D9E530F96}" ap="x64-dev-multi-chrome"',
    },
    "canary": {
        "os": 'platform="win" version="10.0" arch="x64"',
        "app": 'appid="{4EA16AC7-FD5A-47C3-875B-DBF4A2008C20}" ap="x64-canary"',
    },
}


def post_update(os_xml, app_xml):
    xml_data = f'''<?xml version="1.0" encoding="UTF-8"?>
<request protocol="3.0" updater="Omaha" updaterversion="1.3.36.372" shell_version="1.3.36.352" ismachine="0" sessionid="{{11111111-1111-1111-1111-111111111111}}" installsource="taggedmi" requestid="{{11111111-1111-1111-1111-111111111111}}" dedup="cr" domainjoined="0">
  <hw physmemory="16" sse="1" sse2="1" sse3="1" ssse3="1" sse41="1" sse42="1" avx="1"/>
  <os {os_xml}/>
  <app {app_xml}>
    <updatecheck/>
    <data name="install" index="empty"/>
  </app>
</request>'''
    response = requests.post(UPDATE_URL, data=xml_data, timeout=60)
    response.raise_for_status()
    return response.text


def decode_response(text):
    root = tree.fromstring(text)
    manifest = root.find(".//manifest")
    package = root.find(".//package")
    if manifest is None or package is None:
        raise RuntimeError("Google update response did not include a manifest/package.")

    package_name = package.get("name")
    urls = []
    for node in root.findall(".//url"):
        codebase = node.get("codebase")
        if codebase:
            urls.append(codebase + package_name)
    if not urls:
        raise RuntimeError("Google update response did not include download URLs.")
    return manifest.get("version"), package_name, urls


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--channel", choices=sorted(CHANNELS), default="stable")
    args = parser.parse_args()

    config = CHANNELS[args.channel]
    version, file_name, urls = decode_response(post_update(config["os"], config["app"]))
    download_url = urls[0]
    for url in urls:
        if url.startswith("https://dl.google.com"):
            download_url = url
            break

    print(json.dumps({
        "version": version,
        "url": download_url,
        "file_name": file_name or "chrome_installer.exe",
        "verify_ssl": True
    }))


if __name__ == "__main__":
    sys.exit(main())
