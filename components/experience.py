"""
components/experience.py
========================
Animated vertical 3D timeline for work experience / internships matching img2.jpeg style.
Features interactive popup modal for viewing full descriptions and details on click.
"""

import streamlit as st

from utils.data_manager import load_experience
from utils.helpers import inject_html, is_placeholder


def render_experience():
    """Render the Experience section with 3D glassmorphism timeline and interactive detail modals."""
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
        position: relative;
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
    .tl-desc-preview {
        font-size: 0.88rem; color: #94a3b8;
        line-height: 1.5; margin-bottom: 14px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        display: block;
        cursor: pointer;
        transition: color 0.2s ease;
    }
    .tl-desc-preview:hover {
        color: #00d4ff;
    }
    .tl-techs { display: flex; flex-wrap: wrap; gap: 7px; margin-bottom: 14px; }
    .tl-tech {
        padding: 4px 12px; border-radius: 50px;
        font-size: 0.74rem; font-weight: 600;
        background: rgba(16,185,129,0.1); color: #10b981;
        border: 1px solid rgba(16,185,129,0.25);
    }
    .tl-actions-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 8px;
        padding-top: 10px;
        border-top: 1px solid rgba(255, 255, 255, 0.06);
    }
    .tl-open-btn {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-size: 0.82rem;
        font-weight: 700;
        color: #00d4ff;
        background: rgba(0, 212, 255, 0.1);
        border: 1px solid rgba(0, 212, 255, 0.3);
        padding: 7px 16px;
        border-radius: 12px;
        cursor: pointer;
        transition: all 0.25s ease;
        user-select: none;
    }
    .tl-open-btn:hover {
        background: rgba(0, 212, 255, 0.2);
        border-color: #00d4ff;
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.3);
        transform: translateY(-2px);
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

    /* ── POPUP MODAL STYLES (Pure CSS Modal via Checkbox) ────────── */
    .exp-modal-toggle {
        display: none !important;
    }

    .exp-modal-overlay {
        display: none;
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: 999999;
        justify-content: center;
        align-items: center;
        padding: 20px;
    }

    .exp-modal-toggle:checked ~ .exp-modal-overlay {
        display: flex;
        animation: expModalFadeIn 0.25s ease-out forwards;
    }

    .exp-modal-backdrop {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(4, 5, 14, 0.8);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        cursor: pointer;
    }

    .exp-modal-container {
        position: relative;
        z-index: 10;
        width: 100%;
        max-width: 650px;
        background: linear-gradient(135deg, rgba(15, 17, 36, 0.95), rgba(9, 10, 22, 0.98));
        border: 1.5px solid rgba(0, 212, 255, 0.35);
        border-radius: 26px;
        padding: 30px;
        box-shadow: 0 25px 60px rgba(0, 0, 0, 0.85), 0 0 35px rgba(0, 212, 255, 0.25);
        max-height: 88vh;
        overflow-y: auto;
        animation: expModalPop 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }

    .exp-modal-close-icon {
        position: absolute;
        top: 20px;
        right: 22px;
        width: 36px;
        height: 36px;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.15);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.4rem;
        color: #94a3b8;
        cursor: pointer;
        transition: all 0.2s ease;
        line-height: 1;
        user-select: none;
    }
    .exp-modal-close-icon:hover {
        background: rgba(239, 68, 68, 0.2);
        border-color: rgba(239, 68, 68, 0.5);
        color: #f87171;
        transform: rotate(90deg);
    }

    .exp-modal-header {
        display: flex;
        align-items: flex-start;
        gap: 16px;
        margin-bottom: 20px;
        padding-right: 40px;
    }
    .exp-modal-avatar {
        width: 50px;
        height: 50px;
        border-radius: 16px;
        background: linear-gradient(135deg, #00d4ff, #a855f7);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.4rem;
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.4);
        flex-shrink: 0;
    }
    .exp-modal-org {
        font-size: 1.35rem;
        font-weight: 800;
        color: #ffffff;
        display: flex;
        align-items: center;
        gap: 8px;
        flex-wrap: wrap;
    }
    .exp-modal-role {
        font-size: 1.05rem;
        font-weight: 600;
        color: #00d4ff;
        margin-top: 4px;
    }

    .exp-modal-meta-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 12px;
        margin-bottom: 22px;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 16px;
        padding: 14px 18px;
    }
    .exp-modal-meta-item {
        font-size: 0.85rem;
        color: #94a3b8;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .exp-modal-meta-item strong {
        color: #f1f5f9;
    }

    .exp-modal-section-title {
        font-size: 0.88rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #a855f7;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .exp-modal-desc-box {
        background: rgba(0, 0, 0, 0.25);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        padding: 18px 20px;
        margin-bottom: 20px;
    }
    .exp-modal-desc-text {
        font-size: 0.95rem;
        color: #cbd5e1;
        line-height: 1.8;
        white-space: pre-line;
        margin: 0;
    }

    .exp-modal-techs {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-bottom: 24px;
    }
    .exp-modal-tech {
        padding: 6px 14px;
        border-radius: 50px;
        font-size: 0.8rem;
        font-weight: 600;
        background: rgba(16, 185, 129, 0.12);
        color: #10b981;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }

    .exp-modal-footer {
        display: flex;
        align-items: center;
        justify-content: flex-end;
        gap: 12px;
        padding-top: 18px;
        border-top: 1px solid rgba(255, 255, 255, 0.08);
    }
    .exp-modal-close-btn {
        padding: 8px 22px;
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.15);
        color: #e2e8f0;
        font-size: 0.85rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s ease;
        user-select: none;
    }
    .exp-modal-close-btn:hover {
        background: rgba(255, 255, 255, 0.15);
        color: #ffffff;
    }

    @keyframes expModalFadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    @keyframes expModalPop {
        from { opacity: 0; transform: scale(0.9) translateY(20px); }
        to { opacity: 1; transform: scale(1) translateY(0); }
    }

    @media (max-width: 768px) {
        .exp-handwritten { display: none; }
        .exp-title { font-size: 1.9rem; }
        .exp-modal-container { padding: 22px 18px; }
        .exp-modal-header { padding-right: 30px; }
    }

    /* Light Theme Overrides */
    .light-theme .tl-card-3d {
        background: linear-gradient(145deg, rgba(255, 255, 255, 0.98), rgba(240, 249, 255, 0.94)) !important;
        border: 1.5px solid rgba(0, 212, 255, 0.35) !important;
        box-shadow: 0 16px 40px rgba(0, 212, 255, 0.14), 0 4px 12px rgba(0, 0, 0, 0.04) !important;
    }
    .light-theme .tl-card-3d:hover {
        transform: translateX(8px) !important;
        border-color: #00d4ff !important;
        box-shadow: 0 20px 45px rgba(0, 212, 255, 0.25), 0 0 25px rgba(0, 212, 255, 0.2) !important;
    }
    .light-theme .exp-title,
    .light-theme .tl-org {
        color: #0f172a !important;
    }
    .light-theme .exp-subtitle,
    .light-theme .tl-desc-preview {
        color: #475569 !important;
    }
    .light-theme .tl-dot-3d {
        background: linear-gradient(135deg, #00d4ff, #a855f7) !important;
        border-color: #ffffff !important;
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.5) !important;
    }
    .light-theme .exp-badge {
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.12), rgba(168, 85, 247, 0.12)) !important;
        border: 1.5px solid rgba(0, 212, 255, 0.4) !important;
        color: #0284c7 !important;
        box-shadow: 0 4px 15px rgba(0, 212, 255, 0.12) !important;
    }
    .light-theme .tl-role,
    .light-theme .tl-duration {
        color: #0284c7 !important;
        background: rgba(0, 212, 255, 0.12) !important;
        border-color: rgba(0, 212, 255, 0.35) !important;
        box-shadow: 0 2px 8px rgba(0, 212, 255, 0.1) !important;
    }
    .light-theme .tl-type-badge {
        color: #7e22ce !important;
        background: rgba(168, 85, 247, 0.12) !important;
        border-color: rgba(168, 85, 247, 0.35) !important;
    }
    .light-theme .tl-tech {
        color: #047857 !important;
        background: rgba(16, 185, 129, 0.12) !important;
        border-color: rgba(16, 185, 129, 0.35) !important;
    }
    .light-theme .tl-open-btn {
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.15), rgba(168, 85, 247, 0.15)) !important;
        border: 1.5px solid rgba(0, 212, 255, 0.4) !important;
        color: #0284c7 !important;
        box-shadow: 0 4px 15px rgba(0, 212, 255, 0.15) !important;
    }
    .light-theme .tl-open-btn:hover {
        background: linear-gradient(135deg, #0284c7, #7e22ce) !important;
        border-color: transparent !important;
        color: #ffffff !important;
        box-shadow: 0 6px 20px rgba(2, 132, 199, 0.35) !important;
    }
    .light-theme .tl-actions-row {
        border-top: 1px solid rgba(0, 212, 255, 0.15) !important;
    }
    .light-theme .exp-handwritten {
        color: #047857 !important;
    }
    .light-theme .exp-modal-container {
        background: linear-gradient(135deg, #ffffff, #f8faff) !important;
        border: 2px solid rgba(0, 212, 255, 0.45) !important;
        box-shadow: 0 25px 70px rgba(2, 132, 199, 0.22), 0 10px 30px rgba(0, 0, 0, 0.08) !important;
    }
    .light-theme .exp-modal-org { color: #0f172a !important; }
    .light-theme .exp-modal-desc-box {
        background: #f8fafc !important;
        border: 1.5px solid rgba(0, 212, 255, 0.2) !important;
        box-shadow: inset 0 2px 6px rgba(0, 0, 0, 0.02) !important;
    }
    .light-theme .exp-modal-desc-text { color: #334155 !important; }
    .light-theme .exp-modal-meta-grid {
        background: #f8fafc !important;
        border: 1.5px solid rgba(0, 212, 255, 0.2) !important;
    }
    .light-theme .exp-modal-close-btn {
        background: #f1f5f9 !important;
        color: #334155 !important;
        border-color: #cbd5e1 !important;
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

    for idx, exp in enumerate(experiences):
        exp_id   = exp.get("id", idx + 1)
        modal_id = f"modal-exp-{exp_id}"
        org      = exp.get("organization", "")
        pos      = exp.get("position", "")
        duration = exp.get("duration", "")
        desc     = exp.get("description", "")
        techs    = exp.get("technologies", [])
        cert_url = exp.get("certificate_url", "")
        etype    = exp.get("type", "Internship")

        dur_txt   = duration if not is_placeholder(duration) else "Duration TBD"
        tech_html = "".join(f'<span class="tl-tech">{t}</span>' for t in techs)
        modal_tech_html = "".join(f'<span class="exp-modal-tech">{t}</span>' for t in techs) if techs else '<span style="color:#64748b;font-size:0.85rem;">None specified</span>'

        cert_link_timeline = (f'<a href="{cert_url}" target="_blank" class="tl-cert-link">&#127885; View Certificate</a>'
                              if cert_url and not is_placeholder(cert_url) else "")

        cert_btn_modal = (f'<a href="{cert_url}" target="_blank" class="tl-cert-link" style="margin-right:auto;">&#127885; View Certificate</a>'
                          if cert_url and not is_placeholder(cert_url) else "")

        inject_html(f"""
        <!-- Hidden checkbox to control popup modal -->
        <input type="checkbox" id="{modal_id}" class="exp-modal-toggle" />

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
                <label for="{modal_id}" class="tl-desc-preview" title="Click to read full description">
                    {desc}
                </label>
                <div class="tl-techs">{tech_html}</div>
                <div class="tl-actions-row">
                    <label for="{modal_id}" class="tl-open-btn">&#128065; View Full Description &rarr;</label>
                    {cert_link_timeline}
                </div>
            </div>
        </div>

        <!-- Popup Modal Overlay -->
        <div class="exp-modal-overlay">
            <label for="{modal_id}" class="exp-modal-backdrop"></label>
            <div class="exp-modal-container">
                <label for="{modal_id}" class="exp-modal-close-icon" title="Close">&times;</label>
                
                <div class="exp-modal-header">
                    <div class="exp-modal-avatar">&#128188;</div>
                    <div>
                        <div class="exp-modal-org">{org} <span class="tl-type-badge">{etype}</span></div>
                        <div class="exp-modal-role">{pos}</div>
                    </div>
                </div>

                <div class="exp-modal-meta-grid">
                    <div class="exp-modal-meta-item">&#128197; <div><strong>Duration:</strong> {dur_txt}</div></div>
                    <div class="exp-modal-meta-item">&#127970; <div><strong>Type:</strong> {etype}</div></div>
                </div>

                <div class="exp-modal-section-title">&#128221; Role Overview & Key Contributions</div>
                <div class="exp-modal-desc-box">
                    <p class="exp-modal-desc-text">{desc}</p>
                </div>

                <div class="exp-modal-section-title">&#128736;&#65039; Technologies & Skills Used</div>
                <div class="exp-modal-techs">{modal_tech_html}</div>

                <div class="exp-modal-footer">
                    {cert_btn_modal}
                    <label for="{modal_id}" class="exp-modal-close-btn">Close</label>
                </div>
            </div>
        </div>
        """)

    inject_html('</div>')

