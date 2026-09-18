"""
components/skills.py
====================
Technical Skills section matching reference img2.jpeg layout with 3D glowing cards,
category icon boxes, skill count badges, handwritten annotations, and custom neon themes.
"""

import streamlit as st

from utils.data_manager import load_skills
from utils.helpers import inject_html


# Category metadata mapping (Colors, 3D Icons, Descriptions)
CATEGORY_META = {
    "Programming Languages": {
        "color": "#00d4ff",
        "secondary_color": "#0072ff",
        "icon_svg": """<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="#00d4ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="2" y="3" width="20" height="14" rx="2" ry="2"/>
            <line x1="8" y1="21" x2="16" y2="21"/>
            <line x1="12" y1="17" x2="12" y2="21"/>
            <polyline points="7 8 10 11 7 14"/>
            <line x1="13" y1="14" x2="17" y2="14"/>
        </svg>""",
        "description": "Core languages I use to build logic and solve real-world problems.",
    },
    "Frontend Development": {
        "color": "#a855f7",
        "secondary_color": "#ec4899",
        "icon_svg": """<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="#a855f7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="2" y="3" width="20" height="14" rx="2" ry="2"/>
            <line x1="8" y1="21" x2="16" y2="21"/>
            <line x1="12" y1="17" x2="12" y2="21"/>
            <polyline points="8 10 6 12 8 14"/>
            <polyline points="16 10 18 12 16 14"/>
        </svg>""",
        "description": "Building responsive and interactive user interfaces for modern web.",
    },
    "Backend Development": {
        "color": "#06b6d4",
        "secondary_color": "#00f2fe",
        "icon_svg": """<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="#06b6d4" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="2" y="2" width="20" height="8" rx="2" ry="2"/>
            <rect x="2" y="14" width="20" height="8" rx="2" ry="2"/>
            <line x1="6" y1="6" x2="6.01" y2="6"/>
            <line x1="6" y1="18" x2="6.01" y2="18"/>
            <path d="M12 10v4"/>
        </svg>""",
        "description": "Building secure, scalable and efficient server-side applications.",
    },
    "Databases": {
        "color": "#f59e0b",
        "secondary_color": "#f97316",
        "icon_svg": """<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <ellipse cx="12" cy="5" rx="9" ry="3"/>
            <path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/>
            <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/>
        </svg>""",
        "description": "Managing and querying data for powerful applications.",
    },
    "AI / ML": {
        "color": "#d946ef",
        "secondary_color": "#8b5cf6",
        "icon_svg": """<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="#d946ef" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2zm0 16a6 6 0 1 1 6-6 6 6 0 0 1-6 6z"/>
            <circle cx="12" cy="12" r="3"/>
        </svg>""",
        "description": "Building intelligent systems that learn and predict.",
    },
    "Tools & Platforms": {
        "color": "#3b82f6",
        "secondary_color": "#06b6d4",
        "icon_svg": """<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>
        </svg>""",
        "description": "Tools that help me code, collaborate and deploy applications.",
    },
}


def render_skills():
    """Render Technical Skills matching img2.jpeg design."""
    skills_data = load_skills()
    categories = skills_data.get("categories", [])

    css = """
    #skills { scroll-margin-top: 80px; padding-bottom: 50px; position: relative; }

    .skills-header-container {
        position: relative;
        margin-bottom: 35px;
    }

    .skills-badge {
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

    .skills-title {
        font-size: 2.5rem;
        font-weight: 900;
        color: #ffffff;
        margin-bottom: 8px;
        letter-spacing: -0.5px;
        line-height: 1.1;
    }

    .skills-title-accent {
        background: linear-gradient(135deg, #00d4ff 0%, #a855f7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .skills-subtitle {
        color: #94a3b8;
        font-size: 0.95rem;
        max-width: 580px;
        line-height: 1.6;
    }

    .handwritten-annotation {
        position: absolute;
        right: 180px;
        top: 15px;
        font-family: 'Caveat', 'Dancing Script', 'Segoe Script', cursive;
        font-size: 1.45rem;
        color: #00d4ff;
        transform: rotate(-4deg);
        opacity: 0.9;
        text-shadow: 0 0 10px rgba(0, 212, 255, 0.4);
        letter-spacing: 1px;
    }

    .header-3d-graphic {
        position: absolute;
        right: 10px;
        top: -15px;
        width: 140px;
        height: 110px;
        background: radial-gradient(circle at center, rgba(0, 212, 255, 0.15) 0%, transparent 70%);
        border-radius: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        pointer-events: none;
    }

    .skill-card-img2 {
        background: rgba(13, 14, 28, 0.75);
        border-radius: 22px;
        padding: 24px;
        border: 1.5px solid rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(16px);
        transition: transform 0.35s ease, box-shadow 0.35s ease, border-color 0.35s ease;
        margin-bottom: 24px;
        height: calc(100% - 24px);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        position: relative;
        overflow: hidden;
    }

    .skill-card-img2::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.15), transparent);
    }

    .skill-card-img2:hover {
        transform: translateY(-7px);
    }

    .card-top-row {
        display: flex;
        align-items: flex-start;
        gap: 16px;
        margin-bottom: 18px;
        position: relative;
    }

    .icon-box-3d {
        width: 58px;
        height: 58px;
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        position: relative;
        box-shadow: inset 0 0 15px rgba(255, 255, 255, 0.05), 0 8px 20px rgba(0, 0, 0, 0.4);
    }

    .card-title-group {
        flex: 1;
    }

    .card-category-name {
        font-size: 1.12rem;
        font-weight: 800;
        color: #f8fafc;
        margin-bottom: 4px;
        letter-spacing: -0.2px;
    }

    .card-category-desc {
        font-size: 0.78rem;
        color: #94a3b8;
        line-height: 1.45;
    }

    .count-badge-img2 {
        padding: 3px 10px;
        border-radius: 50px;
        font-size: 0.65rem;
        font-weight: 700;
        background: rgba(255, 255, 255, 0.05);
        color: #cbd5e1;
        border: 1px solid rgba(255, 255, 255, 0.1);
        white-space: nowrap;
        height: fit-content;
    }

    .pills-container-img2 {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 12px;
    }

    .pill-item-img2 {
        padding: 7px 14px;
        border-radius: 50px;
        font-size: 0.8rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 6px;
        transition: all 0.25s ease;
        backdrop-filter: blur(8px);
    }

    .pill-item-img2:hover {
        transform: translateY(-2px) scale(1.04);
        filter: brightness(1.25);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }

    @media (max-width: 768px) {
        .handwritten-annotation { display: none; }
        .header-3d-graphic { display: none; }
        .skills-title { font-size: 1.9rem; }
    }

    /* Light Theme Overrides */
    .light-theme .skill-card-img2 {
        background: rgba(255, 255, 255, 0.92) !important;
        border-color: rgba(0, 0, 0, 0.1) !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.06) !important;
    }
    .light-theme .skills-title,
    .light-theme .card-category-name,
    .light-theme .skill-count-num {
        color: #0f172a !important;
    }
    .light-theme .skills-subtitle,
    .light-theme .card-category-desc,
    .light-theme .skill-count-label {
        color: #475569 !important;
    }
    .light-theme .skills-badge {
        background: rgba(0, 0, 0, 0.04) !important;
        border-color: rgba(0, 0, 0, 0.12) !important;
        color: #0284c7 !important;
    }
    .light-theme .pill-item-img2 {
        background: rgba(0, 0, 0, 0.04) !important;
        color: #1e293b !important;
        border: 1px solid rgba(0, 0, 0, 0.08) !important;
    }
    .light-theme .handwritten-annotation {
        color: #0284c7 !important;
    }
    """

    inject_html(f"<style>{css}</style>")
    inject_html('<div id="skills"></div>')

    # Render Header section matching img2.jpeg
    header_html = """
    <div class="skills-header-container">
        <div class="skills-badge">MY SKILLS</div>
        <h2 class="skills-title">Technical <span class="skills-title-accent">Skills</span></h2>
        <p class="skills-subtitle">Technologies I work with to build scalable, intelligent and modern web applications.</p>
        <div class="handwritten-annotation">Code &rarr; Build &rarr; Grow</div>
        <div class="header-3d-graphic">
            <svg width="70" height="70" viewBox="0 0 24 24" fill="none" stroke="#00d4ff" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="filter: drop-shadow(0 0 12px rgba(0,212,255,0.6));">
                <rect x="2" y="3" width="20" height="14" rx="2" ry="2"/>
                <line x1="8" y1="21" x2="16" y2="21"/>
                <line x1="12" y1="17" x2="12" y2="21"/>
                <polyline points="7 8 10 11 7 14"/>
                <line x1="13" y1="14" x2="17" y2="14"/>
            </svg>
        </div>
    </div>
    """
    inject_html(header_html)

    if not categories:
        inject_html('<p style="color:#64748b;text-align:center;padding:40px;">No skills added yet. Use the admin panel to add skills.</p>')
        return

    # Render Category Cards in rows of 3 columns
    COLS_PER_ROW = 3
    for row_start in range(0, len(categories), COLS_PER_ROW):
        row_cats = categories[row_start : row_start + COLS_PER_ROW]
        cols = st.columns(len(row_cats))

        for col, cat in zip(cols, row_cats):
            cat_name = cat.get("name", "")
            skills   = cat.get("skills", [])

            # Meta config or fallback
            meta = CATEGORY_META.get(cat_name, {
                "color": cat.get("color", "#00d4ff"),
                "secondary_color": "#a855f7",
                "icon_svg": f'<span style="font-size:1.8rem;">{cat.get("icon", "🔧")}</span>',
                "description": f"Technologies and tools for {cat_name.lower()}.",
            })

            accent_color = meta["color"]
            sec_color    = meta.get("secondary_color", accent_color)
            icon_svg     = meta["icon_svg"]
            description  = meta["description"]

            # Parse hex to RGB
            try:
                hex_c = accent_color.lstrip("#")
                r, g, b = int(hex_c[0:2], 16), int(hex_c[2:4], 16), int(hex_c[4:6], 16)
            except Exception:
                r, g, b = 0, 212, 255

            # Skill pills HTML
            pills_html = "".join(
                f'<span class="pill-item-img2" style="'
                f'background: rgba({r}, {g}, {b}, 0.12); '
                f'color: #ffffff; '
                f'border: 1px solid rgba({r}, {g}, {b}, 0.3);">'
                f'<span style="display:inline-block; width:6px; height:6px; border-radius:50%; background:{accent_color}; box-shadow:0 0 8px {accent_color};"></span>'
                f'{skill}</span>'
                for skill in skills
            )

            border_style = f"border-color: rgba({r}, {g}, {b}, 0.35); box-shadow: 0 10px 30px rgba(0,0,0,0.4), 0 0 20px rgba({r}, {g}, {b}, 0.15);"
            icon_box_bg  = f"background: linear-gradient(135deg, rgba({r},{g},{b},0.2) 0%, rgba(13,14,28,0.8) 100%); border: 1px solid rgba({r},{g},{b},0.4);"

            with col:
                inject_html(f"""
                <div class="skill-card-img2" style="{border_style}">
                    <div>
                        <div class="card-top-row">
                            <div class="icon-box-3d" style="{icon_box_bg}">
                                {icon_svg}
                            </div>
                            <div class="card-title-group">
                                <div class="card-category-name">{cat_name}</div>
                                <div class="card-category-desc">{description}</div>
                            </div>
                            <div class="count-badge-img2">📊 {len(skills)}+ Skills</div>
                        </div>
                    </div>
                    <div class="pills-container-img2">
                        {pills_html}
                    </div>
                </div>
                """)

