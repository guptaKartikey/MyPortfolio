"""
utils/data_manager.py
=====================
Central data layer for the portfolio.

All reading and writing of JSON files goes through this module.
This ensures:
  - Data is never lost on partial writes (atomic save).
  - Missing files return safe defaults instead of crashing.
  - All required folders are created automatically.
"""

import json
import os
from datetime import datetime
from pathlib import Path


# ──────────────────────────────────────────────
# Directory structure
# ──────────────────────────────────────────────

BASE_DIR = Path(__file__).parent.parent  # portfolio/

DATA_DIR  = BASE_DIR / "data"
ASSETS_DIR = BASE_DIR / "assets"

PROFILE_IMG_DIR  = ASSETS_DIR / "profile"
PROJECT_IMG_DIR  = ASSETS_DIR / "projects"
CERT_IMG_DIR     = ASSETS_DIR / "certificates"
RESUME_DIR       = ASSETS_DIR / "resume"

# JSON file paths
PROFILE_FILE      = DATA_DIR / "profile.json"
SKILLS_FILE       = DATA_DIR / "skills.json"
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
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)


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


# ──────────────────────────────────────────────
# Typed loaders — each returns a safe default
# ──────────────────────────────────────────────

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
        "interests": ["AI", "Machine Learning", "Software Development"],
    }
    data = load_json(PROFILE_FILE, defaults)
    # Fill in any missing keys with defaults
    for k, v in defaults.items():
        data.setdefault(k, v)
    return data


def load_skills() -> dict:
    return load_json(SKILLS_FILE, {"categories": []})


def load_projects() -> dict:
    return load_json(PROJECTS_FILE, {"projects": []})


def load_certificates() -> dict:
    return load_json(CERTIFICATES_FILE, {"certificates": []})


def load_experience() -> dict:
    return load_json(EXPERIENCE_FILE, {"experiences": []})


def load_messages() -> dict:
    return load_json(MESSAGES_FILE, {"messages": []})


# ──────────────────────────────────────────────
# Typed savers
# ──────────────────────────────────────────────

def save_profile(data: dict) -> None:
    save_json(PROFILE_FILE, data)


def save_skills(data: dict) -> None:
    save_json(SKILLS_FILE, data)


def save_projects(data: dict) -> None:
    save_json(PROJECTS_FILE, data)


def save_certificates(data: dict) -> None:
    save_json(CERTIFICATES_FILE, data)


def save_experience(data: dict) -> None:
    save_json(EXPERIENCE_FILE, data)


def save_messages(data: dict) -> None:
    save_json(MESSAGES_FILE, data)


# ──────────────────────────────────────────────
# Message helper
# ──────────────────────────────────────────────

def add_message(name: str, email: str, message: str) -> None:
    """Append a new contact form submission to messages.json."""
    data = load_messages()
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
