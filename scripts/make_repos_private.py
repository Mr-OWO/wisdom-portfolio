import json
import subprocess
import os

GH_BIN = r"C:\Users\user\.gemini\antigravity\bin\gh.exe"
ENV = os.environ.copy()
ENV["GH_TOKEN"] = os.environ.get("GH_TOKEN", "")

KEEP_PUBLIC = {
    "llm-eval-bench",
    "rl-arena-platform",
    "agentic-code-eval-sandbox",
    "alignment-data-factory",
    "wisdom-portfolio",
    "Mr-OWO"  # GitHub special profile README repo
}

def main():
    print("[*] Fetching all repositories for Mr-OWO...")
    cmd = [GH_BIN, "repo", "list", "Mr-OWO", "--limit", "100", "--json", "name,visibility"]
    res = subprocess.run(cmd, env=ENV, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error fetching repos: {res.stderr}")
        return

    repos = json.loads(res.stdout)
    print(f"Found {len(repos)} repositories total.\n")

    for repo in repos:
        name = repo["name"]
        vis = repo["visibility"]
        if name in KEEP_PUBLIC:
            print(f"[KEEP PUBLIC] {name} (Current: {vis})")
        else:
            if vis == "PRIVATE":
                print(f"[ALREADY PRIVATE] {name}")
                continue
            print(f"[-] Converting {name} to PRIVATE...")
            edit_cmd = [
                GH_BIN, "repo", "edit", f"Mr-OWO/{name}",
                "--visibility", "private",
                "--accept-visibility-change-consequences"
            ]
            edit_res = subprocess.run(edit_cmd, env=ENV, capture_output=True, text=True)
            if edit_res.returncode == 0:
                print(f"  [+] Successfully converted {name} to private.")
            else:
                print(f"  [!] Failed to convert {name}: {edit_res.stderr.strip()}")

    print("\n[*] Audit complete. Listing remaining public repositories:")
    check_cmd = [GH_BIN, "repo", "list", "Mr-OWO", "--visibility", "public", "--json", "name,visibility"]
    check_res = subprocess.run(check_cmd, env=ENV, capture_output=True, text=True)
    print(check_res.stdout)

if __name__ == "__main__":
    main()
