"""
components/hero.py
==================
Premium 3-column hero section matching the reference design:
  - LEFT:   Hello pill → Name (KARTIKEY / GUPTA gradient) → tagline dots →
             bio → CTA buttons → stats row
  - CENTER: Spinning neon-ring photo + floating tech badges + specialty cards
  - RIGHT:  Tech Stack card + Quote card

Background: Three.js star-field with mouse parallax.
"""

import json
import streamlit.components.v1 as components

from utils.data_manager import load_profile, load_skills, load_projects, load_certificates
from utils.helpers import get_file_as_b64, is_placeholder


def _build_tech_stack(profile: dict) -> list[str]:
    """Return up to 6 tech stack items for the right panel."""
    skills_data = load_skills()
    cats = skills_data.get("categories", [])
    items = []
    for cat in cats:
        for sk in cat.get("skills", []):
            items.append(sk)
            if len(items) >= 6:
                return items
    # fallback defaults
    return items or ["Python", "Java", "SQL", "Angular", "Spring Boot", "Power BI"]


def render_hero():
    """Render the full hero section inside a components.html iframe."""
    profile  = load_profile()
    name     = profile.get("name", "Kartikey Gupta")
    tagline  = profile.get("tagline", "AI/ML | Data Analytics | Software Engineer")
    bio      = profile.get("short_bio", "I build intelligent systems, turn data into insights and create modern web applications that make an impact.")
    github   = profile.get("github", "")
    linkedin = profile.get("linkedin", "")
    sgpa     = profile.get("sgpa", "8.75")

    # Split name
    parts      = name.strip().split(" ", 1)
    first_name = parts[0].upper()
    last_name  = parts[1].upper() if len(parts) > 1 else ""

    # Tagline as dot-separated items
    tagline_parts = [t.strip() for t in tagline.replace("|", "•").split("•") if t.strip()]
    tagline_dots  = ' <span class="dot">•</span> '.join(tagline_parts[:3])

    # Stats
    proj_count = len(load_projects().get("projects", []))
    cert_count = len(load_certificates().get("certificates", []))
    proj_label = f"{max(proj_count, 2)}+"
    cert_label = f"{max(cert_count, 3)}+"

    # Profile photo
    photo_path = profile.get("profile_image", "assets/profile/profile.jpg")
    photo_b64  = get_file_as_b64(photo_path)
    photo_src  = f"data:image/jpeg;base64,{photo_b64}" if photo_b64 else ""

    # Resume button
    resume_path = profile.get("resume_file", "assets/resume/resume.pdf")
    resume_b64  = get_file_as_b64(resume_path)
    if resume_b64:
        resume_href = f"data:application/pdf;base64,{resume_b64}"
        resume_btn  = f'<a href="{resume_href}" download="Kartikey_Gupta_Resume.pdf" class="btn-resume">&#8595; Download Resume</a>'
    else:
        resume_btn = '<span class="btn-resume btn-disabled" title="Upload via Admin">&#8595; Resume</span>'

    # GitHub / LinkedIn
    gh_link = (f'<a href="{github}"  target="_blank" rel="noopener" class="btn-ghost">&#128025; GitHub</a>'
               if not is_placeholder(github) else "")
    li_link = (f'<a href="{linkedin}" target="_blank" rel="noopener" class="btn-ghost">&#128188; LinkedIn</a>'
               if not is_placeholder(linkedin) else "")

    # Tech stack
    tech_stack = _build_tech_stack(profile)
    tech_icons = {"python":"🐍","java":"☕","sql":"🗄️","angular":"🅰️","spring":"🌱","power bi":"📊",
                  "javascript":"🟨","react":"⚛️","node":"🟩","c++":"⚙️","c#":"🔷","kotlin":"🎯",
                  "flutter":"💙","dart":"🎯","mongodb":"🍃","mysql":"🐬","html":"🌐","css":"🎨"}
    tech_list_html = "".join(
        f'<div class="tech-row"><span class="tech-icon">'
        f'{tech_icons.get(t.lower().split()[0], "💡")}</span>'
        f'<span>{t}</span></div>'
        for t in tech_stack[:6]
    )

    # Quote
    quote_name = name.split()[0] if name else "Kartikey"

    # Typing animation array
    typing_arr = json.dumps(tagline_parts[:3] if tagline_parts else ["AI/ML Developer", "Data Analytics", "Software Engineer"])

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<style>
/* ── Reset ── */
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
body{{
  background:#090b17;
  font-family:'Segoe UI',system-ui,sans-serif;
  overflow:hidden;
  color:#e2e8f0;
  min-height:620px;
}}

/* ── Background canvas ── */
#bg-canvas{{position:fixed;inset:0;width:100%;height:100%;z-index:0;pointer-events:none}}

/* ── Main layout ── */
#hero{{
  position:relative;z-index:1;
  display:grid;
  grid-template-columns:1fr 1.1fr 0.85fr;
  gap:0 24px;
  align-items:center;
  min-height:600px;
  padding:28px 24px 0;
  max-width:1200px;
  margin:0 auto;
}}

/* ════════════════════════ LEFT COLUMN ════════════════════════ */
.col-left{{
  display:flex;flex-direction:column;gap:0;
  animation:fadeUp 0.8s ease both;
}}

.hello-pill{{
  display:inline-flex;align-items:center;gap:6px;
  padding:6px 16px;border-radius:50px;
  background:rgba(255,255,255,0.05);
  border:1px solid rgba(255,255,255,0.12);
  font-size:0.82rem;color:#94a3b8;
  margin-bottom:14px;width:fit-content;
  backdrop-filter:blur(8px);
}}

.name-first{{
  display:block;
  font-size:clamp(2.6rem,5vw,4rem);
  font-weight:900;
  color:#ffffff;
  letter-spacing:-1px;
  line-height:1;
  text-shadow:0 0 40px rgba(255,255,255,0.08);
}}
.name-last{{
  display:block;
  font-size:clamp(2.6rem,5vw,4rem);
  font-weight:900;
  letter-spacing:-1px;
  line-height:1;
  background:linear-gradient(135deg,#6366f1 0%,#a855f7 50%,#ec4899 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  background-clip:text;
  margin-bottom:12px;
}}

.tagline-row{{
  display:flex;flex-wrap:wrap;align-items:center;gap:4px;
  font-size:0.88rem;color:#64748b;font-weight:500;
  margin-bottom:14px;
  letter-spacing:0.3px;
}}
.dot{{color:#a855f7;margin:0 2px}}

.hero-bio{{
  font-size:0.88rem;color:#64748b;
  line-height:1.7;
  max-width:340px;
  margin-bottom:22px;
}}

.cta-row{{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:26px}}

.btn-explore{{
  display:inline-flex;align-items:center;gap:6px;
  padding:11px 22px;border-radius:50px;
  background:linear-gradient(135deg,#6366f1,#a855f7);
  color:#fff;font-weight:700;font-size:0.88rem;
  text-decoration:none;
  box-shadow:0 4px 20px rgba(99,102,241,0.4);
  transition:all 0.3s ease;
}}
.btn-explore:hover{{transform:translateY(-3px);box-shadow:0 8px 30px rgba(99,102,241,0.6)}}

.btn-resume{{
  display:inline-flex;align-items:center;gap:6px;
  padding:11px 22px;border-radius:50px;
  background:transparent;
  color:#e2e8f0;font-weight:600;font-size:0.88rem;
  text-decoration:none;
  border:1.5px solid rgba(255,255,255,0.2);
  backdrop-filter:blur(6px);
  transition:all 0.3s ease;
}}
.btn-resume:hover{{background:rgba(255,255,255,0.06);transform:translateY(-3px)}}
.btn-disabled{{opacity:0.4;cursor:not-allowed;pointer-events:none}}

.btn-ghost{{
  display:inline-flex;align-items:center;gap:5px;
  padding:8px 16px;border-radius:50px;
  background:rgba(255,255,255,0.04);
  color:#94a3b8;font-size:0.82rem;font-weight:500;
  text-decoration:none;
  border:1px solid rgba(255,255,255,0.1);
  transition:all 0.25s;
}}
.btn-ghost:hover{{background:rgba(255,255,255,0.1);color:#fff;transform:translateY(-2px)}}

.stats-row{{
  display:flex;gap:0;
  background:rgba(255,255,255,0.03);
  border:1px solid rgba(255,255,255,0.07);
  border-radius:16px;
  padding:16px 0;
  width:fit-content;
  min-width:260px;
}}
.stat-item{{
  display:flex;flex-direction:column;align-items:center;
  flex:1;padding:0 20px;
  border-right:1px solid rgba(255,255,255,0.06);
}}
.stat-item:last-child{{border-right:none}}
.stat-icon{{font-size:1.1rem;margin-bottom:4px}}
.stat-val{{font-size:1.3rem;font-weight:800;color:#e2e8f0;line-height:1}}
.stat-lab{{font-size:0.68rem;color:#475569;margin-top:3px;letter-spacing:0.3px;text-transform:uppercase}}

/* ════════════════════════ CENTER COLUMN ════════════════════════ */
.col-center{{
  display:flex;flex-direction:column;align-items:center;
  gap:20px;
  animation:fadeUp 0.8s 0.15s ease both;
}}

.photo-scene{{
  position:relative;
  width:320px;height:340px;
  display:flex;align-items:center;justify-content:center;
}}

/* ── Spinning neon ring ── */
.ring-wrap{{
  position:relative;
  width:260px;height:260px;
}}
.ring-spin{{
  position:absolute;inset:-5px;
  border-radius:50%;
  background:conic-gradient(#00c8ff,#6366f1,#a855f7,#ec4899,#00c8ff);
  animation:ring-rotate 4s linear infinite;
  filter:blur(1px);
}}
@keyframes ring-rotate{{from{{transform:rotate(0deg)}}to{{transform:rotate(360deg)}}}}

.ring-inner{{
  position:absolute;
  inset:5px;
  border-radius:50%;
  background:#0d1023;
  overflow:hidden;
  z-index:2;
}}
.ring-inner img{{
  width:100%;height:100%;
  object-fit:cover;object-position:top center;
}}
.ring-placeholder{{
  width:100%;height:100%;
  display:flex;align-items:center;justify-content:center;
  background:linear-gradient(135deg,#1a1040,#0d1023);
  font-size:3.5rem;font-weight:800;
  color:rgba(255,255,255,0.15);
  letter-spacing:-2px;
}}

/* Outer glow rings */
.ring-glow1{{
  position:absolute;inset:-18px;
  border-radius:50%;
  border:1px solid rgba(99,102,241,0.2);
  animation:pulse-ring 3s ease-in-out infinite;
}}
.ring-glow2{{
  position:absolute;inset:-36px;
  border-radius:50%;
  border:1px solid rgba(168,85,247,0.1);
  animation:pulse-ring 3s 1s ease-in-out infinite;
}}
@keyframes pulse-ring{{
  0%,100%{{opacity:0.4;transform:scale(1)}}
  50%{{opacity:0.8;transform:scale(1.02)}}
}}

/* Decorative spheres */
.sphere{{
  position:absolute;border-radius:50%;
  background:radial-gradient(circle at 30% 30%,rgba(255,255,255,0.3),rgba(99,102,241,0.6));
  animation:float-sphere 6s ease-in-out infinite;
}}
.sp1{{width:14px;height:14px;top:-10px;right:60px;animation-delay:0s}}
.sp2{{width:10px;height:10px;top:30px;right:-8px;animation-delay:1s}}
.sp3{{width:8px;height:8px;bottom:20px;right:-12px;animation-delay:2s}}
.sp4{{width:12px;height:12px;bottom:-8px;left:50px;animation-delay:0.5s}}
@keyframes float-sphere{{
  0%,100%{{transform:translateY(0)}}
  50%{{transform:translateY(-8px)}}
}}

/* Platform glow */
.platform{{
  position:absolute;bottom:-12px;left:50%;
  transform:translateX(-50%);
  width:180px;height:18px;
  background:radial-gradient(ellipse,rgba(99,102,241,0.6) 0%,transparent 70%);
  filter:blur(6px);
  border-radius:50%;
}}

/* ── Floating tech badges ── */
.float-badge{{
  position:absolute;
  display:flex;align-items:center;gap:8px;
  padding:8px 14px;border-radius:12px;
  background:rgba(255,255,255,0.05);
  border:1px solid rgba(255,255,255,0.12);
  backdrop-filter:blur(12px);
  font-size:0.8rem;font-weight:600;color:#e2e8f0;
  box-shadow:0 4px 20px rgba(0,0,0,0.3);
  white-space:nowrap;
  z-index:10;
}}
.badge-icon{{font-size:1.1rem}}

.b-python{{top:10px;left:-30px;animation:float-a 3s ease-in-out infinite}}
.b-sql{{top:42%;left:-50px;animation:float-b 3s 0.5s ease-in-out infinite}}
.b-angular{{bottom:28%;left:-20px;animation:float-a 3s 1s ease-in-out infinite}}
.b-powerbi{{top:36%;right:-44px;animation:float-b 3s 0.8s ease-in-out infinite}}

@keyframes float-a{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-7px)}}}}
@keyframes float-b{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(7px)}}}}

/* ── Specialty cards ── */
.spec-row{{
  display:flex;gap:10px;width:100%;
  max-width:520px;
}}
.spec-card{{
  flex:1;
  display:flex;align-items:center;gap:9px;
  padding:10px 12px;border-radius:12px;
  background:rgba(255,255,255,0.03);
  border:1px solid rgba(255,255,255,0.07);
  backdrop-filter:blur(8px);
  transition:all 0.3s;
}}
.spec-card:hover{{
  background:rgba(255,255,255,0.06);
  border-color:rgba(168,85,247,0.3);
  transform:translateY(-3px);
}}
.spec-ico{{font-size:1.2rem}}
.spec-title{{font-size:0.72rem;font-weight:700;color:#e2e8f0;line-height:1.2}}
.spec-sub{{font-size:0.62rem;color:#475569;margin-top:2px;line-height:1.2}}
.mono-tag{{font-family:monospace;font-size:0.9rem;font-weight:700;
  background:linear-gradient(135deg,#00d4ff,#a855f7);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}}

/* ════════════════════════ RIGHT COLUMN ════════════════════════ */
.col-right{{
  display:flex;flex-direction:column;gap:14px;
  animation:fadeUp 0.8s 0.3s ease both;
}}

.tech-stack-card{{
  background:rgba(255,255,255,0.03);
  border:1px solid rgba(255,255,255,0.07);
  border-radius:16px;padding:18px;
  backdrop-filter:blur(10px);
}}
.tech-stack-title{{
  font-size:0.78rem;font-weight:700;
  color:#e2e8f0;letter-spacing:1px;
  text-transform:uppercase;
  margin-bottom:12px;
}}
.tech-row{{
  display:flex;align-items:center;gap:10px;
  padding:8px 10px;border-radius:10px;
  font-size:0.82rem;color:#94a3b8;font-weight:500;
  transition:all 0.2s;cursor:default;
  margin-bottom:4px;
}}
.tech-row:hover{{background:rgba(99,102,241,0.08);color:#e2e8f0;transform:translateX(4px)}}
.tech-icon{{font-size:1rem;width:22px;text-align:center}}

.quote-card{{
  background:rgba(255,255,255,0.03);
  border:1px solid rgba(255,255,255,0.07);
  border-radius:16px;padding:18px;
  backdrop-filter:blur(10px);
}}
.quote-tag{{
  font-family:monospace;font-size:1rem;font-weight:700;
  background:linear-gradient(135deg,#00d4ff,#a855f7);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  background-clip:text;
  margin-bottom:10px;display:block;
}}
.quote-text{{
  font-size:0.82rem;color:#94a3b8;
  line-height:1.65;font-style:italic;
  margin-bottom:10px;
}}
.quote-author{{
  font-size:0.74rem;color:#475569;font-weight:600;
}}

/* ════════════════════════ ANIMATIONS ════════════════════════ */
@keyframes fadeUp{{
  from{{opacity:0;transform:translateY(24px)}}
  to{{opacity:1;transform:translateY(0)}}
}}

/* ── Light Theme Overrides ── */
body.light-theme {{
  background: #f8fafc !important;
  color: #0f172a !important;
}}
body.light-theme .hello-pill {{
  background: rgba(0,0,0,0.04);
  border-color: rgba(0,0,0,0.12);
  color: #475569;
}}
body.light-theme .name-first {{
  color: #0f172a;
}}
body.light-theme .hero-bio {{
  color: #475569;
}}
body.light-theme .stat-val {{
  color: #0f172a;
}}
body.light-theme .stat-lab {{
  color: #64748b;
}}
body.light-theme .stats-row {{
  background: rgba(255,255,255,0.8);
  border-color: rgba(0,0,0,0.08);
}}
body.light-theme .stat-item {{
  border-right-color: rgba(0,0,0,0.08);
}}
body.light-theme .ring-inner {{
  background: #f1f5f9;
}}
body.light-theme .ring-placeholder {{
  background: linear-gradient(135deg, #e2e8f0, #f1f5f9);
  color: rgba(0,0,0,0.2);
}}
body.light-theme .float-badge {{
  background: rgba(255,255,255,0.9);
  border-color: rgba(0,0,0,0.1);
  color: #0f172a;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
}}
body.light-theme .spec-card {{
  background: rgba(255,255,255,0.85);
  border-color: rgba(0,0,0,0.08);
}}
body.light-theme .spec-title {{
  color: #0f172a;
}}
body.light-theme .spec-sub {{
  color: #64748b;
}}
body.light-theme .tech-stack-card,
body.light-theme .quote-card {{
  background: rgba(255,255,255,0.85);
  border-color: rgba(0,0,0,0.08);
}}
body.light-theme .tech-stack-title {{
  color: #0f172a;
}}
body.light-theme .tech-row {{
  color: #475569;
}}
body.light-theme .tech-row:hover {{
  background: rgba(0,212,255,0.08);
  color: #0f172a;
}}
body.light-theme .quote-text {{
  color: #475569;
}}
body.light-theme .quote-author {{
  color: #64748b;
}}
body.light-theme .btn-resume {{
  background: rgba(0, 0, 0, 0.05) !important;
  border: 1.5px solid rgba(0, 0, 0, 0.15) !important;
  color: #0f172a !important;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05) !important;
}}
body.light-theme .btn-resume:hover {{
  background: rgba(0, 212, 255, 0.12) !important;
  border-color: rgba(0, 212, 255, 0.4) !important;
  color: #0f172a !important;
  transform: translateY(-3px) !important;
}}
body.light-theme .tagline-row {{
  color: #334155 !important;
}}
body.light-theme .dot {{
  color: #0284c7 !important;
}}
body.light-theme .btn-ghost {{
  background: rgba(0,0,0,0.04);
  border-color: rgba(0,0,0,0.12);
  color: #334155;
}}
body.light-theme .btn-ghost:hover {{
  background: rgba(0,0,0,0.08);
  color: #0f172a;
}}
</style>
</head>
<body>

<canvas id="bg-canvas"></canvas>

<div id="hero">

  <!-- ═══════════ LEFT ═══════════ -->
  <div class="col-left">
    <div class="hello-pill">👋 Hello, I'm</div>

    <h1>
      <span class="name-first">{first_name}</span>
      <span class="name-last">{last_name}</span>
    </h1>

    <div class="tagline-row">{tagline_dots}</div>
    <p class="hero-bio">{bio}</p>

    <div class="cta-row">
      <a href="#projects" onclick="try{{ const el = window.parent.document.getElementById('projects'); if(el){{ el.scrollIntoView({{behavior:'smooth'}}); return false; }} }}catch(e){{}} window.parent.location.hash='projects'; return false;" class="btn-explore">&#8594; Explore My Work</a>
      {resume_btn}
    </div>
    <div class="cta-row" style="margin-top:-14px;margin-bottom:18px;">
      {gh_link}
      {li_link}
    </div>

    <div class="stats-row">
      <div class="stat-item">
        <span class="stat-icon">🎓</span>
        <span class="stat-val">{sgpa}</span>
        <span class="stat-lab">CGPA</span>
      </div>
      <div class="stat-item">
        <span class="stat-icon">📁</span>
        <span class="stat-val">{proj_label}</span>
        <span class="stat-lab">Projects</span>
      </div>
      <div class="stat-item">
        <span class="stat-icon">🏆</span>
        <span class="stat-val">{cert_label}</span>
        <span class="stat-lab">Certifications</span>
      </div>
    </div>
  </div>

  <!-- ═══════════ CENTER ═══════════ -->
  <div class="col-center">
    <div class="photo-scene">
      <!-- Floating badges -->
      <div class="float-badge b-python">
        <span class="badge-icon">🐍</span>
        <div>
          <div style="font-size:0.72rem;color:#94a3b8;line-height:1">Python</div>
          <div style="font-size:0.82rem;font-weight:700">Python</div>
        </div>
      </div>
      <div class="float-badge b-sql">
        <span class="badge-icon">🗄️</span>
        <div style="font-size:0.82rem;font-weight:700">SQL</div>
      </div>
      <div class="float-badge b-angular">
        <span class="badge-icon">🅰️</span>
        <div style="font-size:0.82rem;font-weight:700">Angular</div>
      </div>
      <div class="float-badge b-powerbi">
        <span class="badge-icon">📊</span>
        <div style="font-size:0.82rem;font-weight:700">Power BI</div>
      </div>

      <!-- Outer glow rings -->
      <div class="ring-glow1"></div>
      <div class="ring-glow2"></div>

      <!-- Spinning neon ring + photo -->
      <div class="ring-wrap">
        <div class="ring-spin"></div>
        <div class="ring-inner">
          {'<img src="' + photo_src + '" alt="' + name + '"/>' if photo_src else '<div class="ring-placeholder">' + first_name[0] + (last_name[0] if last_name else '') + '</div>'}
        </div>
      </div>

      <!-- Decorative spheres -->
      <div class="sphere sp1"></div>
      <div class="sphere sp2"></div>
      <div class="sphere sp3"></div>
      <div class="sphere sp4"></div>

      <!-- Platform glow -->
      <div class="platform"></div>
    </div>

    <!-- Specialty cards -->
    <div class="spec-row">
      <div class="spec-card">
        <span class="spec-ico">🧠</span>
        <div>
          <div class="spec-title">AI / ML</div>
          <div class="spec-sub">Intelligent systems</div>
        </div>
      </div>
      <div class="spec-card">
        <span class="spec-ico">📈</span>
        <div>
          <div class="spec-title">Data Analytics</div>
          <div class="spec-sub">Insights from data</div>
        </div>
      </div>
      <div class="spec-card">
        <span class="spec-ico mono-tag">KG</span>
        <div>
          <div class="spec-title">Full Stack Dev</div>
          <div class="spec-sub">Modern web apps</div>
        </div>
      </div>
    </div>
  </div>

  <!-- ═══════════ RIGHT ═══════════ -->
  <div class="col-right">
    <div class="tech-stack-card">
      <div class="tech-stack-title">Tech Stack</div>
      {tech_list_html}
    </div>

    <div class="quote-card">
      <span class="quote-tag">KG</span>
      <p class="quote-text">"Turning ideas into real solutions through code, data and AI."</p>
      <div class="quote-author">— {quote_name} Gupta</div>
    </div>
  </div>

</div>

<script>
// ── Theme Sync ─────────────────────────────────────────────────────────────
(function syncHeroTheme() {{
  function checkTheme() {{
    let isLight = false;
    try {{
      if (window.parent && window.parent.document) {{
        isLight = window.parent.document.body.classList.contains('light-theme');
      }}
    }} catch(e) {{}}
    if (!isLight) {{
      try {{ isLight = (localStorage.getItem('portfolio-theme') === 'light'); }} catch(e) {{}}
    }}
    if (isLight) {{
      document.body.classList.add('light-theme');
    }} else {{
      document.body.classList.remove('light-theme');
    }}
  }}
  setInterval(checkTheme, 200);
  checkTheme();
}})();

// ── Three.js star-field background ──────────────────────────────────────────
(async function() {{
  try {{
    const s = document.createElement('script');
    s.src = 'https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js';
    document.head.appendChild(s);
    await new Promise((res,rej)=>{{s.onload=res;s.onerror=rej;}});

    const canvas = document.getElementById('bg-canvas');
    const W = window.innerWidth, H = window.innerHeight;
    canvas.width = W; canvas.height = H;

    const renderer = new THREE.WebGLRenderer({{canvas,alpha:true,antialias:true}});
    renderer.setSize(W,H);
    renderer.setPixelRatio(Math.min(devicePixelRatio,2));

    const scene  = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(70,W/H,0.1,1000);
    camera.position.z = 5;

    // Stars
    const N = 1500;
    const pos = new Float32Array(N*3);
    const col = new Float32Array(N*3);
    const palette = [[0.0,0.78,1.0],[0.63,0.33,0.97],[0.98,0.29,0.6],[1,1,1]];
    for(let i=0;i<N;i++){{
      pos[i*3]   = (Math.random()-0.5)*24;
      pos[i*3+1] = (Math.random()-0.5)*16;
      pos[i*3+2] = (Math.random()-0.5)*12;
      const c = palette[Math.floor(Math.random()*palette.length)];
      col[i*3]=c[0];col[i*3+1]=c[1];col[i*3+2]=c[2];
    }}
    const geo = new THREE.BufferGeometry();
    geo.setAttribute('position',new THREE.BufferAttribute(pos,3));
    geo.setAttribute('color',new THREE.BufferAttribute(col,3));
    const mat = new THREE.PointsMaterial({{size:0.04,vertexColors:true,transparent:true,opacity:0.7}});
    scene.add(new THREE.Points(geo,mat));

    // Wireframe sphere (subtle)
    const sGeo = new THREE.SphereGeometry(2.2,12,12);
    const sMat = new THREE.MeshBasicMaterial({{color:0x6366f1,wireframe:true,transparent:true,opacity:0.04}});
    const sph  = new THREE.Mesh(sGeo,sMat);
    sph.position.set(3,0,-3);
    scene.add(sph);

    // Mouse parallax
    let mx=0,my=0;
    document.addEventListener('mousemove',e=>{{
      mx=(e.clientX/W-0.5)*2;
      my=(e.clientY/H-0.5)*2;
    }});

    function animate(){{
      requestAnimationFrame(animate);
      const t=Date.now()*0.001;
      sph.rotation.y=t*0.12;
      sph.rotation.x=t*0.08;
      camera.position.x+=(mx*0.5-camera.position.x)*0.04;
      camera.position.y+=(-my*0.3-camera.position.y)*0.04;
      camera.lookAt(scene.position);
      mat.opacity=0.55+0.15*Math.sin(t);
      renderer.render(scene,camera);
    }}
    animate();
  }} catch(e) {{
    console.warn('Three.js unavailable',e);
    document.getElementById('bg-canvas').style.background='radial-gradient(ellipse at 30% 50%,rgba(99,102,241,0.06),transparent 60%),#090b17';
  }}
}})();
</script>
</body>
</html>"""

    components.html(html, height=630, scrolling=False)
