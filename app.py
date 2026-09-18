"""
app.py
======
Main entry point for Kartikey Gupta's Portfolio Website.

Run with:
    streamlit run app.py

Admin panel:
    http://localhost:8501/?admin=true

Architecture:
  - app.py           → global CSS + routing
  - components/      → one file per section
  - utils/           → data access helpers
  - data/*.json      → all content (editable via admin)
  - assets/          → images, resume PDF
"""

import streamlit as st
import streamlit.components.v1 as components

# ── Must be the FIRST Streamlit call ─────────────────────────────────────────
st.set_page_config(
    page_title="Kartikey Gupta | Portfolio",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        "Get Help": None,
        "Report a bug": None,
        "About": None,
    },
)

# ── Imports (after set_page_config) ──────────────────────────────────────────
from utils.data_manager import ensure_dirs, load_profile
from utils.helpers import inject_css, inject_html

from components.hero         import render_hero
from components.about        import render_about
from components.skills       import render_skills
from components.projects     import render_projects
from components.experience   import render_experience
from components.certificates import render_certificates
from components.contact      import render_contact
from components.admin        import render_admin


# ── Ensure all folders exist on every run ────────────────────────────────────
ensure_dirs()


# ═══════════════════════════════════════════════════════════════════════════════
# GLOBAL STYLES
# Injects all global CSS: reset, typography, navbar, section styles, animations.
# ═══════════════════════════════════════════════════════════════════════════════
GLOBAL_CSS = """
/* ── Google Fonts ─────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Space+Grotesk:wght@400;500;700&family=JetBrains+Mono:wght@400;600&display=swap');

/* ── CSS Variables ────────────────────────────────────────── */
:root {
  --bg-primary:    #0a0a0f;
  --bg-secondary:  #0f0f1a;
  --bg-card:       rgba(15, 15, 26, 0.8);
  --accent-cyan:   #00d4ff;
  --accent-purple: #a855f7;
  --accent-green:  #10b981;
  --text-primary:  #e2e8f0;
  --text-secondary:#94a3b8;
  --text-muted:    #64748b;
  --border-subtle: rgba(255,255,255,0.07);
  --glow-cyan:     rgba(0,212,255,0.15);
  --glow-purple:   rgba(168,85,247,0.15);
  --font-main:     'Inter', system-ui, sans-serif;
  --font-mono:     'JetBrains Mono', monospace;
  --radius-card:   20px;
}

/* ── Global reset / base ──────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; }

a, a:hover, a:focus, a:active, a:visited {
  text-decoration: none !important;
}

html, body, [data-testid="stAppViewContainer"], .stApp, section.main, [data-testid="stMain"] {
  background-color: var(--bg-primary) !important;
  color: var(--text-primary) !important;
  font-family: var(--font-main) !important;
}

/* ── Hide Streamlit chrome ────────────────────────────────── */
#MainMenu                                        { visibility: hidden !important; }
footer[data-testid="stFooter"]                   { display: none !important; }
header                                           { visibility: hidden !important; }
[data-testid="stHeader"]                         { display: none !important; }
[data-testid="stToolbar"]                        { display: none !important; }
[data-testid="collapsedControl"]                 { display: none !important; }
[data-testid="stSidebarNav"]                     { display: none !important; }
[data-testid="stDecoration"]                     { display: none !important; }
.stDeployButton                                  { display: none !important; }
.css-1544g2n, .css-18e3th9                       { padding-top: 0 !important; }
[data-testid="stAppViewContainer"] > section:first-child { padding-top: 0 !important; }

/* Remove default constraints to fit full computer screen */
.block-container {
  padding-top: 0 !important;
  padding-bottom: 0 !important;
  padding-left: 3rem !important;
  padding-right: 3rem !important;
  max-width: 100% !important;
  width: 100% !important;
}

[data-testid="stAppViewContainer"] {
  overflow-x: hidden !important;
  width: 100% !important;
}

/* ── Background gradient animation ───────────────────────── */
body::before {
  content: '';
  position: fixed;
  inset: 0;
  background:
    radial-gradient(ellipse 60% 40% at 10% 20%, rgba(0,212,255,0.04) 0%, transparent 100%),
    radial-gradient(ellipse 50% 60% at 90% 80%, rgba(168,85,247,0.04) 0%, transparent 100%);
  pointer-events: none;
  z-index: 0;
}

/* ── Sticky navigation bar ────────────────────────────────── */
.navbar {
  position: sticky;
  top: 0;
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 32px;
  height: 62px;
  background: rgba(10, 10, 15, 0.85);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--border-subtle);
  box-shadow: 0 2px 20px rgba(0,0,0,0.3);
  animation: slideDown 0.5s ease-out;
}
@keyframes slideDown {
  from { transform: translateY(-100%); opacity: 0; }
  to   { transform: translateY(0);     opacity: 1; }
}

.nav-logo {
  font-family: var(--font-mono);
  font-size: 1rem;
  font-weight: 700;
  background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -0.5px;
  text-decoration: none;
}

.nav-links {
  display: flex;
  gap: 6px;
  list-style: none;
  margin: 0; padding: 0;
}
.nav-links a {
  padding: 7px 16px;
  border-radius: 8px;
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 0.84rem;
  font-weight: 500;
  transition: all 0.25s ease;
  letter-spacing: 0.3px;
}
.nav-links a:hover {
  color: var(--accent-cyan);
  background: rgba(0,212,255,0.08);
}
.nav-links a.nav-active {
  color: var(--accent-cyan);
  background: rgba(0,212,255,0.1);
  border-bottom: 2px solid var(--accent-cyan);
  border-radius: 8px 8px 0 0;
}

.nav-admin-btn {
  padding: 7px 18px;
  border-radius: 50px;
  background: linear-gradient(135deg, rgba(99,102,241,0.15), rgba(168,85,247,0.15));
  color: #c4b5fd !important;
  border: 1px solid rgba(168,85,247,0.3);
  font-size: 0.82rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.25s;
  display: inline-flex;
  align-items: center;
  gap: 5px;
}
.nav-admin-btn:hover {
  background: linear-gradient(135deg, rgba(99,102,241,0.28), rgba(168,85,247,0.28)) !important;
  border-color: rgba(168,85,247,0.6) !important;
  transform: translateY(-1px);
}

@media (max-width: 640px) {
  .nav-links { display: none; }
  .navbar { padding: 0 18px; }
}

/* ── Section headings ─────────────────────────────────────── */
.section-heading {
  text-align: center;
  padding: 60px 0 30px;
}
.section-title {
  font-size: clamp(1.8rem, 4vw, 2.6rem);
  font-weight: 800;
  background: linear-gradient(135deg, var(--text-primary) 0%, var(--accent-cyan) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -0.5px;
  margin-bottom: 12px;
}
.section-divider {
  width: 60px; height: 3px;
  background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple));
  border-radius: 2px;
  margin: 0 auto 14px;
}
.section-subtitle {
  color: var(--text-muted);
  font-size: 0.95rem;
  max-width: 440px;
  margin: 0 auto;
}

/* ── Divider between sections ─────────────────────────────── */
.section-sep {
  border: none;
  border-top: 1px solid var(--border-subtle);
  margin: 20px 0;
}

/* ── Streamlit widget overrides (dark theme polish) ──────── */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
[data-testid="stSelectbox"] select {
  background-color: rgba(15,15,26,0.9) !important;
  border-color: rgba(255,255,255,0.1) !important;
  color: var(--text-primary) !important;
  border-radius: 10px !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
  border-color: var(--accent-cyan) !important;
  box-shadow: 0 0 0 2px rgba(0,212,255,0.15) !important;
}
[data-testid="stButton"] > button {
  border-radius: 10px !important;
  font-weight: 600 !important;
  transition: all 0.25s ease !important;
}
[data-testid="stButton"] > button[kind="primary"],
[data-testid="stFormSubmitButton"] > button {
  background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple)) !important;
  border: none !important;
  color: #fff !important;
  box-shadow: 0 4px 16px rgba(0,212,255,0.3) !important;
}
[data-testid="stButton"] > button:hover,
[data-testid="stFormSubmitButton"] > button:hover {
  transform: translateY(-2px) !important;
  filter: brightness(1.1) !important;
}
[data-testid="stRadio"] label {
  color: var(--text-secondary) !important;
}
[data-testid="stExpander"] {
  background: rgba(15,15,26,0.7) !important;
  border: 1px solid var(--border-subtle) !important;
  border-radius: 12px !important;
}
[data-testid="stTabs"] [role="tab"] {
  font-weight: 600 !important;
}
[data-testid="stTabs"] [aria-selected="true"] {
  color: var(--accent-cyan) !important;
  border-bottom-color: var(--accent-cyan) !important;
}

/* ── Scrollbar styling ───────────────────────────────────── */
::-webkit-scrollbar       { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, var(--accent-cyan), var(--accent-purple));
  border-radius: 6px;
}
::-webkit-scrollbar-thumb:hover { filter: brightness(1.3); }

/* ── Selection colour ────────────────────────────────────── */
/* ── Theme Toggle Button Styling ────────────────────────────── */
.theme-toggle-btn {
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 50%;
  width: 38px;
  height: 38px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 1.1rem;
  transition: all 0.3s ease;
  color: #f8fafc;
  outline: none;
}
.theme-toggle-btn:hover {
  background: rgba(0, 212, 255, 0.15);
  border-color: rgba(0, 212, 255, 0.4);
  transform: scale(1.08) rotate(15deg);
  box-shadow: 0 0 15px rgba(0, 212, 255, 0.3);
}

/* ── Light Theme Overrides ─────────────────────────────────── */
.light-theme,
.light-theme body,
.light-theme [data-testid="stAppViewContainer"],
.light-theme .stApp,
.light-theme section.main,
.light-theme [data-testid="stMain"],
body.light-theme,
[data-testid="stAppViewContainer"].light-theme {
  --bg-primary: #f8fafc !important;
  --bg-secondary: #f1f5f9 !important;
  --bg-card: rgba(255, 255, 255, 0.92) !important;
  --text-primary: #0f172a !important;
  --text-secondary: #334155 !important;
  --text-muted: #64748b !important;
  --border-subtle: rgba(0, 0, 0, 0.1) !important;
  background-color: #f8fafc !important;
  background: #f8fafc !important;
  color: #0f172a !important;
}

.light-theme .navbar {
  background: rgba(255, 255, 255, 0.94) !important;
  border-bottom: 1px solid rgba(0, 0, 0, 0.08) !important;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06) !important;
}

.light-theme .nav-links a {
  color: #334155 !important;
}
.light-theme .nav-links a:hover {
  color: #00d4ff !important;
  background: rgba(0,212,255,0.08) !important;
}

.light-theme .theme-toggle-btn {
  background: rgba(0, 0, 0, 0.06) !important;
  border-color: rgba(0, 0, 0, 0.15) !important;
  color: #0f172a !important;
}

.light-theme .about-profile-card-3d,
.light-theme .who-i-am-card-3d,
.light-theme .edu-card-3d,
.light-theme .skill-card-img2,
.light-theme .project-card-3d,
.light-theme .tl-card-3d,
.light-theme .cert-card-3d,
.light-theme .contact-info-card-3d,
.light-theme .portfolio-footer {
  background: rgba(255, 255, 255, 0.92) !important;
  border-color: rgba(0, 0, 0, 0.1) !important;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.06) !important;
  color: #0f172a !important;
}

.light-theme .skills-title,
.light-theme .projects-title,
.light-theme .exp-title,
.light-theme .cert-title,
.light-theme .contact-title,
.light-theme .who-i-am-title,
.light-theme .about-profile-name,
.light-theme .card-category-name,
.light-theme .project-name-3d,
.light-theme .tl-org,
.light-theme .cert-title-3d,
.light-theme .contact-text-value-3d,
.light-theme .interests-title-3d,
.light-theme .about-stat-val,
.light-theme .edu-degree-text {
  color: #0f172a !important;
}

.light-theme .skills-subtitle,
.light-theme .projects-subtitle,
.light-theme .exp-subtitle,
.light-theme .cert-subtitle,
.light-theme .contact-subtitle,
.light-theme .who-i-am-desc,
.light-theme .card-category-desc,
.light-theme .project-desc-3d,
.light-theme .tl-desc,
.light-theme .cert-meta-3d,
.light-theme .about-profile-role,
.light-theme .about-stat-lbl,
.light-theme .edu-college-text,
.light-theme .contact-text-label-3d {
  color: #475569 !important;
}

.light-theme .skills-badge,
.light-theme .projects-badge,
.light-theme .exp-badge,
.light-theme .cert-badge,
.light-theme .contact-badge,
.light-theme .about-pill-badge {
  background: rgba(0, 0, 0, 0.04) !important;
  border-color: rgba(0, 0, 0, 0.12) !important;
  color: #00d4ff !important;
}

.light-theme .interest-pill-3d,
.light-theme .social-btn-3d,
.light-theme .social-icon-btn-3d,
.light-theme .skill-pill-img2,
.light-theme .proj-btn-gh-3d {
  background: rgba(255, 255, 255, 0.95) !important;
  color: #0f172a !important;
  border-color: rgba(0, 0, 0, 0.12) !important;
}

.light-theme [data-testid="stTextInput"] label,
.light-theme [data-testid="stTextArea"] label,
.light-theme [data-testid="stSelectbox"] label,
.light-theme [data-testid="stWidgetLabel"] {
  color: #1e293b !important;
  font-weight: 600 !important;
}

.light-theme [data-testid="stTextInput"] input,
.light-theme [data-testid="stTextArea"] textarea,
.light-theme [data-testid="stSelectbox"] select {
  background-color: #ffffff !important;
  border-color: rgba(0, 0, 0, 0.18) !important;
  color: #0f172a !important;
}

.light-theme [data-testid="stTextInput"] input::placeholder,
.light-theme [data-testid="stTextArea"] textarea::placeholder {
  color: #64748b !important;
}

.light-theme [data-testid="stRadio"] label {
  color: #334155 !important;
}
"""


# ═══════════════════════════════════════════════════════════════════════════════
# NAVIGATION HTML
# ═══════════════════════════════════════════════════════════════════════════════
NAV_HTML = """
<nav class="navbar">
  <a class="nav-logo" href="#about"><span style="font-weight:900;">KG</span></a>
  <ul class="nav-links">
    <li><a href="#" class="nav-active">Home</a></li>
    <li><a href="#about">About</a></li>
    <li><a href="#skills">Skills</a></li>
    <li><a href="#projects">Projects</a></li>
    <li><a href="#experience">Experience</a></li>
    <li><a href="#certificates">Certificates</a></li>
    <li><a href="#contact">Contact</a></li>
  </ul>
  <div style="display: flex; align-items: center; gap: 10px;">
    <button id="theme-toggle-btn" class="theme-toggle-btn" title="Toggle Light/Dark Theme">
      <span id="theme-toggle-icon">🌙</span>
    </button>
    <a href="?admin=true" class="nav-admin-btn">&#128100; Admin</a>
  </div>
</nav>
"""


# ═══════════════════════════════════════════════════════════════════════════════
# FOOTER HTML
# ═══════════════════════════════════════════════════════════════════════════════
def _footer_html(name: str, github: str) -> str:
    import textwrap
    from datetime import datetime
    year = datetime.now().year
    return textwrap.dedent(f"""
<footer class="portfolio-footer" style="
    visibility: visible !important;
    display: block !important;
    background: rgba(13, 14, 28, 0.85);
    border-top: 1.5px solid rgba(0, 212, 255, 0.2);
    backdrop-filter: blur(16px);
    padding: 35px 40px 25px;
    margin-top: 60px;
    border-radius: 24px 24px 0 0;
    box-shadow: 0 -10px 30px rgba(0,0,0,0.4), 0 0 20px rgba(0,212,255,0.08);
    position: relative;
    z-index: 10;
">
    <div style="
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 16px;
        max-width: 1400px;
        margin: 0 auto 20px;
    ">
        <a href="#about" style="font-size: 1.4rem; font-weight: 900; color: #ffffff; text-decoration: none; font-family: 'Outfit', sans-serif;">
            <span style="background: linear-gradient(135deg, #00d4ff, #a855f7); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">KG</span>
        </a>
        <div style="display: flex; gap: 20px; flex-wrap: wrap;">
            <a href="#" style="color: #94a3b8; text-decoration: none; font-size: 0.86rem; font-weight: 600; transition: color 0.2s;">Home</a>
            <a href="#about" style="color: #94a3b8; text-decoration: none; font-size: 0.86rem; font-weight: 600; transition: color 0.2s;">About</a>
            <a href="#skills" style="color: #94a3b8; text-decoration: none; font-size: 0.86rem; font-weight: 600; transition: color 0.2s;">Skills</a>
            <a href="#projects" style="color: #94a3b8; text-decoration: none; font-size: 0.86rem; font-weight: 600; transition: color 0.2s;">Projects</a>
            <a href="#experience" style="color: #94a3b8; text-decoration: none; font-size: 0.86rem; font-weight: 600; transition: color 0.2s;">Experience</a>
            <a href="#certificates" style="color: #94a3b8; text-decoration: none; font-size: 0.86rem; font-weight: 600; transition: color 0.2s;">Certificates</a>
            <a href="#contact" style="color: #94a3b8; text-decoration: none; font-size: 0.86rem; font-weight: 600; transition: color 0.2s;">Contact</a>
        </div>
    </div>

    <div style="
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 12px;
        padding-top: 18px;
        border-top: 1px solid rgba(255,255,255,0.08);
        font-size: 0.92rem;
        font-weight: 600;
        color: #cbd5e1;
    ">
        <div>
            🐍 Made With <span style="color:#00d4ff; font-weight:800;">Python</span>
        </div>
        <div>
            Designed By <span style="background: linear-gradient(135deg, #00d4ff, #a855f7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900; letter-spacing: 0.5px;">KARTIKEY GUPTA</span>
        </div>
    </div>
</footer>
""").strip()


# ═══════════════════════════════════════════════════════════════════════════════
# ROUTING: Admin vs. Portfolio
# ═══════════════════════════════════════════════════════════════════════════════
def main():
    # Inject global CSS first
    inject_css(GLOBAL_CSS)

    # Check if admin mode is requested via query param
    query_params = st.query_params
    is_admin = query_params.get("admin", "").lower() == "true"

    if is_admin:
        # ── Admin mode ─────────────────────────────────────────────────────
        inject_html("""
        <style>
          /* Slightly different background for admin */
          [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #05050a, #0a050f) !important;
          }
          .block-container { padding-top: 40px !important; }
        </style>
        """)
        render_admin()

    else:
        # ── Portfolio mode ──────────────────────────────────────────────────
        profile = load_profile()

        # Sticky navbar
        inject_html(NAV_HTML)

        # Theme sync and event listener engine
        components.html("""
        <script>
        (function initThemeEngine() {
          function applyTheme(theme) {
            const isLight = (theme === 'light');
            try {
              if (window.parent && window.parent.document) {
                const pDoc = window.parent.document;
                const els = [
                  pDoc.body,
                  pDoc.documentElement,
                  pDoc.querySelector('[data-testid="stAppViewContainer"]'),
                  pDoc.querySelector('.stApp'),
                  pDoc.querySelector('section.main'),
                  pDoc.querySelector('[data-testid="stMain"]')
                ];
                els.forEach(el => {
                  if (el) {
                    if (isLight) el.classList.add('light-theme');
                    else el.classList.remove('light-theme');
                  }
                });
                const icons = pDoc.querySelectorAll('#theme-toggle-icon');
                icons.forEach(ic => { ic.textContent = isLight ? '☀️' : '🌙'; });
              }
            } catch(e) {}
          }

          function setupButtonListener() {
            try {
              if (window.parent && window.parent.document) {
                const btn = window.parent.document.getElementById('theme-toggle-btn');
                if (btn && !btn.dataset.themeBound) {
                  btn.dataset.themeBound = 'true';
                  btn.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    let isLight = window.parent.document.body.classList.contains('light-theme');
                    let newTheme = isLight ? 'dark' : 'light';
                    try { localStorage.setItem('portfolio-theme', newTheme); } catch(err) {}
                    applyTheme(newTheme);
                  });
                }
              }
            } catch(e) {}
          }

          let savedTheme = 'dark';
          try { savedTheme = localStorage.getItem('portfolio-theme') || 'dark'; } catch(e) {}
          applyTheme(savedTheme);

          setInterval(function() {
            setupButtonListener();
            let t = 'dark';
            try { t = localStorage.getItem('portfolio-theme') || 'dark'; } catch(e) {}
            applyTheme(t);
          }, 200);
        })();
        </script>
        """, height=0, width=0)

        # ── Hero ──────────────────────────────────────────────────────────
        render_hero()

        # ── About ─────────────────────────────────────────────────────────
        inject_html('<hr class="section-sep"/>')
        render_about()

        # ── Skills ────────────────────────────────────────────────────────
        inject_html('<hr class="section-sep"/>')
        render_skills()

        # ── Projects ──────────────────────────────────────────────────────
        inject_html('<hr class="section-sep"/>')
        render_projects()

        # ── Experience ────────────────────────────────────────────────────
        inject_html('<hr class="section-sep"/>')
        render_experience()

        # ── Certificates ──────────────────────────────────────────────────
        inject_html('<hr class="section-sep"/>')
        render_certificates()

        # ── Contact ───────────────────────────────────────────────────────
        inject_html('<hr class="section-sep"/>')
        render_contact()

        # ── Footer ────────────────────────────────────────────────────────
        inject_html(_footer_html(
            profile.get("name", "Kartikey Gupta"),
            profile.get("github", ""),
        ))


if __name__ == "__main__":
    main()
