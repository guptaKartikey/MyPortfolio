"""
components/admin.py
===================
Secure admin dashboard.

Access: add  ?admin=true  to the URL, e.g.  http://localhost:8501/?admin=true
Password is stored in  .streamlit/secrets.toml  as  ADMIN_PASSWORD

Features:
  - Profile editor
  - Skills manager (add / edit / delete)
  - Projects manager (add / edit / delete / image upload)
  - Certificates manager (add / edit / delete / image upload)
  - Experience manager (add / edit / delete)
  - Resume uploader
  - Inbox (view messages from contact form)

Fix: All st.success() + st.rerun() pairs replaced with st.toast() + st.rerun()
     so the confirmation is visible AFTER the page refreshes.
"""

import streamlit as st

from utils.data_manager import (
    load_profile, save_profile,
    load_skills, save_skills,
    load_projects, save_projects,
    load_certificates, save_certificates,
    load_experience, save_experience,
    load_messages, save_messages,
    next_id,
    PROFILE_IMG_DIR, PROJECT_IMG_DIR, CERT_IMG_DIR, RESUME_DIR,
)
from utils.helpers import inject_html, save_uploaded_file


# ── Password gate ─────────────────────────────────────────────────────────────

def _check_password() -> bool:
    """
    Return True if the admin is authenticated.
    Uses st.session_state to persist login across reruns.
    """
    if st.session_state.get("admin_authenticated"):
        return True

    st.markdown("## 🔐 Admin Login")
    st.info("Enter the admin password to access the dashboard.")

    password_input = st.text_input("Password", type="password", key="admin_pw_input")
    if st.button("Login", use_container_width=True):
        try:
            correct_pw = st.secrets.get("ADMIN_PASSWORD", "admin123")
        except Exception:
            correct_pw = "admin123"

        if password_input == correct_pw:
            st.session_state.admin_authenticated = True
            st.rerun()
        else:
            st.error("❌ Incorrect password. Please try again.")
    return False


# ── Individual tab renderers ──────────────────────────────────────────────────

def _tab_profile():
    """Profile editor tab."""
    st.markdown("### 👤 Edit Profile")
    profile = load_profile()

    with st.form("profile_form"):
        col1, col2 = st.columns(2)
        with col1:
            name      = st.text_input("Full Name",           value=profile.get("name", ""))
            role      = st.text_input("Role / Title",        value=profile.get("role", ""))
            tagline   = st.text_input("Tagline (hero)",      value=profile.get("tagline", ""))
            college   = st.text_input("College / University", value=profile.get("college", ""))
            grad      = st.text_input("Graduation Year",     value=profile.get("graduation_year", "2027"))
            sgpa      = st.text_input("SGPA",                value=profile.get("sgpa", "8.75"))
        with col2:
            email     = st.text_input("Email",               value=profile.get("email", ""))
            phone     = st.text_input("Phone (optional)",    value=profile.get("phone", ""))
            location  = st.text_input("Location",            value=profile.get("location", ""))
            github    = st.text_input("GitHub URL",          value=profile.get("github", ""))
            linkedin  = st.text_input("LinkedIn URL",        value=profile.get("linkedin", ""))
            instagram = st.text_input("Instagram URL",       value=profile.get("instagram", ""))

        st.markdown("---")
        bio       = st.text_area("Full Biography",   value=profile.get("bio", ""),       height=120)
        short_bio = st.text_area("Short Bio (hero)", value=profile.get("short_bio", ""), height=68)

        interests_raw = st.text_input(
            "Interests (comma-separated)",
            value=", ".join(profile.get("interests", [])),
        )

        st.markdown("---")
        st.markdown("**Profile Photo**")
        st.caption(f"Current: `{profile.get('profile_image', '')}`")
        new_img = st.file_uploader(
            "Upload new profile photo (JPG/PNG)",
            type=["jpg", "jpeg", "png"],
            key="profile_img_up",
        )

        submitted = st.form_submit_button("💾 Save Profile", use_container_width=True)

        if submitted:
            img_path = profile.get("profile_image", "assets/profile/profile.jpg")
            if new_img:
                saved = save_uploaded_file(new_img, str(PROFILE_IMG_DIR), "profile.jpg")
                if saved:
                    img_path = "assets/profile/profile.jpg"

            updated = {
                **profile,
                "name": name, "role": role, "tagline": tagline,
                "college": college, "graduation_year": grad, "sgpa": sgpa,
                "email": email, "phone": phone, "location": location,
                "github": github, "linkedin": linkedin, "instagram": instagram,
                "bio": bio, "short_bio": short_bio,
                "interests": [i.strip() for i in interests_raw.split(",") if i.strip()],
                "profile_image": img_path,
            }
            save_profile(updated)
            st.toast("✅ Profile saved!", icon="✅")
            st.rerun()


def _tab_skills():
    """Skills manager tab."""
    st.markdown("### 🛠️ Manage Skills")
    data       = load_skills()
    categories = data.get("categories", [])

    # ── Add new category ─────────────────────────────────────────────────────
    with st.expander("➕ Add New Category", expanded=False):
        with st.form("add_cat_form"):
            cat_name  = st.text_input("Category Name")
            cat_icon  = st.text_input("Icon (emoji)", value="🔧")
            cat_color = st.color_picker("Color", value="#00d4ff")
            if st.form_submit_button("Add Category"):
                if cat_name.strip():
                    categories.append({
                        "name": cat_name.strip(),
                        "icon": cat_icon,
                        "color": cat_color,
                        "skills": [],
                    })
                    save_skills({"categories": categories})
                    st.toast(f"✅ Category '{cat_name}' added!", icon="✅")
                    st.rerun()

    # ── Edit existing categories ──────────────────────────────────────────────
    for ci, cat in enumerate(categories):
        with st.expander(
            f"{cat.get('icon','')} {cat.get('name','')}  ({len(cat.get('skills',[]))} skills)",
            expanded=False,
        ):
            col1, col2 = st.columns([3, 1])
            with col1:
                new_cat_name  = st.text_input("Name",  value=cat["name"],             key=f"cn_{ci}")
                new_cat_icon  = st.text_input("Icon",  value=cat.get("icon", "🔧"),   key=f"ci_{ci}")
                new_cat_color = st.color_picker("Color", value=cat.get("color","#00d4ff"), key=f"cc_{ci}")
            with col2:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("💾 Save", key=f"save_cat_{ci}"):
                    categories[ci]["name"]  = new_cat_name
                    categories[ci]["icon"]  = new_cat_icon
                    categories[ci]["color"] = new_cat_color
                    save_skills({"categories": categories})
                    st.toast("✅ Category saved!", icon="✅")
                    st.rerun()
                if st.button("🗑️ Delete Category", key=f"del_cat_{ci}"):
                    categories.pop(ci)
                    save_skills({"categories": categories})
                    st.toast("🗑️ Category deleted.", icon="✅")
                    st.rerun()

            # ── Skills within category ────────────────────────────────────────
            st.markdown("**Skills in this category:**")
            skills_list = cat.get("skills", [])
            for si, skill in enumerate(skills_list):
                s_col1, s_col2 = st.columns([3, 1])
                with s_col1:
                    new_skill = st.text_input(
                        "", value=skill, key=f"sk_{ci}_{si}", label_visibility="collapsed"
                    )
                with s_col2:
                    if st.button("✏️ Update", key=f"upd_sk_{ci}_{si}"):
                        categories[ci]["skills"][si] = new_skill
                        save_skills({"categories": categories})
                        st.toast("✅ Skill updated!", icon="✅")
                        st.rerun()
                    if st.button("🗑️", key=f"del_sk_{ci}_{si}"):
                        categories[ci]["skills"].pop(si)
                        save_skills({"categories": categories})
                        st.toast("🗑️ Skill removed.", icon="✅")
                        st.rerun()

            # ── Add skill to this category ────────────────────────────────────
            new_s = st.text_input("Add skill:", key=f"new_sk_{ci}", placeholder="e.g. PyTorch")
            if st.button("➕ Add Skill", key=f"add_sk_{ci}"):
                if new_s.strip():
                    categories[ci]["skills"].append(new_s.strip())
                    save_skills({"categories": categories})
                    st.toast(f"✅ '{new_s}' added!", icon="✅")
                    st.rerun()


def _tab_projects():
    """Projects manager tab."""
    st.markdown("### 🚀 Manage Projects")
    data     = load_projects()
    projects = data.get("projects", [])
    CATS     = ["AI/ML", "Web Development", "Java", "Python", "Other"]

    # ── Add new project ───────────────────────────────────────────────────────
    with st.expander("➕ Add New Project", expanded=False):
        with st.form("add_proj_form"):
            c1, c2 = st.columns(2)
            with c1:
                p_name   = st.text_input("Project Name *")
                p_cat    = st.selectbox("Category", CATS)
                p_github = st.text_input("GitHub URL")
                p_demo   = st.text_input("Live Demo URL")
            with c2:
                p_techs  = st.text_input("Technologies (comma-separated)")
                p_img    = st.file_uploader("Project Image", type=["jpg","jpeg","png"], key="new_proj_img")
                p_feat   = st.checkbox("Featured project")
            p_desc = st.text_area("Description *", height=100)

            if st.form_submit_button("➕ Add Project"):
                if not p_name.strip():
                    st.error("Project name is required.")
                elif not p_desc.strip():
                    st.error("Description is required.")
                else:
                    img_path = ""
                    if p_img:
                        fname    = f"project_{next_id(projects)}_{p_img.name}"
                        saved    = save_uploaded_file(p_img, str(PROJECT_IMG_DIR), fname)
                        img_path = f"assets/projects/{fname}" if saved else ""

                    projects.append({
                        "id":           next_id(projects),
                        "name":         p_name.strip(),
                        "description":  p_desc.strip(),
                        "technologies": [t.strip() for t in p_techs.split(",") if t.strip()],
                        "category":     p_cat,
                        "github":       p_github.strip() or "[PLACEHOLDER]",
                        "demo":         p_demo.strip()   or "[PLACEHOLDER]",
                        "image":        img_path,
                        "featured":     p_feat,
                    })
                    save_projects({"projects": projects})
                    st.toast(f"✅ Project '{p_name}' added!", icon="✅")
                    st.rerun()

    # ── List & edit existing projects ─────────────────────────────────────────
    for pi, proj in enumerate(projects):
        with st.expander(
            f"📁 {proj.get('name','Untitled')}  [{proj.get('category','')}]",
            expanded=False,
        ):
            with st.form(f"edit_proj_{pi}"):
                c1, c2 = st.columns(2)
                with c1:
                    e_name   = st.text_input("Name",     value=proj.get("name",""))
                    e_cat    = st.selectbox(
                        "Category", CATS,
                        index=CATS.index(proj.get("category","Other")) if proj.get("category","Other") in CATS else 4
                    )
                    e_github = st.text_input("GitHub",   value=proj.get("github",""))
                    e_demo   = st.text_input("Demo URL", value=proj.get("demo",""))
                with c2:
                    e_techs  = st.text_input("Technologies", value=", ".join(proj.get("technologies",[])))
                    e_feat   = st.checkbox("Featured",       value=proj.get("featured", False))
                    e_img    = st.file_uploader("Replace image", type=["jpg","jpeg","png"], key=f"proj_img_{pi}")
                e_desc = st.text_area("Description", value=proj.get("description",""), height=100)

                col_save, col_del = st.columns(2)
                with col_save:
                    save_btn = st.form_submit_button("💾 Save Changes")
                with col_del:
                    del_btn  = st.form_submit_button("🗑️ Delete Project", type="secondary")

                if save_btn:
                    img_path = proj.get("image", "")
                    if e_img:
                        fname    = f"project_{proj.get('id',pi)}_{e_img.name}"
                        saved    = save_uploaded_file(e_img, str(PROJECT_IMG_DIR), fname)
                        img_path = f"assets/projects/{fname}" if saved else img_path

                    projects[pi] = {
                        **proj,
                        "name":         e_name,
                        "description":  e_desc,
                        "technologies": [t.strip() for t in e_techs.split(",") if t.strip()],
                        "category":     e_cat,
                        "github":       e_github,
                        "demo":         e_demo,
                        "image":        img_path,
                        "featured":     e_feat,
                    }
                    save_projects({"projects": projects})
                    st.toast("✅ Project saved!", icon="✅")
                    st.rerun()

                if del_btn:
                    projects.pop(pi)
                    save_projects({"projects": projects})
                    st.toast("🗑️ Project deleted.", icon="✅")
                    st.rerun()


def _tab_certificates():
    """Certificates manager tab."""
    st.markdown("### 🏆 Manage Certificates")
    data  = load_certificates()
    certs = data.get("certificates", [])

    with st.expander("➕ Add New Certificate", expanded=False):
        with st.form("add_cert_form"):
            c1, c2 = st.columns(2)
            with c1:
                c_title  = st.text_input("Certificate Title *")
                c_issuer = st.text_input("Issuing Organization *")
                c_date   = st.text_input("Date (e.g. June 2024)")
            with c2:
                c_cred   = st.text_input("Credential ID")
                c_verify = st.text_input("Verification URL")
                c_img    = st.file_uploader("Certificate Image", type=["jpg","jpeg","png"], key="new_cert_img")
            c_desc = st.text_area("Description", height=80)

            if st.form_submit_button("➕ Add Certificate"):
                if not c_title.strip():
                    st.error("Title is required.")
                else:
                    img_path = ""
                    if c_img:
                        fname    = f"cert_{next_id(certs)}_{c_img.name}"
                        saved    = save_uploaded_file(c_img, str(CERT_IMG_DIR), fname)
                        img_path = f"assets/certificates/{fname}" if saved else ""

                    certs.append({
                        "id":            next_id(certs),
                        "title":         c_title.strip(),
                        "issuer":        c_issuer.strip(),
                        "date":          c_date.strip()   or "[PLACEHOLDER]",
                        "credential_id": c_cred.strip()   or "[PLACEHOLDER]",
                        "verify_url":    c_verify.strip() or "[PLACEHOLDER]",
                        "image":         img_path,
                        "description":   c_desc.strip(),
                    })
                    save_certificates({"certificates": certs})
                    st.toast(f"✅ Certificate '{c_title}' added!", icon="✅")
                    st.rerun()

    for ci, cert in enumerate(certs):
        with st.expander(f"🏅 {cert.get('title','Certificate')}", expanded=False):
            with st.form(f"edit_cert_{ci}"):
                c1, c2 = st.columns(2)
                with c1:
                    e_title  = st.text_input("Title",        value=cert.get("title",""))
                    e_issuer = st.text_input("Issuer",       value=cert.get("issuer",""))
                    e_date   = st.text_input("Date",         value=cert.get("date",""))
                with c2:
                    e_cred   = st.text_input("Credential ID", value=cert.get("credential_id",""))
                    e_verify = st.text_input("Verify URL",    value=cert.get("verify_url",""))
                    e_img    = st.file_uploader("Replace image", type=["jpg","jpeg","png"], key=f"cert_img_{ci}")
                e_desc = st.text_area("Description", value=cert.get("description",""), height=80)

                col_s, col_d = st.columns(2)
                with col_s:
                    save_c = st.form_submit_button("💾 Save")
                with col_d:
                    del_c  = st.form_submit_button("🗑️ Delete", type="secondary")

                if save_c:
                    img_path = cert.get("image", "")
                    if e_img:
                        fname    = f"cert_{cert.get('id',ci)}_{e_img.name}"
                        saved    = save_uploaded_file(e_img, str(CERT_IMG_DIR), fname)
                        img_path = f"assets/certificates/{fname}" if saved else img_path
                    certs[ci] = {
                        **cert,
                        "title": e_title, "issuer": e_issuer, "date": e_date,
                        "credential_id": e_cred, "verify_url": e_verify,
                        "image": img_path, "description": e_desc,
                    }
                    save_certificates({"certificates": certs})
                    st.toast("✅ Certificate saved!", icon="✅")
                    st.rerun()

                if del_c:
                    certs.pop(ci)
                    save_certificates({"certificates": certs})
                    st.toast("🗑️ Certificate deleted.", icon="✅")
                    st.rerun()


def _tab_experience():
    """Experience manager tab."""
    st.markdown("### 💼 Manage Experience")
    data  = load_experience()
    exps  = data.get("experiences", [])
    TYPES = ["Internship", "Full-time", "Part-time", "Freelance", "Volunteer", "Research"]

    with st.expander("➕ Add New Experience", expanded=False):
        with st.form("add_exp_form"):
            c1, c2 = st.columns(2)
            with c1:
                e_org  = st.text_input("Organization *")
                e_pos  = st.text_input("Position / Role *")
                e_type = st.selectbox("Type", TYPES)
            with c2:
                e_dur  = st.text_input("Duration (e.g. June 2024 – July 2024)")
                e_cert = st.text_input("Certificate / Verification URL")
                e_tech = st.text_input("Technologies (comma-separated)")
            e_desc = st.text_area("Description *", height=100)

            if st.form_submit_button("➕ Add Experience"):
                if not e_org.strip() or not e_pos.strip():
                    st.error("Organization and Position are required.")
                else:
                    exps.append({
                        "id":              next_id(exps),
                        "organization":    e_org.strip(),
                        "position":        e_pos.strip(),
                        "duration":        e_dur.strip()  or "[PLACEHOLDER]",
                        "description":     e_desc.strip(),
                        "technologies":    [t.strip() for t in e_tech.split(",") if t.strip()],
                        "certificate_url": e_cert.strip() or "[PLACEHOLDER]",
                        "type":            e_type,
                    })
                    save_experience({"experiences": exps})
                    st.toast(f"✅ Experience at '{e_org}' added!", icon="✅")
                    st.rerun()

    for ei, exp in enumerate(exps):
        with st.expander(
            f"💼 {exp.get('organization','')} — {exp.get('position','')}",
            expanded=False,
        ):
            with st.form(f"edit_exp_{ei}"):
                c1, c2 = st.columns(2)
                with c1:
                    ee_org  = st.text_input("Organization", value=exp.get("organization",""))
                    ee_pos  = st.text_input("Position",     value=exp.get("position",""))
                    ee_type = st.selectbox(
                        "Type", TYPES,
                        index=TYPES.index(exp.get("type","Internship")) if exp.get("type","Internship") in TYPES else 0
                    )
                with c2:
                    ee_dur  = st.text_input("Duration",     value=exp.get("duration",""))
                    ee_cert = st.text_input("Cert URL",     value=exp.get("certificate_url",""))
                    ee_tech = st.text_input("Technologies", value=", ".join(exp.get("technologies",[])))
                ee_desc = st.text_area("Description", value=exp.get("description",""), height=100)

                col_s, col_d = st.columns(2)
                with col_s:
                    save_e = st.form_submit_button("💾 Save")
                with col_d:
                    del_e  = st.form_submit_button("🗑️ Delete", type="secondary")

                if save_e:
                    exps[ei] = {
                        **exp,
                        "organization": ee_org, "position": ee_pos, "type": ee_type,
                        "duration": ee_dur, "certificate_url": ee_cert,
                        "technologies": [t.strip() for t in ee_tech.split(",") if t.strip()],
                        "description": ee_desc,
                    }
                    save_experience({"experiences": exps})
                    st.toast("✅ Experience saved!", icon="✅")
                    st.rerun()

                if del_e:
                    exps.pop(ei)
                    save_experience({"experiences": exps})
                    st.toast("🗑️ Experience deleted.", icon="✅")
                    st.rerun()


def _tab_resume():
    """Resume uploader tab."""
    st.markdown("### 📄 Resume")
    profile = load_profile()
    current = profile.get("resume_file", "assets/resume/resume.pdf")
    st.info(f"Current resume path: `{current}`")

    uploaded = st.file_uploader("Upload new resume PDF", type=["pdf"], key="resume_up")
    if uploaded:
        saved = save_uploaded_file(uploaded, str(RESUME_DIR), "resume.pdf")
        if saved:
            profile["resume_file"] = "assets/resume/resume.pdf"
            save_profile(profile)
            st.toast("✅ Resume uploaded! Visitors can now download it.", icon="✅")
            st.rerun()
        else:
            st.error("Upload failed. Please try again.")


def _tab_messages():
    """Contact messages inbox tab."""
    st.markdown("### 📬 Messages Inbox")
    data     = load_messages()
    messages = data.get("messages", [])

    if not messages:
        st.info("No messages yet. Messages submitted via the contact form will appear here.")
        return

    st.markdown(f"**Total messages:** {len(messages)}")
    st.divider()

    for msg in reversed(messages):
        with st.expander(
            f"📨 {msg.get('name','')} | {msg.get('email','')} | {msg.get('timestamp','')[:10]}",
            expanded=False,
        ):
            st.markdown(f"**From:** {msg.get('name','')}  (`{msg.get('email','')}`)")
            st.markdown(f"**Date:** {msg.get('timestamp','')}")
            st.markdown("---")
            st.markdown(msg.get("message", ""))

    if st.button("🗑️ Clear All Messages", type="secondary"):
        save_messages({"messages": []})
        st.toast("🗑️ All messages cleared.", icon="✅")
        st.rerun()


# ── Main entry point ──────────────────────────────────────────────────────────

def render_admin():
    """
    Main admin panel renderer.
    Called from app.py when ?admin=true is in the URL query params.
    """
    inject_html("""
    <style>
    .admin-header {
        background: linear-gradient(135deg, rgba(0,212,255,0.08), rgba(168,85,247,0.08));
        border: 1px solid rgba(0,212,255,0.2);
        border-radius: 16px;
        padding: 20px 28px;
        margin-bottom: 24px;
    }
    .admin-title {
        font-size: 1.6rem; font-weight: 800;
        background: linear-gradient(135deg, #00d4ff, #a855f7);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .admin-sub { font-size: 0.85rem; color: #64748b; margin-top: 4px; }
    </style>
    <div class="admin-header">
        <div class="admin-title">&#9881;&#65039; Admin Dashboard</div>
        <div class="admin-sub">Portfolio content management &#8212; all changes persist automatically.</div>
    </div>
    """)

    if not _check_password():
        return

    if st.button("🚪 Logout", type="secondary"):
        st.session_state.admin_authenticated = False
        st.rerun()

    st.divider()

    tabs = st.tabs([
        "👤 Profile",
        "🛠️ Skills",
        "🚀 Projects",
        "🏆 Certificates",
        "💼 Experience",
        "📄 Resume",
        "📬 Messages",
    ])

    with tabs[0]: _tab_profile()
    with tabs[1]: _tab_skills()
    with tabs[2]: _tab_projects()
    with tabs[3]: _tab_certificates()
    with tabs[4]: _tab_experience()
    with tabs[5]: _tab_resume()
    with tabs[6]: _tab_messages()
