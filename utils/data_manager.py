"""
utils/data_manager.py
=====================
Central data layer for the portfolio.

Supports:
  - Firebase Firestore (Cloud persistence that never sleeps / never resets)
  - Local JSON files (Fallback / offline local mode)
  - Automatic migration from local JSON to Firestore on first run
"""

import json
import os
from datetime import datetime
from pathlib import Path
import streamlit as st

# Safe import for Firebase Admin SDK
try:
    import firebase_admin
    from firebase_admin import credentials, firestore
    FIREBASE_INSTALLED = True
except ImportError:
    FIREBASE_INSTALLED = False


# ──────────────────────────────────────────────
# Directory structure
# ──────────────────────────────────────────────

BASE_DIR = Path(__file__).parent.parent  # portfolio/

DATA_DIR   = BASE_DIR / "data"
ASSETS_DIR = BASE_DIR / "assets"

PROFILE_IMG_DIR  = ASSETS_DIR / "profile"
PROJECT_IMG_DIR  = ASSETS_DIR / "projects"
CERT_IMG_DIR     = ASSETS_DIR / "certificates"
RESUME_DIR       = ASSETS_DIR / "resume"
VIDEO_DIR        = ASSETS_DIR / "video"

# JSON file paths
PROFILE_FILE      = DATA_DIR / "profile.json"
SKILLS_FILE       = DATA_DIR / "skills.json"
PROJECT_FILE      = DATA_DIR / "projects.json"
PROJECTS_FILE     = DATA_DIR / "projects.json"
CERTIFICATES_FILE = DATA_DIR / "certificates.json"
EXPERIENCE_FILE   = DATA_DIR / "experience.json"
MESSAGES_FILE     = DATA_DIR / "messages.json"


def ensure_dirs() -> None:
    """Create all required folders if they don't already exist."""
    dirs = [
        DATA_DIR,
        PROFILE_IMG_DIR,
        PROJECT_IMG_DIR,
        CERT_IMG_DIR,
        RESUME_DIR,
        VIDEO_DIR,
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)


# ──────────────────────────────────────────────
# Firebase Firestore Client
# ──────────────────────────────────────────────

def get_firestore_client():
    """
    Returns a Firestore client if credentials exist in st.secrets or local service key.
    Returns None if Firebase is not configured (gracefully falls back to local JSON files).
    """
    if not FIREBASE_INSTALLED:
        return None

    try:
        if not firebase_admin._apps:
            # 1. From Streamlit secrets: [firebase]
            if "firebase" in st.secrets:
                fb_secrets = dict(st.secrets["firebase"])
                # Fix private key newline formatting if needed
                if "private_key" in fb_secrets and isinstance(fb_secrets["private_key"], str):
                    fb_secrets["private_key"] = fb_secrets["private_key"].replace("\\n", "\n")
                cred = credentials.Certificate(fb_secrets)
                firebase_admin.initialize_app(cred)
            # 2. From serviceAccountKey.json file placed in workspace/portfolio
            elif (BASE_DIR / "serviceAccountKey.json").exists():
                cred = credentials.Certificate(str(BASE_DIR / "serviceAccountKey.json"))
                firebase_admin.initialize_app(cred)
            elif (BASE_DIR.parent / "serviceAccountKey.json").exists():
                cred = credentials.Certificate(str(BASE_DIR.parent / "serviceAccountKey.json"))
                firebase_admin.initialize_app(cred)
            else:
                return None
        return firestore.client()
    except Exception:
        return None


def is_firebase_connected() -> bool:
    """Check if Firebase Firestore is connected and working."""
    return get_firestore_client() is not None


# ──────────────────────────────────────────────
# Generic read / write helpers
# ──────────────────────────────────────────────

def load_json(path: Path, default=None):
    """
    Load a JSON file and return its contents.
    Returns `default` (or an empty dict) if the file is missing or corrupt.
    """
    if default is None:
        default = {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def save_json(path: Path, data) -> None:
    """
    Save `data` as JSON to `path` (direct write, Windows-safe).
    ensure_dirs() guarantees the parent folder exists first.
    """
    ensure_dirs()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    try:
        st.cache_data.clear()
    except Exception:
        pass


def get_doc(doc_name: str, default=None):
    """
    Fetch a document from the 'portfolio_data' collection in Firestore.
    If Firestore is available:
      - Returns doc if exists
      - If doc doesn't exist yet, seeds it with existing local JSON data and stores in Firestore.
    If Firestore is not available:
      - Falls back to local JSON file.
    """
    if default is None:
        default = {}
    local_file = DATA_DIR / f"{doc_name}.json"

    db = get_firestore_client()
    if db is not None:
        try:
            doc_ref = db.collection("portfolio_data").document(doc_name)
            doc_snapshot = doc_ref.get()
            if doc_snapshot.exists:
                data = doc_snapshot.to_dict()
                if data:
                    return data
            else:
                # Seed Firestore on first run from local JSON
                local_data = load_json(local_file, default)
                if local_data:
                    doc_ref.set(local_data)
                return local_data
        except Exception:
            pass

    return load_json(local_file, default)


def set_doc(doc_name: str, data: dict) -> None:
    """
    Save data to Firestore and also to local JSON file as backup.
    """
    local_file = DATA_DIR / f"{doc_name}.json"
    save_json(local_file, data)

    db = get_firestore_client()
    if db is not None:
        try:
            doc_ref = db.collection("portfolio_data").document(doc_name)
            doc_ref.set(data)
        except Exception:
            pass


# ──────────────────────────────────────────────
# Typed loaders — each returns a safe default (cached)
# ──────────────────────────────────────────────

@st.cache_data(show_spinner=False)
def load_profile() -> dict:
    defaults = {
        "name": "Kartikey Gupta",
        "tagline": "CSE Engineer | AI/ML Developer | Software Developer",
        "bio": "Passionate B.Tech CSE student interested in AI/ML and software development.",
        "short_bio": "B.Tech CSE student | AI/ML Enthusiast",
        "role": "B.Tech Computer Science Engineering Student",
        "graduation_year": "2027",
        "sgpa": "8.75",
        "college": "[PLACEHOLDER]",
        "location": "[PLACEHOLDER]",
        "email": "[PLACEHOLDER]",
        "phone": "",
        "github": "[PLACEHOLDER]",
        "linkedin": "[PLACEHOLDER]",
        "instagram": "",
        "resume_file": "assets/resume/resume.pdf",
        "profile_image": "assets/profile/profile.jpg",
        "intro_video": "assets/video/intro_video.mp4",
        "enable_intro_video": True,
        "showcase_video": "assets/video/vid_1.mp4",
        "enable_showcase_video": True,
        "showcase_title": "Cinematic Showcase",
        "showcase_subtitle": "Featured Highlights & Visual Reel",
        "interests": ["AI", "Machine Learning", "Software Development"],
    }
    data = get_doc("profile", defaults)
    # Fill in any missing keys with defaults
    for k, v in defaults.items():
        data.setdefault(k, v)
    return data


@st.cache_data(show_spinner=False)
def load_skills() -> dict:
    return get_doc("skills", {"categories": []})


@st.cache_data(show_spinner=False)
def load_projects() -> dict:
    return get_doc("projects", {"projects": []})


@st.cache_data(show_spinner=False)
def load_certificates() -> dict:
    return get_doc("certificates", {"certificates": []})


@st.cache_data(show_spinner=False)
def load_experience() -> dict:
    return get_doc("experience", {"experiences": []})


def load_messages() -> dict:
    return get_doc("messages", {"messages": []})


# ──────────────────────────────────────────────
# Typed savers
# ──────────────────────────────────────────────

def save_profile(data: dict) -> None:
    set_doc("profile", data)


def save_skills(data: dict) -> None:
    set_doc("skills", data)


def save_projects(data: dict) -> None:
    set_doc("projects", data)


def save_certificates(data: dict) -> None:
    set_doc("certificates", data)


def save_experience(data: dict) -> None:
    set_doc("experience", data)


def save_messages(data: dict) -> None:
    set_doc("messages", data)


# ──────────────────────────────────────────────
# Message helper
# ──────────────────────────────────────────────

def add_message(name: str, email: str, message: str) -> None:
    """Append a new contact form submission to messages."""
    data = load_messages()
    if "messages" not in data or not isinstance(data["messages"], list):
        data["messages"] = []
    data["messages"].append({
        "id": len(data["messages"]) + 1,
        "name": name,
        "email": email,
        "message": message,
        "timestamp": datetime.now().isoformat(),
        "read": False,
    })
    save_messages(data)


# ──────────────────────────────────────────────
# ID generation helpers
# ──────────────────────────────────────────────

def next_id(items: list) -> int:
    """Return max(existing ids) + 1, or 1 if list is empty."""
    if not items:
        return 1
    return max((item.get("id", 0) for item in items), default=0) + 1
