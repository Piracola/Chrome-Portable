import os
import re
import requests
from run import info, post, decode

def get_upstream_version(channel):
    config = info.get(channel)
    if not config:
        return None
    try:
        res = post(config['os'], config['app'])
        data = decode(res)
        return data['version']
    except Exception as e:
        print(f"Error getting upstream version for {channel}: {e}")
        return None

def get_latest_release_info():
    repo = os.getenv('GITHUB_REPOSITORY')
    if not repo:
        print("GITHUB_REPOSITORY not set, assuming local test or first run")
        return None
    
    token = os.getenv('GITHUB_TOKEN')
    headers = {}
    if token:
        headers['Authorization'] = f'token {token}'
        
    url = f"https://api.github.com/repos/{repo}/releases/latest"
    try:
        resp = requests.get(url, headers=headers)
        if resp.status_code == 404:
            print("No releases found.")
            return None
        resp.raise_for_status()
        data = resp.json()
        body = data.get('body', '')
        
        stable_match = re.search(r'Stable 版本:\s*([\d\.]+)', body)
        beta_match = re.search(r'Beta 版本:\s*([\d\.]+)', body)
        
        stable_ver = stable_match.group(1) if stable_match else None
        beta_ver = beta_match.group(1) if beta_match else None
        
        return {
            'id': data.get('id'),
            'tag_name': data.get('tag_name'),
            'stable_version': stable_ver,
            'beta_version': beta_ver,
        }
    except Exception as e:
        print(f"Error getting latest release: {e}")
        return None

def get_major_version(version):
    if not version:
        return None
    parts = version.split('.')
    if parts:
        return parts[0]
    return None

def is_major_version_update(new_version, old_version):
    new_major = get_major_version(new_version)
    old_major = get_major_version(old_version)
    
    if new_major and old_major:
        return new_major != old_major
    return False

def main():
    print("Checking for updates...")
    
    upstream_stable = get_upstream_version('win_stable_x64')
    upstream_beta = get_upstream_version('win_beta_x64')
    
    print(f"Upstream Stable: {upstream_stable}")
    print(f"Upstream Beta: {upstream_beta}")
    
    if not upstream_stable or not upstream_beta:
        print("Failed to get upstream versions. Forcing build to be safe.")
        env_file = os.getenv('GITHUB_ENV')
        if env_file:
            with open(env_file, 'a') as f:
                f.write("UPDATE_NEEDED=true\n")
                f.write("STABLE_UPDATE=true\n")
                f.write("BETA_UPDATE=true\n")
        return

    release_info = get_latest_release_info()
    
    if release_info:
        latest_stable = release_info.get('stable_version')
        latest_beta = release_info.get('beta_version')
        release_id = release_info.get('id')
        release_tag = release_info.get('tag_name')
        print(f"Latest Release ID: {release_id}")
        print(f"Latest Release Tag: {release_tag}")
        print(f"Latest Release Stable: {latest_stable}")
        print(f"Latest Release Beta: {latest_beta}")
    else:
        latest_stable = None
        latest_beta = None
        release_id = None
        release_tag = None
    
    stable_update = upstream_stable != latest_stable
    beta_update = upstream_beta != latest_beta
    
    if stable_update:
        print("Stable version mismatch/update detected.")
    if beta_update:
        print("Beta version mismatch/update detected.")
        
    if not latest_stable and not latest_beta:
        print("No previous version info found or failed to parse. Treating as update needed.")
        stable_update = True
        beta_update = True

    update_needed = stable_update or beta_update
    print(f"Update needed: {update_needed}")
    print(f"Stable update: {stable_update}")
    print(f"Beta update: {beta_update}")
    
    create_new_release = False
    if not release_id:
        create_new_release = True
        print("No existing release found. Will create new release.")
    elif stable_update and is_major_version_update(upstream_stable, latest_stable):
        create_new_release = True
        print(f"Major version update detected: {latest_stable} -> {upstream_stable}. Will create new release.")
    else:
        print("Minor version update. Will update existing release.")
    
    print(f"Create new release: {create_new_release}")
    
    env_file = os.getenv('GITHUB_ENV')
    if env_file:
        with open(env_file, 'a') as f:
            f.write(f"UPDATE_NEEDED={str(update_needed).lower()}\n")
            f.write(f"STABLE_UPDATE={str(stable_update).lower()}\n")
            f.write(f"BETA_UPDATE={str(beta_update).lower()}\n")
            f.write(f"UPSTREAM_STABLE={upstream_stable or ''}\n")
            f.write(f"UPSTREAM_BETA={upstream_beta or ''}\n")
            f.write(f"CREATE_NEW_RELEASE={str(create_new_release).lower()}\n")
            if release_id:
                f.write(f"RELEASE_ID={release_id}\n")
            if release_tag:
                f.write(f"RELEASE_TAG={release_tag}\n")

if __name__ == '__main__':
    main()
