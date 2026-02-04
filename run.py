import base64
import os
import shutil
import xml.etree.ElementTree as tree
from datetime import datetime
import requests

# Configuration from chrome_installer-main/fetch.py
info = {
    "win_stable_x64": {
        "os": '''platform="win" version="10.0" sp="" arch="x64"''',
        "app": '''appid="{8A69D345-D564-463C-AFF1-A69D9E530F96}" version="" nextversion="" lang="en" brand=""  installage="-1" installdate="-1" iid="{11111111-1111-1111-1111-111111111111}"''',
    },
    "win_beta_x64": {
        "os": '''platform="win" version="10.0" arch="x64"''',
        "app": '''appid="{8A69D345-D564-463C-AFF1-A69D9E530F96}" ap="x64-beta-multi-chrome"''',
    },
    "win_dev_x64": {
        "os": '''platform="win" version="10.0" arch="x64"''',
        "app": '''appid="{8A69D345-D564-463C-AFF1-A69D9E530F96}" ap="x64-dev-multi-chrome"''',
    },
    "win_canary_x64": {
        "os": '''platform="win" version="10.0" arch="x64"''',
        "app": '''appid="{4EA16AC7-FD5A-47C3-875B-DBF4A2008C20}" ap="x64-canary"''',
    },
}

update_url = 'https://tools.google.com/service/update2'

def post(os_xml: str, app_xml: str) -> str:
    xml_data = f'''<?xml version="1.0" encoding="UTF-8"?>
    <request protocol="3.0" updater="Omaha" updaterversion="1.3.36.372" shell_version="1.3.36.352" ismachine="0" sessionid="{11111111-1111-1111-1111-111111111111}" installsource="taggedmi" requestid="{11111111-1111-1111-1111-111111111111}" dedup="cr" domainjoined="0">
    <hw physmemory="16" sse="1" sse2="1" sse3="1" ssse3="1" sse41="1" sse42="1" avx="1"/>
    <os {os_xml}/>
    <app {app_xml}>
    <updatecheck/>
    <data name="install" index="empty"/>
    </app>
    </request>'''
    r = requests.post(update_url, data=xml_data)
    return r.text

def decode(text):
    root = tree.fromstring(text)
    
    manifest_node = root.find('.//manifest')
    if manifest_node is None:
        raise Exception("No manifest found in response. Possible XML error or no update available.")
    manifest_version = manifest_node.get('version')
    
    package_node = root.find('.//package')
    package_name = package_node.get('name')
    
    url_nodes = root.findall('.//url')
    url_prefixes = []
    for node in url_nodes:
        url_prefixes.append(node.get('codebase') + package_name)
        
    return {"version": manifest_version, "urls": url_prefixes}

def build_chrome(channel='win_stable_x64'):
    print(f"Starting build for {channel}...")
    
    # 1. 获取版本信息和下载链接
    config = info.get(channel)
    if not config:
        print(f"Error: Configuration for {channel} not found.")
        return

    res = post(config['os'], config['app'])
    try:
        data = decode(res)
    except Exception as e:
        print(f"Error decoding response: {e}")
        print(res)
        return

    version = data['version']
    print(f"Detected version: {version}")

    # 选择下载链接，优先选择 https://dl.google.com
    download_url = None
    for url in data['urls']:
        if "dl.google.com" in url and url.startswith("https"):
            download_url = url
            break
    if not download_url:
        download_url = data['urls'][0]
    
    print(f"Download URL: {download_url}")

    # 2. 下载 7-Zip 命令行工具 (如果不存在)
    seven_zip_url = 'https://www.7-zip.org/a/7zr.exe'
    seven_zip_path = '7zr.exe'

    if not os.path.exists(seven_zip_path):
        print(f'Downloading 7-Zip from {seven_zip_url}...')
        response = requests.get(seven_zip_url)
        with open(seven_zip_path, 'wb') as f:
            f.write(response.content)
        print('7-Zip downloaded successfully!')

    # 3. 下载 Chrome
    print('Downloading Chrome...')
    response = requests.get(download_url)
    with open("chrome.7z.exe", "wb") as file:
        file.write(response.content)
    
    # 4. 解压 Chrome
    print('Extracting Chrome installer...')
    result1 = os.system(f'{seven_zip_path} x chrome.7z.exe -y')
    if result1 != 0:
        print('Error: Chrome installer extraction failed!')
        return

    # 5. 验证解压结果并获取路径
    path = 'Chrome-bin'
    if not os.path.exists(path):
        print(f'Error: {path} directory not found!')
        return

    # 再次确认版本号（从目录结构）
    detected_version = '0.0.0.0'
    for i in os.listdir(path):
        if os.path.isdir(os.path.join(path, i)) and all(c.isdigit() or c == '.' for c in i):
            detected_version = i
            break
    
    print(f"Version from directory: {detected_version}")
    if detected_version != version:
        print(f"Warning: Directory version {detected_version} differs from manifest version {version}")
        version = detected_version # Trust the directory structure

    # 6. 下载并解压 setdll 工具
    print('Downloading setdll tool...')
    setdll_url = 'https://github.com/Bush2021/chrome_plus/releases/latest/download/setdll.7z'
    response = requests.get(setdll_url)
    with open('setdll.7z', 'wb') as f:
        f.write(response.content)

    print('Extracting setdll tool...')
    os.system(f'{seven_zip_path} x setdll.7z -osetdll_temp -y')

    # 7. 组装文件
    print('Copying configuration and DLLs from setdll...')
    if os.path.exists(os.path.join('setdll_temp', 'chrome++.ini')):
        shutil.copy(os.path.join('setdll_temp', 'chrome++.ini'), os.path.join('Chrome-bin', 'chrome++.ini'))

    if os.path.exists(os.path.join('setdll_temp', 'version-x64.dll')):
        shutil.copy(os.path.join('setdll_temp', 'version-x64.dll'), os.path.join('Chrome-bin', 'version.dll'))

    if os.path.exists(os.path.join('setdll_temp', 'setdll-x64.exe')):
        shutil.copy(os.path.join('setdll_temp', 'setdll-x64.exe'), os.path.join('Chrome-bin', 'setdll-x64.exe'))

    if os.path.exists('Chrome'):
        shutil.rmtree('Chrome')
    os.rename(r'Chrome-bin', 'Chrome')

    # 8. 准备构建输出目录
    os.makedirs('build/release', exist_ok=True)
    if os.path.exists('build/release/Chrome'):
        shutil.rmtree('build/release/Chrome')

    shutil.move(r'Chrome', 'build/release/Chrome')

    # 创建版本信息文件
    with open('build/release/Chrome/version.txt', 'w') as f:
        f.write(version)

    # 9. 执行 DLL 注入
    print('Injecting version.dll into chrome.exe...')
    chrome_dir = 'build/release/Chrome'
    chrome_exe = os.path.join(chrome_dir, version, 'chrome.exe')
    setdll_exe = os.path.join(chrome_dir, 'setdll-x64.exe')
    version_dll = os.path.join(chrome_dir, 'version.dll')

    if os.path.exists(setdll_exe) and os.path.exists(chrome_exe):
        os.system(f'"{setdll_exe}" /d:"{version_dll}" "{chrome_exe}"')
        print('DLL injection completed successfully!')
        # 删除setdll工具
        os.remove(setdll_exe)
    else:
        print(f'Warning: setdll-x64.exe or chrome.exe not found. \nsetdll: {setdll_exe}\nchrome: {chrome_exe}')

    # 10. 清理临时文件
    shutil.rmtree('setdll_temp', ignore_errors=True)
    if os.path.exists('setdll.7z'):
        os.remove('setdll.7z')
    if os.path.exists('chrome.7z.exe'):
        os.remove('chrome.7z.exe')

    # 11. 设置 GitHub Environment (如果运行在 CI 中)
    env_file = os.getenv('GITHUB_ENV')
    # 根据 channel 修改 BUILD_NAME 前缀
    prefix = "Win64"
    if "beta" in channel:
        prefix = "Win64_Beta"
    elif "dev" in channel:
        prefix = "Win64_Dev"
    elif "canary" in channel:
        prefix = "Win64_Canary"
        
    build_name = f'{prefix}_{version}_{datetime.now().strftime("%Y-%m-%d")}'
    
    if env_file:
        with open(env_file, 'a') as f:
            f.write(f'BUILD_NAME={build_name}\n')
    else:
        print(f'BUILD_NAME={build_name}')

if __name__ == '__main__':
    build_chrome('win_stable_x64')
