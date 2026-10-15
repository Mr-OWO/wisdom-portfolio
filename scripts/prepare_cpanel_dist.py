import os
import shutil
import ftplib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "cpanel_dist"

def prepare_dist():
    print("[*] Preparing cpanel_dist package...")
    DIST.mkdir(exist_ok=True)
    
    # 1. Copy HTML pages
    templates = ROOT / "app" / "templates"
    for page in ["index.html", "about.html", "projects.html", "contact.html", "admin.html"]:
        shutil.copy2(templates / page, DIST / page)
        print(f"  [+] Copied {page}")
        
    # 2. Copy static files
    static_src = ROOT / "app" / "static"
    static_dst = DIST / "static"
    if static_dst.exists():
        shutil.rmtree(static_dst)
    shutil.copytree(static_src, static_dst)
    print("  [+] Copied static/ directory")
    
    # 3. Copy database
    data_dst = DIST / "data"
    data_dst.mkdir(exist_ok=True)
    shutil.copy2(ROOT / "data" / "portfolio.db", data_dst / "portfolio.db")
    print("  [+] Copied data/portfolio.db")
    
    print("[+] cpanel_dist is fully assembled!")

def upload_ftp():
    host = os.environ.get("CPANEL_FTP_HOST", "131.153.147.162")
    user = os.environ.get("CPANEL_FTP_USER", "winselte")
    password = os.environ.get("CPANEL_FTP_PASS", "8EK*t0#8v8GkiB")
    remote_base = os.environ.get("CPANEL_FTP_PATH", "/public_html/wisdomowabor.online")
    
    print(f"\n[*] Connecting to FTP at {host}...")
    ftp = ftplib.FTP(host, timeout=20)
    ftp.login(user, password)
    print(f"[+] Authenticated as {user}")
    
    # Ensure remote base
    ftp.cwd(remote_base)
    print(f"[+] Changed directory to {remote_base}")
    
    def upload_dir(local_path, remote_path):
        for item in os.listdir(local_path):
            local_item = os.path.join(local_path, item)
            if os.path.isfile(local_item):
                filename = os.path.basename(local_item)
                print(f"  --> Uploading {filename} to {remote_path} ...")
                with open(local_item, "rb") as f:
                    ftp.storbinary(f"STOR {filename}", f)
            elif os.path.isdir(local_item):
                sub_name = os.path.basename(local_item)
                try:
                    ftp.mkd(sub_name)
                except Exception:
                    pass # directory already exists
                ftp.cwd(sub_name)
                upload_dir(local_item, remote_path + "/" + sub_name)
                ftp.cwd("..")
                
    upload_dir(str(DIST), remote_base)
    ftp.quit()
    print("\n[+] FTP Deployment to wisdomowabor.online COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    prepare_dist()
    upload_ftp()
