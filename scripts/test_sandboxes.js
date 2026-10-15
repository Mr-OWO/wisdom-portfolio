const fs = require('fs');

// Mock a minimal DOM environment
class MockElement {
  constructor(id) {
    this.id = id;
    this.innerHTML = '';
    this.value = '';
    this.style = {};
    this.classList = {
      add: () => {},
      remove: () => {},
      contains: () => false
    };
    this.listeners = {};
  }
  addEventListener(event, fn) {
    this.listeners[event] = fn;
  }
  querySelector() { return new MockElement('child'); }
  querySelectorAll() { return []; }
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
  alert: (msg) => console.log('ALERT:', msg)
};
global.crypto = global.window.crypto;

const code = fs.readFileSync('app/static/js/labs.js', 'utf8');
eval(code + '\nglobal.LabsEngine = LabsEngine;\nglobal.window.LabsEngine = LabsEngine;\n');

const slugs = [
  "vuln-scanner", "phishing-detector", "traffic-sentinel", "rbac-simulator",
  "entropy-guard", "honeypot-telemetry", "secure-vault", "ransomware-guard",
  "asset-tracker", "config-auditor", "patch-manager", "keylogger-detector",
  "backup-validator", "ticket-routing", "settlement-debugger", "csat-analytics",
  "kb-assistant", "market-scraper", "market-predictor", "social-trend-bot"
];

console.log("Testing LabsEngine.init() for all 20 slugs:");
let failed = 0;
for (const s of slugs) {
  try {
    elements["lab-sandbox-container"] = new MockElement("lab-sandbox-container");
    const html = LabsEngine.renderSandbox(s);
    if (!html || html.trim() === '') {
      console.error(`[FAIL] ${s}: renderSandbox returned empty!`);
      failed++;
      continue;
    }
    // inject IDs from html into elements map so bindEvents finds them
    const matches = html.match(/id="([^"]+)"/g) || [];
    for (const m of matches) {
      const id = m.replace('id="', '').replace('"', '');
      elements[id] = new MockElement(id);
    }
    LabsEngine.bindEvents(s);
    console.log(`[OK] ${s}: rendered ${html.length} chars, events bound successfully.`);
  } catch (err) {
    console.error(`[ERROR] ${s}:`, err.message);
    failed++;
  }
}
console.log(`\nResults: ${slugs.length - failed}/${slugs.length} passed.`);
