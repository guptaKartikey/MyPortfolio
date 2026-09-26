"""
components/certificates.py
==========================
Certificate gallery matching img2.jpeg 3D neon glassmorphism design.
Features interactive popup modal for viewing full certificate image and details on click.
"""

import streamlit as st

from utils.data_manager import load_certificates
from utils.helpers import inject_html, get_img_tag, is_placeholder


def render_certificates():
    """Render the Certificates section with 3D glassmorphic cards and interactive detail modals."""
    data  = load_certificates()
    certs = data.get("certificates", [])

    css = """
    #certificates { scroll-margin-top: 80px; padding-bottom: 50px; position: relative; }

    .cert-header-container {
        position: relative;
        margin-bottom: 35px;
    }

    .cert-badge {
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

    .cert-title {
        font-size: 2.5rem;
        font-weight: 900;
        color: #ffffff;
        margin-bottom: 8px;
        letter-spacing: -0.5px;
        line-height: 1.1;
    }

    .cert-title-accent {
        background: linear-gradient(135deg, #a855f7 0%, #f59e0b 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .cert-subtitle {
        color: #94a3b8;
        font-size: 0.95rem;
        max-width: 580px;
        line-height: 1.6;
    }

    .cert-handwritten {
        position: absolute;
        right: 180px;
        top: 15px;
        font-family: 'Caveat', 'Dancing Script', 'Segoe Script', cursive;
        font-size: 1.45rem;
        color: #f59e0b;
        transform: rotate(-3deg);
        opacity: 0.9;
        text-shadow: 0 0 10px rgba(245, 158, 11, 0.4);
        letter-spacing: 1px;
    }

    .cert-card-3d {
        background: rgba(13, 14, 28, 0.75);
        border: 1.5px solid rgba(168,85,247,0.25);
        border-radius: 22px; overflow: hidden;
        backdrop-filter: blur(16px);
        transition: transform 0.35s ease, box-shadow 0.35s ease, border-color 0.35s ease;
        margin-bottom: 24px;
        display: flex; flex-direction: column; justify-content: space-between;
        height: calc(100% - 24px);
        position: relative;
    }
    .cert-card-3d:hover {
        transform: translateY(-7px);
        border-color: rgba(168,85,247,0.55);
        box-shadow: 0 12px 36px rgba(0,0,0,0.5), 0 0 30px rgba(168,85,247,0.2);
    }

    .cert-card-clickable {
        display: flex;
        flex-direction: column;
        flex: 1;
        cursor: pointer;
        text-decoration: none !important;
    }

    .cert-img-wrap-3d {
        width: 100%; height: 165px;
        background: linear-gradient(135deg, #0d0d1a, #1a1029);
        display: flex; align-items: center; justify-content: center;
        overflow: hidden; position: relative;
    }
    .cert-img-wrap-3d img {
        width: 100%; height: 100%; object-fit: cover;
        transition: transform 0.4s ease;
    }
    .cert-card-3d:hover .cert-img-wrap-3d img { transform: scale(1.06); }
    .cert-img-wrap-3d .img-placeholder {
        font-size: 2.8rem;
        background: linear-gradient(135deg, #1a0d2e, #16213e);
        width: 100%; height: 165px;
        display: flex; align-items: center; justify-content: center;
    }

    .cert-img-hover-hint {
        position: absolute;
        bottom: 0; left: 0; right: 0;
        background: linear-gradient(to top, rgba(0, 0, 0, 0.85), transparent);
        padding: 20px 10px 8px;
        text-align: center;
        color: #e9d5ff;
        font-size: 0.76rem;
        font-weight: 700;
        opacity: 0;
        transition: opacity 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 6px;
    }
    .cert-card-3d:hover .cert-img-hover-hint {
        opacity: 1;
    }

    .cert-issuer-ribbon-3d {
        position: absolute; top: 12px; left: 12px;
        padding: 5px 14px; border-radius: 50px;
        font-size: 0.72rem; font-weight: 800; letter-spacing: 0.3px;
        background: linear-gradient(135deg, rgba(20, 16, 38, 0.92), rgba(11, 9, 24, 0.96));
        color: #f8fafc;
        border: 1px solid rgba(168, 85, 247, 0.45);
        backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.55), 0 0 12px rgba(168, 85, 247, 0.25), inset 0 1px 1px rgba(255, 255, 255, 0.15);
        display: inline-flex; align-items: center; gap: 6px;
        z-index: 3;
        transition: transform 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
    }
    .cert-card-3d:hover .cert-issuer-ribbon-3d {
        transform: translateY(-1px);
        border-color: rgba(168, 85, 247, 0.75);
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.65), 0 0 18px rgba(168, 85, 247, 0.45);
    }

    .cert-body-3d { padding: 18px; flex: 1; display: flex; flex-direction: column; justify-content: space-between; }
    .cert-title-3d {
        font-size: 0.96rem; font-weight: 800; color: #f8fafc;
        line-height: 1.35; margin-bottom: 8px;
        display: -webkit-box; -webkit-line-clamp: 2;
        -webkit-box-orient: vertical; overflow: hidden;
    }
    .cert-meta-3d { font-size: 0.76rem; color: #94a3b8; margin-bottom: 12px; }

    .cert-actions-3d { padding: 0 18px 18px; display: flex; gap: 8px; }
    .cert-btn-3d {
        flex: 1; padding: 8px 0; border-radius: 10px;
        font-size: 0.76rem; font-weight: 700;
        text-decoration: none; text-align: center;
        transition: all 0.25s ease; border: none; display: block;
    }
    .cert-btn-verify-3d {
        background: linear-gradient(135deg, rgba(168,85,247,0.25), rgba(0,212,255,0.25));
        color: #e9d5ff; border: 1px solid rgba(168,85,247,0.35);
    }
    .cert-btn-verify-3d:hover {
        background: linear-gradient(135deg, rgba(168,85,247,0.4), rgba(0,212,255,0.35));
        transform: translateY(-2px); color: #ffffff;
        box-shadow: 0 4px 15px rgba(168,85,247,0.3);
    }

    /* ── POPUP MODAL STYLES (Pure CSS Modal via Checkbox) ────────── */
    .cert-modal-toggle {
        display: none !important;
    }

    .cert-modal-overlay {
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

    .cert-modal-toggle:checked ~ .cert-modal-overlay {
        display: flex;
        animation: certModalFadeIn 0.25s ease-out forwards;
    }

    .cert-modal-backdrop {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(4, 5, 14, 0.85);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        cursor: pointer;
    }

    .cert-modal-container {
        position: relative;
        z-index: 10;
        width: 100%;
        max-width: 780px;
        background: linear-gradient(135deg, rgba(16, 14, 34, 0.97), rgba(9, 10, 22, 0.98));
        border: 1.5px solid rgba(168, 85, 247, 0.4);
        border-radius: 26px;
        padding: 28px;
        box-shadow: 0 25px 60px rgba(0, 0, 0, 0.9), 0 0 35px rgba(168, 85, 247, 0.25);
        max-height: 88vh;
        overflow-y: auto;
        animation: certModalPop 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }

    .cert-modal-close-icon {
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
    .cert-modal-close-icon:hover {
        background: rgba(239, 68, 68, 0.2);
        border-color: rgba(239, 68, 68, 0.5);
        color: #f87171;
        transform: rotate(90deg);
    }

    .cert-modal-header {
        margin-bottom: 18px;
        padding-right: 40px;
    }
    .cert-modal-title {
        font-size: 1.4rem;
        font-weight: 800;
        color: #ffffff;
        line-height: 1.3;
        margin: 6px 0 0 0;
    }

    .cert-modal-img-box {
        width: 100%;
        background: rgba(0, 0, 0, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 18px;
        padding: 12px;
        margin-bottom: 22px;
        display: flex;
        justify-content: center;
        align-items: center;
        overflow: hidden;
    }
    .cert-modal-img-box img {
        max-width: 100%;
        max-height: 460px;
        width: auto;
        height: auto;
        object-fit: contain;
        border-radius: 12px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
    }
    .cert-modal-img-box .img-placeholder {
        padding: 40px 20px;
        text-align: center;
        font-size: 3rem;
        color: #94a3b8;
    }

    .cert-modal-meta-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 12px;
        margin-bottom: 20px;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 16px;
        padding: 14px 18px;
    }
    .cert-modal-meta-item {
        font-size: 0.85rem;
        color: #94a3b8;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .cert-modal-meta-item strong {
        color: #f1f5f9;
    }

    .cert-modal-desc-box {
        background: rgba(0, 0, 0, 0.25);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        padding: 18px 20px;
        margin-bottom: 22px;
    }
    .cert-modal-desc-text {
        font-size: 0.92rem;
        color: #cbd5e1;
        line-height: 1.75;
        margin: 0;
    }

    .cert-modal-footer {
        display: flex;
        align-items: center;
        justify-content: flex-end;
        gap: 12px;
        padding-top: 18px;
        border-top: 1px solid rgba(255, 255, 255, 0.08);
    }
    .cert-modal-close-btn {
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
    .cert-modal-close-btn:hover {
        background: rgba(255, 255, 255, 0.15);
        color: #ffffff;
    }

    @keyframes certModalFadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    @keyframes certModalPop {
        from { opacity: 0; transform: scale(0.9) translateY(20px); }
        to { opacity: 1; transform: scale(1) translateY(0); }
    }

    @media (max-width: 768px) {
        .cert-handwritten { display: none; }
        .cert-title { font-size: 1.9rem; }
        .cert-modal-container { padding: 20px 16px; }
        .cert-modal-header { padding-right: 30px; }
        .cert-modal-img-box img { max-height: 280px; }
    }

    /* Light Theme Overrides */
    .light-theme .cert-card-3d {
        background: linear-gradient(145deg, rgba(255, 255, 255, 0.97), rgba(250, 245, 255, 0.93)) !important;
        border: 1.5px solid rgba(168, 85, 247, 0.3) !important;
        box-shadow: 0 16px 40px rgba(168, 85, 247, 0.12), 0 4px 16px rgba(0, 0, 0, 0.04) !important;
    }
    .light-theme .cert-card-3d:hover {
        border-color: rgba(168, 85, 247, 0.6) !important;
        box-shadow: 0 20px 48px rgba(168, 85, 247, 0.22), 0 0 25px rgba(168, 85, 247, 0.15) !important;
    }
    .light-theme .cert-img-wrap-3d {
        background: linear-gradient(135deg, #f1f5f9, #f5f3ff) !important;
    }
    .light-theme .cert-title,
    .light-theme .cert-title-3d,
    .light-theme .cert-modal-title {
        color: #0f172a !important;
    }
    .light-theme .cert-subtitle,
    .light-theme .cert-meta-3d {
        color: #475569 !important;
    }
    .light-theme .cert-badge {
        background: rgba(168, 85, 247, 0.1) !important;
        border-color: rgba(168, 85, 247, 0.25) !important;
        color: #7e22ce !important;
        box-shadow: 0 4px 14px rgba(168, 85, 247, 0.1) !important;
    }
    .light-theme .cert-issuer-ribbon-3d {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.98), rgba(243, 232, 255, 0.98)) !important;
        border: 1.5px solid rgba(147, 51, 234, 0.4) !important;
        color: #6b21a8 !important;
        box-shadow: 0 4px 14px rgba(107, 33, 168, 0.18), inset 0 1px 1px #ffffff !important;
    }
    .light-theme .cert-card-3d:hover .cert-issuer-ribbon-3d {
        border-color: rgba(147, 51, 234, 0.7) !important;
        box-shadow: 0 6px 20px rgba(107, 33, 168, 0.28) !important;
    }
    .light-theme .cert-btn-verify-3d {
        color: #7e22ce !important;
        background: linear-gradient(135deg, rgba(168, 85, 247, 0.15), rgba(0, 212, 255, 0.15)) !important;
        border: 1px solid rgba(168, 85, 247, 0.35) !important;
        box-shadow: 0 4px 12px rgba(168, 85, 247, 0.12) !important;
    }
    .light-theme .cert-btn-verify-3d:hover {
        background: linear-gradient(135deg, rgba(168, 85, 247, 0.25), rgba(0, 212, 255, 0.25)) !important;
        color: #581c87 !important;
        border-color: rgba(168, 85, 247, 0.6) !important;
        box-shadow: 0 6px 18px rgba(168, 85, 247, 0.25) !important;
    }
    .light-theme .cert-handwritten {
        color: #d97706 !important;
        text-shadow: 0 0 10px rgba(217, 119, 6, 0.3) !important;
    }
    .light-theme .cert-modal-container {
        background: linear-gradient(145deg, #ffffff, #faf5ff) !important;
        border: 1.5px solid rgba(168, 85, 247, 0.35) !important;
        box-shadow: 0 25px 70px rgba(0, 0, 0, 0.18), 0 0 35px rgba(168, 85, 247, 0.15) !important;
    }
    .light-theme .cert-modal-img-box {
        background: #f8fafc !important;
        border: 1px solid rgba(168, 85, 247, 0.2) !important;
        box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.04) !important;
    }
    .light-theme .cert-modal-desc-box {
        background: linear-gradient(135deg, #f8fafc, #f5f3ff) !important;
        border: 1px solid rgba(168, 85, 247, 0.2) !important;
    }
    .light-theme .cert-modal-desc-text { color: #334155 !important; }
    .light-theme .cert-modal-meta-grid {
        background: linear-gradient(135deg, #f8fafc, #f5f3ff) !important;
        border: 1px solid rgba(168, 85, 247, 0.2) !important;
    }
    .light-theme .cert-modal-meta-item {
        color: #475569 !important;
    }
    .light-theme .cert-modal-meta-item strong {
        color: #0f172a !important;
    }
    .light-theme .cert-modal-close-btn {
        background: linear-gradient(135deg, #f1f5f9, #e2e8f0) !important;
        color: #1e293b !important;
        border: 1px solid #cbd5e1 !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06) !important;
    }
    .light-theme .cert-modal-close-btn:hover {
        background: #e2e8f0 !important;
    }
    .light-theme .cert-modal-close-icon {
        background: rgba(0, 0, 0, 0.05) !important;
        border: 1px solid rgba(0, 0, 0, 0.1) !important;
        color: #64748b !important;
    }
    .light-theme .cert-modal-close-icon:hover {
        background: rgba(239, 68, 68, 0.15) !important;
        border-color: rgba(239, 68, 68, 0.4) !important;
        color: #dc2626 !important;
    }
    """

    inject_html(f"<style>{css}</style>")
    inject_html('<div id="certificates"></div>')

    # Header
    header_html = """
    <div class="cert-header-container">
        <div class="cert-badge">ACHIEVEMENTS</div>
        <h2 class="cert-title">Certifications & <span class="cert-title-accent">Licenses</span></h2>
        <p class="cert-subtitle">Verified professional credentials, specialized course completions, and certifications.</p>
        <div class="cert-handwritten">Study &rarr; Test &rarr; Master</div>
    </div>
    """
    inject_html(header_html)

    if not certs:
        inject_html('<p style="color:#64748b;text-align:center;padding:60px;">No certificates added yet. Use the admin panel.</p>')
        return

    # Render cards in rows of 3
    COLS_PER_ROW = 3
    for row_start in range(0, len(certs), COLS_PER_ROW):
        row_certs = certs[row_start : row_start + COLS_PER_ROW]
        cols = st.columns(len(row_certs))

        for col, cert in zip(cols, row_certs):
            cid        = cert.get("id", 0)
            modal_id   = f"modal-cert-{cid}"
            title      = cert.get("title", "Certificate")
            issuer     = cert.get("issuer", "")
            date       = cert.get("date", "")
            cred_id    = cert.get("credential_id", "")
            verify_url = cert.get("verify_url", "")
            img_path   = cert.get("image", "")
            desc       = cert.get("description", "")

            img_html      = get_img_tag(img_path, alt=title)
            full_img_html = get_img_tag(img_path, alt=title, css_class="cert-modal-full-img")

            date_txt = date if (date and not is_placeholder(date)) else "Date unspecified"
            meta_str = f"&#128197; {date_txt}"
            if cred_id and not is_placeholder(cred_id) and str(cred_id).strip():
                meta_str += f" &nbsp;&middot;&nbsp; ID: {cred_id}"

            # Verify button in card actions (only if verify_url is present)
            if verify_url and not is_placeholder(verify_url) and str(verify_url).strip():
                actions_html = f'<div class="cert-actions-3d"><a href="{verify_url}" target="_blank" class="cert-btn-3d cert-btn-verify-3d">&#128279; Verify Certificate</a></div>'
                modal_verify_btn = f'<a href="{verify_url}" target="_blank" class="cert-btn-3d cert-btn-verify-3d" style="flex: initial; padding: 8px 20px; margin-right: auto;">&#128279; Verify Certificate</a>'
            else:
                actions_html = ''
                modal_verify_btn = ''

            # Credential ID in modal
            if cred_id and not is_placeholder(cred_id) and str(cred_id).strip():
                cred_meta_html = f'<div class="cert-modal-meta-item">&#127380; <div><strong>Credential ID:</strong> {cred_id}</div></div>'
            else:
                cred_meta_html = ''

            # Description in modal
            if desc and str(desc).strip():
                desc_section_html = f'''
                <div class="cert-modal-desc-box">
                    <p class="cert-modal-desc-text">{desc}</p>
                </div>
                '''
            else:
                desc_section_html = ''

            with col:
                inject_html(f"""
                <!-- Hidden checkbox to control certificate popup modal -->
                <input type="checkbox" id="{modal_id}" class="cert-modal-toggle" />

                <div class="cert-card-3d" id="cert-{cid}">
                    <label for="{modal_id}" class="cert-card-clickable" title="Click to view full certificate and details">
                        <div class="cert-img-wrap-3d">
                            {img_html}
                            <span class="cert-issuer-ribbon-3d">{issuer}</span>
                            <div class="cert-img-hover-hint">&#128065; View Full Certificate</div>
                        </div>
                        <div class="cert-body-3d">
                            <div>
                                <div class="cert-title-3d" title="{title}">{title}</div>
                                <div class="cert-meta-3d">{meta_str}</div>
                            </div>
                        </div>
                    </label>
                    {actions_html}
                </div>

                <!-- Popup Modal Overlay -->
                <div class="cert-modal-overlay">
                    <label for="{modal_id}" class="cert-modal-backdrop"></label>
                    <div class="cert-modal-container">
                        <label for="{modal_id}" class="cert-modal-close-icon" title="Close">&times;</label>
                        
                        <div class="cert-modal-header">
                            <span class="cert-issuer-ribbon-3d" style="position: static; display: inline-block; margin-bottom: 6px;">{issuer}</span>
                            <h3 class="cert-modal-title">{title}</h3>
                        </div>

                        <div class="cert-modal-img-box">
                            {full_img_html}
                        </div>

                        <div class="cert-modal-meta-grid">
                            <div class="cert-modal-meta-item">&#127970; <div><strong>Issuer:</strong> {issuer}</div></div>
                            <div class="cert-modal-meta-item">&#128197; <div><strong>Date:</strong> {date_txt}</div></div>
                            {cred_meta_html}
                        </div>

                        {desc_section_html}

                        <div class="cert-modal-footer">
                            {modal_verify_btn}
                            <label for="{modal_id}" class="cert-modal-close-btn">Close</label>
                        </div>
                    </div>
                </div>
                """)



