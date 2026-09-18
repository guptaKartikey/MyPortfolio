"""
components/experience.py
========================
Animated vertical 3D timeline for work experience / internships matching img2.jpeg style.
"""

import streamlit as st

from utils.data_manager import load_experience
from utils.helpers import inject_html, is_placeholder


def render_experience():
    """Render the Experience section with 3D glassmorphism timeline."""
    data        = load_experience()
    experiences = data.get("experiences", [])

    css = """
    #experience { scroll-margin-top: 80px; padding-bottom: 50px; position: relative; }

    .exp-header-container {
        position: relative;
        margin-bottom: 35px;
    }

    .exp-badge {
        display: inline-block;
        padding: 5px 16px;
        border-radius: 50px;
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.12);
        color: #94a3b8;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 12px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }

    .exp-title {
        font-size: 2.5rem;
        font-weight: 900;
        color: #ffffff;
        margin-bottom: 8px;
        letter-spacing: -0.5px;
        line-height: 1.1;
    }

    .exp-title-accent {
        background: linear-gradient(135deg, #00d4ff 0%, #10b981 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .exp-subtitle {
        color: #94a3b8;
        font-size: 0.95rem;
        max-width: 580px;
        line-height: 1.6;
    }

    .exp-handwritten {
        position: absolute;
        right: 180px;
        top: 15px;
        font-family: 'Caveat', 'Dancing Script', 'Segoe Script', cursive;
        font-size: 1.45rem;
        color: #10b981;
        transform: rotate(-3deg);
        opacity: 0.9;
        text-shadow: 0 0 10px rgba(16, 185, 129, 0.4);
        letter-spacing: 1px;
    }

    .tl-wrapper-3d {
        position: relative;
        padding: 10px 0 10px 48px;
        border-left: 3px solid;
        border-image: linear-gradient(to bottom, #00d4ff, #a855f7, #10b981) 1;
        margin-left: 20px;
        max-width: 860px;
    }

    .tl-item-3d {
        position: relative;
        margin-bottom: 32px;
    }

    .tl-dot-3d {
        position: absolute;
        left: -64px; top: 18px;
        width: 32px; height: 32px;
        border-radius: 50%;
        background: linear-gradient(135deg, #00d4ff, #a855f7);
        border: 4px solid #0d0e1c;
        box-shadow: 0 0 20px rgba(0,212,255,0.6);
        display: flex; align-items: center; justify-content: center;
        font-size: 0.85rem; z-index: 2;
    }

    .tl-card-3d {
        background: rgba(13, 14, 28, 0.75);
        border: 1.5px solid rgba(0, 212, 255, 0.2);
        border-radius: 22px; padding: 24px;
        backdrop-filter: blur(16px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4), 0 0 20px rgba(0, 212, 255, 0.1);
        transition: transform 0.35s ease, border-color 0.35s ease, box-shadow 0.35s ease;
    }
    .tl-card-3d:hover {
        transform: translateX(8px);
        border-color: rgba(0,212,255,0.45);
        box-shadow: 0 14px 40px rgba(0, 0, 0, 0.5), 0 0 30px rgba(0, 212, 255, 0.2);
    }

    .tl-top {
        display: flex; justify-content: space-between;
        align-items: flex-start; flex-wrap: wrap; gap: 10px;
        margin-bottom: 12px;
    }
    .tl-org-role  { display: flex; flex-direction: column; gap: 4px; }
    .tl-org       { font-size: 1.15rem; font-weight: 800; color: #f8fafc; }
    .tl-role      { font-size: 0.9rem; color: #00d4ff; font-weight: 600; }
    .tl-type-badge {
        padding: 3px 12px; border-radius: 50px;
        font-size: 0.7rem; font-weight: 700;
        background: rgba(168,85,247,0.18); color: #c084fc;
        border: 1px solid rgba(168,85,247,0.3); margin-left: 8px;
    }
    .tl-duration {
        padding: 5px 15px; border-radius: 50px;
        font-size: 0.75rem; font-weight: 700;
        background: rgba(0,212,255,0.12); color: #00d4ff;
        border: 1px solid rgba(0,212,255,0.25); white-space: nowrap;
    }
    .tl-desc {
        font-size: 0.88rem; color: #94a3b8;
        line-height: 1.7; margin-bottom: 16px;
    }
    .tl-techs { display: flex; flex-wrap: wrap; gap: 7px; margin-bottom: 12px; }
    .tl-tech {
        padding: 4px 12px; border-radius: 50px;
        font-size: 0.74rem; font-weight: 600;
        background: rgba(16,185,129,0.1); color: #10b981;
        border: 1px solid rgba(16,185,129,0.25);
    }
    .tl-cert-link {
        font-size: 0.8rem; color: #a855f7; font-weight: 600;
        text-decoration: none; padding: 7px 16px;
        border-radius: 10px; border: 1px solid rgba(168,85,247,0.3);
        background: rgba(168,85,247,0.1);
        display: inline-block; transition: all 0.25s ease;
    }
    .tl-cert-link:hover {
        background: rgba(168,85,247,0.2);
        border-color: rgba(168,85,247,0.6); transform: translateY(-2px);
    }

    @media (max-width: 768px) {
        .exp-handwritten { display: none; }
        .exp-title { font-size: 1.9rem; }
    }

    /* Light Theme Overrides */
    .light-theme .tl-card-3d {
        background: rgba(255, 255, 255, 0.92) !important;
        border-color: rgba(0, 0, 0, 0.1) !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.06) !important;
    }
    .light-theme .exp-title,
    .light-theme .tl-org {
        color: #0f172a !important;
    }
    .light-theme .exp-subtitle,
    .light-theme .tl-desc {
        color: #475569 !important;
    }
    .light-theme .tl-dot-3d {
        border-color: #f8fafc !important;
    }
    .light-theme .exp-badge {
        background: rgba(0, 0, 0, 0.04) !important;
        border-color: rgba(0, 0, 0, 0.12) !important;
        color: #0284c7 !important;
    }
    .light-theme .tl-role,
    .light-theme .tl-duration {
        color: #0284c7 !important;
        background: rgba(0, 212, 255, 0.12) !important;
        border-color: rgba(0, 212, 255, 0.3) !important;
    }
    .light-theme .tl-type-badge {
        color: #7e22ce !important;
        background: rgba(168, 85, 247, 0.12) !important;
        border-color: rgba(168, 85, 247, 0.3) !important;
    }
    .light-theme .tl-tech {
        color: #047857 !important;
        background: rgba(16, 185, 129, 0.1) !important;
        border-color: rgba(16, 185, 129, 0.3) !important;
    }
    .light-theme .exp-handwritten {
        color: #047857 !important;
    }
    """

    inject_html(f"<style>{css}</style>")
    inject_html('<div id="experience"></div>')

    # Header
    header_html = """
    <div class="exp-header-container">
        <div class="exp-badge">CAREER PATH</div>
        <h2 class="exp-title">Work <span class="exp-title-accent">Experience</span></h2>
        <p class="exp-subtitle">My professional journey, software engineering internships, and core technical impact.</p>
        <div class="exp-handwritten">Learn &rarr; Apply &rarr; Impact</div>
    </div>
    """
    inject_html(header_html)

    if not experiences:
        inject_html('<p style="color:#64748b;text-align:center;padding:60px;">No experience entries yet. Add them via the admin panel.</p>')
        return

    # Timeline wrapper
    inject_html('<div class="tl-wrapper-3d">')

    for exp in experiences:
        org      = exp.get("organization", "")
        pos      = exp.get("position", "")
        duration = exp.get("duration", "")
        desc     = exp.get("description", "")
        techs    = exp.get("technologies", [])
        cert_url = exp.get("certificate_url", "")
        etype    = exp.get("type", "Internship")

        dur_txt   = duration if not is_placeholder(duration) else "Duration TBD"
        tech_html = "".join(f'<span class="tl-tech">{t}</span>' for t in techs)
        cert_html = (f'<a href="{cert_url}" target="_blank" class="tl-cert-link">&#127885; View Certificate</a>'
                     if cert_url and not is_placeholder(cert_url) else "")

        inject_html(f"""
        <div class="tl-item-3d">
            <div class="tl-dot-3d">&#128188;</div>
            <div class="tl-card-3d">
                <div class="tl-top">
                    <div class="tl-org-role">
                        <span class="tl-org">{org} <span class="tl-type-badge">{etype}</span></span>
                        <span class="tl-role">{pos}</span>
                    </div>
                    <span class="tl-duration">&#128197; {dur_txt}</span>
                </div>
                <p class="tl-desc">{desc}</p>
                <div class="tl-techs">{tech_html}</div>
                {cert_html}
            </div>
        </div>
        """)

    inject_html('</div>')

