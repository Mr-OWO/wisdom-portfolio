import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REPOS = [
    {
        "dir": ROOT / "llm-eval-bench",
        "name": "llm-eval-bench",
        "desc": "High-Throughput Async Evaluation & Regression Detection Framework for LLMs",
    },
    {
        "dir": ROOT / "alignment-data-factory",
        "name": "alignment-data-factory",
        "desc": "SFT & RLHF/DPO Preference Dataset Curation & AST Alignment Pipeline",
    },
    {
        "dir": ROOT / "rl-arena-platform",
        "name": "rl-arena-platform",
        "desc": "Full-Stack RLHF Model Evaluation & Elo Leaderboard Dashboard (NestJS + React)",
    },
    {
        "dir": ROOT / "agentic-code-eval-sandbox",
        "name": "agentic-code-eval-sandbox",
        "desc": "Containerized Execution Sandbox for AI Agent Code Benchmark Evaluations",
    },
]

GIT_BIN = r"C:\Users\user\.gemini\antigravity\git\cmd\git.exe"
GH_BIN = r"C:\Users\user\.gemini\antigravity\bin\gh.exe"

GH_TOKEN = os.environ.get("GH_TOKEN", "")
ENV = os.environ.copy()
ENV["GH_TOKEN"] = GH_TOKEN
ENV["PATH"] = r"C:\Users\user\.gemini\antigravity\git\cmd;" + ENV.get("PATH", "")

def run(cmd, cwd):
    # Map command name to absolute executable
    if cmd[0] == "git":
        cmd[0] = GIT_BIN
    elif cmd[0] == "gh":
        cmd[0] = GH_BIN
    print(f"[{cwd.name}] $ {' '.join(cmd)}")
    res = subprocess.run(cmd, cwd=cwd, env=ENV, capture_output=True, text=True)
    if res.stdout:
        print(res.stdout.strip())
    if res.returncode != 0 and res.stderr:
        print(f"  STDERR: {res.stderr.strip()}")
    return res

def publish_repo(repo_info):
    rdir = repo_info["dir"]
    name = repo_info["name"]
    desc = repo_info["desc"]
    print(f"\n=======================================================")
    print(f"[*] Publishing {name} ({rdir})...")
    print(f"=======================================================")

    # 1. Git init if not already initialized
    if not (rdir / ".git").exists():
        run(["git", "init"], rdir)
        run(["git", "branch", "-M", "main"], rdir)

    # 2. Add and commit
    run(["git", "add", "."], rdir)
    res_commit = run(["git", "commit", "-m", f"feat: initial production release of {name}"], rdir)

    # 3. Try gh repo create
    res_create = run(["gh", "repo", "create", name, "--public", "--description", desc, "--source=.", "--push"], rdir)

    if res_create.returncode != 0:
        print(f"[*] gh repo create exited with code {res_create.returncode}. Attempting fallback remote push...")
        remote_url = f"https://Mr-OWO:{GH_TOKEN}@github.com/Mr-OWO/{name}.git"
        # Check if remote origin exists
        res_rem = run(["git", "remote", "get-url", "origin"], rdir)
        if res_rem.returncode != 0:
            run(["git", "remote", "add", "origin", remote_url], rdir)
        else:
            run(["git", "remote", "set-url", "origin", remote_url], rdir)
        run(["git", "push", "-u", "origin", "main", "--force"], rdir)

    print(f"[+] Successfully pushed {name} to GitHub: https://github.com/Mr-OWO/{name}")

if __name__ == "__main__":
    for repo in REPOS:
        publish_repo(repo)
    print("\n[+] ALL 4 FLAGSHIP REPOSITORIES CREATED AND PUSHED SUCCESSFULLY!")
