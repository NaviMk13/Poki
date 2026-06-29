import streamlit as st

# --- 1. STREAMLIT PAGE SETUP ---
st.set_page_config(page_title="VELO-DASH 3D Open World Simulator", layout="wide", page_icon="🚴‍♂️")

st.markdown("""
    <style>
    .stApp {
        background-color: #090d16;
        color: #ffffff;
    }
    iframe {
        border: 4px solid #00f0ff !important;
        border-radius: 15px;
        box-shadow: 0 0 30px rgba(0, 240, 255, 0.3);
    }
    h1 {
        font-family: 'Impact', sans-serif;
        color: #00f0ff !important;
        text-shadow: 0 0 10px rgba(0, 240, 255, 0.5);
        text-align: center;
        text-transform: uppercase;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🚴‍♂️ VELO-DASH 3D: REALTIME OPEN-WORLD SIMULATOR")
st.write("<p style='text-align:center; color:#94a3b8;'>Echte 3D Game Engine in Streamlit eingebettet. Perfekt für das Schul-WLAN!</p>", unsafe_allow_html=True)

# --- 2. THE EMBEDDED 3D ENGINE (HTML / JAVASCRIPT / THREE.JS) ---
# Dieser riesige Block wird als flüssige WebGL-App direkt im Browser gerendert.
three_js_code = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body { margin: 0; overflow: hidden; background-color: #090d16; font-family: monospace; }
        #canvas-container { width: 100vw; height: 75vh; }
        #hud {
            position: absolute; top: 15px; left: 15px;
            color: #00f0ff; background: rgba(11, 15, 25, 0.85);
            padding: 15px; border-radius: 10px; border: 2px solid #00f0ff;
            pointer-events: none; font-size: 14px; box-shadow: 0 0 15px rgba(0,240,255,0.2);
        }
        .player-stat { margin: 5px 0; font-size: 16px; font-weight: bold; }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>

    <div id="hud">
        <h2 style="margin: 0 0 10px 0; color: #facc15;">🏎️ 3D MULTIPLAYER DUEL</h2>
        <div class="player-stat" style="color: #ef4444;">🔴 SPIELER 1 (Aero-Bike): <span id="sp1">0 km/h</span><br><small>Steuerung: W, A, S, D</small></div>
        <div class="player-stat" style="color: #3b82f6;">🔵 SPIELER 2 (Gravel-Bike): <span id="sp2">0 km/h</span><br><small>Steuerung: Pfeiltasten</small></div>
        <hr style="border-color: #00f0ff;">
        <div id="target-info" style="color: #22c55e; font-weight: bold;">Nächstes Ziel-Tor aktiv! Wer erreicht es zuerst?</div>
    </div>

    <div id="canvas-container"></div>

    <script>
        // --- 1. ENGINE BASIC SETUP ---
        const container = document.getElementById('canvas-container');
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x0f172a); // Stylischer Nachthimmel
        scene.fog = new THREE.FogExp2(0x0f172a, 0.015); // Nebel für Open-World-Tiefe

        const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight * 0.75);
        container.appendChild(renderer.domElement);

        // Lichteffekte
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
        scene.add(ambientLight);
        const dirLight = new THREE.DirectionalLight(0x00f0ff, 1);
        dirLight.position.set(50, 100, 50);
        scene.add(dirLight);

        // --- 2. OPEN WORLD GEOMETRIE (Die Map) ---
        // Der Rasen/Asphalt
        const floorGeo = new THREE.PlaneGeometry(1000, 1000);
        const floorMat = new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.9 });
        const floor = new THREE.Mesh(floorGeo, floorMat);
        floor.rotation.x = -Math.PI / 2;
        scene.add(floor);

        // Ein Gitternetz auf dem Boden für die Geschwindigkeits-Illusion
        const grid = new THREE.GridHelper(1000, 100, 0x00f0ff, 0x334155);
        grid.position.y = 0.01;
        scene.add(grid);

        // Random Hindernisse & Gebäude in der Open World spawnen
        const buildings = [];
        for(let i=0; i<60; i++) {
            const h = Math.random() * 30 + 10;
            const bGeo = new THREE.BoxGeometry(10, h, 10);
            const bMat = new THREE.MeshStandardMaterial({ color: 0x334155, wireframe: Math.random() > 0.5 });
            const b = new THREE.Mesh(bGeo, bMat);
            b.position.set((Math.random()-0.5)*400, h/2, (Math.random()-0.5)*400);
            scene.add(b);
        }

        // --- 3. DIE FAHRER (3D-Objekte) ---
        // Spieler 1 (Rot)
        const p1Geo = new THREE.ConeGeometry(1.5, 4, 4);
        const p1Mat = new THREE.MeshStandardMaterial({ color: 0xef4444 });
        const p1Mesh = new THREE.Mesh(p1Geo, p1Mat);
        p1Mesh.rotation.x = Math.PI / 2; // Liegend wie ein Pfeil/Fahrrad
        p1Mesh.position.set(-10, 2, 0);
        scene.add(p1Mesh);

        // Spieler 2 (Blau)
        const p2Geo = new THREE.ConeGeometry(1.5, 4, 4);
        const p2Mat = new THREE.MeshStandardMaterial({ color: 0x3b82f6 });
        const p2Mesh = new THREE.Mesh(p2Geo, p2Mat);
        p2Mesh.rotation.x = Math.PI / 2;
        p2Mesh.position.set(10, 2, 0);
        scene.add(p2Mesh);

        // Das Ziel-Tor (Leuchtende grüne Kugel)
        const targetGeo = new THREE.SphereGeometry(4, 16, 16);
        const targetMat = new THREE.MeshBasicMaterial({ color: 0x22c55e, wireframe: true });
        const targetMesh = new THREE.Mesh(targetGeo, targetMat);
        function relocateTarget() {
            targetMesh.position.set((Math.random()-0.5)*200, 4, (Math.random()-0.5)*200);
        }
        relocateTarget();
        scene.add(targetMesh);

        // --- 4. ENGINE STEUERUNGS-LOGIK ---
        const keys = {};
        window.addEventListener('keydown', (e) => { keys[e.key.toLowerCase()] = true; });
        window.addEventListener('keyup', (e) => { keys[e.key.toLowerCase()] = false; });

        // Physik-Variablen für beide Fahrer
        const p1 = { speed: 0, maxSpeed: 1.8, accel: 0.04, friction: 0.97, angle: 0, rotSpeed: 0.04 };
        const p2 = { speed: 0, maxSpeed: 1.8, accel: 0.04, friction: 0.97, angle: 0, rotSpeed: 0.04 };

        // Kamera-Modus Variablen
        camera.position.set(0, 45, 90);

        // --- 5. MAIN GAME LOOP (60 FPS Echtzeit) ---
        function animate() {
            requestAnimationFrame(animate);

            // --- STEUERUNG SPIELER 1 (WASD) ---
            if (keys['w']) p1.speed = Math.min(p1.maxSpeed, p1.speed + p1.accel);
            if (keys['s']) p1.speed = Math.max(-p1.maxSpeed/2, p1.speed - p1.accel);
            if (keys['a']) p1.angle += p1.rotSpeed * (p1.speed >= 0 ? 1 : -1);
            if (keys['d']) p1.angle -= p1.rotSpeed * (p1.speed >= 0 ? 1 : -1);

            // --- STEUERUNG SPIELER 2 (Pfeiltasten) ---
            if (keys['arrowup']) p2.speed = Math.min(p2.maxSpeed, p2.speed + p2.accel);
            if (keys['arrowdown']) p2.speed = Math.max(-p2.maxSpeed/2, p2.speed - p2.accel);
            if (keys['arrowleft']) p2.angle += p2.rotSpeed * (p2.speed >= 0 ? 1 : -1);
            if (keys['arrowright']) p2.angle -= p2.rotSpeed * (p2.speed >= 0 ? 1 : -1);

            // Reibung anwenden (Ausrollen lassen)
            p1.speed *= p1.friction;
            p2.speed *= p2.friction;

            // Positionen updaten anhand des Winkels (Trigonometrie für echte 360° Open World)
            p1Mesh.position.x += Math.sin(p1.angle) * p1.speed;
            p1Mesh.position.z += Math.cos(p1.angle) * p1.speed;
            p1Mesh.rotation.z = p1.angle; // Modell in Fahrtrichtung drehen

            p2Mesh.position.x += Math.sin(p2.angle) * p2.speed;
            p2Mesh.position.z += Math.cos(p2.angle) * p2.speed;
            p2Mesh.rotation.z = p2.angle;

            // Ziel-Tor Animation (Drehen und Pulsieren)
            targetMesh.rotation.y += 0.02;
            targetMesh.rotation.x += 0.01;

            // --- KOLLISIONS-CHECK ZIEL ---
            const distP1 = p1Mesh.position.distanceTo(targetMesh.position);
            const distP2 = p2Mesh.position.position ? p2Mesh.position.distanceTo(targetMesh.position) : p2Mesh.position.distanceTo(targetMesh.position);
            
            if(distP1 < 5) {
                relocateTarget();
                document.getElementById('target-info').innerHTML = "💥 PUNKT FÜR SPIELER 1 (ROT)! Neues Tor gespawnt!";
                document.getElementById('target-info').style.color = "#ef4444";
            } else if(distP2 < 5) {
                relocateTarget();
                document.getElementById('target-info').innerHTML = "💥 PUNKT FÜR SPIELER 2 (BLAU)! Neues Tor gespawnt!";
                document.getElementById('target-info').style.color = "#3b82f6";
            }

            // HUD Tacho updaten
            document.getElementById('sp1').innerText = Math.abs(Math.round(p1.speed * 40)) + " km/h";
            document.getElementById('sp2').innerText = Math.abs(Math.round(p2.speed * 40)) + " km/h";

            // Kamera positioniert sich dynamisch über dem Geschehen, um beide im Blick zu behalten
            const midX = (p1Mesh.position.x + p2Mesh.position.x) / 2;
            const midZ = (p1Mesh.position.z + p2Mesh.position.z) / 2;
            const distBetween = p1Mesh.position.distanceTo(p2Mesh.position);
            
            camera.position.x = midX;
            camera.position.z = midZ + Math.max(40, distBetween * 1.2);
            camera.position.y = Math.max(30, distBetween * 0.8);
            camera.lookAt(new THREE.Vector3(midX, 0, midZ));

            renderer.render(scene, camera);
        }

        // Engine starten
        animate();

        // Responsive Resizing
        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight * 0.75);
        });
    </script>
</body>
</html>
"""

# --- 3. EXECUTE INTEGRATION ---
# Hier übergeben wir den JavaScript-Code an den Streamlit-HTML-iFrame
st.components.v1.html(three_js_code, height=650, scrolling=False)

# --- 4. SIDEBAR CONTROLS ---
st.sidebar.markdown("""
### 🛠️ Open World Handbuch:
Setz dich mit deinem Kumpel oder Mitschüler vor den Bildschirm. 
Einer greift sich die linke Seite der Tastatur, der andere die rechte!

**🔴 SPIELER 1 (Aero-Bike):**
* `W` = Beschleunigen
* `S` = Bremsen / Rückwärts
* `A` / `D` = 360° Lenken

**🔵 SPIELER 2 (Gravel-Bike):**
* `Pfeiltaste Hoch` = Beschleunigen
* `Pfeiltaste Runter` = Bremsen
* `Pfeiltaste Links/Rechts` = 360° Lenken

*Tipp: Jagt das grüne Leuchttor am Horizont! Wer es rammt, kriegt den Punkt!*
""")
