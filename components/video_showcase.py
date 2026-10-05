# -*- coding: utf-8 -*-
"""
components/video_showcase.py
============================
Cinematic Full-Screen Video Showcase Section placed between Certificates and Contact.
Features:
- Pure clean full-screen widescreen video player.
- Fully automatic: Plays with audio automatically when viewed / scrolled into view.
- Automatically pauses when scrolled away (to Contact or above).
- Resumes automatically when scrolled back into view.
- Manual mute/pause buttons removed as requested. Fullscreen control retained.
"""

import os
import base64
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

from utils.data_manager import load_profile


@st.cache_data(show_spinner=False)
def _get_showcase_video_b64() -> str:
    """Load the showcase video in base64 format."""
    profile = load_profile()
    if not profile.get("enable_showcase_video", True):
        return ""

    candidates = [
        profile.get("showcase_video", ""),
        "assets/video/vid_1.mp4",
        "vid_1.mp4",
        "portfolio/assets/video/vid_1.mp4",
        "assets/video/intro_video.mp4",
        "VIDEO.mp4",
    ]
    for p in candidates:
        if p and Path(p).exists() and Path(p).stat().st_size > 0:
            try:
                with open(p, "rb") as f:
                    return base64.b64encode(f.read()).decode("utf-8")
            except Exception:
                pass
    return ""


def render_video_showcase():
    """Render the full-screen cinematic video showcase section."""
    profile = load_profile()
    if not profile.get("enable_showcase_video", True):
        return

    video_b64 = _get_showcase_video_b64()
    if not video_b64:
        return

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;600;700&display=swap"/>
<style>
* {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

html, body {{
    background: transparent;
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    color: #e2e8f0;
    overflow: hidden;
    padding: 0;
    margin: 0;
    width: 100%;
    height: 100%;
}}

.showcase-container {{
    width: 100%;
    max-width: 1400px;
    margin: 0 auto;
    padding: 10px 0 20px;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
}}

/* ── Massive Cinematic Video Frame ── */
.cinematic-frame {{
    position: relative;
    width: 100%;
    height: calc(100% - 20px);
    min-height: 580px;
    border-radius: 26px;
    padding: 3px;
    background: linear-gradient(135deg, rgba(0, 212, 255, 0.5), rgba(168, 85, 247, 0.4), rgba(244, 63, 94, 0.4));
    box-shadow: 0 25px 80px rgba(0, 0, 0, 0.85), 0 0 45px rgba(0, 212, 255, 0.22), 0 0 75px rgba(168, 85, 247, 0.16);
    transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
}}

.cinematic-frame:hover {{
    box-shadow: 0 30px 95px rgba(0, 0, 0, 0.95), 0 0 60px rgba(0, 212, 255, 0.35), 0 0 95px rgba(168, 85, 247, 0.25);
}}

.video-wrapper {{
    position: relative;
    width: 100%;
    height: 100%;
    border-radius: 23px;
    overflow: hidden;
    background: #000000;
    display: flex;
    align-items: center;
    justify-content: center;
}}

#showcase-vid {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
    cursor: default;
    background: #000;
}}

/* ── Minimal Non-Intrusive HUD Overlay ── */
.hud-overlay {{
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 22px 28px;
    background: linear-gradient(180deg, rgba(0,0,0,0.55) 0%, transparent 22%, transparent 78%, rgba(0,0,0,0.75) 100%);
    opacity: 0.85;
    transition: opacity 0.3s ease;
    pointer-events: none;
    z-index: 10;
}}

.video-wrapper:hover .hud-overlay {{
    opacity: 1;
}}

.hud-top {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    pointer-events: auto;
    width: 100%;
}}

.hud-badge {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 7px 18px;
    border-radius: 50px;
    background: rgba(10, 15, 30, 0.90);
    border: 1px solid rgba(0, 212, 255, 0.35);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    color: #e2e8f0;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.76rem;
    font-weight: 700;
    letter-spacing: 0.5px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.5);
}}

.badge-pulse {{
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #00d4ff;
    box-shadow: 0 0 10px #00d4ff;
    animation: pulse 1.6s infinite ease-in-out;
}}

@keyframes pulse {{
    0%, 100% {{ transform: scale(1); opacity: 1; }}
    50% {{ transform: scale(1.4); opacity: 0.4; }}
}}

.hud-actions {{
    display: flex;
    align-items: center;
    gap: 10px;
}}

.hud-btn {{
    background: rgba(10, 15, 30, 0.90);
    border: 1px solid rgba(255, 255, 255, 0.20);
    border-radius: 50px;
    color: #ffffff;
    padding: 8px 18px;
    font-size: 0.82rem;
    font-weight: 600;
    display: inline-flex;
    align-items: center;
    gap: 7px;
    cursor: pointer;
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    transition: all 0.22s ease;
    user-select: none;
    outline: none;
    box-shadow: 0 4px 18px rgba(0,0,0,0.4);
}}

.hud-btn:hover {{
    background: rgba(0, 212, 255, 0.30);
    border-color: rgba(0, 212, 255, 0.7);
    box-shadow: 0 0 20px rgba(0, 212, 255, 0.45);
    transform: translateY(-2px);
}}

.hud-bottom {{
    display: flex;
    flex-direction: column;
    gap: 12px;
    pointer-events: auto;
    width: 100%;
}}

.progress-track {{
    width: 100%;
    height: 7px;
    background: rgba(255, 255, 255, 0.18);
    border-radius: 6px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    transition: height 0.2s ease;
}}

.progress-track:hover {{
    height: 11px;
}}

.progress-bar {{
    position: absolute;
    top: 0;
    left: 0;
    bottom: 0;
    width: 0%;
    background: linear-gradient(90deg, #00d4ff, #a855f7, #f43f5e);
    border-radius: 6px;
    box-shadow: 0 0 12px rgba(0, 212, 255, 0.9);
    transition: width 0.1s linear;
}}

.hud-info {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: #cbd5e1;
    font-size: 0.82rem;
    font-family: 'JetBrains Mono', monospace;
}}

/* True Fullscreen */
:fullscreen .video-wrapper,
:-webkit-full-screen .video-wrapper {{
    height: 100vh !important;
    max-height: 100vh !important;
    border-radius: 0 !important;
}}

:fullscreen .cinematic-frame,
:-webkit-full-screen .cinematic-frame {{
    height: 100vh !important;
    padding: 0 !important;
    border-radius: 0 !important;
}}
</style>
</head>
<body>

<div class="showcase-container">
    <div class="cinematic-frame" id="frame-box">
        <div class="video-wrapper" id="vid-wrapper">
            <video
                id="showcase-vid"
                src="data:video/mp4;base64,{video_b64}"
                playsinline
                loop
                preload="auto"
            ></video>

            <!-- Minimal HUD Overlay -->
            <div class="hud-overlay">
                <div class="hud-top">
                    <div class="hud-badge" id="status-badge">
                        <span class="badge-pulse" id="status-dot" style="background:#10b981; box-shadow:0 0 8px #10b981;"></span>
                        <span id="status-text">AUTO-PLAYING</span>
                    </div>

                    <div class="hud-actions">
                        <button type="button" class="hud-btn" id="btn-fs" title="Fullscreen">
                            <span>⛶</span>
                            <span>Fullscreen</span>
                        </button>
                    </div>
                </div>

                <div class="hud-bottom">
                    <div class="progress-track" id="prog-track">
                        <div class="progress-bar" id="prog-bar"></div>
                    </div>
                    <div class="hud-info">
                        <span style="display:inline-flex; align-items:center; gap:8px;">
                            <span style="color:#00d4ff;">●</span> 1080p Ultra-HD Reel
                        </span>
                        <span id="time-lbl">0:00 / 0:00</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
(function initAutoVideoPlayer() {{
    const video = document.getElementById('showcase-vid');
    const wrapper = document.getElementById('vid-wrapper');
    const frameBox = document.getElementById('frame-box');
    const statusText = document.getElementById('status-text');
    const statusDot = document.getElementById('status-dot');
    const btnFs = document.getElementById('btn-fs');
    const progTrack = document.getElementById('prog-track');
    const progBar = document.getElementById('prog-bar');
    const timeLbl = document.getElementById('time-lbl');

    function fmtTime(s) {{
        if (isNaN(s)) return '0:00';
        const m = Math.floor(s / 60);
        const sec = Math.floor(s % 60);
        return m + ':' + (sec < 10 ? '0' : '') + sec;
    }}

    function setPlayStatus(playing) {{
        if (playing) {{
            statusText.textContent = 'LIVE PLAYING';
            statusDot.style.background = '#00d4ff';
            statusDot.style.boxShadow = '0 0 10px #00d4ff';
        }} else {{
            statusText.textContent = 'PAUSED';
            statusDot.style.background = '#f59e0b';
            statusDot.style.boxShadow = '0 0 10px #f59e0b';
        }}
    }}

    video.addEventListener('play', () => setPlayStatus(true));
    video.addEventListener('pause', () => setPlayStatus(false));

    video.addEventListener('timeupdate', () => {{
        if (video.duration) {{
            const pct = (video.currentTime / video.duration) * 100;
            progBar.style.width = pct + '%';
            timeLbl.textContent = fmtTime(video.currentTime) + ' / ' + fmtTime(video.duration);
        }}
    }});

    // Fullscreen toggle
    if (btnFs) {{
        btnFs.addEventListener('click', (e) => {{
            e.stopPropagation();
            if (!document.fullscreenElement) {{
                if (wrapper.requestFullscreen) wrapper.requestFullscreen();
                else if (wrapper.webkitRequestFullscreen) wrapper.webkitRequestFullscreen();
                else if (video.requestFullscreen) video.requestFullscreen();
            }} else {{
                if (document.exitFullscreen) document.exitFullscreen();
            }}
        }});
    }}

    // Seek track
    if (progTrack) {{
        progTrack.addEventListener('click', (e) => {{
            e.stopPropagation();
            const r = progTrack.getBoundingClientRect();
            const clickX = e.clientX - r.left;
            if (r.width > 0 && video.duration) {{
                video.currentTime = (clickX / r.width) * video.duration;
            }}
        }});
    }}

    /* ── Fully Automatic Play / Audio / Pause on Scroll ── */
    function autoPlayWithAudio() {{
        video.muted = false;
        video.volume = 1.0;
        const p = video.play();
        if (p !== undefined) {{
            p.catch(function() {{
                // If browser blocks unmuted auto-play without prior gesture, start muted then unmute on next user action
                video.muted = true;
                video.play().catch(function() {{}});

                function unmuteOnGesture() {{
                    video.muted = false;
                    video.volume = 1.0;
                    window.removeEventListener('click', unmuteOnGesture);
                    window.removeEventListener('scroll', unmuteOnGesture);
                    if (window.parent) {{
                        window.parent.removeEventListener('click', unmuteOnGesture);
                        window.parent.removeEventListener('scroll', unmuteOnGesture);
                    }}
                }}
                window.addEventListener('click', unmuteOnGesture, {{ once: true }});
                window.addEventListener('scroll', unmuteOnGesture, {{ once: true }});
                if (window.parent) {{
                    window.parent.addEventListener('click', unmuteOnGesture, {{ once: true }});
                    window.parent.addEventListener('scroll', unmuteOnGesture, {{ once: true }});
                }}
            }});
        }}
    }}

    function checkViewport() {{
        try {{
            const frame = window.frameElement;
            if (!frame) {{
                const r = frameBox.getBoundingClientRect();
                const vh = window.innerHeight;
                const vis = (r.top < vh * 0.85) && (r.bottom > vh * 0.15);
                if (vis && video.paused) autoPlayWithAudio();
                else if (!vis && !video.paused) video.pause();
                return;
            }}

            const pWin = window.parent;
            const r = frame.getBoundingClientRect();
            const vh = pWin.innerHeight || 800;

            const isVisible = (r.top < vh * 0.82) && (r.bottom > vh * 0.18);

            if (isVisible) {{
                if (video.paused) {{
                    autoPlayWithAudio();
                }}
            }} else {{
                if (!video.paused) {{
                    video.pause();
                }}
            }}
        }} catch(e) {{}}
    }}

    try {{
        if (window.parent) {{
            const pDoc = window.parent.document;
            const sc = pDoc.querySelector('[data-testid="stAppViewContainer"]') || window.parent;
            if (sc.addEventListener) sc.addEventListener('scroll', checkViewport, {{ passive: true }});
            if (window.parent.addEventListener) window.parent.addEventListener('scroll', checkViewport, {{ passive: true }});
        }}
    }} catch(e) {{}}

    window.addEventListener('scroll', checkViewport, {{ passive: true }});

    setTimeout(checkViewport, 200);
    setTimeout(checkViewport, 600);
    setInterval(checkViewport, 300);
}})();
</script>
</body>
</html>"""

    components.html(html_content, height=720, scrolling=False)
