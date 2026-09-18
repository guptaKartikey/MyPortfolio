"""
utils/helpers.py
================
Utility functions used across multiple components.

Covers:
  - CSS injection into Streamlit
  - Image → base64 encoding (for embedding in HTML)
  - External link button rendering
  - File download helpers
  - Placeholder image generation
"""

import base64
import os
from pathlib import Path

import streamlit as st


# ──────────────────────────────────────────────
# CSS / HTML injection
# ──────────────────────────────────────────────

def inject_css(css: str) -> None:
    """Inject raw CSS into the Streamlit page."""
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def inject_html(html: str) -> None:
    """Inject raw HTML into the Streamlit page safely without markdown code-block bugs."""
    clean_html = "\n".join(line.strip() for line in html.splitlines())
    st.markdown(clean_html, unsafe_allow_html=True)


# ──────────────────────────────────────────────
# Image helpers
# ──────────────────────────────────────────────

def img_to_base64(path: str) -> str:
    """
    Read an image file and return its base64 encoded string.
    Returns an empty string if path is empty or file doesn't exist.
    """
    # Guard: empty / whitespace path → Path("") resolves to '.' which is a
    # directory, causing PermissionError on Windows when opened as a file.
    if not path or not str(path).strip():
        return ""
    p = Path(path)
    if not p.exists():
        return ""
    with open(p, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def get_img_tag(path: str, alt: str = "image", css_class: str = "") -> str:
    """
    Return an <img> HTML tag with the image embedded as base64.
    Falls back to a gradient placeholder div if image doesn't exist.
    """
    b64 = img_to_base64(path)
    if b64:
        ext = Path(path).suffix.lower().lstrip(".")
        mime = {"jpg": "jpeg", "jpeg": "jpeg", "png": "png", "gif": "gif", "webp": "webp"}.get(ext, "jpeg")
        return f'<img src="data:image/{mime};base64,{b64}" alt="{alt}" class="{css_class}" />'
    else:
        # Gradient placeholder
        return f'''<div class="img-placeholder {css_class}" role="img" aria-label="{alt}">
            <span>🖼️</span>
        </div>'''


# ──────────────────────────────────────────────
# File download helper
# ──────────────────────────────────────────────

def get_file_as_b64(path: str) -> str:
    """Return base64 encoded content of any file (e.g. PDF resume)."""
    p = Path(path)
    if not p.exists():
        return ""
    with open(p, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def get_download_link(path: str, label: str = "Download", filename: str = None) -> str:
    """
    Generate an HTML anchor download link for a file.
    Returns empty string if file doesn't exist.
    """
    b64 = get_file_as_b64(path)
    if not b64:
        return ""
    fname = filename or Path(path).name
    ext = Path(path).suffix.lower()
    mime_map = {".pdf": "application/pdf", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png"}
    mime = mime_map.get(ext, "application/octet-stream")
    return f'<a href="data:{mime};base64,{b64}" download="{fname}" class="btn-primary">{label}</a>'


# ──────────────────────────────────────────────
# External link helper
# ──────────────────────────────────────────────

def external_link_btn(url: str, label: str, icon: str = "", css_class: str = "btn-secondary") -> str:
    """Return an HTML button-styled anchor that opens in a new tab."""
    if not url or url.startswith("[PLACEHOLDER"):
        return ""
    return f'<a href="{url}" target="_blank" rel="noopener noreferrer" class="{css_class}">{icon} {label}</a>'


def is_placeholder(value: str) -> bool:
    """Return True if the value is still a placeholder (not yet filled in)."""
    if not value:
        return True
    return str(value).strip().startswith("[PLACEHOLDER")


# ──────────────────────────────────────────────
# Section heading helper
# ──────────────────────────────────────────────

def section_heading(title: str, subtitle: str = "") -> str:
    """Return HTML for a styled section heading with optional subtitle."""
    sub_html = f'<p class="section-subtitle">{subtitle}</p>' if subtitle else ""
    return f"""
    <div class="section-heading" id="{title.lower().replace(' ', '-')}">
        <h2 class="section-title">{title}</h2>
        <div class="section-divider"></div>
        {sub_html}
    </div>
    """


# ──────────────────────────────────────────────
# Upload helper (save uploaded file to disk)
# ──────────────────────────────────────────────

def save_uploaded_file(uploaded_file, dest_dir: str, filename: str = None) -> str:
    """
    Save a Streamlit UploadedFile object to dest_dir.
    Returns the saved file path string, or empty string on failure.
    """
    if uploaded_file is None:
        return ""
    dest = Path(dest_dir)
    dest.mkdir(parents=True, exist_ok=True)
    fname = filename or uploaded_file.name
    # Sanitize filename
    fname = "".join(c if c.isalnum() or c in "._-" else "_" for c in fname)
    out_path = dest / fname
    with open(out_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return str(out_path)
