"""
components/contact.py
=====================
Contact section matching img2.jpeg 3D neon glassmorphism design.
"""

import streamlit as st

from utils.data_manager import load_profile, add_message
from utils.helpers import inject_html, is_placeholder


def render_contact():
    """Render the Contact section with 3D glassmorphic UI."""
    profile   = load_profile()
    email     = profile.get("email", "")
    phone     = profile.get("phone", "")
    location  = profile.get("location", "")
    github    = profile.get("github", "")
    linkedin  = profile.get("linkedin", "")
    instagram = profile.get("instagram", "")

    css = """
    #contact { scroll-margin-top: 80px; padding-bottom: 60px; position: relative; }

    .contact-header-container {
        position: relative;
        margin-bottom: 35px;
    }

    .contact-badge {
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

    .contact-title {
        font-size: 2.5rem;
        font-weight: 900;
        color: #ffffff;
        margin-bottom: 8px;
        letter-spacing: -0.5px;
        line-height: 1.1;
    }

    .contact-title-accent {
        background: linear-gradient(135deg, #00d4ff 0%, #a855f7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .contact-subtitle {
        color: #94a3b8;
        font-size: 0.95rem;
        max-width: 580px;
        line-height: 1.6;
    }

    .contact-handwritten {
        position: absolute;
        right: 180px;
        top: 15px;
        font-family: 'Caveat', 'Dancing Script', 'Segoe Script', cursive;
        font-size: 1.45rem;
        color: #00d4ff;
        transform: rotate(-3deg);
        opacity: 0.9;
        text-shadow: 0 0 10px rgba(0, 212, 255, 0.4);
        letter-spacing: 1px;
    }

    .contact-info-card-3d {
        background: rgba(13, 14, 28, 0.75);
        border: 1.5px solid rgba(0, 212, 255, 0.18);
        border-radius: 18px;
        padding: 16px 20px;
        display: flex; align-items: center; gap: 16px;
        backdrop-filter: blur(16px);
        transition: transform 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
        text-decoration: none !important; color: inherit;
        margin-bottom: 14px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.3);
    }
    .contact-info-card-3d:hover {
        text-decoration: none !important;
        transform: translateX(8px);
        border-color: rgba(0,212,255,0.45);
        box-shadow: 0 10px 30px rgba(0,0,0,0.4), 0 0 20px rgba(0,212,255,0.15);
    }
    .contact-icon-3d {
        width: 48px; height: 48px; border-radius: 14px;
        background: linear-gradient(135deg, rgba(0,212,255,0.2), rgba(168,85,247,0.2));
        border: 1px solid rgba(0,212,255,0.3);
        display: flex; align-items: center; justify-content: center;
        font-size: 1.3rem; flex-shrink: 0;
        box-shadow: inset 0 0 10px rgba(255,255,255,0.05);
    }
    .contact-text-label-3d {
        font-size: 0.68rem; color: #64748b;
        letter-spacing: 1.2px; text-transform: uppercase; font-weight: 700;
    }
    .contact-text-value-3d { font-size: 0.92rem; color: #f8fafc; margin-top: 2px; font-weight: 600; word-break: break-all; }
    .contact-text-value-3d a, .contact-text-value-3d a:hover { color: #00d4ff; text-decoration: none !important; }

    .social-row-3d { display: flex; gap: 10px; flex-wrap: wrap; margin-top: 10px; }
    .social-btn-3d {
        padding: 10px 22px; border-radius: 14px;
        font-size: 0.84rem; font-weight: 700;
        text-decoration: none;
        background: rgba(13, 14, 28, 0.75); color: #e2e8f0;
        border: 1px solid rgba(255,255,255,0.12);
        transition: all 0.25s ease;
        display: flex; align-items: center; gap: 6px;
        backdrop-filter: blur(12px);
    }
    .social-btn-3d:hover {
        background: rgba(0,212,255,0.15); color: #00d4ff;
        border-color: rgba(0,212,255,0.4); transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(0,212,255,0.25);
    }

    @media (max-width: 768px) {
        .contact-handwritten { display: none; }
        .contact-title { font-size: 1.9rem; }
    }

    /* Light Theme Overrides */
    .light-theme .contact-info-card-3d,
    .light-theme .social-btn-3d {
        background: rgba(255, 255, 255, 0.92) !important;
        border-color: rgba(0, 0, 0, 0.1) !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.06) !important;
    }
    .light-theme .contact-title,
    .light-theme .contact-text-value-3d,
    .light-theme .social-btn-3d {
        color: #0f172a !important;
    }
    .light-theme .contact-subtitle,
    .light-theme .contact-text-label-3d {
        color: #475569 !important;
    }
    .light-theme .contact-badge {
        background: rgba(0, 0, 0, 0.04) !important;
        border-color: rgba(0, 0, 0, 0.12) !important;
        color: #0284c7 !important;
    }
    .light-theme .contact-text-value-3d a,
    .light-theme .contact-text-value-3d a:hover {
        color: #0284c7 !important;
    }
    .light-theme .contact-icon-3d {
        background: linear-gradient(135deg, rgba(0,212,255,0.12), rgba(168,85,247,0.12)) !important;
        border-color: rgba(0,212,255,0.25) !important;
    }
    .contact-form-title {
        color: #f8fafc;
    }
    .light-theme .contact-form-title {
        color: #0f172a !important;
    }
    .light-theme .contact-handwritten {
        color: #0284c7 !important;
    }
    """

    inject_html(f"<style>{css}</style>")
    inject_html('<div id="contact"></div>')

    # Header
    header_html = """
    <div class="contact-header-container">
        <div class="contact-badge">GET IN TOUCH</div>
        <h2 class="contact-title">Contact <span class="contact-title-accent">Me</span></h2>
        <p class="contact-subtitle">Let's connect and build something great together. Open for opportunities, collaborations, and discussions.</p>
        <div class="contact-handwritten">Connect &rarr; Collaborate &rarr; Create</div>
    </div>
    """
    inject_html(header_html)

    col_left, col_right = st.columns([1, 1.4], gap="large")

    # LEFT: contact info cards
    with col_left:
        any_info = False

        if not is_placeholder(email):
            inject_html(f"""
            <a href="mailto:{email}" class="contact-info-card-3d">
                <div class="contact-icon-3d">&#128231;</div>
                <div>
                    <div class="contact-text-label-3d">Email</div>
                    <div class="contact-text-value-3d">{email}</div>
                </div>
            </a>""")
            any_info = True

        if phone and not is_placeholder(phone):
            inject_html(f"""
            <div class="contact-info-card-3d">
                <div class="contact-icon-3d">&#128241;</div>
                <div>
                    <div class="contact-text-label-3d">Phone</div>
                    <div class="contact-text-value-3d">{phone}</div>
                </div>
            </div>""")
            any_info = True

        if not is_placeholder(location):
            inject_html(f"""
            <div class="contact-info-card-3d">
                <div class="contact-icon-3d">&#128205;</div>
                <div>
                    <div class="contact-text-label-3d">Location</div>
                    <div class="contact-text-value-3d">{location}</div>
                </div>
            </div>""")
            any_info = True

        if not is_placeholder(github):
            short_gh = github.replace("https://", "").replace("http://", "")
            inject_html(f"""
            <a href="{github}" target="_blank" rel="noopener" class="contact-info-card-3d">
                <div class="contact-icon-3d">&#128025;</div>
                <div>
                    <div class="contact-text-label-3d">GitHub</div>
                    <div class="contact-text-value-3d">{short_gh}</div>
                </div>
            </a>""")
            any_info = True

        if not is_placeholder(linkedin):
            short_li = linkedin.replace("https://", "").replace("http://", "").replace("www.", "")
            inject_html(f"""
            <a href="{linkedin}" target="_blank" rel="noopener" class="contact-info-card-3d">
                <div class="contact-icon-3d">&#128188;</div>
                <div>
                    <div class="contact-text-label-3d">LinkedIn</div>
                    <div class="contact-text-value-3d">{short_li}</div>
                </div>
            </a>""")
            any_info = True

        if not any_info:
            inject_html('<p style="color:#64748b;padding:10px 0;">Contact info not set yet.<br>Update via the admin panel.</p>')

        # Social buttons row
        social_btns = ""
        if not is_placeholder(github):
            social_btns += f'<a href="{github}" target="_blank" class="social-btn-3d">&#128025; GitHub</a>'
        if not is_placeholder(linkedin):
            social_btns += f'<a href="{linkedin}" target="_blank" class="social-btn-3d">&#128188; LinkedIn</a>'
        if not is_placeholder(email):
            social_btns += f'<a href="mailto:{email}" class="social-btn-3d">&#128231; Email</a>'
        if instagram and not is_placeholder(instagram):
            social_btns += f'<a href="{instagram}" target="_blank" class="social-btn-3d">&#128247; Instagram</a>'

        if social_btns:
            inject_html(f'<div class="social-row-3d">{social_btns}</div>')

    # RIGHT: contact form
    with col_right:
        st.markdown("<h3 class='contact-form-title' style='font-weight:800; margin-bottom:12px;'>✉️ Send Me a Message</h3>", unsafe_allow_html=True)
        with st.form("contact_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                sender_name  = st.text_input("Your Name",  placeholder="John Doe")
            with c2:
                sender_email = st.text_input("Your Email", placeholder="john@example.com")
            message = st.text_area("Message",
                                   placeholder="Hi Kartikey, I wanted to reach out about...",
                                   height=140)
            submit = st.form_submit_button("🚀 Send Message", use_container_width=True)

            if submit:
                if not sender_name.strip():
                    st.error("Please enter your name.")
                elif not sender_email.strip() or "@" not in sender_email:
                    st.error("Please enter a valid email address.")
                elif not message.strip():
                    st.error("Please write a message.")
                else:
                    add_message(sender_name.strip(), sender_email.strip(), message.strip())
                    st.success("✓ Message saved! I will get back to you soon.")

