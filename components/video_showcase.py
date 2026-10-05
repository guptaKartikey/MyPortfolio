# -*- coding: utf-8 -*-
"""
components/video_showcase.py
============================
Cinematic Full-Screen Video Showcase Section placed between Certificates and Contact.
Features:
- Fullscreen immersive player rendered via components.html for 100% reliable execution.
- Scroll-synced auto-playback: Automatically plays when entering viewport,
  pauses when scrolling down to Contact or scrolling up above.
- Interactive HUD: Play/Pause, Mute/Unmute, Fullscreen toggle, progress seek bar.
- Admin customizable via profile data.
"""

import os
import base64
from pathlib import Path
import streamlit.components.v1 as components

from utils.data_manager import load_profile


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

    title = profile.get("showcase_title", "Cinematic Showcase")
    subtitle = profile.get("showcase_subtitle", "Featured Visual Highlights & Project Demo Reel")

    title_parts = title.split(" ", 1)
    title_first = title_parts[0] if title_parts else "Cinematic"
    title_rest = title_parts[1] if len(title_parts) > 1 else "Showcase"

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;600;700&family=Caveat:wght@600;700&display=swap"/>
<style>
* {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

body {{
    background: transparent;
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    color: #e2e8f0;
    overflow: hidden;
    padding: 10px 14px 20px;
    width: 100%;
    margin: 0 auto;
}}

.showcase-container {{
    max-width: 1300px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    gap: 16px;
}}

/* ── Section Header ── */
.video-header {{
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
}}

.video-badge {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 5px 16px;
    border-radius: 50px;
    background: rgba(0, 212, 255, 0.08);
    border: 1px solid rgba(0, 212, 255, 0.3);
    color: #00d4ff;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 8px;
    box-shadow: 0 0 15px rgba(0, 212, 255, 0.12);
}}

.badge-pulse {{
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #00d4ff;
    box-shadow: 0 0 8px #00d4ff;
    animation: pulse 1.6s infinite ease-in-out;
}}

@keyframes pulse {{
    0%, 100% {{ transform: scale(1); opacity: 1; }}
    50% {{ transform: scale(1.4); opacity: 0.4; }}
}}

.video-title {{
    font-size: clamp(1.8rem, 3.2vw, 2.5rem);
    font-weight: 900;
    color: #ffffff;
    letter-spacing: -0.5px;
    line-height: 1.1;
    margin-bottom: 6px;
}}

.video-title-accent {{
    background: linear-gradient(135deg, #00d4ff 0%, #a855f7 50%, #f43f5e 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}}

.video-subtitle {{
    color: #94a3b8;
    font-size: 0.90rem;
    max-width: 600px;
    line-height: 1.5;
}}

.video-handwritten {{
    position: absolute;
    right: 20px;
    top: 5px;
    font-family: 'Caveat', cursive;
    font-size: 1.45rem;
    color: #00d4ff;
    transform: rotate(-3deg);
    opacity: 0.95;
    text-shadow: 0 0 12px rgba(0, 212, 255, 0.4);
}}

@media (max-width: 768px) {{
    .video-handwritten {{ display: none; }}
}}

/* ── Cinematic Video Frame ── */
.cinematic-frame {{
    position: relative;
    width: 100%;
    border-radius: 22px;
    padding: 3px;
    background: linear-gradient(135deg, rgba(0, 212, 255, 0.45), rgba(168, 85, 247, 0.35), rgba(244, 63, 94, 0.35));
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.8), 0 0 35px rgba(0, 212, 255, 0.18), 0 0 60px rgba(168, 85, 247, 0.12);
    transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
}}

.cinematic-frame:hover {{
    box-shadow: 0 25px 75px rgba(0, 0, 0, 0.9), 0 0 50px rgba(0, 212, 255, 0.30), 0 0 80px rgba(168, 85, 247, 0.22);
}}

.video-wrapper {{
    position: relative;
    width: 100%;
    height: 480px;
    max-height: 65vh;
    border-radius: 19px;
    overflow: hidden;
    background: #05050a;
    display: flex;
    align-items: center;
    justify-content: center;
}}

#showcase-vid {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
    cursor: pointer;
    background: #000;
}}

/* ── HUD Controls Overlay ── */
.hud-overlay {{
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 18px 22px;
    background: linear-gradient(180deg, rgba(0,0,0,0.60) 0%, transparent 25%, transparent 75%, rgba(0,0,0,0.80) 100%);
    opacity: 0.95;
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
    padding: 6px 14px;
    border-radius: 50px;
    background: rgba(10, 15, 30, 0.88);
    border: 1px solid rgba(0, 212, 255, 0.3);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    color: #e2e8f0;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.74rem;
    font-weight: 700;
    letter-spacing: 0.5px;
}}

.hud-actions {{
    display: flex;
    align-items: center;
    gap: 8px;
}}

.hud-btn {{
    background: rgba(10, 15, 30, 0.88);
    border: 1px solid rgba(255, 255, 255, 0.18);
    border-radius: 50px;
    color: #ffffff;
    padding: 7px 14px;
    font-size: 0.78rem;
    font-weight: 600;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    cursor: pointer;
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    transition: all 0.2s ease;
    user-select: none;
    outline: none;
}}

.hud-btn:hover {{
    background: rgba(0, 212, 255, 0.28);
    border-color: rgba(0, 212, 255, 0.6);
    box-shadow: 0 0 16px rgba(0, 212, 255, 0.4);
    transform: translateY(-2px);
}}

.hud-btn.active {{
    background: rgba(0, 212, 255, 0.35);
    border-color: #00d4ff;
    color: #00d4ff;
}}

.hud-bottom {{
    display: flex;
    flex-direction: column;
    gap: 10px;
    pointer-events: auto;
    width: 100%;
}}

.progress-track {{
    width: 100%;
    height: 6px;
    background: rgba(255, 255, 255, 0.16);
    border-radius: 6px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    transition: height 0.2s ease;
}}

.progress-track:hover {{
    height: 9px;
}}

.progress-bar {{
    position: absolute;
    top: 0;
    left: 0;
    bottom: 0;
    width: 0%;
    background: linear-gradient(90deg, #00d4ff, #a855f7, #f43f5e);
    border-radius: 6px;
    box-shadow: 0 0 10px rgba(0, 212, 255, 0.8);
    transition: width 0.1s linear;
}}

.hud-info {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: #cbd5e1;
    font-size: 0.78rem;
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
    padding: 0 !important;
    border-radius: 0 !important;
}}
</style>
</head>
<body>

<div class="showcase-container">
    <!-- Header -->
    <div class="video-header">
        <div class="video-badge">
            <span class="badge-pulse"></span>
            <span>FEATURED SHOWCASE</span>
        </div>
        <div class="video-title">
            {title_first} <span class="video-title-accent">{title_rest}</span>
        </div>
        <div class="video-subtitle">
            {subtitle}
        </div>
        <div class="video-handwritten">
            Scroll-Synced &amp; Fullscreen ⚡
        </div>
    </div>

    <!-- Frame -->
    <div class="cinematic-frame" id="frame-box">
        <div class="video-wrapper" id="vid-wrapper">
            <video
                id="showcase-vid"
                src="data:video/mp4;base64,{video_b64}"
                playsinline
                muted
                loop
                preload="auto"
            ></video>

            <!-- HUD Overlay -->
            <div class="hud-overlay">
                <div class="hud-top">
                    <div class="hud-badge" id="status-badge">
                        <span class="badge-pulse" id="status-dot" style="background:#10b981; box-shadow:0 0 8px #10b981;"></span>
                        <span id="status-text">SCROLL-SYNC: READY</span>
                    </div>

                    <div class="hud-actions">
                        <button type="button" class="hud-btn" id="btn-sound" title="Toggle Sound">
                            <span id="sound-ic">🔇</span>
                            <span id="sound-lbl">Unmute</span>
                        </button>
                        <button type="button" class="hud-btn" id="btn-play" title="Play / Pause">
                            <span id="play-ic">▶</span>
                            <span id="play-lbl">Play</span>
                        </button>
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
                        <span style="display:inline-flex; align-items:center; gap:6px;">
                            <span style="color:#00d4ff;">●</span> 1080p Ultra-HD Video Reel
                        </span>
                        <span id="time-lbl">0:00 / 0:00</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
(function initPlayer() {{
    const video = document.getElementById('showcase-vid');
    const wrapper = document.getElementById('vid-wrapper');
    const frameBox = document.getElementById('frame-box');
    const statusText = document.getElementById('status-text');
    const statusDot = document.getElementById('status-dot');
    const btnPlay = document.getElementById('btn-play');
    const playIc = document.getElementById('play-ic');
    const playLbl = document.getElementById('play-lbl');
    const btnSound = document.getElementById('btn-sound');
    const soundIc = document.getElementById('sound-ic');
    const soundLbl = document.getElementById('sound-lbl');
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

    function setPlayState(playing) {{
        if (playing) {{
            playIc.textContent = '⏸';
            playLbl.textContent = 'Pause';
            statusText.textContent = 'SCROLL-SYNC: PLAYING';
            statusDot.style.background = '#00d4ff';
            statusDot.style.boxShadow = '0 0 8px #00d4ff';
        }} else {{
            playIc.textContent = '▶';
            playLbl.textContent = 'Play';
            statusText.textContent = 'SCROLL-SYNC: PAUSED';
            statusDot.style.background = '#f59e0b';
            statusDot.style.boxShadow = '0 0 8px #f59e0b';
        }}
    }}

    function setSoundState(muted) {{
        if (muted) {{
            soundIc.textContent = '🔇';
            soundLbl.textContent = 'Unmute';
            btnSound.classList.remove('active');
        }} else {{
            soundIc.textContent = '🔊';
            soundLbl.textContent = 'Mute';
            btnSound.classList.add('active');
        }}
    }}

    video.addEventListener('play', () => setPlayState(true));
    video.addEventListener('pause', () => setPlayState(false));
    video.addEventListener('volumechange', () => setSoundState(video.muted));

    video.addEventListener('timeupdate', () => {{
        if (video.duration) {{
            const pct = (video.currentTime / video.duration) * 100;
            progBar.style.width = pct + '%';
            timeLbl.textContent = fmtTime(video.currentTime) + ' / ' + fmtTime(video.duration);
        }}
    }});

    // Direct click on video to play/pause
    video.addEventListener('click', () => {{
        if (video.paused) video.play();
        else video.pause();
    }});

    btnPlay.addEventListener('click', (e) => {{
        e.stopPropagation();
        if (video.paused) video.play();
        else video.pause();
    }});

    btnSound.addEventListener('click', (e) => {{
        e.stopPropagation();
        video.muted = !video.muted;
        setSoundState(video.muted);
        if (!video.muted && video.paused) video.play();
    }});

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

    progTrack.addEventListener('click', (e) => {{
        e.stopPropagation();
        const r = progTrack.getBoundingClientRect();
        const clickX = e.clientX - r.left;
        if (r.width > 0 && video.duration) {{
            video.currentTime = (clickX / r.width) * video.duration;
        }}
    }});

    /* ── Viewport Scroll Sync via Parent Window ── */
    function checkViewport() {{
        try {{
            const frame = window.frameElement;
            if (!frame) {{
                // Fallback: If not in iframe, check local window
                const r = frameBox.getBoundingClientRect();
                const vh = window.innerHeight;
                const vis = (r.top < vh * 0.85) && (r.bottom > vh * 0.15);
                if (vis && video.paused) video.play().catch(() => {{ video.muted = true; video.play(); }});
                else if (!vis && !video.paused) video.pause();
                return;
            }}

            const pWin = window.parent;
            const r = frame.getBoundingClientRect();
            const vh = pWin.innerHeight || 800;

            // When at least ~20% of video is visible
            const isVisible = (r.top < vh * 0.82) && (r.bottom > vh * 0.18);

            if (isVisible) {{
                if (video.paused) {{
                    const p = video.play();
                    if (p !== undefined) {{
                        p.catch(() => {{
                            video.muted = true;
                            video.play().catch(() => {{}});
                        }});
                    }}
                }}
            }} else {{
                if (!video.paused) {{
                    video.pause();
                }}
            }}
        }} catch(e) {{}}
    }}

    // Attach listeners to parent window & scroll containers
    try {{
        if (window.parent) {{
            const pDoc = window.parent.document;
            const sc = pDoc.querySelector('[data-testid="stAppViewContainer"]') || window.parent;
            if (sc.addEventListener) sc.addEventListener('scroll', checkViewport, {{ passive: true }});
            if (window.parent.addEventListener) window.parent.addEventListener('scroll', checkViewport, {{ passive: true }});
        }}
    }} catch(e) {{}}

    window.addEventListener('scroll', checkViewport, {{ passive: true }});

    // Check periodically on mount
    setTimeout(checkViewport, 300);
    setTimeout(checkViewport, 800);
    setTimeout(checkViewport, 1500);
    setInterval(checkViewport, 400);
}})();
</script>
</body>
</html>"""

    components.html(html_content, height=650, scrolling=False)
