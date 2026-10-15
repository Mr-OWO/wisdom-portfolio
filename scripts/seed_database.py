import json
import sqlite3
import sys
from pathlib import Path

# Add project root to path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from app.database import get_db, init_db
from app.auth import hash_password
from app.config import GITHUB_USERNAME

def seed():
    print("Initializing database schema...")
    init_db()

    with get_db() as conn:
        cursor = conn.cursor()

        # 1. Admin Users
        cursor.execute("SELECT COUNT(*) FROM admin_users")
        if cursor.fetchone()[0] == 0:
            print("Seeding admin user...")
            pwd_hash = hash_password("SecOps!Admin2026#")
            cursor.execute("""
                INSERT INTO admin_users (username, password_hash, role)
                VALUES (?, ?, ?)
            """, ("wisdom_admin", pwd_hash, "SuperAdmin"))

        # 2. Site Metadata
        cursor.execute("DELETE FROM site_metadata")
        metrics = {
            "uptime_pct": "99.9%",
            "production_labs": "24+",
            "polyglot_stack": "Python 3.12, TypeScript, NestJS, React, PHP",
            "quality_gates": "Pytest, Jest, Docker, CI/CD"
        }
        cursor.execute("""
            INSERT INTO site_metadata (id, full_name, professional_headline, bio, contact_email, phone, location, metrics_json)
            VALUES (1, ?, ?, ?, ?, ?, ?, ?)
        """, (
            "Wisdom Ogechi Owabor",
            "Full-Stack Software Engineer & Python AI Systems Specialist",
            "Architecting resilient full-stack systems with TypeScript, Node.js, NestJS, and React | Building high-throughput Python harnesses for model evaluations (Evals), SFT pipelines, and containerized execution sandboxes.",
            "contact@wisdomowabor.online, wisdomowabor1@gmail.com",
            "+234-800-AI-SYS",
            "Lagos, Nigeria (Hybrid / Global)",
            json.dumps(metrics)
        ))

        # 3. Work History
        cursor.execute("DELETE FROM work_history")
        work_entries = [
            (
                "Winseltech",
                "Lead Systems Architect & Full-Stack Engineer",
                "2023 - Present",
                "Lagos, Nigeria",
                json.dumps([
                    "Architected high-availability cloud infrastructure and zero-trust defensive perimeters maintaining 99.9% operational uptime across enterprise systems.",
                    "Engineered asynchronous high-throughput evaluation harnesses and automated CI/CD pipelines with test-driven quality gates (Pytest, Jest, Docker).",
                    "Directed polyglot engineering squads building responsive React/NestJS workspaces and containerized Python microservices.",
                    "Formulated and implemented automated disaster recovery and backup integrity validation protocols with near-zero RPO."
                ]),
                1
            ),
            (
                "LendingClub",
                "Senior Technical Systems Specialist & Engineer",
                "2021 - 2023",
                "San Francisco, CA / Remote",
                json.dumps([
                    "Engineered resilient API integrations and real-time transaction reconciliation workflows under high-concurrency fintech volumes.",
                    "Investigated systemic performance bottlenecks and automated support diagnostics, decreasing mean time to resolution (MTTR) by 42%.",
                    "Interfaced directly with core engineering squads to isolate microservice latency bottlenecks and database lock contentions."
                ]),
                2
            ),
            (
                "Moniepoint Group",
                "Technical Operations & Escalations Lead",
                "2020 - 2021",
                "Lagos, Nigeria",
                json.dumps([
                    "Built automated dispute reconciliation tooling parsing POS switch payloads and dual-entry ledger balances.",
                    "Trained and led cross-functional technical support teams sustaining a 96.4% customer satisfaction benchmark."
                ]),
                3
            )
        ]
        cursor.executemany("""
            INSERT INTO work_history (company, role_title, period, location, summary_bullets, sort_order)
            VALUES (?, ?, ?, ?, ?, ?)
        """, work_entries)

        # 4. The 24 Projects (Categorized into 4 Disciplines)
        cursor.execute("DELETE FROM projects")
        projects_data = [
            # =========================================================================
            # Category 1: AI Systems & Alignment (4 Flagship Projects)
            # =========================================================================
            (
                "llm-eval-bench",
                "High-Throughput Async Evaluation & Regression Detection Framework",
                "AI Systems & Alignment",
                "Asynchronous model evaluation harness combining deterministic metrics (BLEU, ROUGE-L, JSON Schema) with LLM-as-a-Judge scorecards, governed by Semaphore(10) concurrency and token-bucket rate limiting.",
                "asyncio worker pool + TokenBucketRateLimiter + Pydantic v2 Scorecards + Hypothesis property fuzzing.",
                json.dumps(["Python 3.12", "asyncio", "httpx", "Pydantic v2", "Pytest", "Hypothesis"]),
                f"https://github.com/{GITHUB_USERNAME}/llm-eval-bench",
                1,
                "/projects/llm-eval-bench"
            ),
            (
                "rl-arena-platform",
                "Full-Stack RLHF Model Evaluation & Elo Leaderboard Dashboard",
                "AI Systems & Alignment",
                "Enterprise preference collection platform featuring split-pane model comparisons, live code diffing, 1-5 rubric sliders, dynamic Elo calculations, and Cohen's/Fleiss' Kappa agreement metrics.",
                "Modular NestJS API + React 18 Tailwind workspace + Bradley-Terry Elo rating engine + PostgreSQL Docker.",
                json.dumps(["NestJS", "TypeScript", "React 18", "Tailwind CSS", "Docker", "Jest"]),
                f"https://github.com/{GITHUB_USERNAME}/rl-arena-platform",
                1,
                "/projects/rl-arena-platform"
            ),
            (
                "alignment-data-factory",
                "SFT & RLHF/DPO Preference Dataset Curation Pipeline",
                "AI Systems & Alignment",
                "Streaming data curation pipeline featuring AST code compilation checks (Python/TypeScript), sycophancy detection, verbosity-bias normalization, and sub-200MB memory footprint.",
                "Python ast.parse + JS delimiter parser + Polars Parquet streaming engine + lazy generator pipeline.",
                json.dumps(["Python 3.12", "Polars", "AST Parsing", "Pydantic v2", "Pytest", "Ruff"]),
                f"https://github.com/{GITHUB_USERNAME}/alignment-data-factory",
                1,
                "/projects/alignment-data-factory"
            ),
            (
                "agentic-code-eval-sandbox",
                "Containerized Execution Sandbox for Code Benchmark Evals",
                "AI Systems & Alignment",
                "Isolated code runner evaluating autonomous AI agent completions (Python & Node.js) with 0.5 CPU, 256MB RAM ceilings, ephemeral directories, and 5-second hard timeout watchdogs.",
                "FastAPI execution gateway + Ephemeral isolated subprocess runner + Test assertion harness + Docker.",
                json.dumps(["Docker", "FastAPI", "Python 3.12", "Node.js", "Linux cgroups", "Uvicorn"]),
                f"https://github.com/{GITHUB_USERNAME}/agentic-code-eval-sandbox",
                1,
                "/projects/agentic-code-eval-sandbox"
            ),

            # =========================================================================
            # Category 2: Full-Stack & Web Apps (4 Projects)
            # =========================================================================
            (
                "market-scraper",
                "Real-Time Market Data Scraper & Indicator Alert",
                "Full-Stack & Web Apps",
                "Streaming market data engine monitoring price changes, calculating dynamic technical indicators (RSI, 50-EMA, MACD), and emitting breakout trigger alerts.",
                "Asynchronous price tick generator + real-time technical indicator mathematical pipelines + threshold alert dispatcher.",
                json.dumps(["Python", "WebSockets", "Technical Analysis (RSI/MACD)", "Asynchronous Tasks"]),
                f"https://github.com/{GITHUB_USERNAME}/secops-market-scraper",
                1,
                "/projects/market-scraper"
            ),
            (
                "market-predictor",
                "Binary Market Predictive Analytics & Backtester",
                "Full-Stack & Web Apps",
                "Historical backtesting engine testing algorithmic trading strategies across candlestick historical datasets with win-rate, profit factor, and maximum drawdown metrics.",
                "Candlestick simulation loop + strategy execution model + performance metric calculator (Sharpe/Drawdown).",
                json.dumps(["Quantitative Finance", "Backtesting", "Python", "Data Modeling", "HTML5 Canvas"]),
                f"https://github.com/{GITHUB_USERNAME}/secops-market-predictor",
                1,
                "/projects/market-predictor"
            ),
            (
                "social-trend-bot",
                "Automated Viral Trend Scout & Content Synthesizer",
                "Full-Stack & Web Apps",
                "Trend velocity scout that tracks spikes across developer ecosystems, isolates high-engagement discussion hooks, and synthesizes structured cross-platform promotional updates.",
                "Trend velocity scorer + NLP keyword clusterer + multi-format markdown copy synthesizer.",
                json.dumps(["Python", "NLP Summarization", "Trend Analysis", "Content Syndication", "FastAPI"]),
                f"https://github.com/{GITHUB_USERNAME}/secops-social-trend-bot",
                1,
                "/projects/social-trend-bot"
            ),
            (
                "settlement-debugger",
                "Fintech Transaction Reconciliation Engine",
                "Full-Stack & Web Apps",
                "Automated dispute and settlement debugger analyzing POS connection drops, switch gateway timeouts, and ledger balance discrepancies with auto-remediation.",
                "ISO 8583 message parser + dual-entry ledger discrepancy detector + automated chargeback/reversal trigger.",
                json.dumps(["Fintech Protocols", "ISO 8583", "Double-Entry Ledger", "FastAPI", "Python"]),
                f"https://github.com/{GITHUB_USERNAME}/secops-settlement-debugger",
                1,
                "/projects/settlement-debugger"
            ),

            # =========================================================================
            # Category 3: Backend, Cloud & SecOps (11 Projects)
            # =========================================================================
            (
                "vuln-scanner",
                "Automated Vulnerability Scanner & Patch Advisor",
                "Backend, Cloud & SecOps",
                "Comprehensive network perimeter scanner that executes banner grabs, evaluates CVSS v3.1 scores, and generates copy-paste remediation CLI patches.",
                "FastAPI asynchronous socket prober + CVE database correlation engine + automated shell remediation generator.",
                json.dumps(["Python", "FastAPI", "Nmap Engine", "CVSS v3.1", "SQLite", "Bash Scripting"]),
                f"https://github.com/{GITHUB_USERNAME}/secops-vuln-scanner",
                1,
                "/projects/vuln-scanner"
            ),
            (
                "phishing-detector",
                "Phishing & Domain Threat Heuristic Engine",
                "Backend, Cloud & SecOps",
                "High-throughput URL analyzer checking homoglyph attacks, Shannon entropy, brand typosquatting, and suspicious TLD patterns with 0-100 threat scoring.",
                "Unicode homoglyph canonicalizer + entropy calculator + brand token vector distance matching.",
                json.dumps(["Python", "Regex", "Information Theory", "Security Heuristics", "REST API"]),
                f"https://github.com/{GITHUB_USERNAME}/secops-phishing-detector",
                1,
                "/projects/phishing-detector"
            ),
            (
                "traffic-sentinel",
                "Network Packet Inspector & Anomaly Detector",
                "Backend, Cloud & SecOps",
                "Real-time packet telemetry visualizer with interactive traffic injection (SYN Flood, Port Scan, Normal) and automated firewall IP ban orchestration.",
                "Simulated raw socket streaming engine + sliding-window rate anomaly detector + dynamic iptables/nftables ban generator.",
                json.dumps(["JavaScript", "WebSockets", "FastAPI", "iptables/nftables", "Packet Dissection"]),
                f"https://github.com/{GITHUB_USERNAME}/secops-traffic-sentinel",
                1,
                "/projects/traffic-sentinel"
            ),
            (
                "rbac-simulator",
                "Enterprise IAM & Access Control Sandbox",
                "Backend, Cloud & SecOps",
                "Multi-tenant zero-trust role-based access control tester with live privilege evaluation against sensitive endpoints and immutable audit logs.",
                "Hierarchical role evaluator + cryptographically chained audit logging + real-time 403 Forbidden enforcement.",
                json.dumps(["Python", "FastAPI", "OAuth2 / RBAC", "SQLite Audit Chain", "JSON Web Tokens"]),
                f"https://github.com/{GITHUB_USERNAME}/secops-rbac-simulator",
                1,
                "/projects/rbac-simulator"
            ),
            (
                "entropy-guard",
                "Password Entropy & Credential Risk Analyzer",
                "Backend, Cloud & SecOps",
                "In-browser zero-knowledge password strength engine computing Shannon entropy, character set permutation spaces, and brute-force cracking estimates.",
                "Zero-knowledge client evaluator + SHA-256 fingerprinting + exponential permutation compute model.",
                json.dumps(["Web Crypto API", "Shannon Entropy", "zxcvbn Heuristics", "JavaScript"]),
                f"https://github.com/{GITHUB_USERNAME}/secops-entropy-guard",
                1,
                "/projects/entropy-guard"
            ),
            (
                "honeypot-telemetry",
                "Low-Interaction Honeypot & Telemetry Monitor",
                "Backend, Cloud & SecOps",
                "Synthetic trap emulating exposed SSH and HTTP admin services, capturing attacker credentials, geolocation coordinates, and automated one-click ban rules.",
                "Low-interaction daemon listener + GeoIP metadata lookup + attacker payload sandbox.",
                json.dumps(["Python", "SSH Emulation", "GeoIP", "Syslog", "TailwindCSS"]),
                f"https://github.com/{GITHUB_USERNAME}/secops-honeypot-telemetry",
                1,
                "/projects/honeypot-telemetry"
            ),
            (
                "secure-vault",
                "End-to-End Encrypted File Transfer & Checksum Verifier",
                "Backend, Cloud & SecOps",
                "Client-side zero-knowledge AES-GCM-256 encryption workbench with initialization vector handling, SHA-256 integrity hashing, and tamper detection.",
                "W3C Web Cryptography API + authenticated AES-GCM 256-bit Galois/Counter mode + byte array stream pipeline.",
                json.dumps(["WebCrypto API", "AES-GCM-256", "SHA-256", "Zero-Knowledge", "Vanilla JS"]),
                f"https://github.com/{GITHUB_USERNAME}/secops-secure-vault",
                1,
                "/projects/secure-vault"
            ),
            (
                "ransomware-guard",
                "Ransomware Behavioral Heuristic Detector",
                "Backend, Cloud & SecOps",
                "Simulated file system watchdog detecting rapid encryption frequency, known ransomware extensions (.locked, .crypto), process termination, and shadow copy restoration.",
                "Filesystem watch simulator + Shannon file entropy trigger + automated process SIGKILL + snapshot restore.",
                json.dumps(["Python", "Heuristic Behavioral Engine", "VSS Shadow Mimic", "Process Monitor"]),
                f"https://github.com/{GITHUB_USERNAME}/secops-ransomware-guard",
                1,
                "/projects/ransomware-guard"
            ),
            (
                "asset-tracker",
                "Enterprise IT Asset & Endpoint Manager",
                "Backend, Cloud & SecOps",
                "Comprehensive enterprise hardware and software registry with multi-criteria filtering by operating system, department, warranty expiration, and patch status.",
                "Relational endpoint catalog + dynamic warranty countdown + compliance status dashboard.",
                json.dumps(["FastAPI", "SQLite", "Asset Management", "CIS Benchmarks", "Bootstrap/CSS"]),
                f"https://github.com/{GITHUB_USERNAME}/itsupport-asset-tracker",
                1,
                "/projects/asset-tracker"
            ),
            (
                "config-auditor",
                "Endpoint Security & CIS Benchmark Auditor",
                "Backend, Cloud & SecOps",
                "Automated configuration inspector evaluating endpoint compliance against Center for Internet Security (CIS) Level 1/2 benchmarks with automated shell fix scripts.",
                "Policy compliance rule engine + automated PowerShell/Bash remediation generation + pass/fail scoring.",
                json.dumps(["Python", "CIS Benchmarks", "PowerShell", "Security Compliance", "JSON Schema"]),
                f"https://github.com/{GITHUB_USERNAME}/itsupport-config-auditor",
                1,
                "/projects/config-auditor"
            ),
            (
                "patch-manager",
                "Automated Patch Deployment & Rollback Engine",
                "Backend, Cloud & SecOps",
                "Multi-tier deployment pipeline (Dev -> Staging -> Production) featuring synthetic failure injection and zero-downtime automated rollback validation.",
                "Staged canary deployment pipeline + health check monitor + automated rollback circuit breaker.",
                json.dumps(["FastAPI", "CI/CD Staging", "Rollback Controller", "System Resilience"]),
                f"https://github.com/{GITHUB_USERNAME}/itsupport-patch-manager",
                1,
                "/projects/patch-manager"
            ),

            # =========================================================================
            # Category 4: Customer Ops & Tooling (5 Projects)
            # =========================================================================
            (
                "keylogger-detector",
                "Keylogger Behavioral & Hook Detector",
                "Customer Ops & Tooling",
                "Educational kernel and user-mode simulation tracking Windows API keyboard hook registrations (SetWindowsHookEx) and unmapped background memory anomalies.",
                "Synthetic Win32 hook event bus + hook DLL signature inspection + suspicious process isolation.",
                json.dumps(["C / Win32 Emulation", "Python", "Process Memory Inspector", "Security Forensics"]),
                f"https://github.com/{GITHUB_USERNAME}/itsupport-keylogger-detector",
                1,
                "/projects/keylogger-detector"
            ),
            (
                "backup-validator",
                "Disaster Recovery & Backup Integrity Drill",
                "Customer Ops & Tooling",
                "Automated database snapshot simulator executing cryptographic SHA-256 archive checksum verifications and timed visual recovery drills tracking RTO and RPO metrics.",
                "Automated backup archiver + cryptographic verification pipeline + RTO/RPO stopclock telemetry.",
                json.dumps(["Python", "SQLite Backup API", "SHA-256 Verification", "Disaster Recovery"]),
                f"https://github.com/{GITHUB_USERNAME}/itsupport-backup-validator",
                1,
                "/projects/backup-validator"
            ),
            (
                "ticket-routing",
                "AI-Powered Support Triage & Ticket Categorization",
                "Customer Ops & Tooling",
                "NLP customer text classification engine analyzing intent, sentiment distress, and SLA priority tiers (P1-P4) for zero-delay escalation routing.",
                "Text keyword & sentiment vector matcher + severity ranking matrix + SLA countdown assignment.",
                json.dumps(["Python", "NLP Intent Analysis", "FastAPI", "SLA Engine", "Customer Operations"]),
                f"https://github.com/{GITHUB_USERNAME}/itsupport-ticket-routing",
                1,
                "/projects/ticket-routing"
            ),
            (
                "csat-analytics",
                "Customer Satisfaction & Retention Analytics Radar",
                "Customer Ops & Tooling",
                "Interactive CSAT, NPS, and First Contact Resolution (FCR) analytics radar tracking agent satisfaction metrics, churn alerts, and SLA breach monitors.",
                "Real-time CSAT aggregation engine + sentiment radar visualization + proactive churn risk flagger.",
                json.dumps(["Data Analytics", "CSAT/NPS", "Chart.js / Canvas", "FastAPI", "JSON Store"]),
                f"https://github.com/{GITHUB_USERNAME}/itsupport-csat-analytics",
                1,
                "/projects/csat-analytics"
            ),
            (
                "kb-assistant",
                "Smart Knowledge-Base & Technical SOP Engine",
                "Customer Ops & Tooling",
                "Semantic search and retrieval system over IT troubleshooting runbooks, fintech de-escalation scripts, and enterprise standard operating procedures (SOPs).",
                "Keyword & inverted index search + categorized runbook snippets + copyable resolution templates.",
                json.dumps(["Search Indexing", "Technical Writing", "SOP Documentation", "FastAPI", "UI"]),
                f"https://github.com/{GITHUB_USERNAME}/itsupport-kb-assistant",
                1,
                "/projects/kb-assistant"
            )
        ]

        cursor.executemany("""
            INSERT INTO projects (slug, title, category, summary, architecture_breakdown, tech_stack, github_url, live_status, sandbox_route)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, projects_data)

        # 5. Sample Contact Inquiries
        cursor.execute("DELETE FROM contact_inquiries")
        sample_inquiries = [
            (
                "David Sterling",
                "david.sterling@fintechapex.com",
                "Partnership Inquiry: AI Model Evaluation & Infrastructure",
                "Hi Wisdom, we came across your work on high-throughput LLM evaluation harnesses and containerized code execution sandboxes. Let's schedule a call.",
                "new"
            ),
            (
                "Sarah Al-Mansoor",
                "sarah.m@cloudscale.io",
                "Full-Stack & Systems Engineering Role",
                "Wisdom, thoroughly impressed by your NestJS, React, and Python AI pipeline repositories. Would love to discuss an engineering lead position.",
                "read"
            )
        ]
        cursor.executemany("""
            INSERT INTO contact_inquiries (sender_name, sender_email, subject, message, status)
            VALUES (?, ?, ?, ?, ?)
        """, sample_inquiries)

        print(f"Successfully seeded database with {len(projects_data)} projects, {len(work_entries)} career history entries, and default admin credentials!")

if __name__ == "__main__":
    seed()
