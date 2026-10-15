import urllib.request
import urllib.error
import json
import base64
import time
import sys
from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from app.config import GITHUB_TOKEN, GITHUB_USERNAME

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
    "User-Agent": "WisdomOwabor-ReadmeFixer",
    "X-GitHub-Api-Version": "2022-11-28"
}

def github_request(url, method="GET", data=None):
    payload = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=payload, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            content = resp.read().decode("utf-8")
            return resp.status, json.loads(content) if content else {}
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8")
        try:
            return e.code, json.loads(err_msg)
        except Exception:
            return e.code, {"message": err_msg}
    except Exception as e:
        return 500, {"message": str(e)}

def fix_readmes():
    print(f"[*] Checking all 20 repositories for @{GITHUB_USERNAME}...")
    
    # 20 repositories
    repos = [
        ("secops-vuln-scanner", "vuln-scanner"),
        ("secops-phishing-detector", "phishing-detector"),
        ("secops-traffic-sentinel", "traffic-sentinel"),
        ("secops-rbac-simulator", "rbac-simulator"),
        ("secops-entropy-guard", "entropy-guard"),
        ("secops-honeypot-telemetry", "honeypot-telemetry"),
        ("secops-secure-vault", "secure-vault"),
        ("secops-ransomware-guard", "ransomware-guard"),
        ("itsupport-asset-tracker", "asset-tracker"),
        ("itsupport-config-auditor", "config-auditor"),
        ("itsupport-patch-manager", "patch-manager"),
        ("itsupport-keylogger-detector", "keylogger-detector"),
        ("itsupport-backup-validator", "backup-validator"),
        ("itsupport-ticket-routing", "ticket-routing"),
        ("secops-settlement-debugger", "settlement-debugger"),
        ("itsupport-csat-analytics", "csat-analytics"),
        ("itsupport-kb-assistant", "kb-assistant"),
        ("secops-market-scraper", "market-scraper"),
        ("secops-market-predictor", "market-predictor"),
        ("secops-social-trend-bot", "social-trend-bot"),
    ]
    
    updated_count = 0
    
    for repo_name, slug in repos:
        print(f"\n--> Checking {repo_name} ...", flush=True)
        url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{repo_name}/contents/README.md"
        status, data = github_request(url)
        
        if status != 200 or "content" not in data:
            print(f"    [!] Failed to get README.md for {repo_name}: status {status}", flush=True)
            continue
            
        sha = data["sha"]
        raw_content = base64.b64decode(data["content"]).decode("utf-8")
        
        need_update = False
        new_content = raw_content
        
        if "wisdomportfolio.local" in new_content:
            need_update = True
            new_content = new_content.replace("https://wisdomportfolio.local", "http://wisdomowabor.online")
            new_content = new_content.replace("http://wisdomportfolio.local", "http://wisdomowabor.online")
            
        # Also ensure links point to http://wisdomowabor.online/projects/{slug}
        # e.g., if it has [http://wisdomowabor.online/projects] instead of [http://wisdomowabor.online/projects/{slug}]
        # Let's ensure both live badge and author link have the direct slug route:
        live_badge_old = "[![Live Demo](https://img.shields.io/badge/Live%20Lab-Runnable%20Sandbox-10b981.svg)](http://wisdomowabor.online/projects)"
        live_badge_new = f"[![Live Demo](https://img.shields.io/badge/Live%20Lab-Runnable%20Sandbox-10b981.svg)](http://wisdomowabor.online/projects/{slug})"
        if live_badge_old in new_content:
            need_update = True
            new_content = new_content.replace(live_badge_old, live_badge_new)
            
        live_link_old = "- Portfolio Live Labs: [http://wisdomowabor.online/projects](http://wisdomowabor.online/projects)"
        live_link_new = f"- Portfolio Live Lab: [http://wisdomowabor.online/projects/{slug}](http://wisdomowabor.online/projects/{slug})"
        if live_link_old in new_content:
            need_update = True
            new_content = new_content.replace(live_link_old, live_link_new)

        if need_update:
            print(f"    [*] Updating README.md for {repo_name}...", flush=True)
            encoded = base64.b64encode(new_content.encode("utf-8")).decode("utf-8")
            put_data = {
                "message": f"docs: update live demo link to http://wisdomowabor.online/projects/{slug}",
                "content": encoded,
                "sha": sha
            }
            put_status, put_res = github_request(url, method="PUT", data=put_data)
            if put_status in [200, 201]:
                print(f"    [+] Successfully updated README.md for {repo_name}", flush=True)
                updated_count += 1
            else:
                print(f"    [!] Failed to update {repo_name}: {put_status} - {put_res}", flush=True)
            time.sleep(1)
        else:
            print(f"    [+] {repo_name} README.md is already up-to-date with wisdomowabor.online!", flush=True)
            
    print(f"\n[+] Total READMEs updated on GitHub: {updated_count}", flush=True)

if __name__ == "__main__":
    fix_readmes()
