"""
components/preloader.py
=======================
Cinematic intro splash preloader featuring:
1. Interactive lamp pull-rope reveal with banner photo.
2. Smooth transition to widescreen cinematic video player (with top-right "Skip Intro ⏩" button).
3. Dramatic dissolve & splash transition that reveals the website and triggers ambient music.
"""

import os
import base64
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components
from utils.data_manager import load_profile


@st.cache_data(show_spinner=False)
def _get_intro_img_b64() -> str:
    """Load optimized intro image in base64."""
    for p in ["assets/intro.jpg", "img.png", "assets/intro_banner.png"]:
        path = Path(p)
        if path.exists():
            try:
                with open(path, "rb") as f:
                    return base64.b64encode(f.read()).decode("utf-8")
            except Exception:
                pass
    return ""


@st.cache_data(show_spinner=False)
def _get_intro_video_b64() -> str:
    """Load intro video in base64 if enabled and available."""
    profile = load_profile()
    if not profile.get("enable_intro_video", True):
        return ""

    candidates = [
        profile.get("intro_video", ""),
        "assets/video/intro_video.mp4",
        "assets/VIDEO.mp4",
        "VIDEO.mp4",
        "assets/video/intro.mp4",
    ]
    for p in candidates:
        if p and Path(p).exists() and Path(p).stat().st_size > 0:
            try:
                with open(p, "rb") as f:
                    return base64.b64encode(f.read()).decode("utf-8")
            except Exception:
                pass
    return ""


def render_preloader():
    """Render the cinematic intro preloader overlay with video stage & dissolve splash."""
    img_b64 = _get_intro_img_b64()
    if not img_b64:
        return

    video_b64 = _get_intro_video_b64()
    has_video_js = "true" if video_b64 else "false"
    video_src_js = f'"data:video/mp4;base64,{video_b64}"' if video_b64 else '""'

    components.html(f"""
    <script>
    (function setupCinematicPreloader() {{
        try {{
            var pDoc = window.parent ? window.parent.document : document;
            if (pDoc.getElementById('intro-preloader-overlay')) {{
                return; // already inserted
            }}

            var hasVideo = {has_video_js};
            var videoSrc = {video_src_js};

            var overlay = pDoc.createElement('div');
            overlay.id = 'intro-preloader-overlay';
            overlay.innerHTML = `
                <style>
                #intro-preloader-overlay {{
                    position: fixed !important;
                    top: 0 !important;
                    left: 0 !important;
                    width: 100vw !important;
                    height: 100vh !important;
                    z-index: 9999999999 !important;
                    background: #020308 !important;
                    display: flex !important;
                    align-items: center !important;
                    justify-content: center !important;
                    overflow: hidden !important;
                    transition: opacity 0.75s cubic-bezier(0.16, 1, 0.3, 1), filter 0.75s ease, transform 0.75s cubic-bezier(0.16, 1, 0.3, 1) !important;
                    will-change: opacity, filter, transform !important;
                    user-select: none !important;
                    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
                    touch-action: manipulation !important;
                }}

                /* ── Dissolve & Splash Transition ── */
                #intro-preloader-overlay.intro-dissolve {{
                    opacity: 0 !important;
                    filter: blur(35px) brightness(1.6) saturate(1.4) !important;
                    transform: scale(1.08) !important;
                    pointer-events: none !important;
                }}

                .preloader-ambient-bg {{
                    position: absolute;
                    inset: 0;
                    background:
                        radial-gradient(circle 800px at 20% 70%, rgba(0, 212, 255, 0.20) 0%, transparent 60%),
                        radial-gradient(circle 700px at 80% 30%, rgba(168, 85, 247, 0.22) 0%, transparent 60%),
                        radial-gradient(circle 500px at 50% 50%, rgba(245, 158, 11, 0.12) 0%, transparent 60%),
                        #020308;
                    pointer-events: none;
                }}

                /* ── Stage 1: Photo Banner Frame ── */
                .preloader-frame-wrap {{
                    position: relative;
                    width: 92vw;
                    max-width: 1120px;
                    aspect-ratio: 1536 / 1024;
                    max-height: 86vh;
                    border-radius: 22px;
                    overflow: hidden;
                    box-shadow: 0 25px 70px rgba(0, 0, 0, 0.9), 0 0 50px rgba(0, 212, 255, 0.25), 0 0 80px rgba(168, 85, 247, 0.18);
                    border: 2px solid rgba(0, 212, 255, 0.35);
                    background: #000;
                    cursor: pointer;
                    transition: opacity 0.5s ease, transform 0.5s ease;
                    touch-action: manipulation;
                }}

                .preloader-main-img {{
                    width: 100%;
                    height: 100%;
                    object-fit: contain;
                    display: block;
                }}

                /* Hanging Lamp Pull Rope */
                .lamp-rope-container {{
                    position: absolute;
                    top: 0;
                    right: 50px;
                    z-index: 100;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    cursor: pointer;
                    transition: transform 0.25s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                    touch-action: manipulation;
                }}
                .lamp-rope-container:hover,
                .lamp-rope-container:active {{
                    transform: translateY(12px);
                }}
                .lamp-rope-container.pulled {{
                    transform: translateY(35px) scale(0.96) !important;
                }}
                .lamp-cord {{
                    width: 3.5px;
                    height: 140px;
                    background: linear-gradient(to bottom, rgba(255, 255, 255, 0.5), #f59e0b, #eab308);
                    box-shadow: 0 0 14px rgba(245, 158, 11, 0.7);
                    animation: ropeSway 3s ease-in-out infinite alternate;
                    transform-origin: top center;
                }}
                .lamp-handle {{
                    width: 36px;
                    height: 52px;
                    border-radius: 18px;
                    background: linear-gradient(135deg, #f59e0b, #d97706);
                    border: 2.5px solid #fef08a;
                    box-shadow: 0 0 28px rgba(245, 158, 11, 1), 0 4px 18px rgba(0, 0, 0, 0.7);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 1.3rem;
                    color: #000;
                    font-weight: 900;
                    cursor: pointer;
                    margin-top: -2px;
                    transition: transform 0.2s ease, box-shadow 0.2s ease;
                }}
                .lamp-rope-container:hover .lamp-handle,
                .lamp-rope-container:active .lamp-handle {{
                    transform: scale(1.15);
                    box-shadow: 0 0 35px rgba(245, 158, 11, 1), 0 0 15px #ffffff;
                }}
                .lamp-rope-tag {{
                    margin-top: 10px;
                    padding: 7px 16px;
                    border-radius: 50px;
                    background: rgba(0, 0, 0, 0.9);
                    border: 2px solid rgba(245, 158, 11, 0.75);
                    color: #fef08a;
                    font-size: 0.82rem;
                    font-weight: 800;
                    letter-spacing: 0.5px;
                    white-space: nowrap;
                    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.7), 0 0 15px rgba(245, 158, 11, 0.5);
                    animation: pulseGlow 1.8s infinite ease-in-out alternate;
                }}

                @keyframes ropeSway {{
                    0% {{ transform: rotate(-3deg); }}
                    100% {{ transform: rotate(3deg); }}
                }}
                @keyframes pulseGlow {{
                    0% {{ box-shadow: 0 0 8px rgba(245, 158, 11, 0.3); }}
                    100% {{ box-shadow: 0 0 22px rgba(245, 158, 11, 0.9); color: #ffffff; }}
                }}

                /* ── Stage 2: Cinematic Video Player ── */
                .preloader-video-stage {{
                    position: absolute;
                    inset: 0;
                    display: none;
                    align-items: center;
                    justify-content: center;
                    z-index: 200;
                    background: #000000;
                    opacity: 0;
                    transition: opacity 0.5s cubic-bezier(0.16, 1, 0.3, 1);
                    cursor: pointer;
                }}
                .preloader-video-stage.video-active {{
                    display: flex !important;
                    opacity: 1 !important;
                }}

                .preloader-video-container {{
                    position: relative;
                    width: 92vw;
                    max-width: 1200px;
                    max-height: 82vh;
                    aspect-ratio: 16 / 9;
                    border-radius: 22px;
                    overflow: hidden;
                    box-shadow: 0 30px 90px rgba(0, 0, 0, 0.95), 0 0 60px rgba(0, 212, 255, 0.3), 0 0 100px rgba(168, 85, 247, 0.25);
                    border: 2px solid rgba(0, 212, 255, 0.4);
                    background: #000;
                }}

                .preloader-video-elem {{
                    width: 100%;
                    height: 100%;
                    object-fit: contain;
                    display: block;
                    background: #000;
                }}

                /* ── Top-Right Glowing Skip Button ── */
                .video-skip-btn {{
                    position: fixed !important;
                    top: max(20px, env(safe-area-inset-top, 20px)) !important;
                    right: max(20px, env(safe-area-inset-right, 20px)) !important;
                    z-index: 99999999999 !important;
                    display: inline-flex !important;
                    align-items: center !important;
                    gap: 8px !important;
                    padding: 12px 24px !important;
                    border-radius: 50px !important;
                    background: rgba(10, 12, 28, 0.92) !important;
                    border: 1.5px solid rgba(0, 212, 255, 0.6) !important;
                    color: #ffffff !important;
                    font-size: 0.92rem !important;
                    font-weight: 800 !important;
                    letter-spacing: 0.5px !important;
                    cursor: pointer !important;
                    backdrop-filter: blur(20px) !important;
                    -webkit-backdrop-filter: blur(20px) !important;
                    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.7), 0 0 25px rgba(0, 212, 255, 0.4) !important;
                    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
                    touch-action: manipulation !important;
                }}
                .video-skip-btn:hover,
                .video-skip-btn:active {{
                    transform: translateY(-2px) scale(1.04) !important;
                    background: linear-gradient(135deg, rgba(0, 212, 255, 0.45), rgba(168, 85, 247, 0.45)) !important;
                    border-color: #00d4ff !important;
                    box-shadow: 0 10px 35px rgba(0, 212, 255, 0.8), 0 0 30px rgba(168, 85, 247, 0.6) !important;
                }}

                .preloader-bottom-hint {{
                    position: absolute;
                    bottom: max(18px, env(safe-area-inset-bottom, 18px));
                    left: 50%;
                    transform: translateX(-50%);
                    color: rgba(255, 255, 255, 0.65);
                    font-size: 0.78rem;
                    letter-spacing: 0.5px;
                    pointer-events: none;
                    background: rgba(0, 0, 0, 0.6);
                    padding: 5px 14px;
                    border-radius: 20px;
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    backdrop-filter: blur(8px);
                }}

                .preloader-bottom-enter-btn {{
                    position: absolute;
                    bottom: 24px;
                    right: 32px;
                    padding: 10px 26px;
                    border-radius: 50px;
                    background: rgba(255, 255, 255, 0.12);
                    border: 1.5px solid rgba(0, 212, 255, 0.6);
                    color: #ffffff;
                    font-size: 0.86rem;
                    font-weight: 700;
                    cursor: pointer;
                    backdrop-filter: blur(14px);
                    transition: all 0.25s ease;
                    display: flex;
                    align-items: center;
                    gap: 8px;
                    z-index: 100;
                    box-shadow: 0 4px 20px rgba(0, 212, 255, 0.3);
                    touch-action: manipulation;
                }}
                .preloader-bottom-enter-btn:hover,
                .preloader-bottom-enter-btn:active {{
                    background: linear-gradient(135deg, rgba(0, 212, 255, 0.4), rgba(168, 85, 247, 0.4));
                    border-color: #00d4ff;
                    transform: translateY(-2px);
                    box-shadow: 0 6px 25px rgba(0, 212, 255, 0.6);
                }}

                /* ── Animated Splash Ripple Wave Effect ── */
                .splash-ripple-wave {{
                    position: absolute;
                    top: 50%;
                    left: 50%;
                    width: 10px;
                    height: 10px;
                    margin-top: -5px;
                    margin-left: -5px;
                    border-radius: 50%;
                    background: radial-gradient(circle, rgba(0, 212, 255, 0.95) 0%, rgba(168, 85, 247, 0.8) 40%, transparent 75%);
                    pointer-events: none;
                    opacity: 0;
                    z-index: 300;
                }}
                .splash-ripple-wave.splash-animate {{
                    animation: rippleExpand 0.85s cubic-bezier(0.16, 1, 0.3, 1) forwards;
                }}
                @keyframes rippleExpand {{
                    0% {{ transform: scale(1); opacity: 0.95; }}
                    100% {{ transform: scale(350); opacity: 0; }}
                }}

                @media (max-width: 768px) {{
                    .lamp-rope-container {{ right: 14px; top: 0; }}
                    .lamp-cord {{ height: 85px; width: 3px; }}
                    .lamp-handle {{ width: 32px; height: 46px; font-size: 1.15rem; }}
                    .lamp-rope-tag {{ font-size: 0.72rem; padding: 5px 10px; margin-top: 6px; }}
                    .video-skip-btn {{
                        top: max(14px, env(safe-area-inset-top, 14px)) !important;
                        right: max(14px, env(safe-area-inset-right, 14px)) !important;
                        padding: 10px 20px !important;
                        font-size: 0.82rem !important;
                    }}
                    .preloader-bottom-enter-btn {{ bottom: 14px; right: 14px; padding: 8px 18px; font-size: 0.78rem; }}
                    .preloader-video-container {{
                        width: 95vw;
                        border-radius: 16px;
                    }}
                }}
                </style>

                <div class="preloader-ambient-bg"></div>

                <!-- Stage 1: Hanging Lamp Pull Rope & Banner Photo -->
                <div class="lamp-rope-container" id="lamp-rope-trigger" title="Pull rope to enter!">
                    <div class="lamp-cord"></div>
                    <div class="lamp-handle">&#128161;</div>
                    <div class="lamp-rope-tag">&#10024; Pull Rope to Enter</div>
                </div>

                <div class="preloader-frame-wrap" id="preloader-photo-frame" title="Click anywhere to enter">
                    <img src="data:image/jpeg;base64,{img_b64}" alt="Kartikey Gupta Portfolio" class="preloader-main-img" />
                </div>

                <button class="preloader-bottom-enter-btn" id="preloader-enter-trigger">
                    <span>Enter Portfolio</span> &rarr;
                </button>

                <!-- Stage 2: Fullscreen Cinematic Video Player with Skip Button in Right Corner -->
                <div class="preloader-video-stage" id="preloader-video-stage" title="Tap to skip intro">
                    <button class="video-skip-btn" id="video-skip-btn" title="Skip Intro & Enter">
                        <span>Skip Intro</span> &nbsp;⏩
                    </button>
                    <div class="preloader-video-container">
                        <video
                            class="preloader-video-elem"
                            id="preloader-video-elem"
                            playsinline
                            webkit-playsinline
                            x5-playsinline
                            x5-video-player-type="h5-page"
                            preload="auto">
                        </video>
                    </div>
                    <div class="preloader-bottom-hint">Tap anywhere to skip intro</div>
                </div>

                <!-- Stage 3: Splash Ripple Wave -->
                <div class="splash-ripple-wave" id="splash-ripple-wave"></div>
            `;

            pDoc.body.appendChild(overlay);

            var ropeTrigger = pDoc.getElementById('lamp-rope-trigger');
            var enterTrigger = pDoc.getElementById('preloader-enter-trigger');
            var photoFrame = pDoc.getElementById('preloader-photo-frame');
            var videoStage = pDoc.getElementById('preloader-video-stage');
            var videoElem = pDoc.getElementById('preloader-video-elem');
            var skipBtn = pDoc.getElementById('video-skip-btn');
            var splashWave = pDoc.getElementById('splash-ripple-wave');

            var isDismissed = false;
            var safetyTimer = null;

            function startBackgroundMusic() {{
                try {{
                    function tryPlay() {{
                        var audio = (window.parent && window.parent.document ? window.parent.document.getElementById('portfolio-audio-elem') : null) || document.getElementById('portfolio-audio-elem');
                        if (audio) {{
                            if (audio.paused) {{
                                var p = audio.play();
                                if (p !== undefined) {{
                                    p.catch(function(e) {{
                                        console.log('Autoplay deferred on mobile, will play on next user gesture:', e);
                                        function playOnTouch() {{
                                            audio.play().catch(function() {{}});
                                            pDoc.removeEventListener('click', playOnTouch);
                                            pDoc.removeEventListener('touchstart', playOnTouch);
                                            pDoc.removeEventListener('scroll', playOnTouch);
                                        }}
                                        pDoc.addEventListener('click', playOnTouch, {{ once: true, passive: true }});
                                        pDoc.addEventListener('touchstart', playOnTouch, {{ once: true, passive: true }});
                                        pDoc.addEventListener('scroll', playOnTouch, {{ once: true, passive: true }});
                                    }});
                                }}
                            }}
                            return true;
                        }}
                        return false;
                    }}

                    if (!tryPlay()) {{
                        var retries = 0;
                        var timer = setInterval(function() {{
                            retries++;
                            if (tryPlay() || retries >= 20) {{
                                clearInterval(timer);
                            }}
                        }}, 150);
                    }}
                }} catch(err) {{
                    console.error('Audio play error:', err);
                }}
            }}

            /* ── Dissolve & Splash Reveal Website ── */
            function executeDissolveAndSplash() {{
                if (isDismissed) return;
                isDismissed = true;

                if (safetyTimer) {{
                    clearTimeout(safetyTimer);
                    safetyTimer = null;
                }}

                // Stop video cleanly
                if (videoElem) {{
                    try {{
                        videoElem.pause();
                        videoElem.removeAttribute('src');
                        videoElem.load();
                    }} catch(e) {{}}
                }}

                // Start ambient background music
                startBackgroundMusic();

                // Trigger glowing ripple splash wave
                if (splashWave) {{
                    splashWave.classList.add('splash-animate');
                }}

                // Dissolve overlay with blur & splash
                setTimeout(function() {{
                    if (overlay) {{
                        overlay.classList.add('intro-dissolve');
                        setTimeout(function() {{
                            if (overlay.parentNode) {{
                                overlay.parentNode.removeChild(overlay);
                            }}
                        }}, 800);
                    }}
                }}, 100);
            }}

            /* ── Robust Video Playback with Muted Fallback for Phones ── */
            function startVideoSafely() {{
                if (!videoElem || !videoSrc) {{
                    executeDissolveAndSplash();
                    return;
                }}

                videoElem.src = videoSrc;
                videoElem.volume = 0.85;

                // Event handlers to ensure it never gets stuck
                videoElem.onended = function() {{
                    executeDissolveAndSplash();
                }};
                videoElem.onerror = function(err) {{
                    console.warn('Video failed to load or decode, dissolving smoothly:', err);
                    executeDissolveAndSplash();
                }};

                // Try playing with audio synchronously
                var p = videoElem.play();
                if (p !== undefined) {{
                    p.then(function() {{
                        // Successfully playing
                        armSafetyTimer();
                    }}).catch(function(err) {{
                        console.warn('Direct unmuted play blocked on mobile, retrying muted:', err);
                        // Mobile browser blocked unmuted autoplay -> immediately switch to muted and play
                        videoElem.muted = true;
                        videoElem.play().then(function() {{
                            armSafetyTimer();
                        }}).catch(function(finalErr) {{
                            console.error('Video playback completely unsupported/failed, dissolving:', finalErr);
                            executeDissolveAndSplash();
                        }});
                    }});
                }} else {{
                    armSafetyTimer();
                }}
            }}

            function armSafetyTimer() {{
                if (safetyTimer) clearTimeout(safetyTimer);
                // Set fallback timer based on video duration or safe default of 10s
                var durationSec = (videoElem && videoElem.duration && !isNaN(videoElem.duration) && videoElem.duration > 0) ? videoElem.duration : 10;
                var timeoutMs = Math.min(Math.max((durationSec + 2) * 1000, 5000), 20000);
                safetyTimer = setTimeout(function() {{
                    if (!isDismissed) {{
                        console.log('Video safety timeout reached, completing intro.');
                        executeDissolveAndSplash();
                    }}
                }}, timeoutMs);
            }}

            /* ── Handle Pull Rope / Enter Click ── */
            function onRopePulled() {{
                if (ropeTrigger) {{
                    ropeTrigger.classList.add('pulled');
                }}

                if (hasVideo && videoSrc && videoStage && videoElem) {{
                    // Hide stage 1 immediately
                    if (photoFrame) photoFrame.style.display = 'none';
                    if (ropeTrigger) ropeTrigger.style.display = 'none';
                    if (enterTrigger) enterTrigger.style.display = 'none';

                    // Activate video stage
                    videoStage.classList.add('video-active');

                    // Start video synchronously inside the user event handler
                    startVideoSafely();
                }} else {{
                    // No video: directly dissolve & splash
                    setTimeout(function() {{
                        executeDissolveAndSplash();
                    }}, 200);
                }}
            }}

            // Event bindings with multi-touch / click support
            function addMultiEvent(el, handler) {{
                if (!el) return;
                var triggered = false;
                function triggerOnce(e) {{
                    if (e) {{
                        e.preventDefault();
                        e.stopPropagation();
                    }}
                    if (!triggered) {{
                        triggered = true;
                        handler();
                        setTimeout(function() {{ triggered = false; }}, 500);
                    }}
                }}
                el.addEventListener('click', triggerOnce);
                el.addEventListener('touchend', triggerOnce, {{ passive: false }});
            }}

            addMultiEvent(ropeTrigger, onRopePulled);
            addMultiEvent(enterTrigger, onRopePulled);
            addMultiEvent(photoFrame, onRopePulled);

            // Skip button & tap anywhere on video stage to skip
            addMultiEvent(skipBtn, function() {{
                executeDissolveAndSplash();
            }});
            addMultiEvent(videoStage, function() {{
                executeDissolveAndSplash();
            }});

        }} catch(err) {{
            console.error(err);
        }}
    }})();
    </script>
    """, height=0, width=0)

