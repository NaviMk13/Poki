import streamlit as st
import random
import numpy as np

# --- 1. SETTING UP THE GAME INTERFACE ---
st.set_page_config(page_title="PokeStream 3D Open World", layout="wide", page_icon="🌐")

st.markdown("""
    <style>
    .stApp {
        background-color: #0f172a;
        color: #ffffff;
    }
    h1 {
        font-family: 'Impact', sans-serif;
        color: #ffcb05 !important;
        text-shadow: 2px 2px 0px #3b4cca;
        text-align: center;
    }
    .screen-3d {
        font-family: 'Courier New', monospace;
        font-size: 14px;
        line-height: 10px;
        letter-spacing: 4px;
        background-color: #000000;
        color: #00ff00;
        padding: 20px;
        border: 4px solid #3b4cca;
        border-radius: 10px;
        text-align: center;
        white-space: pre;
    }
    .battle-box {
        background: rgba(30, 41, 59, 0.9);
        border: 3px solid #ef4444;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🌐 POKESTREAM 3D: OPEN WORLD")

# --- 2. THE 3D ENGINE & MAP CONFIGURATION ---
# 1 = Wand, 0 = Offener Weg, P = Möglicher Pokémon-Spawn
WORLD_MAP = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,1,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,0,1,0,1,1,1,1,1,0,1,0,1],
    [1,0,1,0,0,0,1,0,0,0,1,0,1,0,1],
    [1,0,1,1,1,0,1,0,0,0,1,0,1,0,1],
    [1,0,0,0,1,0,0,0,1,0,0,0,1,0,1],
    [1,1,1,0,1,1,1,1,1,1,1,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

POKEMON_POOL = ["Pikachu", "Glurak", "Turtok", "Gengar", "Mewtu"]

# --- 3. INITIALIZE GAME STATE ---
if 'player_x' not in st.session_state:
    st.session_state.player_x = 1
    st.session_state.player_y = 1
    st.session_state.player_dir = 0 # 0: Norden, 1: Osten, 2: Süden, 3: Westen
    st.session_state.game_state = "EXPLORE" # EXPLORE oder BATTLE
    st.session_state.current_enemy = ""
    st.session_state.enemy_hp = 100
    st.session_state.player_hp = 100
    st.session_state.log = "Du bist in der 3D-Welt erwacht! Erkunde das Labyrinth."

# --- 4. 3D RAYCASTING RENDERER (DIE ENGINE) ---
def render_3d_view(map_data, px, py, p_dir):
    # Wir simulieren ein einfaches Sichtfeld vor dem Spieler
    # Richtungsvektoren für die Kamerasicht
    dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)] # N, O, S, W
    dx, dy = dirs[p_dir]
    
    # Checken, wie weit die Wand in Blickrichtung entfernt ist
    distance = 0
    for i in range(1, 6):
        check_x = px + dx * i
        check_y = py + dy * i
        if map_data[check_x][check_y] == 1:
            distance = i
            break
            
    # Generiere eine krasse Retro-3D-Ansicht als Text-Art basierend auf der Entfernung
    if distance == 1:
        view = "###########################\n" * 8
    elif distance == 2:
        view = (
            "###########################\n"
            "##                       ##\n"
            "##  ###################  ##\n"
            "##  ###################  ##\n"
            "##  ###################  ##\n"
            "##  ###################  ##\n"
            "##                       ##\n"
            "###########################\n"
        )
    elif distance == 3:
        view = (
            "###########################\n"
            "##                       ##\n"
            "##   ||#############||   ##\n"
            "##   ||             ||   ##\n"
            "##   ||   #######   ||   ##\n"
            "##   ||             ||   ##\n"
            "##   ||#############||   ##\n"
            "###########################\n"
        )
    else:
        view = (
            "##:::::::::::::::::::::::##\n"
            "##   ||:::::::::::::::||   ##\n"
            "##   ||   |       |   ||   ##\n"
            "##   ||   |   .   |   ||   ##\n"
            "##   ||   |       |   ||   ##\n"
            "##   ||:::::::::::::::||   ##\n"
            "##:::::::::::::::::::::::##\n"
        )
    return view

# --- 5. STEUERUNG LOGIK ---
def move_player(action):
    # Richtungs-Arrays
    dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)] # N, O, S, W
    
    if action == "LINKS":
        st.session_state.player_dir = (st.session_state.player_dir - 1) % 4
        st.session_state.log = "Du drehst dich nach links."
    elif action == "RECHTS":
        st.session_state.player_dir = (st.session_state.player_dir + 1) % 4
        st.session_state.log = "Du drehst dich nach rechts."
    elif action == "VORWÄRTS":
        dx, dy = dirs[st.session_state.player_dir]
        new_x = st.session_state.player_x + dx
        new_y = st.session_state.player_y + dy
        
        # Kollisionsabfrage
        if WORLD_MAP[new_x][new_y] == 0:
            st.session_state.player_x = new_x
            st.session_state.player_y = new_y
            st.session_state.log = "Du gehst einen Schritt vorwärts."
            
            # Zufälliger Kampf-Trigger (25% Chance bei jedem Schritt!)
            if random.random() < 0.25:
                st.session_state.game_state = "BATTLE"
                st.session_state.current_enemy = random.choice(POKEMON_POOL)
                st.session_state.enemy_hp = random.randint(60, 100)
                st.session_state.log = f"⚠️ WILDES POKÉMON ENTTARNT! Ein wildes {st.session_state.current_enemy} greift an!"
        else:
            st.session_state.log = "💥 Autsch! Du bist gegen eine Wand gelaufen!"

# --- 6. GAME INTERFACE RENDERING ---
if st.session_state.game_state == "EXPLORE":
    col_view, col_controls = st.columns([2, 1])
    
    with col_view:
        st.subheader("📺 Deine 3D-Sicht auf die Welt:")
        view_3d = render_3d_view(WORLD_MAP, st.session_state.player_x, st.session_state.player_y, st.session_state.player_dir)
        st.markdown(f"<div class='screen-3d'>{view_3d}</div>", unsafe_allow_html=True)
        
        # Info-Anzeige
        st.info(f"📝 **Log:** {st.session_state.log}")
        
    with col_controls:
        st.subheader("🕹️ Steuerung")
        
        # Richtung anzeigen
        dir_names = ["NORDEN ⬆️", "OSTEN ➡️", "SÜDEN ⬇️", "WESTEN ⬅️"]
        st.metric(label="Blickrichtung", value=dir_names[st.session_state.player_dir])
        st.write(f"Position: X={st.session_state.player_x} | Y={st.session_state.player_y}")
        
        # Das Steuerkreuz
        st.write("")
        col_up = st.columns([1,1,1])
        with col_up[1]:
            if st.button("⬆️ VOR", use_container_width=True):
                move_player("VORWÄRTS")
                st.rerun()
                
        col_lr = st.columns([1,1,1])
        with col_lr[0]:
            if st.button("⬅️ LINKS", use_container_width=True):
                move_player("LINKS")
                st.rerun()
        with col_lr[2]:
            if st.button("➡️ RECHTS", use_container_width=True):
                move_player("RECHTS")
                st.rerun()
                
        st.write("---")
        if st.button("🎲 Cheat: Pokémon rufen", use_container_width=True):
            st.session_state.game_state = "BATTLE"
            st.session_state.current_enemy = random.choice(POKEMON_POOL)
            st.session_state.enemy_hp = 80
            st.rerun()

# --- 7. KAMPF MODUS INTERFACE ---
elif st.session_state.game_state == "BATTLE":
    st.markdown(f"<div class='battle-box'><h2>⚔️ 1VS1 INSTANT POKÉ-BATTLE </h2><h3>Du kämpfst gegen ein wildes {st.session_state.current_enemy}!</h3></div>", unsafe_allow_html=True)
    st.write("")
    
    col_p, col_e = st.columns(2)
    with col_p:
        st.subheader("🔴 Dein Team")
        st.metric(label="Deine KP", value=f"{st.session_state.player_hp} / 100")
        
        # Angriffs-Buttons
        if st.button("💥 Donnerblitz einsetzen (Schaden: 25)", use_container_width=True):
            damage = random.randint(20, 30)
            st.session_state.enemy_hp -= damage
            st.session_state.log = f"Du triffst das wilde {st.session_state.current_enemy} für {damage} Schaden!"
            
            # Gegenschlag, wenn der Feind noch lebt
            if st.session_state.enemy_hp > 0:
                enemy_dmg = random.randint(10, 25)
                st.session_state.player_hp -= enemy_dmg
                st.session_state.log += f" Das wilde Pokémon schlägt zurück und macht {enemy_dmg} Schaden!"
            st.rerun()
            
        if st.button("🩹 Trank nehmen (+30 KP)", use_container_width=True):
            st.session_state.player_hp = min(100, st.session_state.player_hp + 30)
            st.session_state.log = "Du hast dich geheilt! Das wilde Pokémon nutzt die Chance zum Angriff!"
            st.session_state.player_hp -= random.randint(10, 20)
            st.rerun()
            
    with col_e:
        st.subheader(f"🔵 Wildes {st.session_state.current_enemy}")
        st.metric(label="Gegner KP", value=f"{max(0, st.session_state.enemy_hp)}")
        st.progress(max(0, min(100, st.session_state.enemy_hp)) / 100)

    st.write("---")
    st.info(f"💬 **Kampfbericht:** {st.session_state.log}")

    # Kampf-Auswertung
    if st.session_state.enemy_hp <= 0
