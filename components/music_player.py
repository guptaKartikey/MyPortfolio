"""
components/music_player.py
==========================
Soft ambient background music player for the portfolio.
Supports local static audio or high-quality royalty-free CDN audio.
Injected directly into the parent DOM without sandboxed iframes.
"""

import os
from pathlib import Path
import streamlit as st
from utils.helpers import inject_html


def render_music_player(asset_dir: str = "assets") -> None:
    """Inject floating music player into parent document."""
    html = """
    <audio id="portfolio-audio-elem" loop preload="auto" style="display:none;">
        <source src="/app/static/assets/music.mp3" type="audio/mpeg">
        <source src="app/static/assets/music.mp3" type="audio/mpeg">
        <source src="/static/assets/music.mp3" type="audio/mpeg">
        <source src="static/assets/music.mp3" type="audio/mpeg">
        <source src="https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3?filename=lofi-study-112191.mp3" type="audio/mpeg">
    </audio>

    <button id="portfolio-music-btn" type="button" aria-label="Toggle Background Music">
        <style>
            #portfolio-music-btn {
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
            }
            #portfolio-music-btn:hover {
                transform: translateY(-2px) scale(1.03) !important;
                border-color: rgba(0, 212, 255, 0.7) !important;
                box-shadow: 0 6px 25px rgba(0, 212, 255, 0.3) !important;
                color: #ffffff !important;
            }
            #portfolio-music-btn.playing {
                background: rgba(12, 18, 38, 0.95) !important;
                border-color: #00d4ff !important;
                color: #00d4ff !important;
                box-shadow: 0 0 25px rgba(0, 212, 255, 0.4) !important;
            }
            .eq-bars {
                display: flex;
                align-items: flex-end;
                gap: 2px;
                height: 14px;
            }
            .eq-bar {
                width: 3px;
                background: #94a3b8;
                border-radius: 2px;
                height: 4px;
                transition: height 0.2s ease, background 0.2s ease;
            }
            #portfolio-music-btn.playing .eq-bar {
                background: #00d4ff;
                animation: eqWave 1.2s infinite ease-in-out alternate;
            }
            #portfolio-music-btn.playing .eq-bar:nth-child(1) { animation-delay: 0.0s; }
            #portfolio-music-btn.playing .eq-bar:nth-child(2) { animation-delay: 0.3s; }
            #portfolio-music-btn.playing .eq-bar:nth-child(3) { animation-delay: 0.15s; }
            #portfolio-music-btn.playing .eq-bar:nth-child(4) { animation-delay: 0.45s; }
            @keyframes eqWave {
                0% { height: 3px; }
                100% { height: 14px; }
            }
        </style>
        <div class="eq-bars">
            <span class="eq-bar"></span>
            <span class="eq-bar"></span>
            <span class="eq-bar"></span>
            <span class="eq-bar"></span>
        </div>
        <span id="pmusic-label">Play Music</span>
    </button>

    <script>
    (function initMusicPlayer() {
        var audio = document.getElementById('portfolio-audio-elem');
        var btn = document.getElementById('portfolio-music-btn');
        var label = document.getElementById('pmusic-label');
        if (!audio || !btn) return;

        audio.volume = 0.25;

        function updateUI(isPlaying) {
            if (isPlaying) {
                btn.classList.add('playing');
                if (label) label.textContent = 'Pause Music';
            } else {
                btn.classList.remove('playing');
                if (label) label.textContent = 'Play Music';
            }
        }

        audio.addEventListener('play', function() { updateUI(true); });
        audio.addEventListener('pause', function() { updateUI(false); });
        audio.addEventListener('ended', function() { updateUI(false); });

        btn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();

            if (audio.paused) {
                var p = audio.play();
                if (p !== undefined) {
                    p.then(function() {
                        updateUI(true);
                    }).catch(function(err) {
                        console.warn("Audio play prevented:", err);
                    });
                }
            } else {
                audio.pause();
                updateUI(false);
            }
        });
    })();
    </script>
    """
    inject_html(html)
