import os
import shutil
import xml.dom.minidom
from datetime import datetime

import requests

url = 'https://tools.google.com/service/update2'

# Create XML request message for Google Omaha
# https://github.com/google/omaha/blob/master/doc/ServerProtocolV3.md
data = """<?xml version="1.0" encoding="UTF-8"?>
<request protocol="3.0" updater="Omaha" updaterversion="1.3.36.112" shell_version="1.3.36.111"
	installsource="update3web-ondemand" dedup="cr" ismachine="0" domainjoined="0">
	<os platform="win" version="10.0.22000.282" arch="x64"/>
	<app appid="{8A69D345-D564-463C-AFF1-A69D9E530F96}" ap="x64-stable-multi-chrome" lang="en-us">
		<updatecheck />
	</app>
</request>"""

response = requests.post(url, data=data)

dom = xml.dom.minidom.parseString(response.text)

print(dom.toprettyxml(indent='  '))

url = dom.getElementsByTagName("url")[0].getAttribute("codebase")
name = dom.getElementsByTagName("action")[0].getAttribute("run")

print(url, name)

# 下载7-Zip命令行工具（如果不存在）
seven_zip_url = 'https://www.7-zip.org/a/7zr.exe'
seven_zip_path = '7zr.exe'

if not os.path.exists(seven_zip_path):
    print(f'Downloading 7-Zip from {seven_zip_url}...')
    response = requests.get(seven_zip_url)
    with open(seven_zip_path, 'wb') as f:
        f.write(response.content)
    print('7-Zip downloaded successfully!')

# 下载Chrome
response = requests.get(url + name)

with open("chrome.7z.exe", "wb") as file:
    file.write(response.content)

# 使用7zr.exe解压Chrome
print('Extracting Chrome installer...')
result1 = os.system(f'{seven_zip_path} x chrome.7z.exe -y')

if result1 != 0:
    print('Error: Chrome installer extraction failed!')
    exit(1)

# 获得Chrime-bin,version.dll,组装到一块就可以分发了
version = '0.0.0.0'
path = 'Chrome-bin'

# 检查Chrome-bin目录是否存在
if not os.path.exists(path):
    print(f'Error: {path} directory not found!')
    print('Chrome extraction failed. Please check if 7z is installed correctly.')
    print('Current directory contents:')
    for file in os.listdir('.'):
        print(f'  - {file}')
    exit(1)

for i in os.listdir(path):
    if os.path.isdir(os.path.join(path, i)):
        version = i
        break

print(version)
if version == '0.0.0.0':
    exit(1)

# 获得Chrome-bin,version.dll,组装到一块就可以分发了
shutil.move(r'version.dll', 'Chrome-bin')
shutil.move(r'chrome++.ini', 'Chrome-bin')

os.rename(r'Chrome-bin', 'Chrome')

# 确保构建目录存在
os.makedirs('build/release', exist_ok=True)

shutil.move(r'Chrome', 'build/release/Chrome')

# 创建版本信息文件
with open('build/release/Chrome/version.txt', 'w') as f:
    f.write(version)

# 创建必要的数据目录
os.makedirs('build/release/Chrome/Data', exist_ok=True)
os.makedirs('build/release/Chrome/Cache', exist_ok=True)

# 下载setdll工具
print('Downloading setdll tool...')
setdll_url = 'https://github.com/Bush2021/chrome_plus/releases/latest/download/setdll.7z'
response = requests.get(setdll_url)
with open('setdll.7z', 'wb') as f:
    f.write(response.content)

# 解压setdll工具
print('Extracting setdll tool...')
os.system(f'{seven_zip_path} x setdll.7z -osetdll_temp')

# 复制setdll工具到Chrome目录
for file in os.listdir('setdll_temp'):
    if file.startswith('setdll-') or file.startswith('version-'):
        shutil.copy(os.path.join('setdll_temp', file), 'build/release/Chrome/')

# 执行DLL注入
print('Injecting version.dll into chrome.exe...')
chrome_dir = 'build/release/Chrome'
chrome_exe = os.path.join(chrome_dir, version, 'chrome.exe')
setdll_exe = os.path.join(chrome_dir, 'setdll-x64.exe')
version_dll = os.path.join(chrome_dir, 'version.dll')

if os.path.exists(setdll_exe):
    os.system(f'"{setdll_exe}" /d:"{version_dll}" "{chrome_exe}"')
    print('DLL injection completed successfully!')
else:
    print('Warning: setdll-x64.exe not found, skipping DLL injection')

# 清理临时文件
shutil.rmtree('setdll_temp', ignore_errors=True)
os.remove('setdll.7z')

# 清理自动下载的7zr.exe（可选，保留以便下次使用）
# os.remove('7zr.exe')

# 删除setdll工具文件（保留注入后的chrome.exe和version.dll）
for file in os.listdir(chrome_dir):
    if file.startswith('setdll-'):
        os.remove(os.path.join(chrome_dir, file))

# 会自动封装为zip
env = os.getenv('GITHUB_ENV')
with open(env, 'a') as f:
    f.write(f'BUILD_NAME=Win64_{version}_{datetime.now().strftime("%Y-%m-%d")}')

# os.system(f'7z.exe a build/release/Win64_{version}_{datetime.now().strftime("%Y-%m-%d")}.7z Chrome')
