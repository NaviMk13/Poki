import streamlit as st

# --- 1. STREAMLIT CONFIG & GLOBAL ACCOUNT CORE ---
st.set_page_config(page_title="Alpen GP - Hardcore Simulator", layout="wide", page_icon="🚴‍♂️")

# Permanentes Konto für gesammelte Münzen initialisieren
if "global_coins" not in st.session_state:
    st.session_state.global_coins = 0
if "bike_type" not in st.session_state:
    st.session_state.bike_type = None

# Custom CSS für den Gaming-Look
st.markdown("""
    <style>
    .stApp { background-color: #020617; color: #ffffff; font-family: 'Segoe UI', sans-serif; }
    iframe { border: 4px solid #ef4444 !important; border-radius: 24px; box-shadow: 0 25px 60px rgba(239, 68, 68, 0.25); }
    h1 { font-family: 'Impact', sans-serif; color: #facc15 !important; text-shadow: 4px 4px 0px #000; text-align: center; text-transform: uppercase; margin: 0; letter-spacing: 2px; }
    .wallet-box { background: linear-gradient(135deg, #1e293b, #0f172a); border: 2px solid #eab308; padding: 15px; border-radius: 12px; text-align: center; font-weight: bold; font-size: 18px; color: #facc15; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

st.write("<h1>🚴‍♂️ ALPEN GP: ULTIMATE HARDCORE EDITION 🚴‍♂️</h1>", unsafe_allow_html=True)

# URL Query-Parameter auslesen, um Münzen nach dem Rennen an Streamlit zu übergeben
query_params = st.query_params
if "add_coins" in query_params:
    added = int(query_params["add_coins"])
    st.session_state.global_coins += added
    st.toast(f"🪙 +{added} Münzen auf dein Konto gutgeschrieben!", icon="💰")
    st.query_params.clear() # Parameter löschen, um Doppel-Zählung bei Refresh zu verhindern

# Anzeige des Kontostands in der Sidebar
st.sidebar.markdown(f"<div class='wallet-box'>💰 MEIN KONTO:<br><span style='font-size:26px;'>{st.session_state.global_coins} COINS</span></div>", unsafe_allow_html=True)

# --- HAUPTMENÜ-PHASE ---
if st.session_state.bike_type is None:
    st.write("<p style='text-align:center; color:#94a3b8; font-size:16px; margin-top:10px;'>Wähle dein Renn-Chassis, um die Hardcore-Simulation zu starten:</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div style='background:#1e1b4b; padding:25px; border-radius:16px; border:2px solid #4338ca; text-align:center; min-height:180px;'><h2>🚀 AERO-RENNRAD</h2><p style='color:#cbd5e1;'>König des Asphalts (+25% Top-Speed). Reagiert extrem empfindlich auf Offroad-Gras und rutscht bei Gewitter stark weg!</p></div>", unsafe_allow_html=True)
        if st.button("Aero-Chassis ausrüsten", use_container_width=True):
            st.session_state.bike_type = "AERO"
            st.rerun()
            
    with col2:
        st.markdown("<div style='background:#062f4f; padding:25px; border-radius:16px; border:2px solid #0369a1; text-align:center; min-height:180px;'><h2>🚜 GRAVEL-MONSTER</h2><p style='color:#cbd5e1;'>Fettes Stollenprofil. Auf Asphalt etwas langsamer, pflügt dafür fast ohne Geschwindigkeitsverlust durch Schlamm, Gras und Regen!</p></div>", unsafe_allow_html=True)
        if st.button("Gravel-Chassis ausrüsten", use_container_width=True):
            st.session_state.bike_type = "GRAVEL"
            st.rerun()

# --- RENN-PHASE ---
else:
    st.sidebar.markdown("### 🛠️ Renn-Statistiken")
    st.sidebar.info(f"Ausgewähltes Rad: {st.session_state.bike_type}")
    if st.sidebar.button("↩️ Zurück zum Hauptmenü"):
        st.session_state.bike_type = None
        st.rerun()

    is_aero = "true" if st.session_state.bike_type == "AERO" else "false"

    # --- 3. HARDCORE 3D GAME ENGINE (JAVASCRIPT / THREE.JS) ---
    engine_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ margin: 0; overflow: hidden; background-color: #020617; font-family: sans-serif; }}
            #canvas-container {{ width: 100vw; height: 74vh; }}
            #hud {{
                position: absolute; top: 15px; left: 15px; z-index: 10; pointer-events: none;
                color: white; background: linear-gradient(135deg, rgba(15,23,42,0.95), rgba(30,41,59,0.9));
                padding: 16px; border-radius: 14px; border: 3px solid #ef4444; width: 250px;
                box-shadow: 0 20px 45px rgba(0,0,0,0.6);
            }}
            .stat {{ font-size: 14px; margin: 3px 0; font-weight: bold; font-family: monospace; }}
            #weather-tag {{ font-size: 11px; padding: 2px 6px; border-radius: 4px; font-weight: bold; text-transform: uppercase; }}
            #victory {{ display: none; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); background: #facc15; color: black; padding: 40px 60px; border-radius: 24px; font-size: 35px; font-weight: bold; text-align: center; border: 5px solid white; z-index: 100; font-family: 'Impact'; }}
            #repair-overlay {{ display: none; position: absolute; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(239,68,68,0.4); color: white; font-size: 40px; font-weight: bold; font-family: 'Impact'; align-items: center; justify-content: center; z-index: 50; }}
        </style>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    </head>
    <body>

        <div id="hud">
            <h4 style="margin: 0 0 5px 0; color: #facc15; text-transform:uppercase;">📊 SIMULATION TELEMETRIE</h4>
            <div class="stat">Speed: <span id="speed" style="color:#facc15; font-size:16px;">0</span> km/h</div>
            <div class="stat">Höhe: <span id="altimeter" style="color:#38bdf8;">0m</span></div>
            <div class="stat">Münzen im Rennen: <span id="coins-ui" style="color:#fbbf24;">🪙 0</span></div>
            <div class="stat">Integrität: <span id="health" style="color:#ef4444;">100%</span></div>
            <div class="stat" id="slip-ui" style="color:#a855f7; display:none;">⚠️ WINDSCHATTEN BOOST!</div>
            
            <div style="margin: 6px 0; display:flex; align-items:center; gap:6px;">
                <span style="font-size:12px; color:#9ca3af;">Wetter:</span>
                <span id="weather-tag" style="background:#22c55e; color:white;">Sonne ☀️</span>
            </div>
            
            <div id="item-slot" style="border:2px dashed #facc15; height:32px; display:flex; align-items:center; justify-content:center; font-weight:bold; color:#facc15; font-size:12px; background:rgba(255,255,255,0.05); border-radius:6px; margin-top:8px;">LEER</div>
        </div>

        <div id="repair-overlay">💥 TOTALSCHADEN! REPARATUR...</div>
        <div id="victory">🏆 <span id="winner">DU HAST</span> GEWONNEN!<br><button id="save-btn" style="margin-top:15px; padding:10px 20px; font-weight:bold; background:black; color:white; border:none; border-radius:8px; cursor:pointer;">MÜNZEN SPEICHERN</button></div>
        <div id="canvas-container"></div>

        <script>
            const isAero = {is_aero};

            // --- ENGINE BASIC SETUP ---
            const container = document.getElementById('canvas-container');
            const scene = new THREE.Scene();
            let skyColor = new THREE.Color(0xfba575); // Start bei schönem Sonnenuntergang
            scene.background = skyColor;
            const fog = new THREE.FogExp2(0xfba575, 0.004);
            scene.fog = fog;

            const camera = new THREE.PerspectiveCamera(53, window.innerWidth / window.innerHeight, 0.1, 1100);
            const renderer = new THREE.WebGLRenderer({{ antialias: true }});
            renderer.setSize(window.innerWidth, window.innerHeight * 0.74);
            renderer.shadowMap.enabled = true;
            renderer.shadowMap.type = THREE.PCFSoftShadowMap;
            container.appendChild(renderer.domElement);

            const ambientLight = new THREE.AmbientLight(0xffffff, 0.4);
            scene.add(ambientLight);
            const sun = new THREE.DirectionalLight(0xfffaed, 1.4);
            sun.position.set(100, 150, 50);
            sun.castShadow = true;
            scene.add(sun);

            let gameActive = true;
            let isRepairing = false;
            let weatherCondition = "SUN"; // SUN -> STORM

            // --- PROZEDURALES GEBÄUUDE & FELSEN TERRAIN ---
            const terrainGeo = new THREE.PlaneGeometry(3500, 3500, 25, 25);
            const posAttr = terrainGeo.attributes.position;
            for (let i = 0; i < posAttr.count; i++) {{
                const vx = posAttr.getX(i); const vy = posAttr.getY(i);
                posAttr.setZ(i, Math.sin(vx * 0.007) * Math.cos(vy * 0.007) * 38 + Math.sin(vx * 0.002) * 50);
            }}
            terrainGeo.computeVertexNormals();
            const terrain = new THREE.Mesh(terrainGeo, new THREE.MeshStandardMaterial({{ color: 0x1e3f20, roughness: 0.95, flatShading: true }}));
            terrain.rotation.x = -Math.PI / 2; terrain.receiveShadow = true; scene.add(terrain);

            // Streckenverlauf (3D Höhen-Passstraße)
            const trackPoints = [
                new THREE.Vector3(0, 0.5, 520),
                new THREE.Vector3(-140, 16, 320),
                new THREE.Vector3(150, 44, 100),
                new THREE.Vector3(-160, 24, -120),
                new THREE.Vector3(100, 6, -360),
                new THREE.Vector3(0, 2, -560)
            ];
            const curve = new THREE.CatmullRomCurve3(trackPoints);
            const road = new THREE.Mesh(new THREE.TubeGeometry(curve, 350, 22, 12, false), new THREE.MeshStandardMaterial({{ color: 0x1f2937, roughness: 0.6 }}));
            road.scale.y = 0.01; road.receiveShadow = true; scene.add(road);

            const finish = new THREE.Mesh(new THREE.BoxGeometry(44, 0.2, 4), new THREE.MeshStandardMaterial({{ color: 0xffffff }}));
            finish.position.copy(trackPoints[trackPoints.length - 1]); scene.add(finish);

            // --- COLLISION MAP SYSTEM (MASCHINENWEITE HITBOXEN) ---
            const obstacles = [];
            function spawnObstacle(mesh, x, y, z, radius) {{
                mesh.position.set(x, y, z); mesh.castShadow = true; mesh.receiveShadow = true;
                scene.add(mesh); obstacles.push({{ mesh, x, z, radius }});
            }}

            const curvePoints = curve.getPoints(140);
            curvePoints.forEach((pt, idx) => {{
                if (idx > 5 && idx < 130 && idx % 8 === 0) {{
                    const rock = new THREE.Mesh(new THREE.DodecahedronGeometry(3 + Math.random()*2), new THREE.MeshStandardMaterial({{ color: 0x4b5563, flatShading: true }}));
                    spawnObstacle(rock, pt.x + (idx % 2 === 0 ? 25 : -25), pt.y + 1, pt.z, 4.5);

                    if (idx % 24 === 0) {{
                        const pillar = new THREE.Mesh(new THREE.CylinderGeometry(1.2, 1.2, 6), new THREE.MeshStandardMaterial({{ color: 0x9ca3af }}));
                        spawnObstacle(pillar, pt.x + (Math.random()*6 - 3), pt.y + 3, pt.z, 2.2);
                    }}
                }}
                if (idx > 105 && idx % 6 === 0) {{
                    const house = new THREE.Group();
                    const b = new THREE.Mesh(new THREE.BoxGeometry(9, 6, 8), new THREE.MeshStandardMaterial({{ color: 0x78350f }})); b.position.y = 3;
                    const r = new THREE.Mesh(new THREE.ConeGeometry(7, 3.5, 4), new THREE.MeshStandardMaterial({{ color: 0x991b1b }})); r.position.y = 6.5; r.rotation.y = Math.PI/4;
                    house.add(b, r); spawnObstacle(house, pt.x + (idx % 2 === 0 ? 26 : -26), pt.y, pt.z, 5.5);
                }}
            }});

            // --- COIN SYSTEM (3D GOLDMÜNZEN) ---
            const coins = [];
            const coinGeo = new THREE.CylinderGeometry(1.0, 1.0, 0.2, 16);
            const coinMat = new THREE.MeshStandardMaterial({{ color: 0xfacc15, metalness: 0.9, roughness: 0.1 }});
            
            // Verteile 12 Münzen wellenförmig auf der Straße
            for(let i=5; i<135; i+=11) {{
                const pt = curvePoints[i];
                const cMesh = new THREE.Mesh(coinGeo, coinMat);
                cMesh.rotation.x = Math.PI / 2;
                // Leicht versetzt links/rechts auf der Piste
                const roadOffset = Math.sin(i) * 6;
                cMesh.position.set(pt.x + roadOffset, pt.y + 1.2, pt.z);
                cMesh.castShadow = true;
                scene.add(cMesh);
                coins.push(cMesh);
            }}

            // --- RANDOM MARIO KART BOXEN ---
            const itemBoxes = [];
            for (let i = 1; i < trackPoints.length - 1; i++) {{
                const crystal = new THREE.Mesh(new THREE.OctahedronGeometry(1.8, 0), new THREE.MeshStandardMaterial({{ color: 0xa855f7, emissive: 0x7e22ce }}));
                crystal.position.copy(trackPoints[i]); crystal.position.y += 3.0;
                scene.add(crystal); itemBoxes.push(crystal);
            }}

            // --- VEHICLE ENGINE ---
            function createBike(color) {{
                const group = new THREE.Group();
                const f = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 2.3), new THREE.MeshStandardMaterial({{ color: color, metalness: 0.8 }}));
                f.rotation.z = Math.PI/3; f.position.y = 1.2; group.add(f);
                const w = new THREE.Mesh(new THREE.TorusGeometry(0.8, 0.15, 8, 24), new THREE.MeshStandardMaterial({{ color: 0x111827 }}));
                const fw = w.clone(); fw.position.set(1.4, 0.8, 0); const bw = w.clone(); bw.position.set(-1.4, 0.8, 0);
                group.add(fw, bw); const pivot = new THREE.Group(); pivot.add(group); scene.add(pivot);
                return {{ pivot, model: group, fw, bw }};
            }}

            const player = createBike(0xef4444); player.pivot.position.set(-3, 0.5, 500);
            const ai = createBike(0x2563eb); ai.pivot.position.set(3, 0.5, 500);

            // --- VARIABLES & PHYSICS CORES ---
            const keys = {{}};
            window.addEventListener('keydown', (e) => {{ keys[e.key.toLowerCase()] = true; }});
            window.addEventListener('keyup', (e) => {{ keys[e.key.toLowerCase()] = false; }});

            const pState = {{ speed: 0, angle: Math.PI, coinsCollected: 0, health: 100, item: null, activeEffect: null, effectTimer: 0, lean: 0, slipstreamActive: false }};
            let aiProgress = 0;
            let camShake = 0;

            function getTrackData(pos) {{
                let closestPt = curve.getPoint(0); let minDist = 999;
                for (let i = 0; i <= 100; i++) {{
                    let pt = curve.getPoint(i / 100); let d = pos.distanceTo(pt);
                    if (d < minDist) {{ minDist = d; closestPt = pt; }}
                }}
                return {{ height: closestPt.y, distance: minDist }};
            }}

            // --- ANIMATION MASTER LOOP ---
            function animate() {{
                requestAnimationFrame(animate);
                if (!gameActive) return;

                // TOTALSCHADEN RESET TIMER
                if (isRepairing) return;

                const tData = getTrackData(player.pivot.position);
                player.pivot.position.y = THREE.MathUtils.lerp(player.pivot.position.y, tData.height, 0.2);
                const onRoad = tData.distance < 24;

                // DYNAMISCHER WETTER-TRIGGER (Ab Sektor 2 wechselt das Wetter!)
                if (player.pivot.position.z < 100 && weatherCondition === "SUN") {{
                    weatherCondition = "STORM";
                    document.getElementById('weather-tag').innerText = "Gewitter ⛈️ REGEN";
                    document.getElementById('weather-tag').style.background = "#7c3aed";
                    // Visueller Himmel-Wechsel auf dunkles Lila-Grau
                    scene.background = new THREE.Color(0x2e2a3a);
                    fog.color = new THREE.Color(0x2e2a3a);
                }}

                // SPEED-PROFILING (Bike + Münz-Bonus + Wetter + Offroad)
                let coinBonus = pState.coinsCollected * 0.05; // Jede Münze gibt permanent +2 km/h Top-Speed-Kapazität
                let baseMaxSpeed = isAero ? (onRoad ? 2.1 : 0.4) : (onRoad ? 1.6 : 1.2);
                let maxSpeed = baseMaxSpeed + coinBonus;

                if (pState.activeEffect === "BOOST") maxSpeed *= 1.8;
                
                // WINDSCHATTEN LOGIK (Drafting)
                // Ist der Spieler dicht hinter der KI (X-Delta gering, Z-Abstand zwischen 5 und 35 Metern)?
                const dxAI = Math.abs(player.pivot.position.x - ai.pivot.position.x);
                const dzAI = ai.pivot.position.z - player.pivot.position.z; // KI ist weiter vorne
                
                if (dxAI < 6 && dzAI > 6 && dzAI < 40) {{
                    pState.slipstreamActive = true;
                    maxSpeed += 0.5; // Zusätzlicher Sog-Schub
                    document.getElementById('slip-ui').style.display = "block";
                }} else {{
                    pState.slipstreamActive = false;
                    document.getElementById('slip-ui').style.display = "none";
                }}

                // STEUERUNG & REGEN-RUTSCHEN
                if (keys['w']) pState.speed = Math.min(maxSpeed, pState.speed + 0.04);
                if (keys['s']) pState.speed = Math.max(-0.4, pState.speed - 0.04);
                
                let turnFactor = 0.035;
                // Bei Regen/Storm verliert das Aero-Rad drastisch an Seitenführung (Rutsch-Effekt)
                if (weatherCondition === "STORM") {{
                    turnFactor = isAero ? 0.018 : 0.030; // Aero rutscht übel weg, Gravel hält Spur
                }}

                let turn = 0;
                if (keys['a']) {{ pState.angle += turnFactor * (pState.speed >= 0 ? 1 : -1); turn = 0.07; }}
                if (keys['d']) {{ pState.angle -= turnFactor * (pState.speed >= 0 ? 1 : -1); turn = -0.07; }}

                pState.speed *= 0.965; // Reibung

                pState.lean = THREE.MathUtils.lerp(pState.lean, turn * Math.min(1, pState.speed), 0.1);
                player.model.rotation.z = pState.lean * 6;

                // KOLLISIONS-ABFRAGE MIT INTEGRITÄTS-ABZUG
                const nextX = player.pivot.position.x + Math.sin(pState.angle) * pState.speed;
                const nextZ = player.pivot.position.z + Math.cos(pState.angle) * pState.speed;

                let hitObj = null;
                obstacles.forEach(obs => {{
                    const dx = nextX - obs.x; const dz = nextZ - obs.z;
                    if (Math.sqrt(dx*dx + dz*dz) < obs.radius) hitObj = obs;
                }});

                if (hitObj) {{
                    // CRASH!
                    camShake = 12; // Screen Shake auslösen
                    pState.health = Math.max(0, pState.health - 25); // 25% Schaden bei Kollision
                    document.getElementById('health').innerText = pState.health + "%";

                    // Totalschaden Check
                    if (pState.health <= 0) {{
                        isRepairing = true;
                        pState.speed = 0;
                        document.getElementById('repair-overlay').style.display = "flex";
                        setTimeout(() => {{
                            pState.health = 100;
                            document.getElementById('health').innerText = "100%";
                            document.getElementById('repair-overlay').style.display = "none";
                            isRepairing = false;
                        }}, 3000); // 3 Sekunden Zwangspause
                    }}

                    pState.speed = -pState.speed * 0.4;
                    player.pivot.position.x -= Math.sin(pState.angle) * 1.8;
                    player.pivot.position.z -= Math.cos(pState.angle) * 1.8;
                }} else {{
                    player.pivot.position.x = nextX; player.pivot.position.z = nextZ;
                }}

                player.pivot.rotation.y = pState.angle + Math.PI / 2;
                player.fw.rotation.z -= pState.speed * 0.9; player.bw.rotation.z -= pState.speed * 0.9;

                // --- MÜNZEN FREI EINCOLLECTEN ---
                coins.forEach((c) => {{
                    c.rotation.z += 0.04; // Münz-Spin
                    if(player.pivot.position.distanceTo(c.position) < 3.8) {{
                        c.position.y = -500; // Wegbeamen
                        pState.coinsCollected += 1;
                        document.getElementById('coins-ui').innerText = "🪙 " + pState.coinsCollected;
                    }}
                }});

                // Effects & Mario Kart Boxen
                if (pState.effectTimer > 0) {{
                    pState.effectTimer--;
                    if (pState.effectTimer === 0) {{ pState.activeEffect = null; document.getElementById('item-slot').innerText = "LEER"; }}
                }}

                itemBoxes.forEach(box => {{
                    box.rotation.y += 0.03;
                    if (player.pivot.position.distanceTo(box.position) < 4.5 && !pState.item && !pState.activeEffect) {{
                        const r = Math.random();
                        if(r > 0.5) {{
                            pState.item = "🚀 NITRO-PILZ"; document.getElementById('item-slot').innerText = "🚀 NITRO-PILZ";
                        }} else {{
                            pState.item = "🛡️ REPARATUR-KIT"; document.getElementById('item-slot').innerText = "🛡️ REPARATUR-KIT";
                        }}
                        
                        setTimeout(() => {{
                            if(pState.item === "🚀 NITRO-PILZ") {{
                                pState.activeEffect = "BOOST"; pState.speed = 3.3; pState.effectTimer = 90; camShake = 6;
                                document.getElementById('item-slot').innerText = "🔥 ULTRA-BOOST!!";
                            }} else {{
                                pState.health = 100; document.getElementById('health').innerText = "100%";
                                document.getElementById('item-slot').innerText = "🔧 REPARIERT!";
                            }}
                            pState.item = null;
                        }}, 250);
                        box.position.y = -100;
                        setTimeout(() => {{ box.position.y = getTrackData(box.position).height + 3.0; }}, 6000);
                    }}
                }});

                // SMARTES KI RUBBERBANDING
                let aiSpeed = 0.0016;
                if (ai.pivot.position.z > player.pivot.position.z + 45) aiSpeed = 0.0010; // KI bremst ab
                else if (player.pivot.position.z > ai.pivot.position.z + 45) aiSpeed = 0.0024; // KI drückt aufs Gas

                aiProgress += aiSpeed; if (aiProgress > 1) aiProgress = 1;
                const aiTarget = curve.getPointAt(aiProgress);
                ai.pivot.position.lerp(aiTarget, 0.1); ai.pivot.position.y = getTrackData(ai.pivot.position).height;
                const aiFuture = curve.getPointAt(Math.min(1, aiProgress + 0.01));
                ai.pivot.lookAt(aiFuture); ai.pivot.rotateY(Math.PI / 2);

                // HUD REFRESH
                document.getElementById('speed').innerText = Math.round(Math.abs(pState.speed) * 36);
                document.getElementById('altimeter').innerText = Math.round(player.pivot.position.y * 5) + "m";

                // CHASE CAM FOLLOW MIT DYNAMISCHEM SCREEN SHAKE
                const camDist = 22;
                let tCamX = player.pivot.position.x - Math.sin(pState.angle) * camDist;
                let tCamZ = player.pivot.position.z - Math.cos(pState.angle) * camDist;
                let tCamY = player.pivot.position.y + 7.5;

                if (camShake > 0) {{
                    tCamX += (Math.random() - 0.5) * camShake * 0.15;
                    tCamY += (Math.random() - 0.5) * camShake * 0.15;
                    camShake *= 0.9;
                }}

                camera.position.x = THREE.MathUtils.lerp(camera.position.x, tCamX, 0.06);
                camera.position.z = THREE.MathUtils.lerp(camera.position.z, tCamZ, 0.06);
                camera.position.y = THREE.MathUtils.lerp(camera.position.y, tCamY, 0.06);
                camera.lookAt(new THREE.Vector3(player.pivot.position.x, player.pivot.position.y + 1.8, player.pivot.position.z));

                // WINNER DETECTION & SPEICHER-LINK AKTIVIEREN
                if (player.pivot.position.z <= -560 || ai.pivot.position.z <= -560) {{
                    gameActive = false;
                    const won = player.pivot.position.z <= -560;
                    document.getElementById('winner').innerText = won ? "DU HAST" : "DIE KI HAT";
                    document.getElementById('victory').style.display = "block";
                    
                    // Bei Klick Münzen an Streamlit URL-Parameter senden
                    document.getElementById('save-btn').onclick = () => {{
                        const coinsToSave = won ? pState.coinsCollected : Math.floor(pState.coinsCollected / 2);
                        window.location.href = window.location.pathname + "?add_coins=" + coinsToSave;
                    }};
                }}

                renderer.render(scene, camera);
            }}
            animate();
        </script>
    </body>
    </html>
    """

    st.components.v1.html(engine_code, height=670, scrolling=False)

    # --- SPIELREGELN IN SIDEBAR ---
    st.sidebar.markdown("""
    ### 🎮 Pro-Racer Handbuch:
    * **Windschatten 💨:** Bleib direkt hinter dem blauen KI-Bike! Dein Balken leuchtet lila auf, du wirst schneller und sparst Ausdauer.
    * **Münzen-Tipp 🪙:** Sammle so viele Goldmünzen wie möglich! Sie erhöhen deinen Top-Speed sofort. Wenn du gewinnst, wandern alle Münzen auf dein Sparbuch. Verlierst du, rettest du nur die Hälfte!
    * **Wetterwechsel ⛈️:** Sobald der Sturm losbricht, fängt die Piste an zu schmieren. Fahr extrem vorsichtig an Felsen vorbei!
    """)
