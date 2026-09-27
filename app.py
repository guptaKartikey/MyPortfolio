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
from components.preloader    import render_preloader
from components.music_player import render_music_player


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
  --bg-primary:    #000000;
  --bg-secondary:  #080808;
  --bg-card:       rgba(8, 8, 12, 0.85);
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

html:not(.light-theme),
body:not(.light-theme),
[data-testid="stAppViewContainer"]:not(.light-theme),
.stApp:not(.light-theme),
section.main:not(.light-theme),
[data-testid="stMain"]:not(.light-theme) {
  background-color: #000000 !important;
  background:
    radial-gradient(ellipse 60% 50% at 0% 10%,   rgba(0, 212, 255, 0.20)  0%, transparent 60%),
    radial-gradient(ellipse 55% 60% at 100% 90%,  rgba(168, 85, 247, 0.22) 0%, transparent 60%),
    radial-gradient(ellipse 40% 35% at 85% 5%,   rgba(0, 212, 255, 0.10)  0%, transparent 55%),
    radial-gradient(ellipse 35% 30% at 15% 95%,  rgba(16, 185, 129, 0.08) 0%, transparent 55%),
    radial-gradient(ellipse 30% 25% at 50% 48%,  rgba(217, 70, 239, 0.07) 0%, transparent 55%),
    #000000 !important;
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
  padding-top: 64px !important;
  padding-bottom: 0 !important;
  padding-left: 2.5rem !important;
  padding-right: 2.5rem !important;
  max-width: 100% !important;
  width: 100% !important;
}

/* Eliminate extra spacing from headless/zero-height components before hero */
div[data-testid="stCustomComponentV1"]:has(iframe[height="0"]),
div[data-testid="stElementContainer"]:has(iframe[height="0"]),
div[data-testid="element-container"]:has(iframe[height="0"]),
iframe[height="0"],
iframe[height="0px"] {
  display: none !important;
  margin: 0 !important;
  padding: 0 !important;
  height: 0 !important;
  min-height: 0 !important;
}

/* Center all custom component iframes (Hero, Preloader, Music Player) */
div[data-testid="stCustomComponentV1"] {
  width: 100% !important;
  display: flex !important;
  justify-content: center !important;
  align-items: center !important;
  margin: 0 auto !important;
}

div[data-testid="stCustomComponentV1"] > iframe {
  width: 100% !important;
  max-width: 100% !important;
  display: block !important;
  margin: 0 auto !important;
}

[data-testid="stVerticalBlock"] {
  gap: 0 !important;
}

[data-testid="stAppViewContainer"] {
  overflow-x: hidden !important;
  width: 100% !important;
}

[data-testid="stAppViewContainer"]:not(.light-theme) {
  background:
    radial-gradient(ellipse 60% 50% at 0% 10%,   rgba(0, 212, 255, 0.20)  0%, transparent 60%),
    radial-gradient(ellipse 55% 60% at 100% 90%,  rgba(168, 85, 247, 0.22) 0%, transparent 60%),
    radial-gradient(ellipse 40% 35% at 85% 5%,   rgba(0, 212, 255, 0.10)  0%, transparent 55%),
    radial-gradient(ellipse 35% 30% at 15% 95%,  rgba(16, 185, 129, 0.08) 0%, transparent 55%),
    radial-gradient(ellipse 30% 25% at 50% 48%,  rgba(217, 70, 239, 0.07) 0%, transparent 55%),
    #000000 !important;
  min-height: 100vh !important;
}

/* ── Background ambient lights ────────────────────────────── */
body:not(.light-theme)::before {
  content: '';
  position: fixed;
  inset: 0;
  background:
    radial-gradient(ellipse 55% 45% at 5% 15%,  rgba(0, 212, 255, 0.10) 0%, transparent 70%),
    radial-gradient(ellipse 50% 55% at 92% 80%,  rgba(168, 85, 247, 0.12) 0%, transparent 70%),
    radial-gradient(ellipse 40% 40% at 50% 50%,  rgba(217, 70, 239, 0.05) 0%, transparent 70%),
    radial-gradient(ellipse 35% 30% at 80% 10%,  rgba(0, 212, 255, 0.06) 0%, transparent 70%),
    radial-gradient(ellipse 30% 25% at 15% 85%,  rgba(16, 185, 129, 0.05) 0%, transparent 70%);
  pointer-events: none;
  z-index: 0;
}

/* ── Fixed navigation bar / Icon panel ─────────────────────── */
.navbar {
  position: fixed !important;
  top: 0 !important;
  left: 0 !important;
  right: 0 !important;
  width: 100vw !important;
  max-width: 100% !important;
  height: 64px !important;
  z-index: 999999 !important;
  background: rgba(0, 0, 0, 0.88) !important;
  backdrop-filter: blur(24px) saturate(180%) !important;
  -webkit-backdrop-filter: blur(24px) saturate(180%) !important;
  border-bottom: 1px solid rgba(0, 212, 255, 0.12) !important;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.7), 0 0 15px rgba(0, 212, 255, 0.04) !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  padding: 0 !important;
  margin: 0 !important;
  animation: slideDown 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
}
@keyframes slideDown {
  from { transform: translateY(-100%); opacity: 0; }
  to   { transform: translateY(0);     opacity: 1; }
}

.nav-container {
  width: 100% !important;
  max-width: 1400px !important;
  padding: 0 28px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  height: 100% !important;
  gap: 16px !important;
}

.nav-logo {
  font-family: var(--font-mono);
  font-size: 1.15rem;
  font-weight: 800;
  background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -0.5px;
  text-decoration: none !important;
  display: inline-flex;
  align-items: center;
  transition: transform 0.25s ease;
  flex-shrink: 0;
}
.nav-logo:hover {
  transform: scale(1.08);
}

.nav-links {
  display: flex !important;
  align-items: center !important;
  gap: 4px !important;
  list-style: none !important;
  margin: 0 !important;
  padding: 4px 6px !important;
  background: rgba(255, 255, 255, 0.03) !important;
  border: 1px solid rgba(255, 255, 255, 0.08) !important;
  border-radius: 50px !important;
  backdrop-filter: blur(12px) !important;
  -webkit-backdrop-filter: blur(12px) !important;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2) !important;
}

.nav-links li {
  display: flex !important;
  margin: 0 !important;
  padding: 0 !important;
}

.nav-links a {
  display: inline-flex !important;
  align-items: center !important;
  gap: 7px !important;
  padding: 6px 14px !important;
  border-radius: 50px !important;
  color: var(--text-secondary) !important;
  text-decoration: none !important;
  font-size: 0.84rem !important;
  font-weight: 500 !important;
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
  letter-spacing: 0.2px !important;
  border: 1px solid transparent !important;
  cursor: pointer !important;
  white-space: nowrap !important;
}

.nav-links a .nav-icon {
  font-size: 0.95rem !important;
  transition: transform 0.25s ease !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  line-height: 1 !important;
}

.nav-links a:hover {
  color: #ffffff !important;
  background: rgba(0, 212, 255, 0.08) !important;
  border-color: rgba(0, 212, 255, 0.25) !important;
  transform: translateY(-1px) !important;
}
.nav-links a:hover .nav-icon {
  transform: scale(1.15) !important;
}

.nav-links a.nav-active {
  color: #ffffff !important;
  background: linear-gradient(135deg, rgba(0, 212, 255, 0.22), rgba(168, 85, 247, 0.22)) !important;
  border: 1px solid rgba(0, 212, 255, 0.45) !important;
  box-shadow: 0 0 16px rgba(0, 212, 255, 0.25) !important;
  font-weight: 600 !important;
}
.nav-links a.nav-active .nav-icon {
  transform: scale(1.1) !important;
}

.nav-actions {
  display: flex !important;
  align-items: center !important;
  gap: 10px !important;
  flex-shrink: 0;
}

.nav-admin-btn {
  padding: 7px 16px !important;
  border-radius: 50px !important;
  background: linear-gradient(135deg, rgba(99,102,241,0.15), rgba(168,85,247,0.15)) !important;
  color: #c4b5fd !important;
  border: 1px solid rgba(168,85,247,0.3) !important;
  font-size: 0.82rem !important;
  font-weight: 600 !important;
  text-decoration: none !important;
  transition: all 0.25s ease !important;
  display: inline-flex !important;
  align-items: center !important;
  gap: 6px !important;
}
.nav-admin-btn:hover {
  background: linear-gradient(135deg, rgba(99,102,241,0.28), rgba(168,85,247,0.28)) !important;
  border-color: rgba(168,85,247,0.6) !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 0 15px rgba(168, 85, 247, 0.3) !important;
}

@media (max-width: 980px) {
  .nav-links a .nav-text { display: none !important; }
  .nav-links a { padding: 8px 10px !important; }
  .nav-links a .nav-icon { font-size: 1.15rem !important; }
}
@media (max-width: 580px) {
  .nav-container { padding: 0 12px !important; }
  .nav-links { gap: 2px !important; padding: 2px 4px !important; }
  .nav-links a { padding: 6px 8px !important; font-size: 0.95rem !important; }
  .nav-admin-btn .admin-text { display: none !important; }
  .nav-admin-btn { padding: 7px 10px !important; }
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
  --bg-primary: #f1f5f9 !important;
  --bg-secondary: #e2e8f0 !important;
  --bg-card: rgba(255, 255, 255, 0.96) !important;
  --text-primary: #0f172a !important;
  --text-secondary: #334155 !important;
  --text-muted: #64748b !important;
  --border-subtle: rgba(0, 0, 0, 0.08) !important;
  background-color: #f1f5f9 !important;
  background: radial-gradient(ellipse 70% 50% at 5% 15%, rgba(0, 212, 255, 0.12) 0%, transparent 70%),
              radial-gradient(ellipse 60% 60% at 95% 45%, rgba(168, 85, 247, 0.12) 0%, transparent 70%),
              radial-gradient(ellipse 70% 60% at 50% 90%, rgba(16, 185, 129, 0.08) 0%, transparent 70%),
              #f1f5f9 !important;
  color: #0f172a !important;
}

body.light-theme::before {
  background:
    radial-gradient(circle 800px at 10% 20%, rgba(0, 212, 255, 0.08) 0%, transparent 70%),
    radial-gradient(circle 800px at 90% 80%, rgba(168, 85, 247, 0.08) 0%, transparent 70%) !important;
}

.light-theme .navbar {
  background: rgba(255, 255, 255, 0.92) !important;
  border-bottom: 1.5px solid rgba(0, 212, 255, 0.25) !important;
  box-shadow: 0 8px 32px rgba(2, 132, 199, 0.12), 0 2px 8px rgba(0, 0, 0, 0.04) !important;
}

.light-theme .nav-logo {
  background: linear-gradient(135deg, #0284c7, #7e22ce) !important;
  -webkit-background-clip: text !important;
  -webkit-text-fill-color: transparent !important;
}

.light-theme .nav-links {
  background: rgba(255, 255, 255, 0.85) !important;
  border: 1px solid rgba(0, 212, 255, 0.25) !important;
  box-shadow: 0 4px 20px rgba(2, 132, 199, 0.08) !important;
}

.light-theme .nav-links a {
  color: #334155 !important;
}
.light-theme .nav-links a:hover {
  color: #0284c7 !important;
  background: rgba(2, 132, 199, 0.1) !important;
  border-color: rgba(2, 132, 199, 0.35) !important;
}
.light-theme .nav-links a.nav-active {
  color: #ffffff !important;
  background: linear-gradient(135deg, #0284c7, #7e22ce) !important;
  border-color: transparent !important;
  box-shadow: 0 4px 15px rgba(2, 132, 199, 0.35) !important;
  font-weight: 700 !important;
}

.light-theme .theme-toggle-btn {
  background: rgba(255, 255, 255, 0.9) !important;
  border-color: rgba(0, 212, 255, 0.35) !important;
  color: #0f172a !important;
  box-shadow: 0 4px 15px rgba(2, 132, 199, 0.15) !important;
}
.light-theme .theme-toggle-btn:hover {
  background: rgba(2, 132, 199, 0.15) !important;
  border-color: #0284c7 !important;
  box-shadow: 0 0 20px rgba(2, 132, 199, 0.35) !important;
}

.light-theme .nav-admin-btn {
  background: linear-gradient(135deg, rgba(99,102,241,0.12), rgba(168,85,247,0.12)) !important;
  color: #7e22ce !important;
  border-color: rgba(168,85,247,0.4) !important;
  box-shadow: 0 4px 15px rgba(126, 34, 206, 0.12) !important;
}
.light-theme .nav-admin-btn:hover {
  background: linear-gradient(135deg, rgba(99,102,241,0.22), rgba(168,85,247,0.22)) !important;
  border-color: #7e22ce !important;
  box-shadow: 0 6px 20px rgba(126, 34, 206, 0.25) !important;
}

.light-theme .section-title {
  background: linear-gradient(135deg, #0f172a 0%, #0284c7 100%) !important;
  -webkit-background-clip: text !important;
  -webkit-text-fill-color: transparent !important;
}
.light-theme .section-subtitle {
  color: #475569 !important;
}
.light-theme .section-sep {
  border-top: 1.5px solid rgba(0, 212, 255, 0.15) !important;
}

.light-theme .about-profile-card-3d {
  background: linear-gradient(145deg, rgba(255, 255, 255, 0.98), rgba(240, 249, 255, 0.94)) !important;
  border: 1.5px solid rgba(0, 212, 255, 0.35) !important;
  box-shadow: 0 15px 35px rgba(0, 212, 255, 0.14), 0 5px 15px rgba(0, 0, 0, 0.05), inset 0 1px 0 rgba(255, 255, 255, 1) !important;
}
.light-theme .who-i-am-card-3d {
  background: linear-gradient(145deg, rgba(255, 255, 255, 0.98), rgba(245, 243, 255, 0.94)) !important;
  border: 1.5px solid rgba(168, 85, 247, 0.32) !important;
  box-shadow: 0 15px 35px rgba(168, 85, 247, 0.12), 0 5px 15px rgba(0, 0, 0, 0.04) !important;
}
.light-theme .edu-card-3d {
  background: linear-gradient(145deg, rgba(255, 255, 255, 0.98), rgba(238, 242, 255, 0.94)) !important;
  border: 1.5px solid rgba(99, 102, 241, 0.32) !important;
  box-shadow: 0 12px 30px rgba(99, 102, 241, 0.12) !important;
}
.light-theme .skill-card-img2 {
  background: linear-gradient(145deg, rgba(255, 255, 255, 0.98), rgba(248, 250, 252, 0.94)) !important;
  border: 1.5px solid rgba(0, 212, 255, 0.28) !important;
  box-shadow: 0 12px 30px rgba(2, 132, 199, 0.1) !important;
}
.light-theme .project-card-3d {
  background: linear-gradient(145deg, rgba(255, 255, 255, 0.98), rgba(248, 250, 252, 0.94)) !important;
  border: 1.5px solid rgba(0, 212, 255, 0.32) !important;
  box-shadow: 0 15px 35px rgba(2, 132, 199, 0.12) !important;
}
.light-theme .tl-card-3d {
  background: linear-gradient(145deg, rgba(255, 255, 255, 0.98), rgba(240, 249, 255, 0.94)) !important;
  border: 1.5px solid rgba(0, 212, 255, 0.35) !important;
  box-shadow: 0 15px 35px rgba(0, 212, 255, 0.14), 0 5px 15px rgba(0,0,0,0.05) !important;
}
.light-theme .tl-card-3d:hover {
  transform: translateX(8px) !important;
  border-color: #00d4ff !important;
  box-shadow: 0 20px 45px rgba(0, 212, 255, 0.25), 0 0 25px rgba(0, 212, 255, 0.2) !important;
}
.light-theme .cert-card-3d {
  background: linear-gradient(145deg, rgba(255, 255, 255, 0.98), rgba(250, 245, 255, 0.94)) !important;
  border: 1.5px solid rgba(168, 85, 247, 0.35) !important;
  box-shadow: 0 15px 35px rgba(168, 85, 247, 0.16), 0 5px 15px rgba(0,0,0,0.05) !important;
}
.light-theme .cert-card-3d:hover {
  border-color: #a855f7 !important;
  box-shadow: 0 22px 48px rgba(168, 85, 247, 0.28), 0 0 25px rgba(168, 85, 247, 0.25) !important;
}
.light-theme .contact-info-card-3d {
  background: linear-gradient(145deg, rgba(255, 255, 255, 0.98), rgba(240, 253, 250, 0.94)) !important;
  border: 1.5px solid rgba(16, 185, 129, 0.35) !important;
  box-shadow: 0 15px 35px rgba(16, 185, 129, 0.14), 0 5px 15px rgba(0,0,0,0.05) !important;
}

.light-theme .portfolio-footer {
  background: linear-gradient(145deg, rgba(255, 255, 255, 0.98), rgba(245, 243, 255, 0.95)) !important;
  border-top: 2px solid rgba(0, 212, 255, 0.25) !important;
  box-shadow: 0 -15px 40px rgba(2, 132, 199, 0.08) !important;
  color: #334155 !important;
}
.light-theme .portfolio-footer a {
  color: #475569 !important;
}
.light-theme .portfolio-footer a:hover {
  color: #0284c7 !important;
}
.light-theme .portfolio-footer div {
  color: #475569 !important;
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
.light-theme .tl-desc-preview,
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
  background: linear-gradient(135deg, rgba(0, 212, 255, 0.12), rgba(168, 85, 247, 0.12)) !important;
  border: 1.5px solid rgba(0, 212, 255, 0.4) !important;
  color: #0284c7 !important;
  box-shadow: 0 4px 15px rgba(0, 212, 255, 0.12) !important;
}

.light-theme .interest-pill-3d,
.light-theme .social-btn-3d,
.light-theme .social-icon-btn-3d,
.light-theme .skill-pill-img2,
.light-theme .proj-btn-gh-3d {
  background: #ffffff !important;
  color: #0f172a !important;
  border: 1.5px solid rgba(0, 212, 255, 0.28) !important;
  box-shadow: 0 4px 14px rgba(0, 212, 255, 0.1) !important;
}

.light-theme [data-testid="stTextInput"] label,
.light-theme [data-testid="stTextArea"] label,
.light-theme [data-testid="stSelectbox"] label,
.light-theme [data-testid="stWidgetLabel"] {
  color: #0f172a !important;
  font-weight: 700 !important;
}

.light-theme [data-testid="stTextInput"] input,
.light-theme [data-testid="stTextArea"] textarea,
.light-theme [data-testid="stSelectbox"] select {
  background-color: #ffffff !important;
  border: 1.5px solid rgba(0, 212, 255, 0.3) !important;
  color: #0f172a !important;
  box-shadow: 0 4px 15px rgba(2, 132, 199, 0.06) !important;
}
.light-theme [data-testid="stTextInput"] input:focus,
.light-theme [data-testid="stTextArea"] textarea:focus {
  border-color: #0284c7 !important;
  box-shadow: 0 0 0 3px rgba(2, 132, 199, 0.25) !important;
}

.light-theme [data-testid="stTextInput"] input::placeholder,
.light-theme [data-testid="stTextArea"] textarea::placeholder {
  color: #94a3b8 !important;
}

.light-theme [data-testid="stRadio"] label {
  color: #334155 !important;
}
.light-theme [data-testid="stExpander"] {
  background: #ffffff !important;
  border: 1.5px solid rgba(0, 212, 255, 0.25) !important;
  box-shadow: 0 8px 25px rgba(2, 132, 199, 0.08) !important;
}

/* ── Premium Stacking & Layering (Apple Parallax Effect) ── */
#home {
  position: relative;
  z-index: 1;
}

#about, #skills, #projects, #experience, #certificates, #contact {
  position: relative;
  z-index: 10;
}

/* Card 3D perspective enhancements */
.project-card-3d,
.about-profile-card-3d,
.about-details-card-3d,
.skill-card-3d,
.cert-card-3d,
.timeline-card-3d,
.contact-card-3d,
.contact-form-3d {
  position: relative;
  transform-style: preserve-3d;
  will-change: transform, box-shadow;
}

.card-specular-sheen {
  position: absolute;
  inset: 0;
  border-radius: inherit;
  pointer-events: none;
  z-index: 5;
  mix-blend-mode: overlay;
  opacity: 0;
  transition: opacity 0.25s ease;
}
"""


# ═══════════════════════════════════════════════════════════════════════════════
# NAVIGATION HTML (Fixed Icon Panel)
# ═══════════════════════════════════════════════════════════════════════════════
NAV_HTML = """
<nav class="navbar" id="main-navbar">
  <div class="nav-container">
    <a class="nav-logo" href="#home" data-target="home" title="Back to top">
      <span>KG</span>
    </a>
    <ul class="nav-links" id="navbar-nav-links">
      <li><a href="#home" class="nav-active" data-target="home"><span class="nav-icon">🏠</span><span class="nav-text">Home</span></a></li>
      <li><a href="#about" data-target="about"><span class="nav-icon">👤</span><span class="nav-text">About</span></a></li>
      <li><a href="#skills" data-target="skills"><span class="nav-icon">⚡</span><span class="nav-text">Skills</span></a></li>
      <li><a href="#projects" data-target="projects"><span class="nav-icon">💻</span><span class="nav-text">Projects</span></a></li>
      <li><a href="#experience" data-target="experience"><span class="nav-icon">💼</span><span class="nav-text">Experience</span></a></li>
      <li><a href="#certificates" data-target="certificates"><span class="nav-icon">📜</span><span class="nav-text">Certificates</span></a></li>
      <li><a href="#contact" data-target="contact"><span class="nav-icon">📬</span><span class="nav-text">Contact</span></a></li>
    </ul>
    <div class="nav-actions">
      <button id="theme-toggle-btn" class="theme-toggle-btn" title="Toggle Light/Dark Theme">
        <span id="theme-toggle-icon">🌙</span>
      </button>
      <a href="?admin=true" class="nav-admin-btn">&#128100; <span class="admin-text">Admin</span></a>
    </div>
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
    padding: 24px 40px;
    margin-top: 60px;
    border-radius: 24px 24px 0 0;
    box-shadow: 0 -10px 30px rgba(0,0,0,0.4), 0 0 20px rgba(0,212,255,0.08);
    position: relative;
    z-index: 10;
">
    <div style="
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 12px;
        max-width: 1400px;
        margin: 0 auto;
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

        # Cinematic Intro Preloader Overlay
        render_preloader()

        # Background ambient music player (floating pill button, bottom-right)
        render_music_player()

        # Fixed Navbar / Icon Panel
        inject_html(NAV_HTML)

        # Theme sync, smooth scroll, and ScrollSpy engine
        components.html("""
        <script>
        (function initPortfolioEngine() {
          var DARK_BG = [
            'radial-gradient(ellipse 60% 50% at 0% 10%,   rgba(0, 212, 255, 0.20)  0%, transparent 60%)',
            'radial-gradient(ellipse 55% 60% at 100% 90%,  rgba(168, 85, 247, 0.22) 0%, transparent 60%)',
            'radial-gradient(ellipse 40% 35% at 85% 5%,   rgba(0, 212, 255, 0.10)  0%, transparent 55%)',
            'radial-gradient(ellipse 35% 30% at 15% 95%,  rgba(16, 185, 129, 0.08) 0%, transparent 55%)',
            'radial-gradient(ellipse 30% 25% at 50% 48%,  rgba(217, 70, 239, 0.07) 0%, transparent 55%)',
            '#000000'
          ].join(', ');

          var LIGHT_BG = [
            'radial-gradient(ellipse 70% 50% at 5% 15%, rgba(0, 212, 255, 0.14) 0%, transparent 70%)',
            'radial-gradient(ellipse 60% 60% at 95% 45%, rgba(168, 85, 247, 0.14) 0%, transparent 70%)',
            'radial-gradient(ellipse 70% 60% at 50% 90%, rgba(16, 185, 129, 0.10) 0%, transparent 70%)',
            '#f1f5f9'
          ].join(', ');

          function applyBg(pDoc, isLight) {
            var targets = [
              pDoc.body,
              pDoc.documentElement,
              pDoc.querySelector('[data-testid="stAppViewContainer"]'),
              pDoc.querySelector('.stApp'),
              pDoc.querySelector('section.main'),
              pDoc.querySelector('[data-testid="stMain"]')
            ];
            targets.forEach(function(el) {
              if (el) {
                if (isLight) {
                  el.style.setProperty('background', LIGHT_BG, 'important');
                  el.style.setProperty('background-color', '#f1f5f9', 'important');
                  el.style.setProperty('color', '#0f172a', 'important');
                } else {
                  el.style.setProperty('background', DARK_BG, 'important');
                  el.style.setProperty('background-color', '#000000', 'important');
                  el.style.setProperty('color', '#e2e8f0', 'important');
                }
              }
            });
          }

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
                applyBg(pDoc, isLight);
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

          function scrollToTop(pDoc) {
            try {
              var targets = [
                pDoc.querySelector('[data-testid="stAppViewContainer"]'),
                pDoc.querySelector('.stApp'),
                pDoc.querySelector('section.main'),
                pDoc.querySelector('[data-testid="stMain"]'),
                pDoc.documentElement,
                pDoc.body
              ];
              targets.forEach(function(el) {
                if (el) {
                  try { el.scrollTo({ top: 0, left: 0, behavior: 'smooth' }); } catch(e) {}
                  try { el.scrollTop = 0; } catch(e) {}
                }
              });
              try { if (window.parent && window.parent.scrollTo) window.parent.scrollTo({ top: 0, left: 0, behavior: 'smooth' }); } catch(e) {}
              try { window.scrollTo({ top: 0, left: 0, behavior: 'smooth' }); } catch(e) {}
              
              var h = pDoc.getElementById('home');
              if (h && h.scrollIntoView) {
                h.scrollIntoView({ behavior: 'smooth', block: 'start' });
              }
            } catch(err) {
              console.error("Scroll to top error:", err);
            }
          }

          function setupNavLinksAndScrollSpy() {
            try {
              if (window.parent && window.parent.document) {
                const pDoc = window.parent.document;
                const links = pDoc.querySelectorAll('.navbar .nav-links a, .portfolio-footer a[data-target], .navbar .nav-logo');
                const scrollContainer = pDoc.querySelector('[data-testid="stAppViewContainer"]') || window.parent;

                links.forEach(link => {
                  if (!link._boundClick) {
                    link._boundClick = true;
                    link.addEventListener('click', function(e) {
                      e.preventDefault();
                      e.stopPropagation();
                      const targetId = this.getAttribute('data-target') || (this.getAttribute('href') || '').replace('#', '');
                      
                      if (targetId === 'home' || !targetId) {
                        scrollToTop(pDoc);
                      } else {
                        const targetEl = pDoc.getElementById(targetId);
                        if (targetEl) {
                          targetEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
                        }
                      }

                      const navLinks = pDoc.querySelectorAll('.navbar .nav-links a');
                      navLinks.forEach(l => {
                        const tid = l.getAttribute('data-target') || (l.getAttribute('href') || '').replace('#', '');
                        if ((targetId === 'home' && tid === 'home') || (tid === targetId)) {
                          l.classList.add('nav-active');
                        } else {
                          l.classList.remove('nav-active');
                        }
                      });
                    });
                  }
                });

                // ScrollSpy observer
                if (scrollContainer && !scrollContainer.dataset.spyBound) {
                  scrollContainer.dataset.spyBound = 'true';
                  const sections = ['contact', 'certificates', 'experience', 'projects', 'skills', 'about', 'home'];
                  
                  function updateActiveNav() {
                    let activeId = '';
                    for (let i = 0; i < sections.length; i++) {
                      const secId = sections[i];
                      const el = pDoc.getElementById(secId);
                      if (el) {
                        const rect = el.getBoundingClientRect();
                        if (rect.top <= 200) {
                          activeId = secId;
                          break;
                        }
                      }
                    }
                    if (!activeId) activeId = 'home';
                    const navLinks = pDoc.querySelectorAll('.navbar .nav-links a');
                    navLinks.forEach(l => {
                      const tid = l.getAttribute('data-target') || (l.getAttribute('href') || '').replace('#', '');
                      if (tid === activeId) l.classList.add('nav-active');
                      else l.classList.remove('nav-active');
                    });
                  }

                  if (scrollContainer.addEventListener) {
                    scrollContainer.addEventListener('scroll', updateActiveNav, { passive: true });
                  }
                  if (window.parent && window.parent.addEventListener) {
                    window.parent.addEventListener('scroll', updateActiveNav, { passive: true });
                  }
                }
              }
            } catch(e) {}
          }

          /* ── 1. 3D Scroll Parallax & Hero Stacking (Apple Keynote Effect) ── */
          function setup3DScrollParallax(pDoc) {
            try {
              if (pDoc._parallaxBound) return;
              pDoc._parallaxBound = true;

              function getScroll() {
                let y = 0;
                if (window.parent && typeof window.parent.pageYOffset !== 'undefined') y = Math.max(y, window.parent.pageYOffset);
                if (window.pageYOffset) y = Math.max(y, window.pageYOffset);
                if (pDoc.documentElement && pDoc.documentElement.scrollTop) y = Math.max(y, pDoc.documentElement.scrollTop);
                if (pDoc.body && pDoc.body.scrollTop) y = Math.max(y, pDoc.body.scrollTop);
                const sc = pDoc.querySelector('[data-testid="stAppViewContainer"]');
                if (sc && sc.scrollTop) y = Math.max(y, sc.scrollTop);
                return y;
              }

              function updateParallax() {
                const scrollY = getScroll();
                const iframes = pDoc.querySelectorAll('iframe');
                let heroIframe = null;
                iframes.forEach(f => {
                  if (f.offsetHeight >= 400 || (f.parentElement && f.parentElement.offsetHeight >= 400)) {
                    heroIframe = f;
                  }
                });

                if (heroIframe) {
                  if (scrollY < 900) {
                    const scale = Math.max(0.84, 1 - (scrollY * 0.00035));
                    const translateY = scrollY * 0.42;
                    const opacity = Math.max(0.05, 1 - (scrollY * 0.0016));
                    const blur = Math.min(12, scrollY * 0.016);
                    heroIframe.style.setProperty('transform', `translateY(${translateY.toFixed(1)}px) scale(${scale.toFixed(4)})`, 'important');
                    heroIframe.style.setProperty('opacity', `${opacity.toFixed(3)}`, 'important');
                    heroIframe.style.setProperty('filter', `blur(${blur.toFixed(1)}px)`, 'important');
                    heroIframe.style.setProperty('transform-origin', 'center top', 'important');
                    heroIframe.style.setProperty('will-change', 'transform, opacity, filter', 'important');

                    try {
                      heroIframe.contentWindow.postMessage({ type: 'HERO_SCROLL', scrollY: scrollY }, '*');
                    } catch(err) {}
                  } else {
                    heroIframe.style.setProperty('opacity', '0', 'important');
                  }
                }
              }

              const scrollTargets = [
                window,
                window.parent,
                pDoc,
                pDoc.querySelector('[data-testid="stAppViewContainer"]'),
                pDoc.querySelector('section.main'),
                pDoc.querySelector('[data-testid="stMain"]')
              ];
              scrollTargets.forEach(t => {
                if (t && t.addEventListener) {
                  t.addEventListener('scroll', updateParallax, { passive: true });
                }
              });
              setInterval(updateParallax, 50);
            } catch(e) {}
          }

          /* ── 2. 3D Magnetic Card Tilt & Specular Light Sheen ── */
          function setup3DCardTilt(pDoc) {
            try {
              if (pDoc._tiltEngineBound) return;
              pDoc._tiltEngineBound = true;

              const SELECTORS = '.project-card-3d, .about-profile-card-3d, .who-i-am-card-3d, .edu-card-3d, .skill-card-img2, .cert-card-3d, .tl-card-3d, .contact-card-3d, .contact-form-3d';

              pDoc.addEventListener('mousemove', function(e) {
                const card = e.target.closest(SELECTORS);
                if (card) {
                  const r = card.getBoundingClientRect();
                  const x = e.clientX - r.left;
                  const y = e.clientY - r.top;
                  const rx = ((y - r.height/2) / (r.height/2)) * -9;
                  const ry = ((x - r.width/2) / (r.width/2)) * 9;
                  
                  card.style.setProperty('transform', `perspective(1000px) rotateX(${rx.toFixed(2)}deg) rotateY(${ry.toFixed(2)}deg) translateY(-6px) scale3d(1.025, 1.025, 1.025)`, 'important');
                  card.style.setProperty('box-shadow', '0 25px 60px rgba(0, 212, 255, 0.22), 0 0 35px rgba(168, 85, 247, 0.18)', 'important');
                  card.style.setProperty('transition', 'transform 0.1s ease-out, box-shadow 0.2s ease', 'important');

                  let sheen = card.querySelector('.card-specular-sheen');
                  if (!sheen) {
                    sheen = pDoc.createElement('div');
                    sheen.className = 'card-specular-sheen';
                    sheen.style.cssText = 'position:absolute;inset:0;border-radius:inherit;pointer-events:none;z-index:10;mix-blend-mode:overlay;transition:opacity 0.2s ease;';
                    card.style.position = 'relative';
                    card.appendChild(sheen);
                  }
                  sheen.style.background = `radial-gradient(circle 260px at ${x}px ${y}px, rgba(255,255,255,0.35), transparent 70%)`;
                  sheen.style.opacity = '1';
                }
              }, { passive: true });

              pDoc.addEventListener('mouseout', function(e) {
                const card = e.target.closest(SELECTORS);
                if (card && (!e.relatedTarget || !card.contains(e.relatedTarget))) {
                  card.style.setProperty('transform', 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateY(0px) scale3d(1, 1, 1)', 'important');
                  card.style.setProperty('box-shadow', '', '');
                  card.style.setProperty('transition', 'transform 0.4s ease, box-shadow 0.4s ease', 'important');
                  const sheen = card.querySelector('.card-specular-sheen');
                  if (sheen) sheen.style.opacity = '0';
                }
              }, { passive: true });
            } catch(e) {}
          }

          /* ── 3. Fluid Glowing Neon Cursor Aura ── */
          function setupFluidCursor(pDoc) {
            try {
              if (pDoc.getElementById('portfolio-cursor-aura')) return;

              const aura = pDoc.createElement('div');
              aura.id = 'portfolio-cursor-aura';
              aura.innerHTML = `
                <style>
                  #portfolio-cursor-aura {
                    position: fixed !important;
                    top: 0 !important; left: 0 !important;
                    width: 36px !important; height: 36px !important;
                    margin-top: -18px !important; margin-left: -18px !important;
                    border-radius: 50% !important;
                    pointer-events: none !important;
                    z-index: 9999999999 !important;
                    border: 1.5px solid #00d4ff !important;
                    background: radial-gradient(circle, rgba(0, 212, 255, 0.22) 0%, rgba(168, 85, 247, 0.12) 60%, transparent 80%) !important;
                    box-shadow: 0 0 20px rgba(0, 212, 255, 0.6), inset 0 0 10px rgba(168, 85, 247, 0.4) !important;
                    transition: width 0.25s cubic-bezier(0.16, 1, 0.3, 1), height 0.25s cubic-bezier(0.16, 1, 0.3, 1), margin 0.25s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.2s ease, background 0.2s ease, opacity 0.3s ease !important;
                    opacity: 0 !important;
                    backdrop-filter: blur(2px) !important;
                    -webkit-backdrop-filter: blur(2px) !important;
                  }
                  #portfolio-cursor-dot {
                    position: fixed !important;
                    top: 0 !important; left: 0 !important;
                    width: 8px !important; height: 8px !important;
                    margin-top: -4px !important; margin-left: -4px !important;
                    border-radius: 50% !important;
                    pointer-events: none !important;
                    z-index: 99999999999 !important;
                    background: #00d4ff !important;
                    box-shadow: 0 0 14px #00d4ff, 0 0 6px #ffffff !important;
                    opacity: 0 !important;
                  }
                  #portfolio-cursor-aura.cursor-hover {
                    width: 64px !important; height: 64px !important;
                    margin-top: -32px !important; margin-left: -32px !important;
                    border-color: #a855f7 !important;
                    background: radial-gradient(circle, rgba(168, 85, 247, 0.32) 0%, rgba(0, 212, 255, 0.25) 60%, transparent 80%) !important;
                    box-shadow: 0 0 35px rgba(168, 85, 247, 0.8) !important;
                  }
                  @media (hover: none), (max-width: 768px) {
                    #portfolio-cursor-aura, #portfolio-cursor-dot { display: none !important; }
                  }
                </style>
              `;
              const dot = pDoc.createElement('div');
              dot.id = 'portfolio-cursor-dot';

              pDoc.body.appendChild(aura);
              pDoc.body.appendChild(dot);

              let mx = -100, my = -100;
              let ax = -100, ay = -100;

              function handleMove(e) {
                mx = e.clientX;
                my = e.clientY;
                aura.style.setProperty('opacity', '1', 'important');
                dot.style.setProperty('opacity', '1', 'important');
                dot.style.setProperty('transform', `translate3d(${mx}px, ${my}px, 0)`, 'important');
              }

              pDoc.addEventListener('mousemove', handleMove, { passive: true });
              window.addEventListener('mousemove', handleMove, { passive: true });

              pDoc.addEventListener('mouseleave', function() {
                aura.style.setProperty('opacity', '0', 'important');
                dot.style.setProperty('opacity', '0', 'important');
              });

              function loopCursor() {
                ax += (mx - ax) * 0.20;
                ay += (my - ay) * 0.20;
                aura.style.setProperty('transform', `translate3d(${ax.toFixed(2)}px, ${ay.toFixed(2)}px, 0)`, 'important');
                requestAnimationFrame(loopCursor);
              }
              loopCursor();

              pDoc.addEventListener('mouseover', function(e) {
                const target = e.target.closest('a, button, input, textarea, select, .project-card-3d, .about-profile-card-3d, .who-i-am-card-3d, .edu-card-3d, .skill-card-img2, .cert-card-3d, .tl-card-3d, .spec-card, #lamp-rope-trigger, .theme-toggle-btn');
                if (target) {
                  aura.classList.add('cursor-hover');
                } else {
                  aura.classList.remove('cursor-hover');
                }
              }, { passive: true });
            } catch(e) {}
          }

          /* ── 4. Rolling Number Counters ── */
          function setupAnimatedCounters(pDoc) {
            try {
              const counterEls = pDoc.querySelectorAll('.stat-val, .stat-num, [data-counter-val]');
              if (window.IntersectionObserver) {
                const observer = new IntersectionObserver((entries) => {
                  entries.forEach(entry => {
                    if (entry.isIntersecting) {
                      const el = entry.target;
                      if (el._counted) return;
                      el._counted = true;

                      const text = el.textContent.trim();
                      const match = text.match(/^([0-9.]+)(.*)$/);
                      if (match) {
                        const targetNum = parseFloat(match[1]);
                        const suffix = match[2] || '';
                        const isFloat = match[1].includes('.');
                        const decimals = isFloat ? (match[1].split('.')[1] || '').length : 0;
                        const duration = 1600;
                        const startTime = performance.now();

                        function updateCounter(now) {
                          const elapsed = now - startTime;
                          const progress = Math.min(1, elapsed / duration);
                          const eased = progress === 1 ? 1 : 1 - Math.pow(2, -10 * progress);
                          const cur = targetNum * eased;
                          el.textContent = cur.toFixed(decimals) + suffix;

                          if (progress < 1) {
                            requestAnimationFrame(updateCounter);
                          } else {
                            el.textContent = targetNum.toFixed(decimals) + suffix;
                          }
                        }
                        requestAnimationFrame(updateCounter);
                      }
                    }
                  });
                }, { threshold: 0.3 });

                counterEls.forEach(el => observer.observe(el));
              }
            } catch(e) {}
          }

          /* ── 5. Staggered Cascading Scroll Reveals ── */
          function setupScrollReveals(pDoc) {
            try {
              const targets = pDoc.querySelectorAll(`
                .section-header-wrap,
                .about-profile-card-3d,
                .who-i-am-card-3d,
                .edu-card-3d,
                .skill-card-img2,
                .project-card-3d,
                .timeline-item,
                .cert-card-3d,
                .contact-card-3d,
                .contact-form-3d
              `);

              targets.forEach(el => {
                if (!el.classList.contains('reveal-init')) {
                  el.classList.add('reveal-init');
                  el.style.opacity = '0';
                  el.style.transform = 'translateY(28px)';
                  el.style.transition = 'opacity 0.75s cubic-bezier(0.16, 1, 0.3, 1), transform 0.75s cubic-bezier(0.16, 1, 0.3, 1)';
                  el.style.willChange = 'opacity, transform';
                }
              });

              if (window.IntersectionObserver) {
                const observer = new IntersectionObserver((entries) => {
                  entries.forEach(entry => {
                    if (entry.isIntersecting) {
                      const el = entry.target;
                      el.style.opacity = '1';
                      el.style.transform = 'translateY(0)';
                      observer.unobserve(el);
                    }
                  });
                }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

                targets.forEach(el => observer.observe(el));
              }
            } catch(e) {}
          }

          let savedTheme = 'dark';
          try { savedTheme = localStorage.getItem('portfolio-theme') || 'dark'; } catch(e) {}
          applyTheme(savedTheme);

          setInterval(function() {
            if (window.parent && window.parent.document) {
              const pDoc = window.parent.document;
              setupButtonListener();
              setupNavLinksAndScrollSpy();
              setup3DScrollParallax(pDoc);
              setup3DCardTilt(pDoc);
              setupFluidCursor(pDoc);
              setupAnimatedCounters(pDoc);
              setupScrollReveals(pDoc);
            }
            let t = 'dark';
            try { t = localStorage.getItem('portfolio-theme') || 'dark'; } catch(e) {}
            applyTheme(t);
          }, 200);
        })();
        </script>
        """, height=0, width=0)

        # ── Home Anchor ───────────────────────────────────────────────────
        inject_html('<div id="home" style="position:relative;top:-64px;height:1px;width:100%;pointer-events:none;"></div>')

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
