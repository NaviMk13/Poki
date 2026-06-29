import streamlit as st

# --- 1. STREAMLIT CONFIG & DESIGN ---
st.set_page_config(page_title="Tour de Stream 3D", layout="wide", page_icon="🚴‍♂️")

st.markdown("""
    <style>
    .stApp {
        background-color: #0b0f19;
        color: #ffffff;
    }
    iframe {
        border: 4px solid #facc15 !important; /* Tour de France Gelb */
        border-radius: 15px;
        box-shadow: 0 0 35px rgba(250, 204, 21, 0.25);
    }
    h1 {
        font-family: 'Impact', sans-serif;
        color: #facc15 !important;
        text-shadow: 3px 3px 0px #000000;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("💛 TOUR DE STREAM 3D: ALPEN-ETAPPE 💛")
st.write("<p style='text-align:center; color:#94a3b8;'>Klicke einmal in das Spielfeld, um die Steuerung zu aktivieren! Erklimmt den Col du Stream!</p>", unsafe_allow_html=True)

# --- 2. MULTIPLAYER 3D ENGINE COOKED WITH THREE.JS ---
tour_de_france_code = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body { margin: 0; overflow: hidden; background-color: #0b0f19; font-family: 'Arial', sans-serif; }
        #canvas-container { width: 100vw; height: 78vh; }
        #hud {
            position: absolute; top: 15px; left: 15px;
            color: #ffffff; background: rgba(15, 23, 42, 0.9);
            padding: 20px; border-radius: 12px; border: 3px solid #facc15;
            pointer-events: none; width: 280px; box-shadow: 0 10px 25px rgba(0,0,0,0.5);
        }
        .racer-stat { margin: 8px 0; font-size: 15px; font-weight: bold; padding: 6px; border-radius: 6px; }
        #click-alert {
            position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%);
            background: #facc15; color: #000; padding: 10px 20px; font-weight: bold;
            border-radius: 20px; animation: pulse 1.5s infinite; font-size: 14px;
        }
        @keyframes pulse { 0% { opacity: 0.6; } 50% { opacity: 1; } 100% { opacity: 0.6; } }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>

    <div id="hud">
        <h3 style="margin: 0 0 10px 0; color: #facc15; text-align:center; text-transform:uppercase;">Le Tour Simulator</h3>
        <div class="racer-stat" style="background: rgba(239, 68, 68, 0.2); border-left: 4px solid #ef4444;">
            🔴 Maillot Rouge: <span id="sp1">0 km/h</span><br>
            <small style="color: #cbd5e1;">Tasten: W (Gas), S, A, D</small>
        </div>
        <div class="racer-stat" style="background: rgba(59, 130, 246, 0.2); border-left: 4px solid #3b82f6;">
            🔵 Maillot Bleu: <span id="sp2">0 km/h</span><br>
            <small style="color: #cbd5e1;">Tasten: Pfeiltasten (↑, ↓, ←, →)</small>
        </div>
        <hr style="border-color: #334155;">
        <div style="font-size:12px; color:#a1a1aa; text-align:center;">Bergwertung: Wer bezwingt die Serpentinen?</div>
    </div>

    <div id="click-alert" id="alert-box">⚠️ ZUERST HIER REINKLICKEN ZUM STEUERN!</div>

    <div id="canvas-container"></div>

    <script>
        // --- 1. ENGINE BASIC SETUP ---
        const container = document.getElementById('canvas-container');
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0xbfe3dd); // Schöner französischer Sommerhimmel
        scene.fog = new THREE.FogExp2(0xbfe3dd, 0.007);

        const camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight * 0.78);
        renderer.shadowMap.enabled = true;
        container.appendChild(renderer.domElement);

        // Beleuchtung für die Bergetappe
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
        scene.add(ambientLight);
        const sunLight = new THREE.DirectionalLight(0xfffaed, 1.2);
        sunLight.position.set(100, 150, 50);
        scene.castShadow = true;
        scene.shadow.mapSize.width = 2048;
        scene.shadow.mapSize.height = 2048;
        scene.add(sunLight);

        // Hide Alert on click
        window.addEventListener('click', () => {
            const alertBox = document.getElementById('click-alert');
            if(alertBox) alertBox.style.display = 'none';
        });

        // --- 2. MAP DESIGN: TOUR DE FRANCE ALPINE PASS ---
        // Das Bergterrain (Boden)
        const terrainGeo = new THREE.PlaneGeometry(2000, 2000, 20, 20);
        terrainGeo.rotateX(-Math.PI / 2);
        const terrainMat = new THREE.MeshStandardMaterial({ color: 0x3d7a44, roughness: 0.9 }); // Alpengras
        const terrain = new THREE.Mesh(terrainGeo, terrainMat);
        scene.add(terrain);

        // Serpentinen-Rennstrecke (Ein geschwungener Asphaltkurs)
        const roadGroup = new THREE.Group();
        scene.add(roadGroup);

        // Wir generieren eine kurvige Passstraße über mathematische Kurven (Splines)
        const points = [];
        points.push(new THREE.Vector3(0, 0.1, 400));
        points.push(new THREE.Vector3(-80, 0.1, 250));
        points.push(new THREE.Vector3(120, 0.1, 100));
        points.push(new THREE.Vector3(-140, 0.1, -50));
        points.push(new THREE.Vector3(60, 0.1, -200));
        points.push(new THREE.Vector3(0, 0.1, -400));

        const curve = new THREE.CatmullRomCurve3(points);
        const roadGeo = new THREE.TubeGeometry(curve, 200, 14, 8, false);
        const roadMat = new THREE.MeshStandardMaterial({ color: 0x475569, roughness: 0.7 }); // Grauer Asphalt
        const asphalt = new THREE.Mesh(roadGeo, roadMat);
        asphalt.scale.y = 0.01; // Flach auf den Boden drücken
        roadGroup.add(asphalt);

        // Dekorationen: Tannen & Zuschauer entlang der Strecke platzieren
        const curvePoints = curve.getPoints(150);
        curvePoints.forEach((pt, idx) => {
            if(idx % 3 === 0) {
                // Tannenbaum spawnen
                const treeGroup = new THREE.Group();
                const trunkGeo = new THREE.CylinderGeometry(0.4, 0.6, 2);
                const trunkMat = new THREE.MeshStandardMaterial({ color: 0x4a3728 });
                const trunk = new THREE.Mesh(trunkGeo, trunkMat);
                trunk.position.y = 1;
                treeGroup.add(trunk);

                const leavesGeo = new THREE.ConeGeometry(3, 7, 5);
                const leavesMat = new THREE.MeshStandardMaterial({ color: 0x14532d, roughness: 0.8 });
                const leaves = new THREE.Mesh(leavesGeo, leavesMat);
                leaves.position.y = 4.5;
                treeGroup.add(leaves);

                // Seitlich der Straße versetzen
                const sideOffset = (Math.random() > 0.5 ? 20 : -20) + (Math.random() * 5);
                treeGroup.position.set(pt.x + sideOffset, 0, pt.z + (Math.random() * 5));
                scene.add(treeGroup);
            }

            if(idx % 5 === 0) {
                // Zuschauer / Flaggen-Masten spawnen (Tour de France Feeling!)
                const flagGroup = new THREE.Group();
                const poleGeo = new THREE.CylinderGeometry(0.1, 0.1, 6);
                const poleMat = new THREE.MeshStandardMaterial({ color: 0xcccccc });
                const pole = new THREE.Mesh(poleGeo, poleMat);
                pole.position.y = 3;
                flagGroup.add(pole);

                // Tricolore Flagge (Frankreich)
                const flagGeo = new THREE.BoxGeometry(2, 1.2, 0.1);
                const flagMat = new THREE.MeshBasicMaterial({ color: 0x002395 }); // Blau (Stellvertretend)
                const flag = new THREE.Mesh(flagGeo, flagMat);
                flag.position.set(1, 5.4, 0);
                flagGroup.add(flag);

                const flagOffset = idx % 2 === 0 ? 10 : -10;
                flagGroup.position.set(pt.x + flagOffset, 0, pt.z);
                scene.add(flagGroup);
            }
        });

        // --- 3. RICHTIGE 3D RENNRÄDER BAUEN ---
        function create3dBike(colorHex) {
            const bike = new THREE.Group();

            // Rahmen (Dünne Tubes/Zylinder)
            const frameMat = new THREE.MeshStandardMaterial({ color: colorHex, roughness: 0.5 });
            const pipeGeo = new THREE.CylinderGeometry(0.1, 0.1, 3);
            pipeGeo.rotateZ(Math.PI / 4);
            
            const mainTriangle = new THREE.Mesh(pipeGeo, frameMat);
            mainTriangle.position.set(0, 1.5, 0);
            bike.add(mainTriangle);

            // Laufräder (Torus Geometrie für echte Felgen + Speichen-Zentrum)
            const wheelMat = new THREE.MeshStandardMaterial({ color: 0x111111, roughness: 0.9 });
            const wheelGeo = new THREE.TorusGeometry(0.9, 0.15, 8, 24);
            
            const frontWheel = new THREE.Mesh(wheelGeo, wheelMat);
            frontWheel.position.set(1.8, 0.9, 0);
            bike.add(frontWheel);

            const backWheel = new THREE.Mesh(wheelGeo, wheelMat);
            backWheel.position.set(-1.8, 0.9, 0);
            bike.add(backWheel);

            // Lenker & Sattel
            const componentMat = new THREE.MeshStandardMaterial({ color: 0x222222 });
            const handlebarGeo = new THREE.CylinderGeometry(0.08, 0.08, 1.4);
            handlebarGeo.rotateX(Math.PI / 2);
            const handlebar = new THREE.Mesh(handlebarGeo, componentMat);
            handlebar.position.set(1.5, 2.5, 0);
            bike.add(handlebar);

            const saddleGeo = new THREE.BoxGeometry(0.6, 0.15, 0.3);
            const saddle = new THREE.Mesh(saddleGeo, componentMat);
            saddle.position.set(-0.6, 2.3, 0);
            bike.add(saddle);

            bike.castShadow = true;
            return { mesh: bike, frontWheel: frontWheel, backWheel: backWheel };
        }

        const player1 = create3dBike(0xef4444); // Rotes Rennrad
        player1.mesh.position.set(-3, 0, 380);
        scene.add(player1.mesh);

        const player2 = create3dBike(0x3b82f6); // Blaues Rennrad
        player2.mesh.position.set(3, 0, 380);
        scene.add(player2.mesh);


        // --- 4. ROBUSTE TASTATUR-STEUERUNG ---
        const keyMap = {};
        
        // Event-Listener direkt an das Window binden
        window.addEventListener('keydown', (e) => { 
            keyMap[e.key.toLowerCase()] = true; 
        });
        window.addEventListener('keyup', (e) => { 
            keyMap[e.key.toLowerCase()] = false; 
        });

        // Fahrphysik Datenstrukturen
        const bike1 = { speed: 0, angle: Math.PI, maxSpeed: 1.6, accel: 0.03, friction: 0.96 };
        const bike2 = { speed: 0, angle: Math.PI, maxSpeed: 1.6, accel: 0.03, friction: 0.96 };

        // --- 5. GAME ENGINE LOOP (60 FPS) ---
        function animate() {
            requestAnimationFrame(animate);

            // --- SPIELER 1 ENGINE LOGIK (WASD) ---
            if (keyMap['w']) bike1.speed = Math.min(bike1.maxSpeed, bike1.speed + bike1.accel);
            if (keyMap['s']) bike1.speed = Math.max(-bike1.maxSpeed/3, bike1.speed - bike1.accel);
            if (keyMap['a']) bike1.angle += 0.035 * (bike1.speed >= 0 ? 1 : -1);
            if (keyMap['d']) bike1.angle -= 0.035 * (bike1.speed >= 0 ? 1 : -1);

            // --- SPIELER 2 ENGINE LOGIK (Pfeiltasten) ---
            if (keyMap['arrowup']) bike2.speed = Math.min(bike2.maxSpeed, bike2.speed + bike2.accel);
            if (keyMap['arrowdown']) bike2.speed = Math.max(-bike2.maxSpeed/3, bike2.speed - bike2.accel);
            if (keyMap['arrowleft']) bike2.angle += 0.035 * (bike2.speed >= 0 ? 1 : -1);
            if (keyMap['arrowright']) bike2.angle -= 0.035 * (bike2.speed >= 0 ? 1 : -1);

            // Reibungssimulation (Rollen lassen)
            bike1.speed *= bike1.friction;
            bike2.speed *= bike2.friction;

            // P1 Positions- & Rotations-Update
            player1.mesh.position.x += Math.sin(bike1.angle) * bike1.speed;
            player1.mesh.position.z += Math.cos(bike1.angle) * bike1.speed;
            player1.mesh.rotation.y = bike1.angle + Math.PI/2; // Ausrichtung anpassen

            // P2 Positions- & Rotations-Update
            player2.mesh.position.x += Math.sin(bike2.angle) * bike2.speed;
            player2.mesh.position.z += Math.cos(bike2.angle) * bike2.speed;
            player2.mesh.rotation.y = bike2.angle + Math.PI/2;

            // Laufrad-Rotationen animieren (Sieht aus als ob sie fahren!)
            player1.frontWheel.rotation.z -= bike1.speed * 0.8;
            player1.backWheel.rotation.z -= bike1.speed * 0.8;
            player2.frontWheel.rotation.z -= bike2.speed * 0.8;
            player2.backWheel.rotation.z -= bike2.speed * 0.8;

            // HUD Tacho-Werte in Echtzeit manipulieren
            document.getElementById('sp1').innerText = Math.abs(Math.round(bike1.speed * 38)) + " km/h";
            document.getElementById('sp2').innerText = Math.abs(Math.round(bike2.speed * 38)) + " km/h";

            // Dynamischer Kamera-Fokus (Folgt dem Mittelpunkt beider Racer)
            const mx = (player1.mesh.position.x + player2.mesh.position.x) / 2;
            const mz = (player1.mesh.position.z + player2.mesh.position.z) / 2;
            const distance = player1.mesh.position.distanceTo(player2.mesh.position);

            camera.position.x = mx;
            camera.position.z = mz + Math.max(35, distance * 1.1);
            camera.position.y = Math.max(25, distance * 0.7);
            camera.lookAt(new THREE.Vector3(mx, 1, mz));

            renderer.render(scene, camera);
        }

        animate();

        // Fenster-Resizing absichern
        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight * 0.78);
        });
    </script>
</body>
</html>
"""

# --- 3. INJECT HTML TO STREAMLIT ---
st.components.v1.html(tour_de_france_code, height=680, scrolling=False)

# --- 4. SIDEBAR MECHANICS ---
st.sidebar.markdown("""
### 🏁 Rennleiter-Zentrale:
Willkommen bei der Königsetappe! Ihr fahrt auf einem originalgetreuen Asphaltband durch die Alpen.

**🚨 Wichtig bei Steuerungshacks:**
Weil Webbrowser iFrames absichern, müsst ihr **einmal mitten in das 3D-Spielfeld klicken**, damit die Tastaturbefehle direkt an die Rennräder gesendet werden.

**🔴 Spieler 1 (Maillot Rouge):**
* `W` / `S` = Vorwärts / Rückwärts
* `A` / `D` = Lenken (360°)

**🔵 Spieler 2 (Maillot Bleu):**
* `Pfeiltaste Hoch / Runter` = Vorwärts / Rückwärts
* `Pfeiltaste Links / Rechts` = Lenken (360°)
""")
