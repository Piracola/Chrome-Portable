import os
import re
import requests
import sys
from run import info, post, decode

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def get_upstream_version(channel):
    config = info.get(channel)
    if not config:
        return None
    try:
        res = post(config['os'], config['app'])
        data = decode(res)
        return data['version']
    except Exception as e:
        print(f"[ERROR] Failed to get upstream version for {channel}: {e}")
        return None

def extract_version_from_body(body, version_type):
    patterns = [
        rf'{version_type}\s*版本[:：]\s*([\d\.]+)',
        rf'{version_type}\s*Version[:：]\s*([\d\.]+)',
        rf'{version_type}\s*[:：]\s*([\d\.]+)',
    ]
    for pattern in patterns:
        match = re.search(pattern, body, re.IGNORECASE)
        if match:
            return match.group(1)
    return None

def get_latest_release_info():
    repo = os.getenv('GITHUB_REPOSITORY')
    if not repo:
        print("[INFO] GITHUB_REPOSITORY not set, assuming local test or first run")
        return None

    token = os.getenv('GITHUB_TOKEN')
    headers = {}
    if token:
        headers['Authorization'] = f'token {token}'

    url = f"https://api.github.com/repos/{repo}/releases/latest"
    try:
        resp = requests.get(url, headers=headers)
        if resp.status_code == 404:
            print("[INFO] No releases found.")
            return None
        resp.raise_for_status()
        data = resp.json()
        body = data.get('body', '')
        tag_name = data.get('tag_name', '')

        print(f"[DEBUG] Release body preview (first 500 chars):\n{body[:500]}...")

        stable_ver = extract_version_from_body(body, 'Stable')
        beta_ver = extract_version_from_body(body, 'Beta')

        if not stable_ver:
            print("[WARN] Failed to extract Stable version from release body")
        if not beta_ver:
            print("[WARN] Failed to extract Beta version from release body")

        return {
            'id': data.get('id'),
            'tag_name': tag_name,
            'stable_version': stable_ver,
            'beta_version': beta_ver,
        }
    except Exception as e:
        print(f"[ERROR] Failed to get latest release: {e}")
        return None

def get_major_version(version):
    if not version:
        return None
    parts = version.split('.')
    if parts:
        return parts[0]
    return None

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

def is_major_version_update(new_version, old_version):
    new_major = get_major_version(new_version)
    old_major = get_major_version(old_version)

    if new_major and old_major:
        return new_major != old_major
    return False

def is_stable_minor_update(new_version, old_version):
    if not new_version or not old_version:
        return False
    new_major = get_major_version(new_version)
    old_major = get_major_version(old_version)
    if new_major and old_major and new_major == old_major:
        return new_version != old_version
    return False

def main():
    print("=" * 60)
    print("[INFO] Starting version check...")
    print("=" * 60)

    # Manual dispatch forces build regardless of version comparison
    event_name = os.getenv('GITHUB_EVENT_NAME', '')
    force_build = event_name == 'workflow_dispatch'
    if force_build:
        print("[INFO] Manual dispatch detected — forcing build.")

    upstream_stable = get_upstream_version('win_stable_x64')
    upstream_beta = get_upstream_version('win_beta_x64')

    print(f"[INFO] Upstream Stable: {upstream_stable}")
    print(f"[INFO] Upstream Beta: {upstream_beta}")

    if not upstream_stable or not upstream_beta:
        print("[ERROR] Failed to get upstream versions. Forcing build to be safe.")
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
        print(f"[INFO] Latest Release ID: {release_id}")
        print(f"[INFO] Latest Release Tag: {release_tag}")
        print(f"[INFO] Latest Release Stable: {latest_stable}")
        print(f"[INFO] Latest Release Beta: {latest_beta}")
    else:
        latest_stable = None
        latest_beta = None
        release_id = None
        release_tag = None

    # Force build when manually triggered
    if force_build:
        stable_update = True
        beta_update = True
        update_needed = True
        print("[FORCE] All updates forced by manual dispatch.")
    elif latest_stable and latest_beta:
        stable_update = False
        beta_update = False
        if upstream_stable != latest_stable:
            if is_version_upgrade(upstream_stable, latest_stable):
                stable_update = True
                print(f"[INFO] Stable version upgrade detected: {latest_stable} -> {upstream_stable}")
            else:
                print(f"[WARN] Stable version not upgraded ({latest_stable} -> {upstream_stable}), skipping update")

        if upstream_beta != latest_beta:
            if is_version_upgrade(upstream_beta, latest_beta):
                beta_update = True
                print(f"[INFO] Beta version upgrade detected: {latest_beta} -> {upstream_beta}")
            else:
                print(f"[WARN] Beta version not upgraded ({latest_beta} -> {upstream_beta}), skipping update")

        update_needed = stable_update or beta_update
    else:
        print("[WARN] Previous version info incomplete or missing. Checking for safe update...")
        if latest_stable:
            if upstream_stable != latest_stable and is_version_upgrade(upstream_stable, latest_stable):
                stable_update = True
                print(f"[INFO] Stable update needed (partial info): {latest_stable} -> {upstream_stable}")
        else:
            stable_update = True
            print("[INFO] No previous stable version found, will update stable")

        if latest_beta:
            if upstream_beta != latest_beta and is_version_upgrade(upstream_beta, latest_beta):
                beta_update = True
                print(f"[INFO] Beta update needed (partial info): {latest_beta} -> {upstream_beta}")
        else:
            beta_update = True
            print("[INFO] No previous beta version found, will update beta")

        update_needed = stable_update or beta_update

    print("-" * 60)
    print(f"[RESULT] Update needed: {update_needed}")
    print(f"[RESULT] Stable update: {stable_update}")
    print(f"[RESULT] Beta update: {beta_update}")
    print("-" * 60)

    create_new_release = False
    stable_minor_update = False

    if not release_id:
        create_new_release = True
        print("[INFO] No existing release found. Will create new release.")
    elif stable_update and latest_stable and is_major_version_update(upstream_stable, latest_stable):
        create_new_release = True
        print(f"[INFO] Major Stable version update detected: {latest_stable} -> {upstream_stable}. Will create new release.")
    else:
        print("[INFO] Will update existing release.")
        if stable_update and latest_stable and is_stable_minor_update(upstream_stable, latest_stable):
            stable_minor_update = True
            print(f"[INFO] Stable minor version update detected: {latest_stable} -> {upstream_stable}. Will update release title.")

    print(f"[RESULT] Create new release: {create_new_release}")
    print(f"[RESULT] Stable minor update: {stable_minor_update}")
    print("=" * 60)

    env_file = os.getenv('GITHUB_ENV')
    if env_file:
        with open(env_file, 'a') as f:
            f.write(f"UPDATE_NEEDED={str(update_needed).lower()}\n")
            f.write(f"STABLE_UPDATE={str(stable_update).lower()}\n")
            f.write(f"BETA_UPDATE={str(beta_update).lower()}\n")
            f.write(f"UPSTREAM_STABLE={upstream_stable or ''}\n")
            f.write(f"UPSTREAM_BETA={upstream_beta or ''}\n")
            f.write(f"CREATE_NEW_RELEASE={str(create_new_release).lower()}\n")
            f.write(f"STABLE_MINOR_UPDATE={str(stable_minor_update).lower()}\n")
            if release_id:
                f.write(f"RELEASE_ID={release_id}\n")
            if release_tag:
                f.write(f"RELEASE_TAG={release_tag}\n")
        print("[INFO] Environment variables written successfully.")

if __name__ == '__main__':
    main()
