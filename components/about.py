"""
components/about.py
===================
About Me section matching reference img3.jpeg 3D neon glassmorphism design.
"""

import streamlit as st

from utils.data_manager import load_profile
from utils.helpers import inject_html, get_img_tag, get_download_link, is_placeholder


# Default interest items with icons and colors matching img3.jpeg
INTEREST_ITEMS = [
    {"name": "Artificial Intelligence", "icon": "🧠", "color": "#00d4ff"},
    {"name": "Machine Learning", "icon": "🔲", "color": "#a855f7"},
    {"name": "Software Development", "icon": "</>", "color": "#06b6d4"},
    {"name": "Web Development", "icon": "🌐", "color": "#f59e0b"},
    {"name": "Computer Vision", "icon": "👁️", "color": "#d946ef"},
    {"name": "Generative AI", "icon": "✨", "color": "#00d4ff"},
]


def render_about():
    """Render the About Me section matching img3.jpeg design."""
    profile  = load_profile()
    name     = profile.get("name", "Kartikey Gupta")
    bio      = profile.get("bio", "I am a passionate B.Tech Computer Science Engineering student with a strong interest in Artificial Intelligence, Machine Learning, and Software Development. I love building intelligent systems and exploring the intersection of code and creativity. Currently maintaining a SGPA of 8.75, I am always eager to learn new technologies and work on impactful real-world projects.")
    role     = profile.get("role", "B.Tech Computer Science & Engineering Student")
    college  = profile.get("college", "[PLACEHOLDER]")
    grad     = profile.get("graduation_year", "2027")
    sgpa     = profile.get("sgpa", "8.75")
    img_path = profile.get("profile_image", "assets/profile/profile.jpg")
    interests_raw = profile.get("interests", [])
    resume_path   = profile.get("resume_file", "assets/resume/resume.pdf")

    github    = profile.get("github", "")
    linkedin  = profile.get("linkedin", "")
    instagram = profile.get("instagram", "")
    email     = profile.get("email", "")

    css = """
    #about { scroll-margin-top: 80px; padding-bottom: 50px; position: relative; }

    .about-profile-card-3d {
        background: rgba(13, 14, 28, 0.75);
        border: 1.5px solid rgba(0, 212, 255, 0.22);
        border-radius: 24px;
        padding: 32px 24px 28px;
        text-align: center;
        backdrop-filter: blur(16px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.4), 0 0 25px rgba(0,212,255,0.12);
        transition: transform 0.35s ease, box-shadow 0.35s ease;
        margin-bottom: 24px;
        position: relative;
    }
    .about-profile-card-3d:hover {
        transform: translateY(-6px);
        box-shadow: 0 14px 40px rgba(0,0,0,0.5), 0 0 35px rgba(0,212,255,0.22);
    }

    .about-img-wrap-3d {
        position: relative;
        width: 140px; height: 140px;
        margin: 0 auto 16px;
    }
    .about-img-wrap-3d img,
    .about-img-wrap-3d .img-placeholder {
        width: 140px; height: 140px;
        border-radius: 50%; object-fit: cover;
        border: 3.5px solid #00d4ff;
        box-shadow: 0 0 25px rgba(0, 212, 255, 0.5);
        display: block; margin: 0 auto;
    }
    .about-img-wrap-3d .img-placeholder {
        display: flex; align-items: center; justify-content: center;
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        font-size: 3.2rem;
    }

    .about-profile-name {
        font-size: 1.4rem; font-weight: 900; color: #f8fafc;
        letter-spacing: 1px; text-transform: uppercase; margin-bottom: 4px;
    }
    .about-profile-role {
        font-size: 0.72rem; color: #94a3b8; font-weight: 700;
        letter-spacing: 1.2px; text-transform: uppercase; margin-bottom: 22px;
    }

    .about-stats-row-3d {
        display: flex; justify-content: space-around;
        padding: 16px 0;
        border-top: 1px solid rgba(255,255,255,0.08);
        border-bottom: 1px solid rgba(255,255,255,0.08);
        margin-bottom: 20px;
    }
    .about-stat-item { text-align: center; }
    .about-stat-val  { font-size: 1.35rem; font-weight: 800; color: #ffffff; }
    .about-stat-lbl  { font-size: 0.7rem; color: #94a3b8; margin-top: 2px; }

    .social-icons-row-3d {
        display: flex; justify-content: center; gap: 12px;
        margin-bottom: 22px;
    }
    .social-icon-btn-3d {
        width: 40px; height: 40px; border-radius: 50%;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.12);
        color: #00d4ff; font-size: 1.05rem;
        display: flex; align-items: center; justify-content: center;
        text-decoration: none; transition: all 0.25s ease;
    }
    .social-icon-btn-3d:hover {
        background: rgba(0, 212, 255, 0.15);
        border-color: rgba(0, 212, 255, 0.4);
        transform: translateY(-3px);
        box-shadow: 0 4px 15px rgba(0, 212, 255, 0.3);
        color: #ffffff;
    }

    .btn-resume-3d {
        display: flex; align-items: center; justify-content: center; gap: 8px;
        width: 100%; padding: 12px 20px; border-radius: 50px;
        background: linear-gradient(135deg, #00d4ff 0%, #a855f7 100%);
        color: #ffffff !important; font-size: 0.88rem; font-weight: 700;
        text-decoration: none !important; transition: all 0.3s ease;
        box-shadow: 0 6px 20px rgba(0,212,255,0.35); border: none;
    }
    .btn-resume-3d:hover {
        text-decoration: none !important;
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,212,255,0.55);
        filter: brightness(1.1);
    }
    .btn-resume-disabled-3d {
        display: block; width: 100%; padding: 12px 20px;
        border-radius: 50px; background: rgba(255,255,255,0.05);
        color: #64748b; font-size: 0.85rem; font-weight: 600;
        border: 1px dashed rgba(255,255,255,0.15); text-align: center;
    }

    /* RIGHT COLUMN STYLES */
    .who-i-am-card-3d {
        background: rgba(13, 14, 28, 0.75);
        border: 1.5px solid rgba(255, 255, 255, 0.08);
        border-radius: 24px; padding: 30px;
        backdrop-filter: blur(16px);
        margin-bottom: 24px; position: relative; overflow: hidden;
    }

    .about-pill-badge {
        display: inline-flex; align-items: center; gap: 8px;
        padding: 4px 14px; border-radius: 50px;
        background: rgba(0, 212, 255, 0.08);
        border: 1px solid rgba(0, 212, 255, 0.2);
        color: #00d4ff; font-size: 0.75rem; font-weight: 700;
        letter-spacing: 1px; text-transform: uppercase; margin-bottom: 14px;
    }

    .who-i-am-title {
        font-size: 2.3rem; font-weight: 900; color: #ffffff;
        margin-bottom: 14px; letter-spacing: -0.5px; line-height: 1.1;
    }
    .who-i-am-title-accent {
        background: linear-gradient(135deg, #00d4ff 0%, #a855f7 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }

    .who-i-am-desc {
        color: #94a3b8; font-size: 0.96rem; line-height: 1.8;
        max-width: 620px;
    }

    .who-i-am-graphic {
        position: absolute; right: 20px; top: 20px; width: 140px; height: 110px;
        pointer-events: none; opacity: 0.85;
    }

    .edu-card-3d {
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.08) 0%, rgba(13, 14, 28, 0.85) 100%);
        border: 1.5px solid rgba(0, 212, 255, 0.25);
        border-radius: 22px; padding: 24px 28px;
        margin-bottom: 28px; backdrop-filter: blur(16px);
        display: flex; align-items: center; justify-content: space-between;
        transition: border-color 0.3s ease, box-shadow 0.3s ease;
    }
    .edu-card-3d:hover {
        border-color: rgba(0, 212, 255, 0.5);
        box-shadow: 0 8px 30px rgba(0, 212, 255, 0.15);
    }

    .edu-left-group { display: flex; align-items: center; gap: 18px; }
    .edu-icon-3d {
        width: 52px; height: 52px; border-radius: 16px;
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.2), rgba(168, 85, 247, 0.2));
        border: 1px solid rgba(0, 212, 255, 0.4);
        display: flex; align-items: center; justify-content: center;
        font-size: 1.6rem; flex-shrink: 0;
    }
    .edu-header-label { font-size: 0.72rem; color: #00d4ff; font-weight: 700; text-transform: uppercase; letter-spacing: 1.2px; margin-bottom: 4px; }
    .edu-degree-text  { font-size: 1.15rem; font-weight: 800; color: #ffffff; margin-bottom: 3px; }
    .edu-college-text { font-size: 0.86rem; color: #94a3b8; margin-bottom: 8px; }
    .edu-meta-badges  { display: flex; gap: 12px; font-size: 0.78rem; color: #94a3b8; }
    .edu-meta-badge   { background: rgba(255,255,255,0.05); padding: 3px 10px; border-radius: 50px; border: 1px solid rgba(255,255,255,0.1); }
    .edu-meta-badge span { color: #00d4ff; font-weight: 700; }

    .interests-section-3d { margin-top: 10px; }
    .interests-title-3d {
        font-size: 1.15rem; font-weight: 800; color: #f8fafc;
        margin-bottom: 16px; display: flex; align-items: center; gap: 8px;
    }

    .interest-pills-grid-3d {
        display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px;
    }

    .interest-pill-3d {
        background: rgba(13, 14, 28, 0.75);
        border-radius: 50px; padding: 10px 18px;
        font-size: 0.84rem; font-weight: 700; color: #ffffff;
        display: flex; align-items: center; gap: 10px;
        transition: all 0.25s ease; backdrop-filter: blur(12px);
    }
    .interest-pill-3d:hover {
        transform: translateY(-3px) scale(1.03);
        filter: brightness(1.2);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
    }

    @media (max-width: 992px) {
        .interest-pills-grid-3d { grid-template-columns: repeat(2, 1fr); }
        .who-i-am-graphic { display: none; }
    }
    @media (max-width: 576px) {
        .interest-pills-grid-3d { grid-template-columns: 1fr; }
    }

    /* Light Theme Overrides */
    .light-theme .about-profile-card-3d,
    .light-theme .who-i-am-card-3d,
    .light-theme .edu-card-3d {
        background: rgba(255, 255, 255, 0.92) !important;
        border-color: rgba(0, 0, 0, 0.1) !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.06) !important;
    }
    .light-theme .about-profile-name,
    .light-theme .about-stat-val,
    .light-theme .who-i-am-title,
    .light-theme .edu-degree-text,
    .light-theme .interests-title-3d {
        color: #0f172a !important;
    }
    .light-theme .about-profile-role,
    .light-theme .about-stat-lbl,
    .light-theme .who-i-am-desc,
    .light-theme .edu-college-text,
    .light-theme .edu-meta-badges {
        color: #475569 !important;
    }
    .light-theme .interest-pill-3d {
        background: rgba(255, 255, 255, 0.95) !important;
        color: #0f172a !important;
        border-color: rgba(0, 0, 0, 0.12) !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05) !important;
    }
    .light-theme .social-icon-btn-3d {
        background: rgba(0, 0, 0, 0.04) !important;
        border-color: rgba(0, 0, 0, 0.12) !important;
        color: #00d4ff !important;
    }
    .light-theme .social-icon-btn-3d:hover {
        background: rgba(0, 212, 255, 0.15) !important;
        color: #0f172a !important;
    }
    .light-theme .about-stats-row-3d {
        border-top-color: rgba(0, 0, 0, 0.08) !important;
        border-bottom-color: rgba(0, 0, 0, 0.08) !important;
    }
    .light-theme .edu-header-label {
        color: #0284c7 !important;
    }
    .light-theme .edu-meta-badge span {
        color: #0284c7 !important;
    }
    """

    inject_html(f"<style>{css}</style>")
    inject_html('<div id="about"></div>')

    # Resume button link
    resume_link = get_download_link(resume_path, "Download Resume", "Kartikey_Gupta_Resume.pdf")
    if resume_link:
        resume_btn_html = resume_link.replace(
            'class="btn-primary"',
            'class="btn-resume-3d"'
        ).replace('Download Resume', '📥 Download Resume &nbsp;&gt;')
    else:
        resume_btn_html = '<span class="btn-resume-disabled-3d">📄 Resume (upload in admin)</span>'

    img_tag = get_img_tag(img_path, alt=name)
    college_display = college if not is_placeholder(college) else "College name (update in admin)"

    # Build Social Links HTML
    social_html = ""
    if not is_placeholder(linkedin):
        social_html += f'<a href="{linkedin}" target="_blank" class="social-icon-btn-3d" title="LinkedIn">in</a>'
    else:
        social_html += '<span class="social-icon-btn-3d" style="opacity:0.4;">in</span>'

    if not is_placeholder(github):
        social_html += f'<a href="{github}" target="_blank" class="social-icon-btn-3d" title="GitHub">&#128025;</a>'
    else:
        social_html += '<span class="social-icon-btn-3d" style="opacity:0.4;">&#128025;</span>'

    if instagram and not is_placeholder(instagram):
        social_html += f'<a href="{instagram}" target="_blank" class="social-icon-btn-3d" title="Instagram">&#128247;</a>'
    else:
        social_html += '<span class="social-icon-btn-3d" style="opacity:0.4;">&#128247;</span>'

    if not is_placeholder(email):
        social_html += f'<a href="mailto:{email}" class="social-icon-btn-3d" title="Email">&#128231;</a>'
    else:
        social_html += '<span class="social-icon-btn-3d" style="opacity:0.4;">&#128231;</span>'

    # Build Areas of Interest HTML matching img3.jpeg
    if interests_raw and len(interests_raw) > 0:
        display_interests = []
        for i, item_name in enumerate(interests_raw):
            color = INTEREST_ITEMS[i % len(INTEREST_ITEMS)]["color"]
            icon  = INTEREST_ITEMS[i % len(INTEREST_ITEMS)]["icon"]
            display_interests.append({"name": item_name, "icon": icon, "color": color})
    else:
        display_interests = INTEREST_ITEMS

    interests_html = "".join(
        f'<div class="interest-pill-3d" style="border: 1.5px solid {item["color"]}; box-shadow: 0 0 15px rgba(0,0,0,0.3), 0 0 10px {item["color"]}22;">'
        f'<span style="font-size:1.1rem;">{item["icon"]}</span>'
        f'<span>{item["name"]}</span>'
        f'</div>'
        for item in display_interests
    )

    col_left, col_right = st.columns([1, 2], gap="large")

    # LEFT COLUMN: Profile Card
    with col_left:
        inject_html(f"""
        <div class="about-profile-card-3d">
            <div class="about-img-wrap-3d">{img_tag}</div>
            <div class="about-profile-name">{name}</div>
            <div class="about-profile-role">{role}</div>
            <div class="about-stats-row-3d">
                <div class="about-stat-item">
                    <div class="about-stat-val">{grad}</div>
                    <div class="about-stat-lbl">Graduation</div>
                </div>
                <div class="about-stat-item">
                    <div class="about-stat-val">{sgpa}</div>
                    <div class="about-stat-lbl">SGPA</div>
                </div>
                <div class="about-stat-item">
                    <div class="about-stat-val">2+</div>
                    <div class="about-stat-lbl">Internships</div>
                </div>
            </div>
            <div class="social-icons-row-3d">
                {social_html}
            </div>
            {resume_btn_html}
        </div>
        """)

    # RIGHT COLUMN: Content Side
    with col_right:
        inject_html(f"""
        <div class="who-i-am-card-3d">
            <div class="about-pill-badge">👤 About Me</div>
            <h2 class="who-i-am-title">Who I am and <span class="who-i-am-title-accent">what I do</span></h2>
            <p class="who-i-am-desc">{bio}</p>
            <div class="who-i-am-graphic">
                <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="#00d4ff" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="filter: drop-shadow(0 0 12px rgba(0,212,255,0.6));">
                    <rect x="2" y="3" width="20" height="14" rx="2" ry="2"/>
                    <line x1="8" y1="21" x2="16" y2="21"/>
                    <line x1="12" y1="17" x2="12" y2="21"/>
                    <polyline points="7 8 10 11 7 14"/>
                    <line x1="13" y1="14" x2="17" y2="14"/>
                </svg>
            </div>
        </div>

        <div class="edu-card-3d">
            <div class="edu-left-group">
                <div class="edu-icon-3d">🎓</div>
                <div>
                    <div class="edu-header-label">Education</div>
                    <div class="edu-degree-text">B.Tech &mdash; Computer Science &amp; Engineering</div>
                    <div class="edu-college-text">{college_display}</div>
                    <div class="edu-meta-badges">
                        <div class="edu-meta-badge">Graduating: <span>{grad}</span></div>
                        <div class="edu-meta-badge">SGPA: <span>{sgpa}</span></div>
                    </div>
                </div>
            </div>
            <div style="font-size: 1.4rem; color: #00d4ff; opacity: 0.8;">&gt;</div>
        </div>

        <div class="interests-section-3d">
            <div class="interests-title-3d">💡 Areas of Interest</div>
            <div class="interest-pills-grid-3d">
                {interests_html}
            </div>
        </div>
        """)

