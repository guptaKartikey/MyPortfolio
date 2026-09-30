"""
components/music_player.py
==========================
Soft ambient background music player for the portfolio.
Supports local assets/music.mp3 (preferred, 100% offline & reliable)
or high-quality royalty-free CDN audio.
"""

import os
import base64
import streamlit.components.v1 as components


def _get_audio_source(asset_dir: str = "assets") -> str:
    """Return base64 data URI if custom uploaded song or assets/music.mp3 exists, else fallback CDN link."""
    candidates = [
        os.path.join(asset_dir, "music.mp3"),
        os.path.join(asset_dir, "SONG.mpeg"),
        os.path.join(asset_dir, "song.mpeg"),
        "SONG.mpeg",
        "song.mpeg",
        os.path.join(asset_dir, "music.mpeg"),
        os.path.join(asset_dir, "music.wav"),
        os.path.join(asset_dir, "music.ogg"),
    ]
    for local in candidates:
        if os.path.exists(local) and os.path.getsize(local) > 0:
            try:
                ext = os.path.splitext(local)[1].lower().lstrip(".")
                mime = "audio/mpeg" if ext in ["mp3", "mpeg", "mpga"] else f"audio/{ext}"
                with open(local, "rb") as f:
                    b64 = base64.b64encode(f.read()).decode()
                return f"data:{mime};base64,{b64}"
            except Exception:
                pass
    # High-reliability fallback royalty-free lofi stream
    return "https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3?filename=lofi-study-112191.mp3"


def render_music_player(asset_dir: str = "assets") -> None:
    """Inject floating music player into parent document."""
    audio_src = _get_audio_source(asset_dir)

    components.html(f"""
    <script>
    (function() {{
        var AUDIO_SRC = {repr(audio_src)};

        function getParentDoc() {{
            try {{ return window.parent ? window.parent.document : document; }}
            catch(e) {{ return document; }}
        }}

        function setupPlayer() {{
            var doc = getParentDoc();
            if (!doc || !doc.body) return;
            if (doc.getElementById('portfolio-music-btn')) return;

            /* ── Global Audio Element ── */
            var audio = doc.getElementById('portfolio-audio-elem');
            if (!audio) {{
                audio = doc.createElement('audio');
                audio.id = 'portfolio-audio-elem';
                audio.loop = true;
                audio.preload = 'auto';
                audio.src = AUDIO_SRC;
                audio.volume = 0.25; // 25% comfortable soft volume
                audio.style.display = 'none';
                doc.body.appendChild(audio);
            }}

            /* ── Floating Pill Button ── */
            var btn = doc.createElement('button');
            btn.id = 'portfolio-music-btn';
            btn.type = 'button';
            btn.setAttribute('aria-label', 'Toggle Background Music');
            btn.innerHTML = `
                <style>
                    #portfolio-music-btn {{
                        position: fixed !important;
                        bottom: 24px !important;
                        right: 24px !important;
                        z-index: 999999 !important;
                        display: flex !important;
                        align-items: center !important;
                        gap: 8px !important;
                        padding: 9px 18px 9px 14px !important;
                        border-radius: 50px !important;
                        background: rgba(10, 12, 28, 0.90) !important;
                        border: 1.5px solid rgba(0, 212, 255, 0.35) !important;
                        color: #cbd5e1 !important;
                        font-family: 'Segoe UI', system-ui, -apple-system, sans-serif !important;
                        font-size: 0.80rem !important;
                        font-weight: 700 !important;
                        letter-spacing: 0.5px !important;
                        cursor: pointer !important;
                        backdrop-filter: blur(16px) !important;
                        -webkit-backdrop-filter: blur(16px) !important;
                        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.45), 0 0 15px rgba(0, 212, 255, 0.15) !important;
                        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
                        outline: none !important;
                        user-select: none !important;
                    }}
                    #portfolio-music-btn:hover {{
                        transform: translateY(-2px) scale(1.03) !important;
                        border-color: rgba(0, 212, 255, 0.7) !important;
                        box-shadow: 0 6px 25px rgba(0, 212, 255, 0.3) !important;
                        color: #ffffff !important;
                    }}
                    #portfolio-music-btn.playing {{
                        background: rgba(12, 18, 38, 0.95) !important;
                        border-color: #00d4ff !important;
                        color: #00d4ff !important;
                        box-shadow: 0 0 25px rgba(0, 212, 255, 0.4) !important;
                    }}
                    .eq-bars {{
                        display: flex;
                        align-items: flex-end;
                        gap: 2px;
                        height: 14px;
                    }}
                    .eq-bar {{
                        width: 3px;
                        background: #94a3b8;
                        border-radius: 2px;
                        height: 4px;
                        transition: height 0.2s ease, background 0.2s ease;
                    }}
                    #portfolio-music-btn.playing .eq-bar {{
                        background: #00d4ff;
                        animation: eqWave 1.2s infinite ease-in-out alternate;
                    }}
                    #portfolio-music-btn.playing .eq-bar:nth-child(1) {{ animation-delay: 0.0s; }}
                    #portfolio-music-btn.playing .eq-bar:nth-child(2) {{ animation-delay: 0.3s; }}
                    #portfolio-music-btn.playing .eq-bar:nth-child(3) {{ animation-delay: 0.15s; }}
                    #portfolio-music-btn.playing .eq-bar:nth-child(4) {{ animation-delay: 0.45s; }}
                    @keyframes eqWave {{
                        0% {{ height: 3px; }}
                        100% {{ height: 14px; }}
                    }}
                </style>
                <div class="eq-bars">
                    <span class="eq-bar"></span>
                    <span class="eq-bar"></span>
                    <span class="eq-bar"></span>
                    <span class="eq-bar"></span>
                </div>
                <span id="pmusic-label">Play Music</span>
            `;
            doc.body.appendChild(btn);

            var label = doc.getElementById('pmusic-label');

            function updateUI(isPlaying) {{
                if (isPlaying) {{
                    btn.classList.add('playing');
                    if (label) label.textContent = 'Pause Music';
                }} else {{
                    btn.classList.remove('playing');
                    if (label) label.textContent = 'Play Music';
                }}
            }}

            // Sync state if audio ends or pauses
            audio.addEventListener('play', function() {{ updateUI(true); }});
            audio.addEventListener('pause', function() {{ updateUI(false); }});
            audio.addEventListener('ended', function() {{ updateUI(false); }});

            // Synchronous direct click handler for maximum browser compatibility
            btn.addEventListener('click', function(e) {{
                e.preventDefault();
                e.stopPropagation();

                if (audio.paused) {{
                    var playPromise = audio.play();
                    if (playPromise !== undefined) {{
                        playPromise.then(function() {{
                            updateUI(true);
                        }}).catch(function(err) {{
                            console.error("Audio playback error:", err);
                        }});
                    }}
                }} else {{
                    audio.pause();
                    updateUI(false);
                }}
            }});
        }}

        // Initialize immediately and after DOM content loaded
        if (document.readyState === 'loading') {{
            document.addEventListener('DOMContentLoaded', setupPlayer);
        }} else {{
            setupPlayer();
        }}
        setTimeout(setupPlayer, 300);
        setTimeout(setupPlayer, 1000);
    }})();
    </script>
    """, height=0, width=0)
