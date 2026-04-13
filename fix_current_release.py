
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

def fix_current_release():
    repo = 'Piracola/Chrome-Portable'
    url = f"https://api.github.com/repos/{repo}/releases/latest"
    headers = get_github_api_headers()
    
    print("[INFO] Getting current latest release...")
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    
    release_id = data['id']
    current_title = data['name']
    current_tag = data['tag_name']
    
    print(f"[INFO] Current Release ID: {release_id}")
    print(f"[INFO] Current Title: {current_title}")
    print(f"[INFO] Current Tag: {current_tag}")
    
    # The correct values should be:
    new_title = "Chrome++ 146.0.7680.178"
    new_tag = "v146.0.7680.178"
    
    print("-" * 60)
    print(f"[INFO] New Title: {new_title}")
    print(f"[INFO] New Tag: {new_tag}")
    
    # Update the release
    update_url = f"https://api.github.com/repos/{repo}/releases/{release_id}"
    data_update = {
        'name': new_title,
        'tag_name': new_tag
    }
    
    print("\n[INFO] Updating release...")
    resp_patch = requests.patch(update_url, headers=headers, json=data_update)
    
    if resp_patch.status_code == 200:
        print("[SUCCESS] Release updated successfully!")
    else:
        print(f"[ERROR] Failed: {resp_patch.status_code}")
        print(resp_patch.text)
        
    return

if __name__ == "__main__":
    import sys
    if len(sys.argv) &lt; 2:
        print("Usage: python fix_current_release.py &lt;GITHUB_TOKEN&gt;")
        exit(1)
    os.environ['GITHUB_TOKEN'] = sys.argv[1]
    fix_current_release()

