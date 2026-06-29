import streamlit as st
import random

# --- 1. SETTING UP THE GAME INTERFACE ---
st.set_page_config(page_title="VELO-DASH 3D Racing", layout="wide", page_icon="🚴")

st.markdown("""
    <style>
    .stApp {
        background-color: #0f172a;
        color: #ffffff;
    }
    h1 {
        font-family: 'Impact', sans-serif;
        color: #00f0ff !important; /* Cyberpunk Cyan */
        text-shadow: 2px 2px 0px #3b82f6;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    .screen-3d {
        font-family: 'Courier New', monospace;
        font-size: 14px;
        line-height: 10px;
        letter-spacing: 4px;
        background-color: #000000;
        color: #00f0ff;
        padding: 20px;
        border: 4px solid #3b82f6;
        border-radius: 10px;
        text-align: center;
        white-space: pre;
    }
    .racer-card {
        background: rgba(30, 41, 59, 0.9);
        border: 3px solid #3b4cca;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
    }
    .track-info {
        background-color: #1e293b;
        border-left: 5px solid #facc15;
        padding: 12px;
        border-radius: 6px;
        font-family: 'Arial', sans-serif;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🚴 VELO-DASH 3D: THE TRACK DUEL")

# --- 2. INITIALIZE GAME STATE ---
if 'race_initialized' not in st.session_state:
    st.session_state.track_length = 500  # Gesamte Distanz in Metern
    st.session_state.p1_dist = 0
    st.session_state.p2_dist = 0
    st.session_state.p1_energy = 100
    st.session_state.p2_energy = 100
    st.session_state.p1_speed = 0
    st.session_state.p2_speed = 0
    st.session_state.aktiver_racer = 1  # Spieler 1 beginnt
    st.session_state.race_log = "Das grüne Licht leuchtet! Klickt in die Pedale!"
    st.session_state.race_over = False
    st.session_state.next_curve = random.randint(80, 150)
    st.session_state.race_initialized = True

# Reset-Button in der Sidebar
if st.sidebar.button("🔄 Rennen neu starten"):
    st.session_state.race_initialized = False
    st.rerun()

# --- 3. 3D ROAD RAYCASTING RENDERER (DIE BIKE ENGINE) ---
def render_race_3d(p1_d, p2_d, next_c, aktiver):
    # Berechnung, wie weit die nächste Kurve entfernt ist
    aktuelle_dist = p1_d if aktiver == 1 else p2_d
    dist_to_curve = next_c - aktuelle_dist
    
    # Wer führt gerade?
    if p1_d > p2_d:
        lead_text = "P1 LEADS"
    elif p2_d > p1_d:
        lead_text = "P2 LEADS"
    else:
        lead_text = "NECK-NECK"

    # Generiere 3D-Straßenperspektive je nach Kurven-Entfernung
    if dist_to_curve < 15:
        # Scharfe Kurve voraus!
        view = (
            f"=== {lead_text} === DIST: {int(aktuelle_dist)}m ===\n"
            "         / / / /                   \n"
            "        / / / /                    \n"
            "       / / / /                     \n"
            "      / / / /                      \n"
            "     / / / /  <<<< SHARP CURVE!    \n"
            "    / / / /                        \n"
            "   / / / /                         \n"
            "===================================\n"
        )
    elif dist_to_curve < 50:
        # Leichte Kurve am Horizont
        view = (
            f"=== {lead_text} === DIST: {int(aktuelle_dist)}m ===\n"
            "             /   /                 \n"
            "            /   /                  \n"
            "           /   /                   \n"
            "          /   /                    \n"
            "         /   /                     \n"
            "        /   /                      \n"
            "       /   /                       \n"
            "===================================\n"
        )
    else:
        # Lange, gerade Aero-Gerade
        view = (
            f"=== {lead_text} === DIST: {int(aktuelle_dist)}m ===\n"
            "             |   |                 \n"
            "             |   |                 \n"
            "            /     \\                \n"
            "           /       \\               \n"
            "          /   AERO  \\              \n"
            "         /  STRAIGHT \\             \n"
            "        /             \\            \n"
            "===================================\n"
        )
    return view

# --- 4. RENN-LOGIK FÜR EINEN ZUG ---
def execute_race_turn(action):
    # Variablen holen
    if st.session_state.aktiver_racer == 1:
        current_dist = st.session_state.p1_dist
        current_energy = st.session_state.p1_energy
        other_dist = st.session_state.p2_dist
        racer_name = "Spieler 1 (Rot)"
    else:
        current_dist = st.session_state.p2_dist
        current_energy = st.session_state.p2_energy
        other_dist = st.session_state.p1_dist
        racer_name = "Spieler 2 (Blau)"

    # Windschatten-Bonus berechnen (Wenn man dicht dahinter fährt)
    in_draft = False
    if 0 < (other_dist - current_dist) <= 15:
        in_draft = True

    # Checken, ob eine Kurve da ist
    dist_to_curve = st.session_state.next_curve - current_dist
    is_curving = dist_to_curve < 15

    # Aktionen auswerten
    speed = 0
    energy_cost = 0
    log_msg = ""

    if action == "AERO":
        # Energiesparend auf der Geraden, katastrophal in der Kurve
        if is_curving:
            speed = random.randint(5, 12)
            energy_cost = 5
            log_msg = f"⚠️ {racer_name} geht in Aero-Haltung, rutscht aber fast aus der Kurve!"
        else:
            speed = random.randint(22, 30)
            energy_cost = 8 if not in_draft else 3  # Windschatten spart Energie!
            log_msg = f"💨 {racer_name} macht sich flach! Perfekte Aerodynamik."

    elif action == "SPRINT":
        # Extrem schnell, verbraucht massig Energie
        if current_energy >= 20:
            speed = random.randint(35, 48)
            energy_cost = 22
            log_msg = f"🔥 {racer_name} geht in den Wiegetritt und sprintet brachial!"
        else:
            speed = random.randint(10, 15)
            energy_cost = 5
            log_msg = f"🥵 {racer_name} wollte sprinten, hat aber keine Körner mehr!"

    elif action == "ROLLEN":
        # Regeneriert Ausdauer, wenig Speed
        speed = random.randint(12, 18)
        energy_cost = -15  # Lädt Energie auf
        log_msg = f"🔋 {racer_name} nimmt die Beine hoch und regeneriert im Windschatten/Rollen."

    # Werte anwenden & begrenzen
    neue_energy = max(0, min(100, current_energy - energy_cost))
    neue_dist = current_dist + speed

    if in_draft and action != "ROLLEN":
        log_msg += " (inkl. Windschatten-Bonus! 🚴💨)"

    # Zurückschreiben in den State
    if st.session_state.aktiver_racer == 1:
        st.session_state.p1_dist = neue_dist
        st.session_state.p1_energy = neue_energy
        st.session_state.p1_speed = speed
    else:
        st.session_state.p2_dist = neue_dist
        st.session_state.p2_energy = neue_energy
        st.session_state.p2_speed = speed

    st.session_state.race_log = log_msg

    # Neue Kurve generieren, wenn die alte passiert wurde
    if neue_dist >= st.session_state.next_curve:
        st.session_state.next_curve += random.randint(100, 180)

    # Check Ziellinie
    if st.session_state.p1_dist >= st.session_state.track_length or st.session_state.p2_dist >= st.session_state.track_length:
        st.session_state.race_over = True
        return

    # Spieler wechseln
    st.session_state.aktiver_racer = 2 if st.session_state.aktiver_racer == 1 else 1

# --- 5. INTERFACE RENDERING ---
col_view, col_stats = st.columns([2, 1.2])

with col_view:
    st.subheader("📺 Live-Sicht (3D-Strecken-Engine):")
    view_data = render_race_3d(st.session_state.p1_dist, st.session_state.p2_dist, st.session_state.next_curve, st.session_state.aktiver_racer)
    st.markdown(f"<div class='screen-3d'>{view_data}</div>", unsafe_allow_html=True)
    
    # Aktueller Ticker
    st.markdown(f"<div class='track-info'>🎙️ **Rennleitung:** {st.session_state.race_log}</div>", unsafe_allow_html=True)

with col_stats:
    st.subheader("🏁 Renn-Statistiken")
    
    # Fortschrittsbalken bis zum Ziel (500m)
    p1_progress = min(1.0, st.session_state.p1_dist / st.session_state.track_length)
    p2_progress = min(1.0, st.session_state.p2_dist / st.session_state.track_length)
    
    st.write(f"🔴 **Spieler 1:** {int(st.session_state.p1_dist)}m / {st.session_state.track_length}m (Speed: {st.session_state.p1_speed} km/h)")
    st.progress(p1_progress)
    st.caption(f"🔋 Ausdauer (Energie): {st.session_state.p1_energy}%")
    
    st.write("")
    st.write(f"🔵 **Spieler 2:** {int(st.session_state.p2_dist)}m / {st.session_state.track_length}m (Speed: {st.session_state.p2_speed} km/h)")
    st.progress(p2_progress)
    st.caption(f"🔋 Ausdauer (Energie): {st.session_state.p2_energy}%")

st.write("---")

# --- 6. GAME CONTROLS (WER IST DRAN?) ---
if not st.session_state.race_over:
    aktueller_spieler_name = "🔴 SPIELER 1 (Rot)" if st.session_state.aktiver_racer == 1 else "🔵 SPIELER 2 (Blau)"
    border_clr = "#ef4444" if st.session_state.aktiver_racer == 1 else "#3b82f6"
    
    st.markdown(f"""
        <div class='racer-card' style='border-color: {border_clr};'>
            <h2>DU BIST DRAN: {aktueller_spieler_name}</h2>
            <p>Wähle deine Taktik für das nächste Streckenstück!</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    col_act1, col_act2, col_act3 = st.columns(3)
    
    with col_act1:
        if st.button("💨 Aero-Haltung (Guter Speed, anfällig in Kurven)", use_container_width=True):
            execute_race_turn("Aero")
            st.rerun()
            
    with col_act2:
        if st.button("🔥 Sprint / Wiegetritt (Maximaler Speed, kostet viel Ausdauer)", use_container_width=True):
            execute_race_turn("Sprint")
            st.rerun()
            
    with col_act3:
        if st.button("🔋 Beine hoch / Rollen (Regeneriert +15 Ausdauer, weniger Speed)", use_container_width=True):
            execute_race_turn("Rollen")
            st.rerun()

# --- 7. WINNER CELEBRATION ---
else:
    st.balloons()
    if st.session_state.p1_dist >= st.session_state.track_length and st.session_state.p1_dist >= st.session_state.p2_dist:
        st.success("🏆 SPIELER 1 GEWINNT DAS 3D-RENNEN! Absoluter Sprint-König! 🥇🔴")
    else:
        st.success("🏆 SPIELER 2 GEWINNT DAS 3D-RENNEN! Überragende Taktik auf dem Rad! 🥇🔵")
        
    if st.button("🔄 Sofort Revanche fordern! Neues Rennen starten", use_container_width=True):
        st.session_state.race_initialized = False
        st.rerun()
