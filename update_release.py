import os
import requests

def get_github_api_headers():
    token = os.getenv('GITHUB_TOKEN')
    headers = {
        'Accept': 'application/vnd.github.v3+json',
    }
    if token:
        headers['Authorization'] = f'token {token}'
    return headers

def delete_release_asset(release_id, asset_id):
    repo = os.getenv('GITHUB_REPOSITORY')
    url = f"https://api.github.com/repos/{repo}/releases/assets/{asset_id}"
    headers = get_github_api_headers()
    
    resp = requests.delete(url, headers=headers)
    if resp.status_code == 204:
        print(f"Deleted asset {asset_id}")
        return True
    else:
        print(f"Failed to delete asset {asset_id}: {resp.status_code} {resp.text}")
        return False

def get_release_assets(release_id):
    repo = os.getenv('GITHUB_REPOSITORY')
    url = f"https://api.github.com/repos/{repo}/releases/{release_id}"
    headers = get_github_api_headers()
    
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    return data.get('assets', [])

def delete_assets_by_pattern(release_id, pattern):
    assets = get_release_assets(release_id)
    for asset in assets:
        name = asset.get('name', '')
        if pattern in name.lower():
            asset_id = asset.get('id')
            print(f"Deleting asset: {name} (ID: {asset_id})")
            delete_release_asset(release_id, asset_id)

def update_release_body(release_id, new_body):
    repo = os.getenv('GITHUB_REPOSITORY')
    url = f"https://api.github.com/repos/{repo}/releases/{release_id}"
    headers = get_github_api_headers()
    
    data = {
        'body': new_body
    }
    
    resp = requests.patch(url, headers=headers, json=data)
    if resp.status_code == 200:
        print(f"Updated release {release_id} body")
        return True
    else:
        print(f"Failed to update release body: {resp.status_code} {resp.text}")
        return False

def generate_release_body(stable_version, beta_version):
    lines = [
        "Chrome++ 构建版本",
        "",
        f"Stable 版本: {stable_version}",
        f"Beta 版本: {beta_version}",
    ]
    return "\n".join(lines)

def main():
    release_id = os.getenv('RELEASE_ID')
    stable_update = os.getenv('STABLE_UPDATE', 'false').lower() == 'true'
    beta_update = os.getenv('BETA_UPDATE', 'false').lower() == 'true'
    stable_version = os.getenv('STABLE_VERSION', '')
    beta_version = os.getenv('BETA_VERSION', '')
    upstream_stable = os.getenv('UPSTREAM_STABLE', '')
    upstream_beta = os.getenv('UPSTREAM_BETA', '')
    
    if not release_id:
        print("No existing release ID found. This will be handled by the create release step.")
        return
    
    print(f"Updating release {release_id}")
    print(f"Stable update: {stable_update}")
    print(f"Beta update: {beta_update}")
    
    if stable_update:
        print("Deleting old stable assets...")
        delete_assets_by_pattern(release_id, 'stable')
    
    if beta_update:
        print("Deleting old beta assets...")
        delete_assets_by_pattern(release_id, 'beta')
    
    final_stable = stable_version if stable_version else upstream_stable
    final_beta = beta_version if beta_version else upstream_beta
    
    new_body = generate_release_body(final_stable, final_beta)
    update_release_body(release_id, new_body)
    
    print("Release update completed.")

if __name__ == '__main__':
    main()
