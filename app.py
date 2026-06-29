import streamlit as st
from assets import get_asset_pipeline

st.set_page_config(page_title="Tour de Stream 3D: GRAND EDITION", layout="wide", page_icon="💛")

# Session State Initialisierung für Highscores und globale Rennstatistiken
if 'p1_wins' not in st.session_state: st.session_state.p1_wins = 0
if 'p2_wins' not in st.session_state: st.session_state.p2_wins = 0

# Custom CSS Injektion für echtes Gaming-UI
st.markdown("""
    <style>
    .stApp { background-color: #05070f; color: #ffffff; font-family: 'Helvetica', Arial, sans-serif; }
    .header-box { text-align: center; padding: 20px; background: linear-gradient(135deg, #111827, #070a13); border-bottom: 4px solid #facc15; border-radius: 12px; margin-bottom: 20px; }
    .score-banner { font-size: 24px; font-weight: bold; color: #facc15; text-shadow: 0 0 10px rgba(250,204,21,0.3); }
    iframe { border: 3px solid #1e293b !important; border-radius: 16px; box-shadow: 0 20px 40px rgba(0,0,0,0.6); }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class='header-box'>
        <h1 style='color: #facc15; margin:0; font-size:38px; letter-spacing:2px;'>🚴‍♂️ TOUR DE STREAM 3D: GRAND EDITION 🚴‍♂️</h1>
        <p style='color: #94a3b8; margin:5px 0 0 0;'>Die ultimative, prozedurale 3D-Simulation der Alpen-Königsetappe</p>
    </div>
""", unsafe_allow_html=True)

# Dashboard-Statistiken in Streamlit-Columns auslagern
c1, c2, c3 = st.columns(3)
with c1: st.metric("🏆 Siege Spieler 1 (Rot)", st.session_state.p1_wins)
with c2: st.metric("🏆 Siege Spieler 2 (Blau)", st.session_state.p2_wins)
with c3: st.markdown(f"<div style='text-align:center; padding-top:10px;'><span class='score-banner'>GESAMT-DUELL: {st.session_state.p1_wins} : {st.session_state.p2_wins}</span></div>", unsafe_allow_html=True)

# HIER BINDEN WIR DIE EXTREM GROSSE JAVASCRIPT ENGINE EIN (Teil 3)
# Um das Token-Limit zu sprengen, fordern wir die JavaScript-Engine modular an.
def build_mega_engine_string():
    # Lädt das prozedurale Asset-System aus der anderen Python-Datei
    asset_code = get_asset_pipeline()
    
    # Der Grundrahmen des HTML/JS-Dokuments
    html_start = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ margin: 0; overflow: hidden; background-color: #05070f; font-family: monospace; }}
            #canvas-container {{ width: 100vw; height: 75vh; }}
            #ui-layer {{ position: absolute; top: 15px; left: 15px; pointer-events: none; z-index: 10; }}
            .dashboard {{ background: rgba(10, 15, 30, 0.9); border: 2px solid #facc15; padding: 15px; border-radius: 10px; width: 300px; color: white; box-shadow: 0 10px 30px rgba(0,0,0,0.7); }}
            .bar-bg {{ background: #2d3748; height: 8px; border-radius: 4px; margin-top: 5px; overflow: hidden; }}
            .bar-fill {{ height: 100%; width: 100%; transition: width 0.05s linear; }}
            #victory-popup {{ display: none; position: absolute; top: 50%; left: 50%; transform: translate(-50%,-50%); background: #facc15; color: black; padding: 40px; font-size: 36px; font-weight: bold; border-radius: 20px; text-align: center; border: 6px solid white; z-index: 100; box-shadow: 0 0 100px rgba(250,204,21,0.6); }}
            #click-to-focus {{ position: absolute; bottom: 30px; left: 50%; transform: translateX(-50%); background: #facc15; color: black; padding: 12px 30px; font-weight: bold; border-radius: 30px; animation: flash 1.5s infinite; font-size: 16px; z-index: 20; cursor: pointer; }}
            @keyframes flash {{ 0% {{ opacity: 0.4; }} 50% {{ opacity: 1; }} 100% {{ opacity: 0.4; }} }}
        </style>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    </head>
    <body>
        <div id="ui-layer">
            <div class="dashboard">
                <h3 style="margin:0 0 10px 0; color:#facc15; text-align:center;">📊 TELEMETRIE-DATEN</h3>
                <div style="padding: 6px; background:rgba(239,68,68,0.2); border-left:4px solid #ef4444; margin-bottom:8px; border-radius:4px;">
                    <b style="color:#ef4444;">🔴 P1 (WASD):</b> <span id="v1">0 km/h</span> | <span id="surf1">Asphalt</span>
                    <div class="bar-bg"><div id="st1" class="bar-fill" style="background:#ef4444;"></div></div>
                </div>
                <div style="padding: 6px; background:rgba(59,130,246,0.2); border-left:4px solid #3b82f6; border-radius:4px;">
                    <b style="color:#3b82f6;">🔵 P2 (Pfeile):</b> <span id="v2">0 km/h</span> | <span id="surf2">Asphalt</span>
                    <div class="bar-bg"><div id="st2" class="bar-fill" style="background:#3b82f6;"></div></div>
                </div>
                <hr style="border-color:#2d3748; margin:10px 0;">
                <div id="live-ticker" style="color:#22c55e; font-weight:bold; text-align:center; font-size:12px;">Rennen läuft...</div>
            </div>
        </div>

        <div id="click-to-focus">🎮 KLICKE HIER REIN ZUM STEUERN</div>
        <div id="victory-popup">🏆 <span id="winner-name">SPIELER</span> GEWINNT! 💛</div>
        <div id="canvas-container"></div>

        <script>
            // --- INJEKTION DER ASSETS ---
            {asset_code}
            
            // AB HIER FOLGT DIE MASSIVE RECHNERISCHE GRAFIK-ENGINE
    """
    return html_start

# Das wird im nächsten Schritt mit der kompletten JavaScript-Engine verknüpft!
