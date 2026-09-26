"""
components/preloader.py
=======================
Cinematic intro splash preloader featuring the user's photo with updated laptop screen
displaying "Welcome to My Portfolio Website" and an interactive lamp pull-rope reveal animation.
"""

import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import base64


def _get_intro_img_b64() -> str:
    """Load optimized intro image in base64."""
    for p in ["assets/intro.jpg", "img.png", "assets/intro_banner.png"]:
        path = Path(p)
        if path.exists():
            with open(path, "rb") as f:
                return base64.b64encode(f.read()).decode("utf-8")
    return ""


def render_preloader():
    """Render the cinematic intro preloader overlay with interactive pull-rope."""
    img_b64 = _get_intro_img_b64()
    if not img_b64:
        return

    # Injects the preloader directly into the top-level parent document
    components.html(f"""
    <script>
    (function setupCinematicPreloader() {{
        try {{
            var pDoc = window.parent ? window.parent.document : document;
            if (pDoc.getElementById('intro-preloader-overlay')) {{
                return; // already inserted
            }}

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
                    background: #030408 !important;
                    display: flex !important;
                    align-items: center !important;
                    justify-content: center !important;
                    overflow: hidden !important;
                    transition: transform 1.1s cubic-bezier(0.76, 0, 0.24, 1), opacity 0.6s ease 0.5s !important;
                    will-change: transform, opacity !important;
                    user-select: none !important;
                    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
                }}

                #intro-preloader-overlay.intro-dismissed {{
                    transform: translateY(-100%) !important;
                    opacity: 0.95 !important;
                    pointer-events: none !important;
                }}

                .preloader-ambient-bg {{
                    position: absolute;
                    inset: 0;
                    background:
                        radial-gradient(circle 800px at 20% 70%, rgba(0, 212, 255, 0.18) 0%, transparent 60%),
                        radial-gradient(circle 700px at 80% 30%, rgba(168, 85, 247, 0.20) 0%, transparent 60%),
                        radial-gradient(circle 500px at 50% 50%, rgba(245, 158, 11, 0.10) 0%, transparent 60%),
                        #030408;
                    pointer-events: none;
                }}

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
                }}
                .lamp-rope-container:hover {{
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
                    width: 32px;
                    height: 48px;
                    border-radius: 16px;
                    background: linear-gradient(135deg, #f59e0b, #d97706);
                    border: 2.5px solid #fef08a;
                    box-shadow: 0 0 28px rgba(245, 158, 11, 1), 0 4px 18px rgba(0, 0, 0, 0.7);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 1.2rem;
                    color: #000;
                    font-weight: 900;
                    cursor: pointer;
                    margin-top: -2px;
                    transition: transform 0.2s ease, box-shadow 0.2s ease;
                }}
                .lamp-rope-container:hover .lamp-handle {{
                    transform: scale(1.15);
                    box-shadow: 0 0 35px rgba(245, 158, 11, 1), 0 0 15px #ffffff;
                }}
                .lamp-rope-tag {{
                    margin-top: 10px;
                    padding: 6px 14px;
                    border-radius: 50px;
                    background: rgba(0, 0, 0, 0.9);
                    border: 2px solid rgba(245, 158, 11, 0.75);
                    color: #fef08a;
                    font-size: 0.80rem;
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

                .preloader-skip-btn {{
                    position: absolute;
                    bottom: 24px;
                    right: 32px;
                    padding: 10px 26px;
                    border-radius: 50px;
                    background: rgba(255, 255, 255, 0.1);
                    border: 1.5px solid rgba(0, 212, 255, 0.5);
                    color: #ffffff;
                    font-size: 0.84rem;
                    font-weight: 700;
                    cursor: pointer;
                    backdrop-filter: blur(12px);
                    transition: all 0.25s ease;
                    display: flex;
                    align-items: center;
                    gap: 8px;
                    z-index: 100;
                    box-shadow: 0 4px 20px rgba(0, 212, 255, 0.25);
                }}
                .preloader-skip-btn:hover {{
                    background: linear-gradient(135deg, rgba(0, 212, 255, 0.35), rgba(168, 85, 247, 0.35));
                    border-color: #00d4ff;
                    transform: translateY(-2px);
                    box-shadow: 0 6px 25px rgba(0, 212, 255, 0.5);
                }}

                @media (max-width: 768px) {{
                    .lamp-rope-container {{ right: 15px; }}
                    .lamp-cord {{ height: 85px; }}
                    .preloader-skip-btn {{ bottom: 12px; right: 16px; padding: 6px 16px; font-size: 0.75rem; }}
                }}
                </style>

                <div class="preloader-ambient-bg"></div>

                <!-- Hanging Lamp Pull Rope -->
                <div class="lamp-rope-container" id="lamp-rope-trigger" title="Pull rope to enter!">
                    <div class="lamp-cord"></div>
                    <div class="lamp-handle">&#128161;</div>
                    <div class="lamp-rope-tag">&#10024; Pull Rope to Enter</div>
                </div>

                <!-- Central Photo Container (No HTML overlay in front of laptop) -->
                <div class="preloader-frame-wrap" id="preloader-photo-frame" title="Click anywhere to enter portfolio">
                    <img src="data:image/jpeg;base64,{img_b64}" alt="Kartikey Gupta Portfolio" class="preloader-main-img" />
                </div>

                <!-- Bottom Enter Button -->
                <button class="preloader-skip-btn" id="preloader-skip-trigger">
                    <span>Enter Portfolio</span> &rarr;
                </button>
            `;

            pDoc.body.appendChild(overlay);

            var ropeTrigger = pDoc.getElementById('lamp-rope-trigger');
            var skipTrigger = pDoc.getElementById('preloader-skip-trigger');
            var photoFrame = pDoc.getElementById('preloader-photo-frame');

            var isDismissed = false;

            function pullAndDismiss() {{
                if (isDismissed) return;
                isDismissed = true;

                // Animate pull stretch
                if (ropeTrigger) {{
                    ropeTrigger.classList.add('pulled');
                }}

                // Slide curtain upwards smoothly
                setTimeout(function() {{
                    if (overlay) {{
                        overlay.classList.add('intro-dismissed');
                        setTimeout(function() {{
                            if (overlay.parentNode) {{
                                overlay.parentNode.removeChild(overlay);
                            }}
                        }}, 1200);
                    }}
                }}, 220);
            }}

            if (ropeTrigger) {{
                ropeTrigger.addEventListener('click', function(e) {{
                    e.preventDefault();
                    pullAndDismiss();
                }});
            }}
            if (skipTrigger) {{
                skipTrigger.addEventListener('click', function(e) {{
                    e.preventDefault();
                    pullAndDismiss();
                }});
            }}
            if (photoFrame) {{
                photoFrame.addEventListener('click', function(e) {{
                    e.preventDefault();
                    pullAndDismiss();
                }});
            }}

        }} catch(err) {{
            console.error(err);
        }}
    }})();
    </script>
    """, height=0, width=0)
