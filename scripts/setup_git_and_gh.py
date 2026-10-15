import os
import sys
import zipfile
import urllib.request
import shutil
from pathlib import Path

BIN_DIR = Path(r"C:\Users\user\.gemini\antigravity\bin")
BIN_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR = Path(r"C:\Users\user\.gemini\antigravity\temp_tools")
TEMP_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {"User-Agent": "Mozilla/5.0"}

def download_and_extract_git():
    git_url = "https://github.com/git-for-windows/git/releases/download/v2.56.0.windows.2/MinGit-2.56.0.2-64-bit.zip"
    zip_path = TEMP_DIR / "mingit.zip"
    print(f"[*] Downloading MinGit from {git_url}...")
    req = urllib.request.Request(git_url, headers=HEADERS)
    with urllib.request.urlopen(req) as resp, open(zip_path, "wb") as out:
        shutil.copyfileobj(resp, out)
    print("[+] Downloaded MinGit. Extracting to C:\\Users\\user\\.gemini\\antigravity\\git...")
    git_install = Path(r"C:\Users\user\.gemini\antigravity\git")
    git_install.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(git_install)
    
    # Symlink or copy git.exe and cmd tools to BIN_DIR
    git_cmd = git_install / "cmd"
    for item in git_cmd.glob("*"):
        dst = BIN_DIR / item.name
        if not dst.exists():
            shutil.copy2(item, dst)
            print(f"  [+] Copied {item.name} to {BIN_DIR}")
    print("[+] Git setup completed successfully!")

def download_and_extract_gh():
    gh_url = "https://github.com/cli/cli/releases/download/v2.102.0/gh_2.102.0_windows_amd64.zip"
    zip_path = TEMP_DIR / "gh.zip"
    print(f"\n[*] Downloading gh CLI from {gh_url}...")
    req = urllib.request.Request(gh_url, headers=HEADERS)
    with urllib.request.urlopen(req) as resp, open(zip_path, "wb") as out:
        shutil.copyfileobj(resp, out)
    print("[+] Downloaded gh CLI. Extracting...")
    gh_extract = TEMP_DIR / "gh_extract"
    gh_extract.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(gh_extract)
    
    # Find gh.exe inside extracted directory
    gh_exe = list(gh_extract.rglob("gh.exe"))
    if gh_exe:
        dst = BIN_DIR / "gh.exe"
        shutil.copy2(gh_exe[0], dst)
        print(f"[+] Placed gh.exe into {BIN_DIR}")
    print("[+] GitHub CLI setup completed successfully!")

if __name__ == "__main__":
    download_and_extract_git()
    download_and_extract_gh()
