"""
components/certificates.py
==========================
Certificate gallery matching img2.jpeg 3D neon glassmorphism design.
"""

import streamlit as st

from utils.data_manager import load_certificates
from utils.helpers import inject_html, get_img_tag, is_placeholder


def render_certificates():
    """Render the Certificates section with 3D glassmorphic cards."""
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
        cursor: pointer;
        display: flex; flex-direction: column; justify-content: space-between;
        height: calc(100% - 24px);
    }
    .cert-card-3d:hover {
        transform: translateY(-7px);
        border-color: rgba(168,85,247,0.55);
        box-shadow: 0 12px 36px rgba(0,0,0,0.5), 0 0 30px rgba(168,85,247,0.2);
    }

    .cert-img-wrap-3d {
        width: 100%; height: 160px;
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
        width: 100%; height: 160px;
        display: flex; align-items: center; justify-content: center;
    }

    .cert-issuer-ribbon-3d {
        position: absolute; top: 10px; left: 10px;
        padding: 4px 12px; border-radius: 50px;
        font-size: 0.68rem; font-weight: 700;
        background: rgba(168,85,247,0.25); color: #e9d5ff;
        border: 1px solid rgba(168,85,247,0.4);
        backdrop-filter: blur(8px);
    }

    .cert-body-3d { padding: 18px; flex: 1; display: flex; flex-direction: column; justify-content: space-between; }
    .cert-title-3d {
        font-size: 0.96rem; font-weight: 800; color: #f8fafc;
        line-height: 1.35; margin-bottom: 8px;
        display: -webkit-box; -webkit-line-clamp: 2;
        -webkit-box-orient: vertical; overflow: hidden;
    }
    .cert-meta-3d { font-size: 0.76rem; color: #94a3b8; margin-bottom: 14px; }

    .cert-actions-3d { display: flex; gap: 8px; }
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
    .cert-btn-disabled-3d { opacity: 0.35; cursor: not-allowed; pointer-events: none; }

    @media (max-width: 768px) {
        .cert-handwritten { display: none; }
        .cert-title { font-size: 1.9rem; }
    }

    /* Light Theme Overrides */
    .light-theme .cert-card-3d {
        background: rgba(255, 255, 255, 0.92) !important;
        border-color: rgba(0, 0, 0, 0.1) !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.06) !important;
    }
    .light-theme .cert-title,
    .light-theme .cert-title-3d {
        color: #0f172a !important;
    }
    .light-theme .cert-subtitle,
    .light-theme .cert-meta-3d {
        color: #475569 !important;
    }
    .light-theme .cert-badge {
        background: rgba(0, 0, 0, 0.04) !important;
        border-color: rgba(0, 0, 0, 0.12) !important;
        color: #0284c7 !important;
    }
    .light-theme .cert-issuer-ribbon-3d,
    .light-theme .cert-btn-verify-3d {
        color: #7e22ce !important;
        background: rgba(168, 85, 247, 0.15) !important;
        border-color: rgba(168, 85, 247, 0.3) !important;
    }
    .light-theme .cert-handwritten {
        color: #d97706 !important;
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
            title      = cert.get("title", "Certificate")
            issuer     = cert.get("issuer", "")
            date       = cert.get("date", "")
            cred_id    = cert.get("credential_id", "")
            verify_url = cert.get("verify_url", "")
            img_path   = cert.get("image", "")

            img_html  = get_img_tag(img_path, alt=title)
            date_txt  = date   if not is_placeholder(date)    else "&mdash;"
            meta_str  = f"&#128197; {date_txt}"
            if cred_id and not is_placeholder(cred_id):
                meta_str += f" &nbsp;&middot;&nbsp; ID: {cred_id}"

            if verify_url and not is_placeholder(verify_url):
                verify_btn = f'<a href="{verify_url}" target="_blank" class="cert-btn-3d cert-btn-verify-3d">&#128279; Verify Certificate</a>'
            else:
                verify_btn = '<span class="cert-btn-3d cert-btn-verify-3d cert-btn-disabled-3d">&#128279; Verify Certificate</span>'

            with col:
                inject_html(f"""
                <div class="cert-card-3d" id="cert-{cid}">
                    <div class="cert-img-wrap-3d">
                        {img_html}
                        <span class="cert-issuer-ribbon-3d">{issuer}</span>
                    </div>
                    <div class="cert-body-3d">
                        <div>
                            <div class="cert-title-3d" title="{title}">{title}</div>
                            <div class="cert-meta-3d">{meta_str}</div>
                        </div>
                        <div class="cert-actions-3d">{verify_btn}</div>
                    </div>
                </div>
                """)

    # Expandable details
    st.markdown("")
    with st.expander("📋 View All Certificate Details", expanded=False):
        for cert in certs:
            title      = cert.get("title", "Certificate")
            issuer     = cert.get("issuer", "")
            date       = cert.get("date", "")
            verify_url = cert.get("verify_url", "")
            desc       = cert.get("description", "")

            c1, c2 = st.columns([3, 1])
            with c1:
                st.markdown(f"**{title}**")
                st.caption(f"Issued by: {issuer}  |  Date: {date}")
                if desc:
                    st.markdown(f"<small style='color:#64748b'>{desc}</small>", unsafe_allow_html=True)
            with c2:
                if verify_url and not is_placeholder(verify_url):
                    st.link_button("🔗 Verify", verify_url, use_container_width=True)
            st.divider()

