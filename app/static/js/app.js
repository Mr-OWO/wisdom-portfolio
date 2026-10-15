/**
 * WISDOM OGECHI OWABOR - MAIN APPLICATION CONTROLLER
 * Handles client-side routing, public data feeds, and modal sandboxes.
 */

const App = {
  allProjects: [],
  activeCategory: "ALL",

  init() {
    this.bindGlobalEvents();
    this.loadMetadata();
    this.loadExperience();
    this.loadProjects();
    this.handleRoute();

    window.addEventListener("popstate", () => this.handleRoute());
  },

  handleRoute() {
    const path = window.location.pathname;
    if (path.startsWith("/admin")) {
      this.showAdminSection();
    } else if (path.startsWith("/projects/")) {
      const slug = path.split("/projects/")[1].replace(/\/$/, "");
      if (slug) {
        this.openProjectLab(slug, false);
      }
    } else {
      this.showPublicSection();
    }
  },

  showPublicSection() {
    document.getElementById("public-view").style.display = "block";
    document.getElementById("admin-portal-view").style.display = "none";
    document.getElementById("lab-modal-overlay").classList.remove("active");
  },

  showAdminSection() {
    document.getElementById("public-view").style.display = "none";
    document.getElementById("admin-portal-view").style.display = "block";
    document.getElementById("lab-modal-overlay").classList.remove("active");
    if (window.AdminPortal) window.AdminPortal.init();
  },

  bindGlobalEvents() {
    // Navigation links
    document.querySelectorAll("[data-nav]").forEach(link => {
      link.addEventListener("click", (e) => {
        e.preventDefault();
        const route = link.getAttribute("href");
        history.pushState(null, "", route);
        this.handleRoute();
        if (route.startsWith("#")) {
          const el = document.querySelector(route);
          if (el) el.scrollIntoView({ behavior: "smooth" });
        }
      });
    });

    // Category filters
    document.querySelectorAll(".filter-tab").forEach(tab => {
      tab.addEventListener("click", () => {
        document.querySelectorAll(".filter-tab").forEach(t => t.classList.remove("active"));
        tab.classList.add("active");
        this.activeCategory = tab.dataset.category;
        this.filterProjects();
      });
    });

    // Contact Form
    const contactForm = document.getElementById("public-contact-form");
    if (contactForm) {
      contactForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const statusBox = document.getElementById("contact-form-status");
        statusBox.style.display = "block";
        statusBox.innerHTML = `<span style="color:#06b6d4;">Encrypting & submitting inquiry...</span>`;

        const payload = {
          sender_name: document.getElementById("cf-name").value,
          sender_email: document.getElementById("cf-email").value,
          subject: document.getElementById("cf-subject").value,
          message: document.getElementById("cf-message").value
        };

        try {
          const res = await fetch("/api/public/contact", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
          });
          const data = await res.json();
          if (res.ok) {
            statusBox.innerHTML = `<span style="color:#10b981;">✔ Message received. Wisdom's SecOps dispatch will reply shortly.</span>`;
            contactForm.reset();
          } else {
            statusBox.innerHTML = `<span style="color:#f43f5e;">✖ Error: ${data.detail || "Submission failed"}</span>`;
          }
        } catch (err) {
          statusBox.innerHTML = `<span style="color:#f43f5e;">✖ Failed to communicate with contact endpoint.</span>`;
        }
      });
    }

    // Modal Close
    const closeBtn = document.getElementById("lab-modal-close");
    if (closeBtn) {
      closeBtn.addEventListener("click", () => {
        document.getElementById("lab-modal-overlay").classList.remove("active");
        history.pushState(null, "", "/");
      });
    }
  },

  async loadMetadata() {
    try {
      const res = await fetch("/api/public/metadata");
      if (res.ok) {
        const d = await res.json();
        document.getElementById("hero-name").textContent = d.full_name;
        document.getElementById("hero-headline").textContent = d.professional_headline;
        document.getElementById("hero-bio").textContent = d.bio;
        
        // Populate HUD stats
        if (d.metrics) {
          document.getElementById("stat-uptime").textContent = d.metrics.uptime_pct || "99.98%";
          document.getElementById("stat-csat").textContent = d.metrics.csat_score || "96.4%";
          document.getElementById("stat-incidents").textContent = d.metrics.incidents_resolved || "450+";
          document.getElementById("stat-latency").textContent = d.metrics.p99_latency || "12ms";
        }
      }
    } catch (e) {
      console.error("Metadata load error", e);
    }
  },

  async loadExperience() {
    const timeline = document.getElementById("experience-timeline");
    try {
      const res = await fetch("/api/public/experience");
      const list = await res.json();
      timeline.innerHTML = list.map(item => `
        <div class="timeline-item">
          <div class="timeline-marker"></div>
          <div class="timeline-content">
            <div class="timeline-header">
              <div>
                <h3 class="timeline-company">${item.company}</h3>
                <div class="timeline-role">${item.role_title}</div>
              </div>
              <div class="timeline-period">${item.period} · ${item.location}</div>
            </div>
            <ul class="timeline-bullets">
              ${item.summary_bullets.map(b => `<li>${b}</li>`).join("")}
            </ul>
          </div>
        </div>
      `).join("");
    } catch (e) {
      timeline.innerHTML = "<p>Error loading career history.</p>";
    }
  },

  async loadProjects() {
    const grid = document.getElementById("projects-grid");
    try {
      const res = await fetch("/api/public/projects");
      this.allProjects = await res.json();
      this.filterProjects();
    } catch (e) {
      grid.innerHTML = "<p>Error loading project matrix.</p>";
    }
  },

  filterProjects() {
    const grid = document.getElementById("projects-grid");
    const filtered = this.activeCategory === "ALL" 
      ? this.allProjects 
      : this.allProjects.filter(p => p.category === this.activeCategory);

    grid.innerHTML = filtered.map(p => {
      let badgeClass = "badge-cyber";
      if (p.category === "IT Support") badgeClass = "badge-it";
      else if (p.category === "Customer Service") badgeClass = "badge-cs";
      else if (p.category === "Financial/Data") badgeClass = "badge-fin";

      return `
        <div class="project-card">
          <div class="project-card-header">
            <span class="project-category-badge ${badgeClass}">${p.category}</span>
            <span style="font-family:var(--font-mono); font-size:0.75rem; color:#10b981;">● Runnable Lab</span>
          </div>
          <h3 class="project-title">${p.title}</h3>
          <p class="project-summary">${p.summary}</p>
          <div class="tech-badges-list">
            ${p.tech_stack.map(t => `<span class="tech-badge">${t}</span>`).join("")}
          </div>
          <div class="project-actions">
            <a href="/projects/${p.slug}" class="btn-sandbox" onclick="event.preventDefault(); App.openProjectLab('${p.slug}');">
              🚀 Launch Sandbox
            </a>
            <a href="${p.github_url}" target="_blank" class="btn-github-link" title="Open GitHub Repository">
              GitHub ↗
            </a>
          </div>
        </div>
      `;
    }).join("");
  },

  async openProjectLab(slug, pushHistory = true) {
    if (pushHistory) {
      history.pushState(null, "", `/projects/${slug}`);
    }

    const modal = document.getElementById("lab-modal-overlay");
    const title = document.getElementById("lab-modal-title");
    const categoryBadge = document.getElementById("lab-modal-category");
    const desc = document.getElementById("lab-modal-desc");
    const arch = document.getElementById("lab-modal-arch");
    const techBox = document.getElementById("lab-modal-tech");
    const githubLink = document.getElementById("lab-modal-github");

    modal.classList.add("active");

    try {
      const res = await fetch(`/api/public/projects/${slug}`);
      if (res.ok) {
        const p = await res.json();
        title.textContent = p.title;
        categoryBadge.textContent = p.category;
        desc.textContent = p.summary;
        arch.textContent = p.architecture_breakdown;
        techBox.innerHTML = p.tech_stack.map(t => `<span class="tech-badge">${t}</span>`).join(" ");
        githubLink.href = p.github_url;

        // Initialize Sandbox
        if (window.LabsEngine) {
          window.LabsEngine.init(slug);
        }
      }
    } catch (e) {
      title.textContent = "Error Loading Lab";
    }
  }
};

document.addEventListener("DOMContentLoaded", () => App.init());
