import streamlit as st
import random

# --- 1. GAME DESIGNS & STYLING ---
st.set_page_config(page_title="PokeStream Arena", layout="wide", page_icon="🎮")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(15, 23, 42, 0.95), rgba(15, 23, 42, 0.98)), 
                    url('https://images.unsplash.com/photo-1613771404724-17d1e83a227c?q=80&w=1920') no-repeat center center fixed;
        background-size: cover;
        color: #ffffff !important;
    }
    h1 {
        font-family: 'Impact', 'Arial Black', sans-serif;
        text-transform: uppercase;
        color: #ffcb05 !important; /* Pokémon Gelb */
        text-shadow: 3px 3px 0px #3b4cca; /* Pokémon Blau Umrandung */
        text-align: center;
        letter-spacing: 2px;
    }
    .poke-card {
        background: rgba(30, 41, 59, 0.85);
        border: 3px solid #3b4cca;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 10px 20px rgba(0,0,0,0.5);
    }
    .hp-bar {
        background-color: #475569;
        border-radius: 10px;
        padding: 3px;
        margin-top: 10px;
    }
    .hp-fill {
        height: 15px;
        border-radius: 8px;
        transition: width 0.5s ease-in-out;
    }
    .battle-log {
        background-color: #0f172a;
        border-left: 5px solid #ffcb05;
        padding: 12px;
        border-radius: 6px;
        font-family: 'Courier New', monospace;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🎮 POKESTREAM ARENA 1VS1")

# --- 2. DATA POOL (DIE POKÉMON & ATTACKEN) ---
POKEMON_POOL = [
    {"name": "Glurak", "type": "Feuer"},
    {"name": "Turtok", "type": "Wasser"},
    {"name": "Bisaflor", "type": "Pflanze"},
    {"name": "Pikachu", "type": "Elektro"},
    {"name": "Gengar", "type": "Geist"},
    {"name": "Mewtu", "type": "Psycho"},
    {"name": "Lucario", "type": "Kampf"},
    {"name": "Nachtara", "type": "Unlicht"}
]

ATTACKEN_POOL = [
    {"name": "Donnerblitz", "min": 15, "max": 25, "chance": 95, "type": "Normal"},
    {"name": "Flammenwurf", "min": 18, "max": 22, "chance": 90, "type": "Normal"},
    {"name": "Hyperstrahl", "min": 30, "max": 50, "chance": 55, "type": "Risiko"},
    {"name": "Erdbeben", "min": 20, "max": 28, "chance": 85, "type": "Normal"},
    {"name": "Kreuzhieb", "min": 25, "max": 35, "chance": 70, "type": "Risiko"},
    {"name": "Genesung", "min": 15, "max": 25, "chance": 100, "type": "Heilung"},
    {"name": "Trank werfen", "min": 12, "max": 20, "chance": 100, "type": "Heilung"}
]

# --- 3. GAME STATE MANAGEMENT ---
if 'initialized' not in st.session_state:
    st.session_state.initialized = False

def start_neues_spiel():
    p1 = random.choice(POKEMON_POOL)
    p2 = random.choice(POKEMON_POOL)
    while p2["name"] == p1["name"]: # Verhindern, dass es zweimal exakt dasselbe ist
        p2 = random.choice(POKEMON_POOL)
        
    st.session_state.p1_name = p1["name"]
    st.session_state.p1_max_hp = random.randint(90, 120)
    st.session_state.p1_hp = st.session_state.p1_max_hp
    st.session_state.p1_attacks = random.sample(ATTACKEN_POOL, 3)
    
    st.session_state.p2_name = p2["name"]
    st.session_state.p2_max_hp = random.randint(90, 120)
    st.session_state.p2_hp = st.session_state.p2_max_hp
    st.session_state.p2_attacks = random.sample(ATTACKEN_POOL, 3)
    
    st.session_state.aktiver_spieler = 1
    st.session_state.log = "Das Match hat begonnen! Wer holt sich den Sieg?"
    st.session_state.game_over = False
    st.session_state.initialized = True

# Buttons für Spiel-Modus in der Sidebar
st.sidebar.header("🕹️ Menü")
bot_modus = st.sidebar.checkbox("🤖 Gegen KI spielen (Singleplayer)", value=False)

if st.sidebar.button("🎲 NEUES RANDOM MATCH STARTEN") or not st.session_state.initialized:
    start_neues_spiel()

# --- 4. SPIEL-LOGIK FÜR EINEN ZUG ---
def execute_turn(attack, angreifer, verteidiger_name):
    if random.randint(1, 100) <= attack["chance"]:
        wert = random.randint(attack["min"], attack["max"])
        if attack["type"] == "Heilung":
            if angreifer == 1:
                st.session_state.p1_hp = min(st.session_state.p1_max_hp, st.session_state.p1_hp + wert)
                st.session_state.log = f"🟢 {st.session_state.p1_name} setzt {attack['name']} ein und heilt sich um {wert} KP!"
            else:
                st.session_state.p2_hp = min(st.session_state.p2_max_hp, st.session_state.p2_hp + wert)
                st.session_state.log = f"🟢 {st.session_state.p2_name} setzt {attack['name']} ein und heilt sich um {wert} KP!"
        else:
            if angreifer == 1:
                st.session_state.p2_hp = max(0, st.session_state.p2_hp - wert)
                st.session_state.log = f"💥 {st.session_state.p1_name} setzt {attack['name']} ein und trifft {verteidiger_name} für {wert} Schaden!"
            else:
                st.session_state.p1_hp = max(0, st.session_state.p1_hp - wert)
                st.session_state.log = f"💥 {st.session_state.p2_name} setzt {attack['name']} ein und trifft {verteidiger_name} für {wert} Schaden!"
    else:
        name = st.session_state.p1_name if angreifer == 1 else st.session_state.p2_name
        st.session_state.log = f"💨 Oh nein! Die Attacke {attack['name']} von {name} ging daneben!"

    # Check ob jemand besiegt ist
    if st.session_state.p1_hp <= 0 or st.session_state.p2_hp <= 0:
        st.session_state.game_over = True
        return

    # Spieler wechseln
    if not st.session_state.game_over:
        if bot_modus and angreifer == 1:
            # KI führt direkt ihren Zug aus
            st.session_state.aktiver_spieler = 2
            ki_attack = random.choice(st.session_state.p2_attacks)
            execute_turn(ki_attack, 2, st.session_state.p1_name)
            st.session_state.aktiver_spieler = 1
        else:
            st.session_state.aktiver_spieler = 2 if angreifer == 1 else 1

# --- 5. INTERFACE RENDERING ---
col_p1, col_space, col_p2 = st.columns([2, 0.5, 2])

# SPIELER 1 CARD
with col_p1:
    p1_pct = int((st.session_state.p1_hp / st.session_state.p1_max_hp) * 100)
    p1_color = "#22c55e" if p1_pct > 40 else ("#f59e0b" if p1_pct > 15 else "#ef4444")
    border_color = "#ef4444" if st.session_state.aktiver_spieler == 1 and not st.session_state.game_over else "#3b4cca"
    
    st.markdown(f"""
        <div class='poke-card' style='border-color: {border_color};'>
            <h2 style='margin:0; color:#ffcb05 !important;'>🔴 Spieler 1</h2>
            <h1 style='font-size:32px; margin:5px 0;'>{st.session_state.p1_name}</h1>
            <div style='text-align:right; font-weight:bold;'>KP: {st.session_state.p1_hp} / {st.session_state.p1_max_hp}</div>
            <div class='hp-bar'>
                <div class='hp-fill' style='width: {p1_pct}%; background-color: {p1_color};'></div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    # Angriffs-Buttons für Spieler 1
    if st.session_state.aktiver_spieler == 1 and not st.session_state.game_over:
        st.write("⚔️ WÄHLE DEINE ATTACKE:")
        for atk in st.session_state.p1_attacks:
            btn_label = f"{atk['name']} ({atk['type']} | Treffer: {atk['chance']}%)"
            if st.button(btn_label, key=f"p1_{atk['name']}", use_container_width=True):
                execute_turn(atk, 1, st.session_state.p2_name)
                st.rerun()
    elif not st.session_state.game_over:
        st.info("Warte auf Spieler 2...")

# SPIELER 2 CARD
with col_p2:
    p2_pct = int((st.session_state.p2_hp / st.session_state.p2_max_hp) * 100)
    p2_color = "#22c55e" if p2_pct > 40 else ("#f59e0b" if p2_pct > 15 else "#ef4444")
    border_color = "#3b82f6" if st.session_state.aktiver_spieler == 2 and not st.session_state.game_over else "#3b4cca"
    
    p2_title = "🤖 KI-Gegner" if bot_modus else "🔵 Spieler 2"
    
    st.markdown(f"""
        <div class='poke-card' style='border-color: {border_color};'>
            <h2 style='margin:0; color:#ffcb05 !important;'>{p2_title}</h2>
            <h1 style='font-size:32px; margin:5px 0;'>{st.session_state.p2_name}</h1>
            <div style='text-align:right; font-weight:bold;'>KP: {st.session_state.p2_hp} / {st.session_state.p2_max_hp}</div>
            <div class='hp-bar'>
                <div class='hp-fill' style='width: {p2_pct}%; background-color: {p2_color};'></div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    # Angriffs-Buttons für Spieler 2 (nur sichtbar wenn kein Bot-Modus)
    if st.session_state.aktiver_spieler == 2 and not st.session_state.game_over and not bot_modus:
        st.write("⚔️ WÄHLE DEINE ATTACKE:")
        for atk in st.session_state.p2_attacks:
            btn_label = f"{atk['name']} ({atk['type']} | Treffer: {atk['chance']}%)"
            if st.button(btn_label, key=f"p2_{atk['name']}", use_container_width=True):
                execute_turn(atk, 2, st.session_state.p1_name)
                st.rerun()

# --- 6. KAMPF-LOG UND GEWINNER-ANZEIGE ---
st.write("---")
st.subheader("📝 Kampf-Protokoll:")
st.markdown(f"<div class='battle-log'>{st.session_state.log}</div>", unsafe_allow_html=True)

if st.session_state.game_over:
    st.balloons() # Konfetti-Regen im Browser!
    if st.session_state.p1_hp <= 0:
        winner = st.session_state.p2_name if not bot_modus else f"Die KI ({st.session_state.p2_name})"
        st.success(f"🏆 {winner} hat gewonnen! {st.session_state.p1_name} ist K.O. gegangen!")
    else:
        st.success(f"🏆 Spieler 1 ({st.session_state.p1_name}) hat gewonnen! {st.session_state.p2_name} ist K.O. gegangen!")
        
    if st.button("🔄 Direkt Revanche fordern!", use_container_width=True):
        start_neues_spiel()
        st.rerun()
