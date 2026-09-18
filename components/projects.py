"""
components/projects.py
======================
Project showcase matching reference img2.jpeg 3D neon glassmorphism design.
"""

import streamlit as st

from utils.data_manager import load_projects
from utils.helpers import inject_html, get_img_tag


CATEGORY_COLORS = {
    "AI/ML":            "#d946ef",
    "Web Development":  "#00d4ff",
    "Java":             "#f59e0b",
    "Python":           "#10b981",
    "Other":            "#a855f7",
}


def _hex_to_rgb(hex_color: str):
    try:
        h = hex_color.lstrip("#")
        return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    except Exception:
        return 0, 212, 255


def render_projects():
    """Render the Projects section with 3D glassmorphic UI matching img2.jpeg."""
    data     = load_projects()
    projects = data.get("projects", [])

    css = """
    #projects { scroll-margin-top: 80px; padding-bottom: 50px; position: relative; }

    .projects-header-container {
        position: relative;
        margin-bottom: 28px;
    }

    .projects-badge {
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

    .projects-title {
        font-size: 2.5rem;
        font-weight: 900;
        color: #ffffff;
        margin-bottom: 8px;
        letter-spacing: -0.5px;
        line-height: 1.1;
    }

    .projects-title-accent {
        background: linear-gradient(135deg, #a855f7 0%, #00d4ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .projects-subtitle {
        color: #94a3b8;
        font-size: 0.95rem;
        max-width: 580px;
        line-height: 1.6;
    }

    .proj-handwritten {
        position: absolute;
        right: 180px;
        top: 15px;
        font-family: 'Caveat', 'Dancing Script', 'Segoe Script', cursive;
        font-size: 1.45rem;
        color: #a855f7;
        transform: rotate(-3deg);
        opacity: 0.9;
        text-shadow: 0 0 10px rgba(168, 85, 247, 0.4);
        letter-spacing: 1px;
    }

    .project-card-3d {
        background: rgba(13, 14, 28, 0.75);
        border-radius: 22px;
        overflow: hidden;
        border: 1.5px solid rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(16px);
        transition: transform 0.35s ease, box-shadow 0.35s ease, border-color 0.35s ease;
        margin-bottom: 24px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: calc(100% - 24px);
    }

    .project-card-3d:hover {
        transform: translateY(-8px);
    }

    .project-img-wrap-3d {
        width: 100%;
        height: 180px;
        overflow: hidden;
        position: relative;
        background: linear-gradient(135deg, #0d1117, #1a1a2e);
    }

    .project-img-wrap-3d img {
        width: 100%; height: 100%; object-fit: cover;
        transition: transform 0.5s ease;
    }

    .project-card-3d:hover .project-img-wrap-3d img {
        transform: scale(1.08);
    }

    .project-img-wrap-3d .img-placeholder {
        width: 100%; height: 180px; display: flex;
        align-items: center; justify-content: center; font-size: 3rem;
        background: linear-gradient(135deg, #0d1117, #1a1a2e);
    }

    .cat-tag-3d {
        position: absolute; top: 12px; right: 12px;
        padding: 4px 13px; border-radius: 50px;
        font-size: 0.7rem; font-weight: 700; letter-spacing: 0.5px;
        backdrop-filter: blur(8px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }

    .project-body-3d { padding: 20px; flex: 1; display: flex; flex-direction: column; justify-content: space-between; }
    .project-name-3d {
        font-size: 1.1rem; font-weight: 800; color: #f8fafc;
        margin-bottom: 8px; line-height: 1.3;
    }
    .project-desc-3d {
        font-size: 0.82rem; color: #94a3b8; line-height: 1.6;
        margin-bottom: 14px;
        display: -webkit-box; -webkit-line-clamp: 3;
        -webkit-box-orient: vertical; overflow: hidden;
    }
    .tech-badges-3d { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 18px; }
    .tech-badge-3d {
        padding: 4px 11px; border-radius: 50px; font-size: 0.72rem; font-weight: 600;
        background: rgba(0,212,255,0.08); color: #00d4ff;
        border: 1px solid rgba(0,212,255,0.22);
    }

    .project-actions-3d { display: flex; gap: 10px; }
    .proj-btn-3d {
        flex: 1; padding: 10px 0; border-radius: 12px;
        font-size: 0.78rem; font-weight: 700;
        text-decoration: none; text-align: center;
        transition: all 0.25s ease; border: none; cursor: pointer;
        display: block;
    }
    .proj-btn-gh-3d {
        background: rgba(255,255,255,0.06); color: #e2e8f0;
        border: 1px solid rgba(255,255,255,0.14);
    }
    .proj-btn-gh-3d:hover { background: rgba(255,255,255,0.14); transform: translateY(-2px); color: #ffffff; }
    .proj-btn-demo-3d {
        background: linear-gradient(135deg, #00d4ff 0%, #a855f7 100%);
        color: #ffffff; box-shadow: 0 4px 15px rgba(0, 212, 255, 0.35);
    }
    .proj-btn-demo-3d:hover { transform: translateY(-2px); filter: brightness(1.15); box-shadow: 0 6px 20px rgba(0, 212, 255, 0.5); }
    .proj-btn-disabled-3d { opacity: 0.35; cursor: not-allowed; pointer-events: none; }

    @media (max-width: 768px) {
        .proj-handwritten { display: none; }
        .projects-title { font-size: 1.9rem; }
    }

    /* Light Theme Overrides */
    .light-theme .project-card-3d {
        background: rgba(255, 255, 255, 0.92) !important;
        border-color: rgba(0, 0, 0, 0.1) !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.06) !important;
    }
    .light-theme .projects-title,
    .light-theme .project-name-3d {
        color: #0f172a !important;
    }
    .light-theme .projects-subtitle,
    .light-theme .project-desc-3d {
        color: #475569 !important;
    }
    .light-theme .projects-badge {
        background: rgba(0, 0, 0, 0.04) !important;
        border-color: rgba(0, 0, 0, 0.12) !important;
        color: #00d4ff !important;
    }
    .light-theme .proj-btn-gh-3d {
        background: rgba(0, 0, 0, 0.05) !important;
        border-color: rgba(0, 0, 0, 0.15) !important;
        color: #0f172a !important;
    }
    .light-theme .proj-btn-gh-3d:hover {
        background: rgba(0, 0, 0, 0.1) !important;
    }
    .light-theme .tech-badge-3d {
        background: rgba(0, 212, 255, 0.1) !important;
        border-color: rgba(0, 212, 255, 0.3) !important;
        color: #0284c7 !important;
    }
    .light-theme .proj-handwritten {
        color: #7e22ce !important;
    }
    """

    inject_html(f"<style>{css}</style>")
    inject_html('<div id="projects"></div>')

    # Render Header section matching img2.jpeg style
    header_html = """
    <div class="projects-header-container">
        <div class="projects-badge">MY WORK</div>
        <h2 class="projects-title">Featured <span class="projects-title-accent">Projects</span></h2>
        <p class="projects-subtitle">Innovative software solutions, AI models, and web applications I've designed and engineered.</p>
        <div class="proj-handwritten">Ideas &rarr; Code &rarr; Reality</div>
    </div>
    """
    inject_html(header_html)

    if not projects:
        inject_html('<p style="color:#64748b;text-align:center;padding:60px;">No projects yet. Add them via the admin panel.</p>')
        return

    # Filter bar
    all_cats    = sorted(set(p.get("category", "Other") for p in projects))
    filter_opts = ["All"] + all_cats
    chosen = st.radio(
        "Filter:",
        filter_opts,
        horizontal=True,
        label_visibility="collapsed",
        key="project_filter",
    )

    filtered = [p for p in projects if chosen == "All" or p.get("category") == chosen]

    if not filtered:
        inject_html(f'<p style="color:#64748b;text-align:center;padding:40px;">No {chosen} projects found.</p>')
        return

    is_ph = lambda v: not v or str(v).strip().startswith("[PLACEHOLDER")

    # Render cards in rows of 3 columns
    COLS_PER_ROW = 3
    for row_start in range(0, len(filtered), COLS_PER_ROW):
        row_projs = filtered[row_start : row_start + COLS_PER_ROW]
        cols = st.columns(len(row_projs))

        for col, proj in zip(cols, row_projs):
            pid      = proj.get("id", 0)
            name     = proj.get("name", "Untitled")
            desc     = proj.get("description", "")
            techs    = proj.get("technologies", [])
            category = proj.get("category", "Other")
            github   = proj.get("github", "")
            demo     = proj.get("demo", "")
            img_path = proj.get("image", "")

            fg_color = CATEGORY_COLORS.get(category, "#a855f7")
            r, g, b  = _hex_to_rgb(fg_color)

            img_html = get_img_tag(img_path, alt=name)
            cat_tag  = (f'<span class="cat-tag-3d" '
                        f'style="background:rgba({r},{g},{b},0.25);color:#ffffff;border:1px solid rgba({r},{g},{b},0.4);">'
                        f'{category}</span>')

            tech_pills = "".join(f'<span class="tech-badge-3d">{t}</span>' for t in techs[:5])

            gh_btn   = (f'<a href="{github}" target="_blank" class="proj-btn-3d proj-btn-gh-3d">&#128025; GitHub</a>'
                        if not is_ph(github)
                        else '<span class="proj-btn-3d proj-btn-gh-3d proj-btn-disabled-3d">&#128025; GitHub</span>')
            demo_btn = (f'<a href="{demo}" target="_blank" class="proj-btn-3d proj-btn-demo-3d">&#128640; Live Demo</a>'
                        if not is_ph(demo)
                        else '<span class="proj-btn-3d proj-btn-demo-3d proj-btn-disabled-3d">&#128640; Live Demo</span>')

            border_style = f"border-color: rgba({r},{g},{b},0.35); box-shadow: 0 10px 30px rgba(0,0,0,0.4), 0 0 20px rgba({r},{g},{b},0.15);"

            with col:
                inject_html(f"""
                <div class="project-card-3d" id="project-{pid}" style="{border_style}">
                    <div class="project-img-wrap-3d">
                        {img_html}
                        {cat_tag}
                    </div>
                    <div class="project-body-3d">
                        <div>
                            <div class="project-name-3d">{name}</div>
                            <div class="project-desc-3d">{desc}</div>
                        </div>
                        <div>
                            <div class="tech-badges-3d">{tech_pills}</div>
                            <div class="project-actions-3d">{gh_btn}{demo_btn}</div>
                        </div>
                    </div>
                </div>
                """)

