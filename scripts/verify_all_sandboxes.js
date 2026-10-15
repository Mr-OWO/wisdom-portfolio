const fs = require('fs');

class MockElement {
  constructor(id) {
    this.id = id;
    this.innerHTML = '';
    this.innerText = '';
    this.textContent = '';
    this.value = 'test_val';
    this.style = {};
    this.classList = {
      add: () => {},
      remove: () => {},
      contains: () => false
    };
    this.listeners = {};
    this.options = [{ text: 'Sample Topic Option' }];
    this.selectedIndex = 0;
  }
  addEventListener(event, fn) {
    this.listeners[event] = fn;
  }
  click() {
    if (this.listeners['click']) {
      this.listeners['click']({ preventDefault: () => {}, target: this });
    }
  }
  change(val) {
    this.value = val;
    if (this.listeners['change']) {
      this.listeners['change']({ preventDefault: () => {}, target: this });
    }
  }
  input(val) {
    this.value = val;
    if (this.listeners['input']) {
      this.listeners['input']({ preventDefault: () => {}, target: this });
    }
  }
}

const elements = {};
global.document = {
  getElementById: (id) => {
    if (!elements[id]) {
      elements[id] = new MockElement(id);
    }
    return elements[id];
  },
  querySelectorAll: () => [],
  createElement: (tag) => new MockElement(tag)
};
global.window = {
  crypto: {
    subtle: {
      digest: async () => new Uint8Array(32),
      importKey: async () => ({}),
      encrypt: async () => new Uint8Array(32),
      decrypt: async () => new Uint8Array(32)
    },
    getRandomValues: (arr) => arr
  },
  alert: (msg) => {},
  navigator: { clipboard: { writeText: async () => {} } }
};
global.crypto = global.window.crypto;
global.fetch = async (url, opts) => {
  return {
    ok: true,
    status: 200,
    json: async () => ({
      status: 'success',
      entropy_bits: 65,
      strength: 'Strong',
      crack_time: 'Centuries',
      hash_sha256: 'abc...',
      verdict: 'Benign',
      remediation: 'No action needed',
      p1_events: []
    })
  };
};

const code = fs.readFileSync('app/static/js/labs.js', 'utf8');
eval(code);

const slugs = [
  "llm-eval-bench", "rl-arena-platform", "alignment-data-factory", "agentic-code-eval-sandbox",
  "vuln-scanner", "phishing-detector", "traffic-sentinel", "rbac-simulator",
  "entropy-guard", "honeypot-telemetry", "secure-vault", "ransomware-guard",
  "asset-tracker", "config-auditor", "patch-manager", "keylogger-detector",
  "backup-validator", "ticket-routing", "settlement-debugger", "csat-analytics",
  "kb-assistant", "market-scraper", "market-predictor", "social-trend-bot"
];

console.log("=== COMPREHENSIVE 24 LABS VERIFICATION ===");
let passed = 0;

for (const s of slugs) {
  try {
    elements["lab-sandbox-container"] = new MockElement("lab-sandbox-container");
    const html = window.LabsEngine.renderSandbox(s);
    if (!html || html.length < 50) {
      throw new Error(`Rendered HTML too short or empty (${html ? html.length : 0} bytes)`);
    }

    // Populate all element IDs
    const idMatches = html.match(/id="([^"]+)"/g) || [];
    for (const m of idMatches) {
      const id = m.replace('id="', '').replace('"', '');
      elements[id] = new MockElement(id);
    }

    // Bind events
    window.LabsEngine.bindEvents(s);

    // Simulate clicking any primary buttons in this lab
    for (const m of idMatches) {
      const id = m.replace('id="', '').replace('"', '');
      if (id.includes('btn') || id.includes('scan') || id.includes('run') || id.includes('check')) {
        elements[id].click();
      }
    }

    console.log(`[PASS] ${s} -> Rendered ${html.length} chars | Interactive events tested`);
    passed++;
  } catch (err) {
    console.error(`[FAIL] ${s}:`, err.message);
  }
}

console.log(`\nFinal Score: ${passed}/${slugs.length} Labs Passed!`);
