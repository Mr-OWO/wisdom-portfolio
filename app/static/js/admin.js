/**
 * WISDOM OGECHI OWABOR - CMS ADMIN ENGINE & DIAGNOSTICS
 * Manages career history editor, project manager, inquiries inbox triage, and real-time telemetry.
 */

const AdminPortal = {
  currentUser: null,
  diagnosticsTimer: null,

  init() {
    this.checkSession();
    this.bindEvents();
  },

  async checkSession() {
    try {
      const res = await fetch("/api/admin/me");
      if (res.ok) {
        const data = await res.json();
        this.currentUser = data.admin;
        this.showDashboard();
      } else {
        this.showLogin();
      }
    } catch (e) {
      this.showLogin();
    }
  },

  showLogin() {
    document.getElementById("admin-login-view").style.display = "block";
    document.getElementById("admin-dashboard-view").style.display = "none";
    if (this.diagnosticsTimer) clearInterval(this.diagnosticsTimer);
  },

  showDashboard() {
    document.getElementById("admin-login-view").style.display = "none";
    document.getElementById("admin-dashboard-view").style.display = "block";
    document.getElementById("admin-username-badge").textContent = this.currentUser.username;
    this.loadDiagnostics();
    this.loadExperience();
    this.loadProjects();
    this.loadInquiries();

    // Start diagnostics poll every 5s
    if (this.diagnosticsTimer) clearInterval(this.diagnosticsTimer);
    this.diagnosticsTimer = setInterval(() => this.loadDiagnostics(), 5000);
  },

  bindEvents() {
    // Login form
    const loginForm = document.getElementById("admin-login-form");
    if (loginForm) {
      loginForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const u = document.getElementById("admin-u").value;
        const p = document.getElementById("admin-p").value;
        const err = document.getElementById("admin-login-error");
        err.textContent = "";

        try {
          const res = await fetch("/api/admin/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username: u, password: p })
          });
          if (res.ok) {
            const data = await res.json();
            this.currentUser = data.user;
            this.showDashboard();
          } else {
            const d = await res.json();
            err.textContent = d.detail || "Authentication failed";
          }
        } catch (error) {
          err.textContent = "Server communication error";
        }
      });
    }

    // Logout button
    const logoutBtn = document.getElementById("admin-logout-btn");
    if (logoutBtn) {
      logoutBtn.addEventListener("click", async () => {
        await fetch("/api/admin/logout", { method: "POST" });
        this.currentUser = null;
        this.showLogin();
      });
    }

    // Admin Tabs
    const tabs = document.querySelectorAll(".admin-nav-tab");
    tabs.forEach(tab => {
      tab.addEventListener("click", () => {
        tabs.forEach(t => t.classList.remove("active"));
        tab.classList.add("active");
        const target = tab.dataset.target;
        document.querySelectorAll(".admin-tab-pane").forEach(p => p.style.display = "none");
        document.getElementById(target).style.display = "block";
      });
    });

    // Add Experience button
    const addExpBtn = document.getElementById("admin-btn-add-exp");
    if (addExpBtn) {
      addExpBtn.addEventListener("click", () => this.openExperienceModal());
    }
  },

  async loadDiagnostics() {
    try {
      const res = await fetch("/api/admin/diagnostics");
      if (res.ok) {
        const d = await res.json();
        document.getElementById("diag-uptime").textContent = d.uptime;
        document.getElementById("diag-latency").textContent = `${d.db_latency_ms} ms`;
        document.getElementById("diag-mem").textContent = `${d.memory_mb} MB`;
        document.getElementById("diag-cpu").textContent = `${d.cpu_usage_percent}%`;
        document.getElementById("diag-status").textContent = d.status.toUpperCase();
      }
    } catch (e) {
      console.error("Diagnostics load error", e);
    }
  },

  async loadExperience() {
    const list = document.getElementById("admin-experience-list");
    try {
      const res = await fetch("/api/admin/experience");
      const data = await res.json();
      list.innerHTML = data.map(item => `
        <div class="admin-table-row" style="background:#111827; border:1px solid rgba(255,255,255,0.08); padding:1rem; border-radius:8px; margin-bottom:0.75rem; display:flex; justify-content:space-between; align-items:center;">
          <div>
            <strong style="color:#ffffff; font-size:1.05rem;">${item.company}</strong>
            <span style="color:#06b6d4; margin-left:0.5rem;">— ${item.role_title}</span>
            <div style="color:#9ca3af; font-size:0.85rem; margin-top:0.25rem;">${item.period} | ${item.location} (Order: ${item.sort_order})</div>
          </div>
          <div style="display:flex; gap:0.5rem;">
            <button class="btn btn-outline" style="font-size:0.8rem; padding:0.35rem 0.75rem;" onclick="AdminPortal.openExperienceModal(${JSON.stringify(item).replace(/"/g, '&quot;')})">Edit</button>
            <button class="btn btn-outline" style="font-size:0.8rem; padding:0.35rem 0.75rem; border-color:#ef4444; color:#ef4444;" onclick="AdminPortal.deleteExperience(${item.id})">Delete</button>
          </div>
        </div>
      `).join("");
    } catch (e) {
      list.innerHTML = "<p>Error loading experience entries.</p>";
    }
  },

  openExperienceModal(item = null) {
    const isEdit = !!item;
    const modal = document.getElementById("admin-generic-modal");
    const title = document.getElementById("admin-modal-title");
    const body = document.getElementById("admin-modal-body");

    title.textContent = isEdit ? `Edit Experience: ${item.company}` : "Add Career Experience Entry";
    body.innerHTML = `
      <form id="exp-modal-form">
        <div class="form-group">
          <label class="form-label">Company Name:</label>
          <input type="text" id="m-exp-company" class="form-control" value="${item ? item.company : ''}" required>
        </div>
        <div class="form-group">
          <label class="form-label">Role Title:</label>
          <input type="text" id="m-exp-role" class="form-control" value="${item ? item.role_title : ''}" required>
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:1rem;">
          <div class="form-group">
            <label class="form-label">Period (e.g. 2023 - Present):</label>
            <input type="text" id="m-exp-period" class="form-control" value="${item ? item.period : ''}" required>
          </div>
          <div class="form-group">
            <label class="form-label">Location:</label>
            <input type="text" id="m-exp-location" class="form-control" value="${item ? item.location : ''}" required>
          </div>
        </div>
        <div class="form-group">
          <label class="form-label">Summary Bullets (one per line):</label>
          <textarea id="m-exp-bullets" class="form-control" style="min-height:120px;" required>${item ? item.summary_bullets.join("\n") : ''}</textarea>
        </div>
        <div class="form-group">
          <label class="form-label">Sort Order (lower is higher priority):</label>
          <input type="number" id="m-exp-sort" class="form-control" value="${item ? item.sort_order : 0}">
        </div>
        <div style="display:flex; justify-content:flex-end; gap:0.5rem; margin-top:1.5rem;">
          <button type="button" class="btn btn-outline" onclick="document.getElementById('admin-generic-modal').classList.remove('active')">Cancel</button>
          <button type="submit" class="btn btn-primary">${isEdit ? 'Save Changes' : 'Create Entry'}</button>
        </div>
      </form>
    `;

    document.getElementById("exp-modal-form").addEventListener("submit", async (e) => {
      e.preventDefault();
      const payload = {
        company: document.getElementById("m-exp-company").value,
        role_title: document.getElementById("m-exp-role").value,
        period: document.getElementById("m-exp-period").value,
        location: document.getElementById("m-exp-location").value,
        summary_bullets: document.getElementById("m-exp-bullets").value.split("\n").filter(b => b.trim().length > 0),
        sort_order: parseInt(document.getElementById("m-exp-sort").value) || 0
      };

      const url = isEdit ? `/api/admin/experience/${item.id}` : "/api/admin/experience";
      const method = isEdit ? "PUT" : "POST";

      const res = await fetch(url, {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      if (res.ok) {
        modal.classList.remove("active");
        this.loadExperience();
        if (window.App) window.App.loadExperience();
      } else {
        alert("Failed to save experience entry");
      }
    });

    modal.classList.add("active");
  },

  async deleteExperience(id) {
    if (!confirm("Are you sure you want to delete this career history entry?")) return;
    const res = await fetch(`/api/admin/experience/${id}`, { method: "DELETE" });
    if (res.ok) {
      this.loadExperience();
      if (window.App) window.App.loadExperience();
    }
  },

  async loadProjects() {
    const list = document.getElementById("admin-projects-list");
    try {
      const res = await fetch("/api/admin/projects");
      const data = await res.json();
      list.innerHTML = data.map(p => `
        <div style="background:#111827; border:1px solid rgba(255,255,255,0.08); padding:1rem; border-radius:8px; margin-bottom:0.75rem; display:flex; justify-content:space-between; align-items:center;">
          <div>
            <strong style="color:#ffffff; font-size:1rem;">${p.title}</strong>
            <span style="font-size:0.75rem; background:rgba(6,182,212,0.1); color:#06b6d4; padding:0.2rem 0.5rem; border-radius:4px; margin-left:0.5rem;">${p.category}</span>
            <div style="font-size:0.8rem; color:#9ca3af; margin-top:0.25rem;">
              Repo: <a href="${p.github_url}" target="_blank" style="color:#06b6d4;">${p.github_url}</a> | Status: <span style="color:${p.live_status ? '#10b981' : '#f43f5e'}; font-weight:700;">${p.live_status ? 'LIVE' : 'DISABLED'}</span>
            </div>
          </div>
          <div style="display:flex; gap:0.5rem;">
            <button class="btn btn-outline" style="font-size:0.8rem; padding:0.35rem 0.75rem;" onclick="AdminPortal.openProjectModal(${JSON.stringify(p).replace(/"/g, '&quot;')})">Edit Details</button>
          </div>
        </div>
      `).join("");
    } catch (e) {
      list.innerHTML = "<p>Error loading projects.</p>";
    }
  },

  openProjectModal(p) {
    const modal = document.getElementById("admin-generic-modal");
    const title = document.getElementById("admin-modal-title");
    const body = document.getElementById("admin-modal-body");

    title.textContent = `Edit Project: ${p.title}`;
    body.innerHTML = `
      <form id="proj-modal-form">
        <div class="form-group">
          <label class="form-label">Project Title:</label>
          <input type="text" id="m-p-title" class="form-control" value="${p.title}" required>
        </div>
        <div class="form-group">
          <label class="form-label">Executive Summary:</label>
          <textarea id="m-p-summary" class="form-control" style="min-height:80px;" required>${p.summary}</textarea>
        </div>
        <div class="form-group">
          <label class="form-label">Architecture Breakdown:</label>
          <textarea id="m-p-arch" class="form-control" style="min-height:80px;" required>${p.architecture_breakdown}</textarea>
        </div>
        <div class="form-group">
          <label class="form-label">Tech Stack (comma-separated):</label>
          <input type="text" id="m-p-tech" class="form-control" value="${p.tech_stack.join(', ')}">
        </div>
        <div class="form-group">
          <label class="form-label">GitHub Repository URL:</label>
          <input type="text" id="m-p-github" class="form-control" value="${p.github_url}">
        </div>
        <div class="form-group">
          <label class="form-label">Live Availability Status:</label>
          <select id="m-p-status" class="form-control">
            <option value="1" ${p.live_status === 1 ? 'selected' : ''}>Active / Live (1)</option>
            <option value="0" ${p.live_status === 0 ? 'selected' : ''}>Offline / Maintenance (0)</option>
          </select>
        </div>
        <div style="display:flex; justify-content:flex-end; gap:0.5rem; margin-top:1.5rem;">
          <button type="button" class="btn btn-outline" onclick="document.getElementById('admin-generic-modal').classList.remove('active')">Cancel</button>
          <button type="submit" class="btn btn-primary">Update Project</button>
        </div>
      </form>
    `;

    document.getElementById("proj-modal-form").addEventListener("submit", async (e) => {
      e.preventDefault();
      const payload = {
        title: document.getElementById("m-p-title").value,
        summary: document.getElementById("m-p-summary").value,
        architecture_breakdown: document.getElementById("m-p-arch").value,
        tech_stack: document.getElementById("m-p-tech").value.split(",").map(t => t.trim()).filter(Boolean),
        github_url: document.getElementById("m-p-github").value,
        live_status: parseInt(document.getElementById("m-p-status").value)
      };

      const res = await fetch(`/api/admin/projects/${p.id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      if (res.ok) {
        modal.classList.remove("active");
        this.loadProjects();
        if (window.App) window.App.loadProjects();
      } else {
        alert("Failed to update project");
      }
    });

    modal.classList.add("active");
  },

  async loadInquiries() {
    const list = document.getElementById("admin-inquiries-list");
    try {
      const res = await fetch("/api/admin/inquiries");
      const data = await res.json();
      if (data.length === 0) {
        list.innerHTML = "<p style='color:#9ca3af;'>No contact inquiries in inbox.</p>";
        return;
      }
      list.innerHTML = data.map(inq => `
        <div style="background:#111827; border:1px solid rgba(255,255,255,0.08); padding:1.25rem; border-radius:8px; margin-bottom:0.75rem;">
          <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.5rem;">
            <div>
              <strong style="color:#ffffff; font-size:1.05rem;">${inq.sender_name}</strong>
              <span style="color:#06b6d4; font-size:0.85rem; margin-left:0.5rem;">&lt;${inq.sender_email}&gt;</span>
            </div>
            <span style="background:${inq.status === 'new' ? '#06b6d422' : 'rgba(255,255,255,0.05)'}; color:${inq.status === 'new' ? '#06b6d4' : '#9ca3af'}; font-size:0.75rem; padding:0.2rem 0.6rem; border-radius:4px; font-weight:700;">
              ${inq.status.toUpperCase()}
            </span>
          </div>
          <div style="color:#e2e8f0; font-weight:600; font-size:0.95rem; margin-bottom:0.4rem;">${inq.subject}</div>
          <p style="color:#9ca3af; font-size:0.9rem; line-height:1.5; white-space:pre-wrap; background:#05080f; padding:0.75rem; border-radius:6px; margin-bottom:0.75rem;">${inq.message}</p>
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <span style="color:#6b7280; font-size:0.75rem; font-family:var(--font-mono);">${inq.timestamp}</span>
            <div style="display:flex; gap:0.5rem;">
              ${inq.status !== 'read' ? `<button class="btn btn-outline" style="font-size:0.75rem; padding:0.25rem 0.6rem;" onclick="AdminPortal.updateInquiryStatus(${inq.id}, 'read')">Mark as Read</button>` : ''}
              ${inq.status !== 'archived' ? `<button class="btn btn-outline" style="font-size:0.75rem; padding:0.25rem 0.6rem;" onclick="AdminPortal.updateInquiryStatus(${inq.id}, 'archived')">Archive</button>` : ''}
              <button class="btn btn-outline" style="font-size:0.75rem; padding:0.25rem 0.6rem; border-color:#ef4444; color:#ef4444;" onclick="AdminPortal.deleteInquiry(${inq.id})">Delete</button>
            </div>
          </div>
        </div>
      `).join("");
    } catch (e) {
      list.innerHTML = "<p>Error loading inbox inquiries.</p>";
    }
  },

  async updateInquiryStatus(id, newStatus) {
    const res = await fetch(`/api/admin/inquiries/${id}/status`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status: newStatus })
    });
    if (res.ok) this.loadInquiries();
  },

  async deleteInquiry(id) {
    if (!confirm("Delete this contact message permanently?")) return;
    const res = await fetch(`/api/admin/inquiries/${id}`, { method: "DELETE" });
    if (res.ok) this.loadInquiries();
  }
};
