import os
import re
import requests
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def get_github_api_headers():
    token = os.getenv('GITHUB_TOKEN')
    headers = {
        'Accept': 'application/vnd.github.v3+json',
    }
    if token:
        headers['Authorization'] = f'token {token}'
    return headers

def compare_versions(v1, v2):
    if not v1 or not v2:
        return 0
    try:
        parts1 = [int(x) for x in v1.split('.')]
        parts2 = [int(x) for x in v2.split('.')]
        for i in range(max(len(parts1), len(parts2))):
            p1 = parts1[i] if i < len(parts1) else 0
            p2 = parts2[i] if i < len(parts2) else 0
            if p1 > p2:
                return 1
            elif p1 < p2:
                return -1
        return 0
    except ValueError as e:
        print(f"[WARN] Version comparison error: {e}")
        return 0

def is_version_upgrade(new_version, old_version):
    return compare_versions(new_version, old_version) > 0

def delete_release_asset(release_id, asset_id):
    repo = os.getenv('GITHUB_REPOSITORY')
    url = f"https://api.github.com/repos/{repo}/releases/assets/{asset_id}"
    headers = get_github_api_headers()
    
    resp = requests.delete(url, headers=headers)
    if resp.status_code == 204:
        print(f"[INFO] Deleted asset {asset_id}")
        return True
    else:
        print(f"[ERROR] Failed to delete asset {asset_id}: {resp.status_code} {resp.text}")
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
    print(f"[INFO] Searching for assets matching pattern: '{pattern}'")
    assets = get_release_assets(release_id)
    deleted_count = 0
    for asset in assets:
        name = asset.get('name', '')
        if pattern in name.lower():
            asset_id = asset.get('id')
            print(f"[INFO] Deleting asset: {name} (ID: {asset_id})")
            if delete_release_asset(release_id, asset_id):
                deleted_count += 1
    print(f"[INFO] Deleted {deleted_count} assets matching '{pattern}'")
    return deleted_count

def update_release_body(release_id, new_body):
    repo = os.getenv('GITHUB_REPOSITORY')
    url = f"https://api.github.com/repos/{repo}/releases/{release_id}"
    headers = get_github_api_headers()
    
    data = {
        'body': new_body
    }
    
    resp = requests.patch(url, headers=headers, json=data)
    if resp.status_code == 200:
        print(f"[INFO] Updated release {release_id} body")
        return True
    else:
        print(f"[ERROR] Failed to update release body: {resp.status_code} {resp.text}")
        return False

def delete_git_tag(tag_name):
    repo = os.getenv('GITHUB_REPOSITORY')
    if not tag_name:
        print("[WARN] No tag name provided for deletion")
        return False
    
    url = f"https://api.github.com/repos/{repo}/git/refs/tags/{tag_name}"
    headers = get_github_api_headers()
    
    print(f"[INFO] Deleting old git tag: {tag_name}")
    resp = requests.delete(url, headers=headers)
    if resp.status_code == 204:
        print(f"[INFO] Successfully deleted git tag: {tag_name}")
        return True
    else:
        print(f"[WARN] Failed to delete git tag {tag_name}: {resp.status_code} {resp.text}")
        print("[WARN] This may be expected if the tag was lightweight or already deleted")
        return False

def update_release_title_and_tag(release_id, new_title, new_tag, old_tag=None):
    repo = os.getenv('GITHUB_REPOSITORY')
    url = f"https://api.github.com/repos/{repo}/releases/{release_id}"
    headers = get_github_api_headers()
    
    data = {
        'name': new_title,
        'tag_name': new_tag
    }
    
    print(f"[INFO] Updating release title to '{new_title}' and tag to '{new_tag}'")
    resp = requests.patch(url, headers=headers, json=data)
    if resp.status_code == 200:
        print(f"[INFO] Successfully updated release {release_id} title and tag")
        
        if old_tag and old_tag != new_tag:
            delete_git_tag(old_tag)
        
        env_file = os.getenv('GITHUB_ENV')
        if env_file:
            with open(env_file, 'a') as f:
                f.write(f"RELEASE_TAG={new_tag}\n")
                f.write(f"RELEASE_TITLE={new_title}\n")
            print(f"[INFO] Updated environment variables: RELEASE_TAG={new_tag}, RELEASE_TITLE={new_title}")
        
        return True
    else:
        print(f"[ERROR] Failed to update release title/tag: {resp.status_code} {resp.text}")
        return False

def generate_release_body(stable_version, beta_version):
    lines = [
        "Chrome++ 构建版本",
        "",
        f"Stable 版本: {stable_version}",
        f"Beta 版本: {beta_version}",
    ]
    return "\n".join(lines)

def extract_version_from_tag(tag_name):
    if not tag_name:
        return None
    match = re.search(r'v?(\d+\.\d+\.\d+\.\d+)', tag_name)
    if match:
        return match.group(1)
    return None

def main():
    print("=" * 60)
    print("[INFO] Starting release update process...")
    print("=" * 60)
    
    release_id = os.getenv('RELEASE_ID')
    stable_update = os.getenv('STABLE_UPDATE', 'false').lower() == 'true'
    beta_update = os.getenv('BETA_UPDATE', 'false').lower() == 'true'
    stable_minor_update = os.getenv('STABLE_MINOR_UPDATE', 'false').lower() == 'true'
    stable_version = os.getenv('STABLE_VERSION', '')
    beta_version = os.getenv('BETA_VERSION', '')
    upstream_stable = os.getenv('UPSTREAM_STABLE', '')
    upstream_beta = os.getenv('UPSTREAM_BETA', '')
    release_tag = os.getenv('RELEASE_TAG', '')
    
    print(f"[INFO] Release ID: {release_id}")
    print(f"[INFO] Stable update: {stable_update}")
    print(f"[INFO] Beta update: {beta_update}")
    print(f"[INFO] Stable minor update: {stable_minor_update}")
    print(f"[INFO] Build Stable version: {stable_version}")
    print(f"[INFO] Build Beta version: {beta_version}")
    print(f"[INFO] Upstream Stable: {upstream_stable}")
    print(f"[INFO] Upstream Beta: {upstream_beta}")
    print(f"[INFO] Current release tag: {release_tag}")
    
    if not release_id:
        print("[WARN] No existing release ID found. This will be handled by the create release step.")
        return
    
    final_stable = stable_version if stable_version else upstream_stable
    final_beta = beta_version if beta_version else upstream_beta

    # Safety check: skip body update if both versions are empty
    if not final_stable and not final_beta:
        print("[WARN] Both stable and beta versions are empty. Skipping release body update.")
        print("[WARN] This likely means the build steps didn't produce version info.")
        return
    
    print("-" * 60)
    print(f"[INFO] Final Stable version: {final_stable}")
    print(f"[INFO] Final Beta version: {final_beta}")
    print("-" * 60)
    
    if stable_update:
        print("[INFO] Processing Stable update...")
        delete_assets_by_pattern(release_id, 'stable')
    else:
        print("[INFO] No Stable update needed, skipping stable asset deletion")
    
    if beta_update:
        print("[INFO] Processing Beta update...")
        delete_assets_by_pattern(release_id, 'beta')
    else:
        print("[INFO] No Beta update needed, skipping beta asset deletion")
    
    new_body = generate_release_body(final_stable, final_beta)
    print(f"[INFO] Generated new release body:\n{new_body}")
    update_release_body(release_id, new_body)
    
    if stable_minor_update and final_stable:
        current_version = extract_version_from_tag(release_tag)
        print(f"[INFO] Checking version upgrade for title update:")
        print(f"  Current tag version: {current_version}")
        print(f"  New Stable version: {final_stable}")
        
        if current_version:
            if is_version_upgrade(final_stable, current_version):
                new_title = f"Chrome++ {final_stable}"
                new_tag = f"v{final_stable}"
                update_release_title_and_tag(release_id, new_title, new_tag, old_tag=release_tag)
            else:
                print(f"[WARN] New version ({final_stable}) is NOT newer than current ({current_version}).")
                print("[WARN] Skipping title/tag update to prevent version rollback.")
        else:
            print("[WARN] Could not extract version from current tag. Updating anyway.")
            new_title = f"Chrome++ {final_stable}"
            new_tag = f"v{final_stable}"
            update_release_title_and_tag(release_id, new_title, new_tag, old_tag=release_tag)
    else:
        if not stable_minor_update:
            print("[INFO] Not a stable minor update, skipping title/tag update")
        if not final_stable:
            print("[INFO] No stable version available, skipping title/tag update")
    
    print("=" * 60)
    print("[INFO] Release update completed successfully.")
    print("=" * 60)

if __name__ == '__main__':
    main()
