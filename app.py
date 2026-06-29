import streamlit as st

# --- 1. STREAMLIT CONFIG & DESIGN ---
st.set_page_config(page_title="Tour de Stream 3D ULTRA", layout="wide", page_icon="💛")

st.markdown("""
    <style>
    .stApp { background-color: #05070f; color: #ffffff; font-family: Arial, sans-serif; }
    iframe { border: 4px solid #facc15 !important; border-radius: 15px; box-shadow: 0 0 35px rgba(250, 204, 21, 0.4); }
    h1 { font-family: 'Impact', sans-serif; color: #facc15 !important; text-shadow: 3px 3px 0px #000000; text-align: center; text-transform: uppercase; margin: 0; }
    </style>
""", unsafe_allow_html=True)

st.write("<h1>🚴‍♂️ TOUR DE STREAM 3D: GRAND EDITION 🚴‍♂️</h1>", unsafe_allow_html=True)
st.write("<p style='text-align:center; color:#94a3b8; margin-bottom:15px;'>Klicke einmal in das Spielfeld, um die Steuerung zu aktivieren! Wer holt sich das Gelbe Trikot?</p>", unsafe_allow_html=True)

# --- 2. MULTIPLAYER 3D ENGINE COOKED WITH THREE.JS ---
full_game_code = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body { margin: 0; overflow: hidden; background-color: #05070f; font-family: 'Arial', sans-serif; }
        #canvas-container { width: 100vw; height: 75vh; }
        #hud {
            position: absolute; top: 15px; left: 15px;
            color: #ffffff; background: rgba(10, 15, 30, 0.9);
            padding: 15px; border-radius: 12px; border: 3px solid #facc15;
            pointer-events: none; width: 290px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); z-index: 10;
        }
        .racer-stat { margin: 8px 0; font-size: 14px; font-weight: bold; padding: 8px; border-radius: 6px; }
        .stamina-bar { background: #475569; height: 6px; border-radius: 3px; margin-top: 4px; overflow: hidden; }
        .stamina-fill { height: 100%; transition: width 0.1s linear; }
        #click-alert {
            position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%);
            background: #facc15; color: #000; padding: 10px 20px; font-weight: bold;
            border-radius: 20px; animation: pulse 1.5s infinite; font-size: 14px; z-index: 10;
        }
        #victory-screen {
            display: none; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
            background: rgba(250, 204, 21, 0.95); color: #000; padding: 40px; border-radius: 20px;
            font-size: 32px; font-weight: bold; text-align: center; border: 5px solid #fff;
            box-shadow: 0 0 50px rgba(255,255,255,0.6); z-index: 100;
        }
        @keyframes pulse { 0% { opacity: 0.6; } 50% { opacity: 1; } 100% { opacity: 0.6; } }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>

    <div id="hud">
        <h3 style="margin: 0 0 10px 0; color: #facc15; text-align:center; text-transform:uppercase;">Le Tour ULTRA</h3>
        
        <div class="racer-stat" style="background: rgba(239, 68, 68, 0.15); border-left: 4px solid #ef4444;">
            🔴 P1 (WASD): <span id="sp1">0 km/h</span> <span id="surf1" style="font-size:10px;"></span>
            <div class="stamina-bar"><div id="st1" class="stamina-fill" style="background:#ef4444; width:100%;"></div></div>
        </div>
        
        <div class="racer-stat" style="background: rgba(59, 130, 246, 0.15); border-left: 4px solid #3b82f6;">
            🔵 P2 (Pfeile): <span id="sp2">0 km/h</span> <span id="surf2" style="font-size:10px;"></span>
            <div class="stamina-bar"><div id="st2" class="stamina-fill" style="background:#3b82f6; width:100%;"></div></div>
        </div>
        
        <hr style="border-color: #334155; margin: 10px 0;">
        <div id="draft-ticker" style="font-size:12px; color:#22c55e; text-align:center; font-weight:bold;">Suche Windschatten...</div>
    </div>

    <div id="click-alert">⚠️ KLICKE HIER REIN ZUM ZOCKEN!</div>
    <div id="victory-screen">🏆 <span id="winner-text">SPIELER</span> GEWINNT! 💛</div>
    <div id="canvas-container"></div>

    <script>
        // --- 1. BASIC ENGINE SETUP ---
        const container = document.getElementById('canvas-container');
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0xbfe3dd); // Heller französischer Sommerhimmel
        scene.fog = new THREE.FogExp2(0xbfe3dd, 0.006);

        const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight * 0.75);
        container.appendChild(renderer.domElement);

        scene.add(new THREE.AmbientLight(0xffffff, 0.6));
        const sun = new THREE.DirectionalLight(0xfffaed, 1.2);
        sun.position.set(100, 150, 50);
        scene.add(sun);

        let gameActive = true;

        window.addEventListener('click', () => {
            const alertBox = document.getElementById('click-alert');
            if(alertBox) alertBox.style.display = 'none';
        });

        // --- 2. TERRAIN & PASSSTRASSE ---
        const terrainGeo = new THREE.PlaneGeometry(3000, 3000);
        const terrainMat = new THREE.MeshStandardMaterial({ color: 0x22c55e, roughness: 1.0 }); // Alpengras
        const terrain = new THREE.Mesh(terrainGeo, terrainMat);
        terrain.rotation.x = -Math.PI / 2;
        scene.add(terrain);

        // Die Rennstrecke als mathematischer Spline-Pfad
        const points = [
            new THREE.Vector3(0, 0.05, 450),
            new THREE.Vector3(-120, 0.05, 300),
            new THREE.Vector3(140, 0.05, 120),
            new THREE.Vector3(-160, 0.05, -80),
            new THREE.Vector3(90, 0.05, -280),
            new THREE.Vector3(0, 0.05, -450)
        ];
        const curve = new THREE.CatmullRomCurve3(points);
        
        const roadGeo = new THREE.TubeGeometry(curve, 300, 24, 8, false);
        const roadMat = new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.8 }); // Asphalt
        const road = new THREE.Mesh(roadGeo, roadMat);
        road.scale.y = 0.001; 
        scene.add(road);

        // Ziellinie am Ende der Etappe (-450m Z-Koordinate)
        const finishLineGroup = new THREE.Group();
        const finishMesh = new THREE.Mesh(new THREE.BoxGeometry(48, 0.1, 4), new THREE.MeshStandardMaterial({ color: 0x111111 }));
        finishLineGroup.add(finishMesh);

        const stripeMesh = new THREE.Mesh(new THREE.BoxGeometry(48, 0.15, 1.5), new THREE.MeshBasicMaterial({ color: 0xffffff }));
        stripeMesh.position.y = 0.02;
        finishLineGroup.add(stripeMesh);
        finishLineGroup.position.copy(points[points.length - 1]);
        scene.add(finishLineGroup);

        // Prozedurale Deko (Bäume entlang der Strecke)
        const curvePoints = curve.getPoints(150);
        curvePoints.forEach((pt, idx) => {
            if(idx % 4 === 0) {
                const tree = new THREE.Group();
                const trunk = new THREE.Mesh(new THREE.CylinderGeometry(0.3, 0.5, 2), new THREE.MeshStandardMaterial({color: 0x5c4033}));
                trunk.position.y = 1;
                const leaves = new THREE.Mesh(new THREE.ConeGeometry(2.5, 6, 5), new THREE.MeshStandardMaterial({color: 0x065f46}));
                leaves.position.y = 4;
                tree.add(trunk, leaves);
                const side = idx % 2 === 0 ? 32 : -32;
                tree.position.set(pt.x + side, 0, pt.z);
                scene.add(tree);
            }
        });

        // --- 3. PRO RENNRÄDER GENERATOR ---
        function createUltraBike(color) {
            const bike = new THREE.Group();
            const frameMat = new THREE.MeshStandardMaterial({ color: color, roughness: 0.4 });
            
            const frame = new THREE.Mesh(new THREE.CylinderGeometry(0.09, 0.09, 2.4), frameMat);
            frame.rotation.z = Math.PI / 3;
            frame.position.y = 1.2;
            bike.add(frame);

            const wMat = new THREE.MeshStandardMaterial({ color: 0x111111, roughness: 0.9 });
            const wGeo = new THREE.TorusGeometry(0.8, 0.12, 6, 18);
            
            const fw = new THREE.Mesh(wGeo, wMat); fw.position.set(1.5, 0.8, 0); bike.add(fw);
            const bw = new THREE.Mesh(wGeo, wMat); bw.position.set(-1.5, 0.8, 0); bike.add(bw);

            return { mesh: bike, fw, bw };
        }

        const p1 = createUltraBike(0xef4444); p1.mesh.position.set(-5, 0, 440); scene.add(p1.mesh);
        const p2 = createUltraBike(0x3b82f6); p2.mesh.position.set(5, 0, 440); scene.add(p2.mesh);

        // --- 4. INPUTS & CONFIG ---
        const keys = {};
        window.addEventListener('keydown', (e) => { keys[e.key.toLowerCase()] = true; });
        window.addEventListener('keyup', (e) => { keys[e.key.toLowerCase()] = false; });

        const b1 = { speed: 0, angle: Math.PI, stamina: 100, onRoad: true, draft: false };
        const b2 = { speed: 0, angle: Math.PI, stamina: 100, onRoad: true, draft: false };

        // Abstands-Grip-Abfrage für die Straße
        function checkOnRoad(pos) {
            let minDist = 999;
            for(let i=0; i<=100; i+=2) {
                let testPt = curve.getPoint(i/100);
                let d = pos.distanceTo(testPt);
                if(d < minDist) minDist = d;
            }
            return minDist < 26; // Abstands-Grip-Radius
        }

        // --- 5. MAIN ENGINE LOOP ---
        function animate() {
            requestAnimationFrame(animate);
            if (!gameActive) return;

            // Grip checken
            b1.onRoad = checkOnRoad(p1.mesh.position);
            b2.onRoad = checkOnRoad(p2.mesh.position);

            const maxS1 = b1.onRoad ? (b1.draft ? 2.1 : 1.7) : 0.4; // Gras bremst extrem aus
            const maxS2 = b2.onRoad ? (b2.draft ? 2.1 : 1.7) : 0.4;

            // --- WINDSCHATTEN-BERECHNUMG (DRAFTING) ---
            const distBetweenBikes = p1.mesh.position.distanceTo(p2.mesh.position);
            b1.draft = false; b2.draft = false;
            document.getElementById('draft-ticker').innerText = "Freie Fahrt im Peloton";
            document.getElementById('draft-ticker').style.color = "#a1a1aa";

            if (distBetweenBikes < 18) {
                if (p1.mesh.position.z > p2.mesh.position.z) {
                    b1.draft = true;
                    document.getElementById('draft-ticker').innerText = "🔴 P1 nutzt den WINDSCHATTEN! 💨";
                    document.getElementById('draft-ticker').style.color = "#ef4444";
                } else if (p2.mesh.position.z > p1.mesh.position.z) {
                    b2.draft = true;
                    document.getElementById('draft-ticker').innerText = "🔵 P2 nutzt den WINDSCHATTEN! 💨";
                    document.getElementById('draft-ticker').style.color = "#3b82f6";
                }
            }

            // --- KOLLISIONS-PHYSIK (Rammen) ---
            if (distBetweenBikes < 3.2) {
                const pushDir = new THREE.Vector3().subVectors(p1.mesh.position, p2.mesh.position).normalize();
                p1.mesh.position.addScaledVector(pushDir, 0.4);
                p2.mesh.position.addScaledVector(pushDir, -0.4);
                b1.speed *= 0.7; b2.speed *= 0.7;
            }

            // --- SPIELER 1 (WASD) ---
            if (keys['w'] && b1.stamina > 5) { 
                b1.speed = Math.min(maxS1, b1.speed + 0.04); 
                b1.stamina = Math.max(0, b1.stamina - (b1.draft ? 0.05 : 0.16));
            } else {
                b1.stamina = Math.min(100, b1.stamina + (b1.draft ? 0.4 : 0.2));
            }
            if (keys['s']) b1.speed = Math.max(-0.3, b1.speed - 0.03);
            if (keys['a']) b1.angle += 0.038 * (b1.speed >= 0 ? 1 : -1);
            if (keys['d']) b1.angle -= 0.038 * (b1.speed >= 0 ? 1 : -1);

            // --- SPIELER 2 (Pfeiltasten) ---
            if (keys['arrowup'] && b2.stamina > 5) { 
                b2.speed = Math.min(maxS2, b2.speed + 0.04); 
                b2.stamina = Math.max(0, b2.stamina - (b2.draft ? 0.05 : 0.16));
            } else {
                b2.stamina = Math.min(100, b2.stamina + (b2.draft ? 0.4 : 0.2));
            }
            if (keys['arrowdown']) b2.speed = Math.max(-0.3, b2.speed - 0.03);
            if (keys['arrowleft']) b2.angle += 0.038 * (b2.speed >= 0 ? 1 : -1);
            if (keys['arrowright']) b2.angle -= 0.038 * (b2.speed >= 0 ? 1 : -1);

            // Reibungsdämpfung
            b1.speed *= 0.96; b2.speed *= 0.96;

            // Positions-Updates
            p1.mesh.position.x += Math.sin(b1.angle) * b1.speed; p1.mesh.position.z += Math.cos(b1.angle) * b1.speed;
            p1.mesh.rotation.y = b1.angle + Math.PI/2;
            p1.fw.rotation.z -= b1.speed * 0.9; p1.bw.rotation.z -= b1.speed * 0.9;

            p2.mesh.position.x += Math.sin(b2.angle) * b2.speed; p2.mesh.position.z += Math.cos(b2.angle) * b2.speed;
            p2.mesh.rotation.y = b2.angle + Math.PI/2;
            p2.fw.rotation.z -= b2.speed * 0.9; p2.bw.rotation.z -= b2.speed * 0.9;

            // HUD-Werte synchronisieren
            document.getElementById('sp1').innerText = Math.round(b1.speed * 36) + " km/h";
            document.getElementById('sp2').innerText = Math.round(b2.speed * 36) + " km/h";
            document.getElementById('st1').style.width = b1.stamina + "%";
            document.getElementById('st2').style.width = b2.stamina + "%";
            document.getElementById('surf1').innerText = b1.onRoad ? "🛣️" : "🌱 GRAS";
            document.getElementById('surf2').innerText = b2.onRoad ? "🛣️" : "🌱 GRAS";

            // --- ZIELEINLAUF CHECK ---
            if (p1.mesh.position.z <= -450) {
                gameActive = false;
                document.getElementById('winner-text').innerText = "SPIELER 1 (ROT) HOLET SICH DAS GELBE TRIKOT";
                document.getElementById('victory-screen').style.display = "block";
            } else if (p2.mesh.position.z <= -450) {
                gameActive = false;
                document.getElementById('winner-text').innerText = "SPIELER 2 (BLAU) HOLT SICH DAS GELBE TRIKOT";
                document.getElementById('victory-screen').style.display = "block";
            }

            // CHASE-CAMERA FOLLOW
            const targetCamX = (p1.mesh.position.x + p2.mesh.position.x) / 2;
            const targetCamZ = (p1.mesh.position.z + p2.mesh.position.z) / 2 + 32;
            
            camera.position.x = THREE.MathUtils.lerp(camera.position.x, targetCamX, 0.05);
            camera.position.z = THREE.MathUtils.lerp(camera.position.z, targetCamZ, 0.05);
            camera.position.y = 18;
            camera.lookAt(new THREE.Vector3(targetCamX, 1.5, targetCamZ - 32));

            renderer.render(scene, camera);
        }
        animate();

        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight; camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight * 0.75);
        });
    </script>
</body>
</html>
"""

st.components.v1.html(full_game_code, height=680, scrolling=False)

# --- 3. SIDEBAR MECHANICS ---
st.sidebar.markdown("""
### 🏁 Rennleiter-Handbuch:
* **Windschatten:** Bleib dicht hinter dem vorderen Rad, um Kraft zu sparen und an Höchstgeschwindigkeit zuzulegen!
* **Grip-Verlust:** Komm bloß nicht von der Strecke ab! Das Gras bremst dein Bike sofort ab.

*Tipp: Zum Neustarten nach einem Zielsprint einfach im Browser F5 drücken!*
""")
