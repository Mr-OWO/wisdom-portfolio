import time
import math
import re
import random
import hashlib
from typing import Dict, Any, List
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from app.database import get_db

router = APIRouter(prefix="/api/labs", tags=["Interactive Labs"])

# 1. Vuln Scanner
class VulnScanRequest(BaseModel):
    target: str

@router.post("/vuln-scan")
def vuln_scan(req: VulnScanRequest):
    target = req.target.strip()
    if not target:
        raise HTTPException(status_code=400, detail="Target host or IP is required")
        
    ports = [
        {"port": 22, "service": "OpenSSH 7.4p1", "state": "open", "cve": "CVE-2018-15473", "cvss": 5.3, "severity": "MEDIUM", "fix": "sudo apt-get --only-upgrade install openssh-server"},
        {"port": 80, "service": "Apache httpd 2.4.49", "state": "open", "cve": "CVE-2021-41773", "cvss": 9.8, "severity": "CRITICAL", "fix": "apt-get install --only-upgrade apache2 && a2dismod cgi"},
        {"port": 443, "service": "OpenSSL 1.1.1k", "state": "open", "cve": "CVE-2021-3711", "cvss": 7.5, "severity": "HIGH", "fix": "sudo apt update && sudo apt install --only-upgrade libssl1.1"},
        {"port": 3306, "service": "MySQL 5.7.33", "state": "filtered", "cve": "CVE-2021-2166", "cvss": 6.5, "severity": "MEDIUM", "fix": "iptables -A INPUT -p tcp --dport 3306 -j DROP"}
    ]
    return {
        "target": target,
        "scan_duration_ms": 340,
        "ports_scanned": 1024,
        "open_ports": ports,
        "overall_risk_score": 8.7,
        "recommendation": "CRITICAL: Immediate path-traversal remediation required on HTTP port 80."
    }

# 2. Phishing Detector
class PhishingScanRequest(BaseModel):
    url: str

@router.post("/phishing-scan")
def phishing_scan(req: PhishingScanRequest):
    url = req.url.strip()
    if not url:
        raise HTTPException(status_code=400, detail="URL is required")
        
    threat_score = 0
    flags = []
    
    # Check suspicious TLDs
    suspicious_tlds = [".xyz", ".top", ".buzz", ".work", ".tk", ".cf", ".gq"]
    if any(url.lower().endswith(tld) or (tld + "/") in url.lower() for tld in suspicious_tlds):
        threat_score += 35
        flags.append("High-risk top level domain (.xyz/.top/.tk)")
        
    # Check IP address as hostname
    if re.search(r"https?://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", url):
        threat_score += 40
        flags.append("Raw IPv4 address in place of legitimate domain name")
        
    # Check homoglyph / typosquat patterns
    typos = ["paypa1", "g00gle", "micros0ft", "moniep0int", "app1e", "lendingc1ub", "secure-login", "verify-account"]
    if any(kw in url.lower() for kw in typos):
        threat_score += 45
        flags.append("Homoglyph / Typosquatting token detected mimicking reputable brand")
        
    # Check excessive hyphens / subdomains
    if url.count("-") >= 3:
        threat_score += 20
        flags.append("Multiple hyphen separators typical of phishing proxies")
        
    threat_score = min(threat_score, 100)
    verdict = "SAFE" if threat_score < 30 else ("SUSPICIOUS" if threat_score < 70 else "MALICIOUS")
    
    return {
        "url": url,
        "threat_score": threat_score,
        "verdict": verdict,
        "flags": flags if flags else ["Valid domain syntax", "No known brand spoofing tokens"]
    }

# 3. Traffic Sentinel (Packet Inspector & IP Ban)
class TrafficSimulationRequest(BaseModel):
    traffic_type: str # normal, syn_flood, port_scan

@router.post("/traffic-simulate")
def traffic_simulate(req: TrafficSimulationRequest):
    traffic_type = req.traffic_type.lower()
    if traffic_type == "syn_flood":
        packets = [
            {"src": "194.26.29.11", "dst": "10.0.0.1", "proto": "TCP", "flags": "SYN", "len": 64, "anomaly": True},
            {"src": "194.26.29.11", "dst": "10.0.0.1", "proto": "TCP", "flags": "SYN", "len": 64, "anomaly": True},
            {"src": "194.26.29.11", "dst": "10.0.0.1", "proto": "TCP", "flags": "SYN", "len": 64, "anomaly": True},
            {"src": "194.26.29.11", "dst": "10.0.0.1", "proto": "TCP", "flags": "SYN", "len": 64, "anomaly": True},
        ]
        return {
            "status": "ALERT",
            "threat": "SYN Flood Denial of Service Attack",
            "attacker_ip": "194.26.29.11",
            "action": "AUTO_MITIGATE_TRIGGERED",
            "firewall_rule": "iptables -A INPUT -s 194.26.29.11 -j DROP",
            "packets": packets
        }
    elif traffic_type == "port_scan":
        packets = [
            {"src": "45.154.255.8", "dst": "10.0.0.1", "proto": "TCP", "port": 21, "flags": "SYN", "anomaly": True},
            {"src": "45.154.255.8", "dst": "10.0.0.1", "proto": "TCP", "port": 22, "flags": "SYN", "anomaly": True},
            {"src": "45.154.255.8", "dst": "10.0.0.1", "proto": "TCP", "port": 80, "flags": "SYN", "anomaly": True},
            {"src": "45.154.255.8", "dst": "10.0.0.1", "proto": "TCP", "port": 443, "flags": "SYN", "anomaly": True},
        ]
        return {
            "status": "ALERT",
            "threat": "Rapid Vertical Port Reconnaissance",
            "attacker_ip": "45.154.255.8",
            "action": "AUTO_MITIGATE_TRIGGERED",
            "firewall_rule": "nft add element inet filter blacklist { 45.154.255.8 }",
            "packets": packets
        }
    else:
        packets = [
            {"src": "172.16.0.45", "dst": "10.0.0.1", "proto": "HTTPS", "len": 1420, "anomaly": False},
            {"src": "172.16.0.45", "dst": "10.0.0.1", "proto": "TCP", "flags": "ACK", "len": 54, "anomaly": False},
            {"src": "10.0.0.1", "dst": "172.16.0.45", "proto": "HTTPS", "len": 1280, "anomaly": False},
        ]
        return {
            "status": "NORMAL",
            "threat": "None (Legitimate HTTPS User Session)",
            "attacker_ip": None,
            "action": "ALLOW_TRAFFIC",
            "firewall_rule": None,
            "packets": packets
        }

# 4. RBAC Simulator
class RBACRequest(BaseModel):
    role: str # SuperAdmin, RiskAnalyst, Tier1Support
    endpoint: str # /api/v1/ledger/override, /api/v1/kyc/review, /api/v1/tickets/assign

@router.post("/rbac-test")
def rbac_test(req: RBACRequest):
    permissions = {
        "SuperAdmin": ["/api/v1/ledger/override", "/api/v1/kyc/review", "/api/v1/tickets/assign", "/api/v1/sys/config"],
        "RiskAnalyst": ["/api/v1/kyc/review", "/api/v1/tickets/assign"],
        "Tier1Support": ["/api/v1/tickets/assign"]
    }
    allowed = req.endpoint in permissions.get(req.role, [])
    
    with get_db() as conn:
        conn.execute("""
            INSERT INTO audit_logs (actor, action, resource, status, ip_address)
            VALUES (?, ?, ?, ?, ?)
        """, (req.role, f"ACCESS_{req.endpoint}", req.endpoint, "ALLOWED" if allowed else "DENIED_403", "127.0.0.1"))
        
    return {
        "role": req.role,
        "endpoint": req.endpoint,
        "access_granted": allowed,
        "status_code": 200 if allowed else 403,
        "audit_entry_created": True,
        "policy_rule": f"Role '{req.role}' has scope: {', '.join(permissions.get(req.role, []))}"
    }

# 5. Entropy Guard
class EntropyRequest(BaseModel):
    password: str

@router.post("/entropy-evaluate")
def entropy_evaluate(req: EntropyRequest):
    pwd = req.password
    if not pwd:
        return {"entropy_bits": 0, "crack_time": "Instant", "strength": "Empty"}
        
    charset = 0
    if re.search(r"[a-z]", pwd): charset += 26
    if re.search(r"[A-Z]", pwd): charset += 26
    if re.search(r"[0-9]", pwd): charset += 10
    if re.search(r"[^a-zA-Z0-9]", pwd): charset += 33
    
    entropy = round(len(pwd) * math.log2(max(charset, 1)), 2)
    
    # Brute force at 10^10 hashes/sec
    combos = math.pow(charset, len(pwd)) if charset > 0 else 1
    seconds = combos / (10 ** 10)
    
    if seconds < 1:
        crack_time = "Less than 1 second"
    elif seconds < 60:
        crack_time = f"{round(seconds, 1)} seconds"
    elif seconds < 3600:
        crack_time = f"{round(seconds / 60, 1)} minutes"
    elif seconds < 86400 * 365:
        crack_time = f"{round(seconds / 86400, 1)} days"
    elif seconds < 86400 * 365 * 1000:
        crack_time = f"{round(seconds / (86400 * 365), 1)} years"
    else:
        crack_time = "Centuries+"
        
    strength = "Very Weak" if entropy < 28 else ("Weak" if entropy < 45 else ("Medium" if entropy < 60 else ("Strong" if entropy < 80 else "Military Grade")))
    
    return {
        "entropy_bits": entropy,
        "charset_pool": charset,
        "crack_time": crack_time,
        "strength": strength,
        "hash_sha256": hashlib.sha256(pwd.encode()).hexdigest()[:16] + "..."
    }

# 6. Ticket Routing (NLP Intent & Severity Triage)
class TicketTriageRequest(BaseModel):
    complaint_text: str

@router.post("/ticket-triage")
def ticket_triage(req: TicketTriageRequest):
    text = req.complaint_text.lower()
    
    severity = "P3 - Moderate"
    tier = "Tier 1 - Customer Support"
    intent = "General Inquiry"
    sentiment = "Neutral"
    
    if any(w in text for w in ["fraud", "unauthorized", "hacked", "stolen", "breach", "zero balance", "missing funds"]):
        severity = "P1 - Critical Severity"
        tier = "Tier 3 - Security Operations & Risk Lead"
        intent = "Dispute / Security Incident"
        sentiment = "High Distress / Urgent"
    elif any(w in text for w in ["pos declined", "settlement", "timeout", "double debit", "reversal", "chargeback"]):
        severity = "P2 - High Priority"
        tier = "Tier 2 - Fintech Settlement & Operations"
        intent = "Transaction Settlement Failure"
        sentiment = "Frustrated"
    elif any(w in text for w in ["password reset", "login issue", "mfa", "locked out"]):
        severity = "P3 - Moderate"
        tier = "Tier 1 - Technical Support"
        intent = "Authentication & Access Recovery"
        sentiment = "Mildly Annoyed"
        
    return {
        "severity": severity,
        "routing_tier": tier,
        "intent_category": intent,
        "sentiment_detected": sentiment,
        "sla_target": "15 minutes" if "P1" in severity else ("1 hour" if "P2" in severity else "4 hours"),
        "confidence_score": 0.94
    }

# 7. Settlement Debugger
class SettlementDebugRequest(BaseModel):
    transaction_id: str

@router.post("/settlement-debug")
def settlement_debug(req: SettlementDebugRequest):
    tx_id = req.transaction_id.strip()
    return {
        "transaction_id": tx_id,
        "pos_terminal_id": "POS-LAG-98231",
        "processor_code": "NIBSS_SWITCH_TIMEOUT",
        "iso8583_response": "91 - System Error / Issuer Inoperative",
        "ledger_debit_status": "COMMITTED_ON_HOST",
        "merchant_credit_status": "PENDING_REVERSAL",
        "discrepancy_amount": "NGN 45,000.00",
        "root_cause": "Packet loss on cellular gateway during stage 2 ACK commit.",
        "auto_resolution": "Automated Reversal Triggered (TXN-REV-7721); Ledger reconciles in zero balance."
    }

# 8. Market Predictor & Backtester
class BacktestRequest(BaseModel):
    strategy: str # rsi_divergence, ema_cross, bollinger_bounce
    period_days: int = 30

@router.post("/market-backtest")
def market_backtest(req: BacktestRequest):
    strat = req.strategy.lower()
    if "ema" in strat:
        win_rate = 68.4
        profit_factor = 2.15
        max_drawdown = 6.2
        trades = 84
    elif "bollinger" in strat:
        win_rate = 62.1
        profit_factor = 1.82
        max_drawdown = 8.5
        trades = 112
    else:
        win_rate = 74.2
        profit_factor = 2.48
        max_drawdown = 4.8
        trades = 96
        
    return {
        "strategy": req.strategy,
        "period_days": req.period_days,
        "total_trades": trades,
        "win_rate_percent": win_rate,
        "profit_factor": profit_factor,
        "max_drawdown_percent": max_drawdown,
        "sharpe_ratio": 2.18,
        "net_pnl_percent": round(win_rate * profit_factor * 0.45, 2),
        "status": "BACKTEST_VALIDATED"
    }
