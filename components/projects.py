"""
components/projects.py
======================
Project showcase matching reference img2.jpeg 3D neon glassmorphism design.
"""

import streamlit as st

from utils.data_manager import load_projects
from utils.helpers import inject_html, get_img_tag


CATEGORY_COLORS = {
    "AI/ML":                    "#d946ef",
    "Web Development":          "#00d4ff",
    "Java":                     "#f59e0b",
    "Python":                   "#10b981",
    "Data Analysis Dashboard":  "#f97316",
    "Other":                    "#a855f7",
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

    /* ── Filter Pills ──────────────────────────────────────────── */
    .proj-filter-bar {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-bottom: 28px;
    }
    .proj-filter-pill {
        padding: 7px 20px;
        border-radius: 50px;
        font-size: 0.80rem;
        font-weight: 700;
        cursor: pointer;
        border: 1.5px solid rgba(255, 255, 255, 0.15);
        background: rgba(255, 255, 255, 0.06);
        color: #cbd5e1;
        transition: all 0.22s ease;
        user-select: none;
        letter-spacing: 0.3px;
    }
    .proj-filter-pill:hover {
        border-color: rgba(0, 212, 255, 0.45);
        background: rgba(0, 212, 255, 0.12);
        color: #00d4ff;
        transform: translateY(-1px);
        box-shadow: 0 4px 14px rgba(0, 212, 255, 0.2);
    }
    .proj-filter-pill.active {
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.3), rgba(168, 85, 247, 0.3));
        border-color: #00d4ff;
        color: #ffffff;
        box-shadow: 0 4px 16px rgba(0, 212, 255, 0.35);
    }

    /* Light Theme Overrides — Filter Pills */
    .light-theme .proj-filter-pill {
        background: rgba(255, 255, 255, 0.9) !important;
        border: 1.5px solid rgba(0, 0, 0, 0.12) !important;
        color: #334155 !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06) !important;
    }
    .light-theme .proj-filter-pill:hover {
        border-color: rgba(2, 132, 199, 0.5) !important;
        background: rgba(2, 132, 199, 0.1) !important;
        color: #0284c7 !important;
        box-shadow: 0 4px 14px rgba(2, 132, 199, 0.18) !important;
    }
    .light-theme .proj-filter-pill.active {
        background: linear-gradient(135deg, rgba(2, 132, 199, 0.18), rgba(126, 34, 206, 0.18)) !important;
        border-color: #0284c7 !important;
        color: #0284c7 !important;
        box-shadow: 0 4px 16px rgba(2, 132, 199, 0.25) !important;
    }

    /* Light Theme Overrides — Cards */
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
        color: #0284c7 !important;
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
        background: rgba(2, 132, 199, 0.08) !important;
        border-color: rgba(2, 132, 199, 0.25) !important;
        color: #0284c7 !important;
    }
    .light-theme .proj-handwritten {
        color: #7e22ce !important;
    }
    .light-theme .project-img-wrap-3d {
        background: linear-gradient(135deg, #e2e8f0, #f1f5f9) !important;
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

    # Filter bar — custom HTML pills
    all_cats    = sorted(set(p.get("category", "Other") for p in projects))
    filter_opts = ["All"] + all_cats

    # Inject only the pill HTML (no script here — st.markdown strips scripts)
    pills_html = '<div class="proj-filter-bar">'
    for opt in filter_opts:
        pills_html += f'<span class="proj-filter-pill" data-filter="{opt}">{opt}</span>'
    pills_html += '</div>'
    inject_html(pills_html)

    # Inject the JS via components.html so it actually executes
    import streamlit.components.v1 as components
    components.html("""
    <script>
    (function() {
        function setupFilterPills() {
            try {
                var pDoc = window.parent ? window.parent.document : document;
                var pills = pDoc.querySelectorAll('.proj-filter-pill');
                if (!pills.length || pills[0].__filterBound) return;
                pills.forEach(function(p) { p.__filterBound = true; });

                var hasActive = Array.from(pills).some(function(p) { return p.classList.contains('active'); });
                if (!hasActive && pills[0]) pills[0].classList.add('active');

                pills.forEach(function(pill) {
                    pill.addEventListener('click', function() {
                        pills.forEach(function(p) { p.classList.remove('active'); });
                        pill.classList.add('active');
                        var filter = pill.getAttribute('data-filter');
                        var cards = pDoc.querySelectorAll('[data-proj-cat]');
                        cards.forEach(function(card) {
                            if (filter === 'All' || card.getAttribute('data-proj-cat') === filter) {
                                card.style.display = '';
                            } else {
                                card.style.display = 'none';
                            }
                        });
                    });
                });
            } catch(e) {}
        }
        var _interval = setInterval(setupFilterPills, 300);
        setTimeout(function() { clearInterval(_interval); }, 10000);
    })();
    </script>
    """, height=0, width=0)

    filtered = projects  # render all; JS hides/shows based on filter click

    is_ph = lambda v: not v or str(v).strip().startswith("[PLACEHOLDER")

    # ── Build all project data as JSON for the modal ──────────────────────────
    import json as _json
    projects_json = _json.dumps([
        {
            "id":          p.get("id", i),
            "name":        p.get("name", "Untitled"),
            "description": p.get("description", ""),
            "category":    p.get("category", "Other"),
            "technologies":p.get("technologies", []),
            "github":      p.get("github", ""),
            "demo":        p.get("demo", ""),
            "image":       p.get("image", ""),
            "featured":    p.get("featured", False),
        }
        for i, p in enumerate(projects)
    ], ensure_ascii=False)

    # ── Render cards in rows of 3 columns ────────────────────────────────────
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
                <div class="project-card-3d" id="project-{pid}" data-proj-cat="{category}"
                     data-proj-id="{pid}" style="{border_style}; cursor:pointer;">
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

    # ── Inject modal overlay + JS via components.html ─────────────────────────
    import streamlit.components.v1 as components
    components.html(f"""
    <script>
    (function() {{
        var PROJECTS = {projects_json};
        var CAT_COLORS = {_json.dumps(CATEGORY_COLORS)};

        function hexToRgb(hex) {{
            var r = parseInt(hex.slice(1,3),16), g = parseInt(hex.slice(3,5),16), b = parseInt(hex.slice(5,7),16);
            return r+','+g+','+b;
        }}

        function buildImgUrl(path) {{
            if (!path) return '';
            // Try to get image via parent window's base URL
            try {{
                var base = window.parent.location.href.split('?')[0].replace(/\\/$/, '');
                // Streamlit serves static files under /static/ — but user images are served differently.
                // Fallback: return path as-is (get_img_tag already embeds base64 for known paths).
            }} catch(e) {{}}
            return '';
        }}

        function openModal(projId) {{
            var pDoc = window.parent ? window.parent.document : document;
            var proj = PROJECTS.find(function(p) {{ return String(p.id) === String(projId); }});
            if (!proj) return;

            var color = CAT_COLORS[proj.category] || '#a855f7';
            var rgb   = hexToRgb(color);

            // Tech badges
            var techHTML = proj.technologies.slice(0,8).map(function(t) {{
                return '<span style="padding:5px 13px;border-radius:50px;font-size:0.78rem;font-weight:600;'+
                       'background:rgba('+rgb+',0.15);color:'+color+';border:1px solid rgba('+rgb+',0.35);">'+t+'</span>';
            }}).join('');

            // Buttons
            var ghBtn  = proj.github && !proj.github.startsWith('[PLACEHOLDER')
                ? '<a href="'+proj.github+'" target="_blank" rel="noopener" style="flex:1;padding:11px 0;border-radius:12px;font-size:0.82rem;font-weight:700;text-decoration:none;text-align:center;background:rgba(255,255,255,0.07);color:#e2e8f0;border:1px solid rgba(255,255,255,0.15);transition:all .2s;">&#128025; GitHub</a>'
                : '<span style="flex:1;padding:11px 0;border-radius:12px;font-size:0.82rem;font-weight:700;text-align:center;background:rgba(255,255,255,0.03);color:#475569;border:1px solid rgba(255,255,255,0.06);opacity:.45;">&#128025; GitHub</span>';
            var demoBtn = proj.demo && !proj.demo.startsWith('[PLACEHOLDER')
                ? '<a href="'+proj.demo+'" target="_blank" rel="noopener" style="flex:1;padding:11px 0;border-radius:12px;font-size:0.82rem;font-weight:700;text-decoration:none;text-align:center;background:linear-gradient(135deg,#00d4ff,#a855f7);color:#fff;box-shadow:0 4px 15px rgba(0,212,255,.4);transition:all .2s;">&#128640; Live Demo</a>'
                : '<span style="flex:1;padding:11px 0;border-radius:12px;font-size:0.82rem;font-weight:700;text-align:center;background:linear-gradient(135deg,rgba(0,212,255,.25),rgba(168,85,247,.25));color:#fff;opacity:.4;pointer-events:none;">&#128640; Live Demo</span>';

            // Image section
            var imgCardHTML = '';
            // Get the image from the existing card's img tag (already rendered by Python)
            var cardEl = pDoc.getElementById('project-'+projId);
            if (cardEl) {{
                var cardImg = cardEl.querySelector('.project-img-wrap-3d img');
                if (cardImg) {{
                    imgCardHTML = '<img src="'+cardImg.src+'" alt="'+proj.name+'" style="width:100%;max-height:340px;object-fit:cover;border-radius:16px;display:block;margin-bottom:22px;box-shadow:0 8px 30px rgba(0,0,0,0.5);"/>';
                }}
            }}
            if (!imgCardHTML) {{
                imgCardHTML = '<div style="width:100%;height:180px;border-radius:16px;background:linear-gradient(135deg,rgba('+rgb+',0.15),rgba(13,14,28,0.9));display:flex;align-items:center;justify-content:center;font-size:3rem;margin-bottom:22px;">🚀</div>';
            }}

            var featuredBadge = proj.featured
                ? '<span style="display:inline-block;padding:3px 12px;border-radius:50px;font-size:0.7rem;font-weight:700;background:rgba('+rgb+',0.2);color:'+color+';border:1px solid rgba('+rgb+',0.4);margin-left:8px;letter-spacing:.5px;">⭐ FEATURED</span>'
                : '';

            var modal = pDoc.getElementById('proj-modal-overlay');
            modal.querySelector('#proj-modal-inner').innerHTML = `
                ${{imgCardHTML}}
                <div style="display:flex;align-items:center;flex-wrap:wrap;gap:8px;margin-bottom:10px;">
                    <span style="font-size:1.45rem;font-weight:900;color:#f8fafc;line-height:1.2;">${{proj.name}}</span>
                    ${{featuredBadge}}
                    <span style="margin-left:auto;padding:4px 13px;border-radius:50px;font-size:0.72rem;font-weight:700;background:rgba(${{rgb}},0.25);color:#fff;border:1px solid rgba(${{rgb}},0.4);">${{proj.category}}</span>
                </div>
                <p style="color:#94a3b8;font-size:0.88rem;line-height:1.7;margin-bottom:18px;">${{proj.description || 'No description provided.'}}</p>
                <div style="display:flex;flex-wrap:wrap;gap:7px;margin-bottom:20px;">${{techHTML}}</div>
                <div style="display:flex;gap:12px;">${{ghBtn}}${{demoBtn}}</div>
            `;
            modal.style.display = 'flex';
            requestAnimationFrame(function() {{ modal.style.opacity = '1'; }});
        }}

        function closeModal() {{
            var pDoc = window.parent ? window.parent.document : document;
            var modal = pDoc.getElementById('proj-modal-overlay');
            if (modal) {{ modal.style.opacity = '0'; setTimeout(function() {{ modal.style.display='none'; }}, 260); }}
        }}

        function injectModal(pDoc) {{
            if (pDoc.getElementById('proj-modal-overlay')) return;
            var overlay = pDoc.createElement('div');
            overlay.id = 'proj-modal-overlay';
            overlay.style.cssText = [
                'display:none','position:fixed','inset:0','z-index:99999',
                'background:rgba(0,0,0,0.75)','backdrop-filter:blur(8px)',
                'align-items:center','justify-content:center',
                'padding:20px','opacity:0','transition:opacity .26s ease'
            ].join(';');
            overlay.innerHTML = `
                <div style="
                    position:relative;max-width:680px;width:100%;max-height:88vh;overflow-y:auto;
                    background:rgba(10,11,25,0.97);border:1.5px solid rgba(255,255,255,0.1);
                    border-radius:24px;padding:28px;
                    box-shadow:0 30px 80px rgba(0,0,0,0.7),0 0 40px rgba(0,212,255,0.08);
                    backdrop-filter:blur(20px);
                    scrollbar-width:thin;scrollbar-color:rgba(255,255,255,0.12) transparent;
                ">
                    <button id="proj-modal-close" style="
                        position:absolute;top:16px;right:16px;background:rgba(255,255,255,0.08);
                        border:1px solid rgba(255,255,255,0.15);color:#e2e8f0;
                        width:34px;height:34px;border-radius:50%;font-size:1.1rem;
                        cursor:pointer;display:flex;align-items:center;justify-content:center;
                        transition:all .2s;z-index:1;
                    ">✕</button>
                    <div id="proj-modal-inner"></div>
                </div>
            `;
            pDoc.body.appendChild(overlay);
            pDoc.getElementById('proj-modal-close').addEventListener('click', closeModal);
            overlay.addEventListener('click', function(e) {{ if(e.target === overlay) closeModal(); }});
            pDoc.addEventListener('keydown', function(e) {{ if(e.key==='Escape') closeModal(); }});
        }}

        function setupCards() {{
            try {{
                var pDoc = window.parent ? window.parent.document : document;
                injectModal(pDoc);

                // Filter pills
                var pills = pDoc.querySelectorAll('.proj-filter-pill');
                if (pills.length && !pills[0].__filterBound) {{
                    pills.forEach(function(p) {{ p.__filterBound = true; }});
                    var hasActive = Array.from(pills).some(function(p) {{ return p.classList.contains('active'); }});
                    if (!hasActive && pills[0]) pills[0].classList.add('active');
                    pills.forEach(function(pill) {{
                        pill.addEventListener('click', function() {{
                            pills.forEach(function(p) {{ p.classList.remove('active'); }});
                            pill.classList.add('active');
                            var filter = pill.getAttribute('data-filter');
                            var cards = pDoc.querySelectorAll('[data-proj-cat]');
                            cards.forEach(function(card) {{
                                card.style.display = (filter === 'All' || card.getAttribute('data-proj-cat') === filter) ? '' : 'none';
                            }});
                        }});
                    }});
                }}

                // Card click → open modal
                var cards = pDoc.querySelectorAll('[data-proj-id]');
                cards.forEach(function(card) {{
                    if (card.__modalBound) return;
                    card.__modalBound = true;
                    card.addEventListener('click', function(e) {{
                        // Don't open modal if user clicked a link/button inside card
                        if (e.target.tagName === 'A' || e.target.tagName === 'BUTTON' || e.target.closest('a')) return;
                        openModal(card.getAttribute('data-proj-id'));
                    }});
                }});
            }} catch(e) {{}}
        }}

        var _iv = setInterval(setupCards, 350);
        setTimeout(function() {{ clearInterval(_iv); }}, 12000);
    }})();
    </script>
    """, height=0, width=0)


