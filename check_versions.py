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

def get_latest_release_versions():
    repo = os.getenv('GITHUB_REPOSITORY')
    if not repo:
        print("GITHUB_REPOSITORY not set, assuming local test or first run")
        return None, None
    
    token = os.getenv('GITHUB_TOKEN')
    headers = {}
    if token:
        headers['Authorization'] = f'token {token}'
        
    url = f"https://api.github.com/repos/{repo}/releases/latest"
    try:
        resp = requests.get(url, headers=headers)
        if resp.status_code == 404:
            print("No releases found.")
            return None, None
        resp.raise_for_status()
        data = resp.json()
        body = data.get('body', '')
        
        # 解析 Body
        # 格式:
        # Stable 版本: 121.0.6167.160
        # Beta 版本: 122.0.6261.39
        
        stable_match = re.search(r'Stable 版本:\s*([\d\.]+)', body)
        beta_match = re.search(r'Beta 版本:\s*([\d\.]+)', body)
        
        stable_ver = stable_match.group(1) if stable_match else None
        beta_ver = beta_match.group(1) if beta_match else None
        
        return stable_ver, beta_ver
    except Exception as e:
        print(f"Error getting latest release: {e}")
        return None, None

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
        return

    latest_stable, latest_beta = get_latest_release_versions()
    print(f"Latest Release Stable: {latest_stable}")
    print(f"Latest Release Beta: {latest_beta}")
    
    update_needed = False
    
    if upstream_stable != latest_stable:
        print("Stable version mismatch/update detected.")
        update_needed = True
        
    if upstream_beta != latest_beta:
        print("Beta version mismatch/update detected.")
        update_needed = True
        
    if not latest_stable and not latest_beta:
        print("No previous version info found or failed to parse. Treating as update needed.")
        update_needed = True

    print(f"Update needed: {update_needed}")
    
    # Write to GITHUB_ENV
    env_file = os.getenv('GITHUB_ENV')
    if env_file:
        with open(env_file, 'a') as f:
            f.write(f"UPDATE_NEEDED={str(update_needed).lower()}\n")

if __name__ == '__main__':
    main()
