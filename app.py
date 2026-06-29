import streamlit as st

# --- 1. STREAMLIT ULTRABOX DESIGN ---
st.set_page_config(page_title="Alpen Grand Prix 3D - NextGen", layout="wide", page_icon="🏎️")

st.markdown("""
    <style>
    .stApp { background-color: #030712; color: #ffffff; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    iframe { border: 4px solid #facc15 !important; border-radius: 24px; box-shadow: 0 25px 60px rgba(250, 204, 21, 0.25); }
    h1 { font-family: 'Impact', sans-serif; color: #facc15 !important; text-shadow: 4px 4px 0px #000; text-align: center; text-transform: uppercase; margin: 0; letter-spacing: 2px; }
    .hud-sub { text-align: center; color: #94a3b8; font-weight: 500; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

st.write("<h1>🏎️ ALPEN GRAND PRIX: NEXT-GEN GRAPHICS 🏎️</h1>", unsafe_allow_html=True)
st.write("<div class='hud-sub'>Erlebe die Königsetappe in prozeduralem 3D mit Realtime-Shadows, Partikeleffekten & Schräglagen-Physik</div>", unsafe_allow_html=True)

# --- 2. NEXT-GEN 3D ENGINE FRAMEWORK ---
engine_code = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body { margin: 0; overflow: hidden; background-color: #030712; font-family: 'Segoe UI', sans-serif; }
        #canvas-container { width: 100vw; height: 74vh; }
        #hud-overlay {
            position: absolute; top: 20px; left: 20px; pointer-events: none; z-index: 10;
            color: #ffffff; background: linear-gradient(135deg, rgba(17,24,39,0.95), rgba(31,41,55,0.85));
            padding: 22px; border-radius: 18px; border: 3px solid #facc15;
            width: 280px; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.7);
        }
        .crypto-card { background: rgba(255,255,255,0.05); padding: 10px; border-radius: 8px; margin-top: 12px; border: 1px solid rgba(255,255,255,0.1); }
        .item-display {
            background: rgba(250, 204, 21, 0.1); border: 2px dashed #facc15; 
            height: 45px; border-radius: 8px; display: flex; align-items: center; 
            justify-content: center; font-weight: bold; font-size: 16px; color: #facc15; margin-top: 8px;
            text-transform: uppercase; letter-spacing: 1px;
        }
        #victory-screen {
            display: none; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
            background: linear-gradient(135deg, #facc15, #eab308); color: #000; padding: 50px 70px; border-radius: 28px;
            font-size: 40px; font-weight: bold; text-align: center; border: 6px solid #fff;
            box-shadow: 0 0 100px rgba(250,204,21,0.6); z-index: 100; font-family: 'Impact', sans-serif;
        }
        #interaction-alert {
            position: absolute; bottom: 40px; left: 50%; transform: translateX(-50%);
            background: #facc15; color: #000; padding: 14px 40px; font-weight: bold;
            border-radius: 40px; animation: pulse-glow 1.5s infinite; font-size: 16px; z-index: 20; box-shadow: 0 10px 25px rgba(250,204,21,0.4);
        }
        @keyframes pulse-glow { 0% { opacity: 0.6; transform: translateX(-50%) scale(0.98); } 50% { opacity: 1; transform: translateX(-50%) scale(1.02); } 100% { opacity: 0.6; transform: translateX(-50%) scale(0.98); } }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>

    <div id="hud-overlay">
        <h3 style="margin: 0 0 5px 0; color: #facc15; text-transform:uppercase; letter-spacing:1px; font-size:18px;">🏁 CYBER CUP GP</h3>
        <div style="font-size: 12px; color: #9ca3af; margin-bottom: 12px;">Next-Gen Rendering Engine</div>
        
        <div style="font-size: 15px; margin: 4px 0;">Tacho: <span id="speed-indicator" style="color:#facc15; font-weight:bold; font-family:monospace; font-size:18px;">0</span> <span style="font-size:12px; color:#facc15;">km/h</span></div>
        <div style="font-size: 13px; color: #d1d5db;">Abstand zur KI: <span id="gap-indicator" style="font-family:monospace; font-weight:bold;">0m</span></div>
        
        <div class="crypto-card">
            <div style="font-size:11px; text-transform:uppercase; color:#9ca3af; font-weight:bold; letter-spacing:0.5px;">📦 AKTIVES ITEM:</div>
            <div id="item-slot" class="item-display">Keins</div>
        </div>
    </div>

    <div id="interaction-alert">🎮 INS SPIELFELD KLICKEN ZUM SPRINTEN</div>
    <div id="victory-screen">🏆 <span id="winner-banner">SPIELER</span> GEWINNT! 💛</div>
    <div id="canvas-container"></div>

    <script>
        // --- 1. ENGINE & ADVANCED SHADOW SETUP ---
        const container = document.getElementById('canvas-container');
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0xfdba74); // Atmosphärischer, warmer Sunset-Himmel
        scene.fog = new THREE.FogExp2(0xfdba74, 0.004);

        const camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.1, 1200);
        const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
        renderer.setSize(window.innerWidth, window.innerHeight * 0.74);
        renderer.shadowMap.enabled = true;
        renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        container.appendChild(renderer.domElement);

        // Ausgeklügelte Licht-Architektur für lebhafte Plastizität
        scene.add(new THREE.AmbientLight(0xffffff, 0.35));
        
        const directionalLight = new THREE.DirectionalLight(0xfff7ed, 1.5);
        directionalLight.position.set(120, 140, 60);
        directionalLight.castShadow = true;
        directionalLight.shadow.mapSize.width = 4096; // Gestochen scharfe Schattenkanten
        directionalLight.shadow.mapSize.height = 4096;
        directionalLight.shadow.camera.near = 0.5;
        directionalLight.shadow.camera.far = 600;
        const shadowZone = 200;
        directionalLight.shadow.camera.left = -shadowZone; directionalLight.shadow.camera.right = shadowZone;
        directionalLight.shadow.camera.top = shadowZone; directionalLight.shadow.camera.bottom = -shadowZone;
        directionalLight.shadow.bias = -0.0005;
        scene.add(directionalLight);

        let gameActive = true;

        window.addEventListener('click', () => {
            document.getElementById('interaction-alert').style.display = 'none';
        });

        // --- 2. NEXT-GEN MAP GENERATOR (LOW POLY ALPS) ---
        const terrainGeo = new THREE.PlaneGeometry(3500, 3500, 20, 20);
        const terrainMat = new THREE.MeshStandardMaterial({ color: 0x14532d, roughness: 0.95, metalness: 0.05 }); // Edles Waldgrün
        const terrain = new THREE.Mesh(terrainGeo, terrainMat);
        terrain.rotation.x = -Math.PI / 2;
        terrain.receiveShadow = true;
        scene.add(terrain);

        // Massiver, prozeduraler Gebirgspass aus zerklüfteten Low-Poly-Strukturen
        for(let i=0; i<35; i++) {
            const mGeo = new THREE.ConeGeometry(50 + Math.random()*70, 70 + Math.random()*90, 5); // 5 Segmente für kantigen Low-Poly Look
            const mMat = new THREE.MeshStandardMaterial({ color: 0x374151, roughness: 0.9, flatShading: true });
            const mountain = new THREE.Mesh(mGeo, mMat);
            const angle = Math.random() * Math.PI * 2;
            const distance = 550 + Math.random() * 300;
            mountain.position.set(Math.cos(angle)*distance, 25, Math.sin(angle)*distance);
            mountain.castShadow = true;
            mountain.receiveShadow = true;
            scene.add(mountain);
        }

        // Mathematischer Kurven-Kurs (Königsetappe)
        const points = [
            new THREE.Vector3(0, 0.1, 550),
            new THREE.Vector3(-150, 0.1, 350),
            new THREE.Vector3(180, 0.1, 120),
            new THREE.Vector3(-190, 0.1, -120),
            new THREE.Vector3(120, 0.1, -360),
            new THREE.Vector3(0, 0.1, -580)
        ];
        const curve = new THREE.CatmullRomCurve3(points);
        
        const roadGeo = new THREE.TubeGeometry(curve, 350, 24, 16, false);
        const roadMat = new THREE.MeshStandardMaterial({ color: 0x1f2937, roughness: 0.5, metalness: 0.2 }); // Anthrazitfarbener Belag
        const road = new THREE.Mesh(roadGeo, roadMat);
        road.scale.y = 0.001;
        road.receiveShadow = true;
        scene.add(road);

        // High-Quality Ziellinie am Berg-Scheitelpunkt
        const finishGroup = new THREE.Group();
        const fMesh = new THREE.Mesh(new THREE.BoxGeometry(50, 0.1, 5), new THREE.MeshStandardMaterial({ color: 0x111827 }));
        fMesh.receiveShadow = true;
        finishGroup.add(fMesh);
        
        const whiteStrip = new THREE.Mesh(new THREE.BoxGeometry(50, 0.16, 1.8), new THREE.MeshBasicMaterial({ color: 0xffffff }));
        whiteStrip.position.y = 0.03;
        finishGroup.add(whiteStrip);
        finishGroup.position.copy(points[points.length - 1]);
        scene.add(finishGroup);

        // Reiche Detail-Deko: Mehrschichtige Tannen & Barrieren am Streckenrand
        const trackPoints = curve.getPoints(180);
        trackPoints.forEach((pt, idx) => {
            if(idx % 3 === 0 && idx > 5 && idx < 175) {
                // Tannen
                const tree = new THREE.Group();
                const trunk = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.4, 2.5), new THREE.MeshStandardMaterial({color: 0x451a03}));
                trunk.position.y = 1.25; trunk.castShadow = true; tree.add(trunk);
                
                for(let layer=0; layer<3; layer++) {
                    const leaves = new THREE.Mesh(new THREE.ConeGeometry(2.4 - (layer*0.5), 3.5, 5), new THREE.MeshStandardMaterial({color: 0x064e3b, flatShading:true}));
                    leaves.position.y = 3.0 + (layer*1.5); leaves.castShadow = true; tree.add(leaves);
                }
                const sideDir = idx % 2 === 0 ? 34 : -34;
                tree.position.set(pt.x + sideDir + (Math.random()*4), 0, pt.z);
                scene.add(tree);

                // Rot-Weiß karierte Renn-Barrieren direkt an der Strecke
                if (idx % 6 === 0) {
                    const barrier = new THREE.Mesh(new THREE.BoxGeometry(6, 1.8, 0.4), new THREE.MeshStandardMaterial({ color: idx % 12 === 0 ? 0xef4444 : 0xffffff, roughness: 0.4 }));
                    barrier.position.set(pt.x + (sideDir*0.8), 0.9, pt.z);
                    barrier.lookAt(pt);
                    barrier.rotateY(Math.PI/2);
                    barrier.castShadow = true;
                    scene.add(barrier);
                }
            }
        });

        // --- 3. HIGH-TECH ITEM BOXEN (Kristall-Geometrie) ---
        const itemBoxes = [];
        const crystalGeo = new THREE.OctahedronGeometry(2, 0); // Stylischer Diamanten-Look
        const crystalMat = new THREE.MeshStandardMaterial({ color: 0xfacc15, metalness: 0.9, roughness: 0.1, emissive: 0xeab308, emissiveIntensity: 0.5 });

        for (let i = 1; i < points.length - 1; i++) {
            const box = new THREE.Mesh(crystalGeo, crystalMat);
            box.position.copy(points[i]);
            box.position.y = 3.0;
            box.castShadow = true;
            scene.add(box);
            itemBoxes.push(box);
        }

        // --- 4. ENGINE PARTIKEL-SYSTEM (BOOST FUNKEN) ---
        const particleCount = 25;
        const particleGeo = new THREE.SphereGeometry(0.15, 4, 4);
        const particleMat = new THREE.MeshBasicMaterial({ color: 0xfacc15 });
        const particles = [];

        for(let i=0; i<particleCount; i++) {
            const p = new THREE.Mesh(particleGeo, particleMat);
            p.position.set(0, -100, 0); // Verstecken
            scene.add(p);
            particles.push({ mesh: p, age: 0, maxAge: 0, vx: 0, vy: 0, vz: 0 });
        }

        function triggerSparks(pos, angle) {
            particles.forEach(p => {
                if(p.age >= p.maxAge) {
                    p.mesh.position.copy(pos);
                    p.mesh.position.y = 0.6; // Auf Reifenhöhe ausstoßen
                    p.age = 0;
                    p.maxAge = 15 + Math.random()*20;
                    p.vx = (Math.random() - 0.5) * 0.4 - Math.sin(angle)*0.5;
                    p.vy = Math.random() * 0.3;
                    p.vz = (Math.random() - 0.5) * 0.4 - Math.cos(angle)*0.5;
                }
            });
        }

        // --- 5. HIGH-POLY BIKE ENGINE (Mit realer Rahmen-Geometrie) ---
        function createGrandPrixBike(frameColor) {
            const model = new THREE.Group();
            const frameMat = new THREE.MeshStandardMaterial({ color: frameColor, metalness: 0.8, roughness: 0.1 });
            const componentsMat = new THREE.MeshStandardMaterial({ color: 0x1f2937, metalness: 0.9, roughness: 0.3 });

            // Hauptrahmen (Dreiecks-Verbund)
            const t1 = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 2.2), frameMat);
            t1.rotation.z = Math.PI/4; t1.position.set(0.2, 1.4, 0); t1.castShadow = true; model.add(t1);
            
            const t2 = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 2.0), frameMat);
            t2.rotation.z = -Math.PI/3; t2.position.set(-0.5, 1.4, 0); t2.castShadow = true; model.add(t2);

            // Bullhorn-Rennlenker
            const handlebars = new THREE.Mesh(new THREE.CylinderGeometry(0.07, 0.07, 1.8), componentsMat);
            handlebars.position.set(1.1, 2.5, 0); handlebars.rotation.x = Math.PI/2; handlebars.castShadow = true; model.add(handlebars);

            // Sport-Laufräder mit Alufelge & fettem Reifenbett
            const wheelGeo = new THREE.TorusGeometry(0.9, 0.18, 10, 36);
            const fw = new THREE.Mesh(wheelGeo, componentsMat); fw.position.set(1.5, 0.9, 0); fw.castShadow = true;
            const bw = new THREE.Mesh(wheelGeo, componentsMat); bw.position.set(-1.5, 0.9, 0); bw.castShadow = true;
            model.add(fw, bw);

            // Container für Schräglagen-Kompensation (Pivot)
            const pivot = new THREE.Group();
            pivot.add(model);
            scene.add(pivot);

            return { pivot, model, fw, bw };
        }

        const player = createGrandPrixBike(0xef4444); // Spieler: Racing Red
        player.pivot.position.set(-5, 0, 530);

        const ai = createGrandPrixBike(0x2563eb); // KI-Gegner: Cyber Blue
        ai.pivot.position.set(5, 0, 530);

        // --- 6. PHYSICS & ALGORITHMIC AI STATE ---
        const keys = {};
        window.addEventListener('keydown', (e) => { keys[e.key.toLowerCase()] = true; });
        window.addEventListener('keyup', (e) => { keys[e.key.toLowerCase()] = false; });

        const pState = { speed: 0, angle: Math.PI, item: null, boostFrames: 0, turnLean: 0 };
        let aiProgress = 0;
        let lastPlayerAngle = Math.PI;

        // --- 7. REALTIME GRAPHICS LOOP ---
        function animate() {
            requestAnimationFrame(animate);
            if (!gameActive) return;

            // --- STRASSEN-GRIP DETECTION ---
            let minDistToTrack = 999;
            for(let i=0; i<=100; i+=3) {
                let d = player.pivot.position.distanceTo(curve.getPoint(i/100));
                if(d < minDistToTrack) minDistToTrack = d;
            }
            
            let maxAvailableSpeed = pState.boostFrames > 0 ? 3.3 : 2.0;
            if (minDistToTrack > 25) maxAvailableSpeed = 0.5; // Brutaler Offroad-Widerstand im Gras

            // --- INPUT HANDLING ---
            if (keys['w']) pState.speed = Math.min(maxAvailableSpeed, pState.speed + 0.05);
            if (keys['s']) pState.speed = Math.max(-0.4, pState.speed - 0.05);
            
            // Smarte Kurvenschräge (Leaning) berechnen anhand des Lenkeinschlag-Deltas
            let turnVelocity = 0;
            if (keys['a']) { pState.angle += 0.038 * (pState.speed >= 0 ? 1 : -1); turnVelocity = 0.08; }
            if (keys['d']) { pState.angle -= 0.038 * (pState.speed >= 0 ? 1 : -1); turnVelocity = -0.08; }

            pState.speed *= 0.965; // Reibungskoeffizient

            // Kurvenschräglage dämpfen und zuweisen (Lean-Angle)
            pState.turnLean = THREE.MathUtils.lerp(pState.turnLean, turnVelocity * Math.min(1, pState.speed), 0.1);
            player.model.rotation.z = pState.turnLean * 6; // Physikalische Rahmenneigung

            // Physik-Translation anwenden
            player.pivot.position.x += Math.sin(pState.angle) * pState.speed;
            player.pivot.position.z += Math.cos(pState.angle) * pState.speed;
            player.pivot.rotation.y = pState.angle + Math.PI/2;
            
            // Rotierende Laufräder
            player.fw.rotation.z -= pState.speed * 0.9;
            player.bw.rotation.z -= pState.speed * 0.9;

            // --- PARTIKEL REFRESH & UPDATE ---
            if (pState.boostFrames > 0) {
                pState.boostFrames--;
                triggerSparks(player.pivot.position, pState.angle);
                if (pState.boostFrames === 0) document.getElementById('item-slot').innerText = "Keins";
            }

            particles.forEach(p => {
                if(p.age < p.maxAge) {
                    p.age++;
                    p.mesh.position.x += p.vx;
                    p.mesh.position.y += p.vy;
                    p.mesh.position.z += p.vz;
                    p.mesh.scale.setScalar(1 - (p.age / p.maxAge)); // Schrumpfen
                } else {
                    p.mesh.position.y = -100;
                }
            });

            // --- PROZEDURALE CYBER-KI ---
            const oldAIPos = ai.pivot.position.clone();
            aiProgress += 0.0017; // Konstantes Master-Renntempo der KI
            if (aiProgress > 1) aiProgress = 1;
            
            const aiTarget = curve.getPointAt(aiProgress);
            ai.pivot.position.lerp(aiTarget, 0.1);
            
            // KI Blickrichtung und automatische Kurvenschräglage berechnen
            const aiFutureTarget = curve.getPointAt(Math.min(1, aiProgress + 0.015));
            ai.pivot.lookAt(aiFutureTarget);
            ai.pivot.rotateY(Math.PI / 2);
            
            const aiHeadingDelta = ai.pivot.position.x - oldAIPos.x;
            ai.model.rotation.z = THREE.MathUtils.lerp(ai.model.rotation.z, -aiHeadingDelta * 0.5, 0.1);
            ai.fw.rotation.z -= 1.4; ai.bw.rotation.z -= 1.4;

            // --- CRYSTAL ITEM BOX COLLISION ---
            itemBoxes.forEach((box) => {
                box.rotation.y += 0.03;
                box.rotation.z += 0.015;
                
                if (player.pivot.position.distanceTo(box.position) < 4.5 && !pState.item && pState.boostFrames === 0) {
                    pState.item = "🚀 NITRO-PILZ";
                    document.getElementById('item-slot').innerText = "🚀 NITRO-PILZ";
                    
                    // Automatischer Raketenstart nach exakt 0.4 Sekunden
                    setTimeout(() => {
                        if (pState.item) {
                            pState.boostFrames = 100; // 100 Ticks purer Feuer-Schub
                            pState.speed = 3.3;
                            pState.item = null;
                            document.getElementById('item-slot').innerText = "🔥 SPRINT-BOOST 🔥";
                        }
                    }, 400);

                    box.position.y = -200; // Ausblenden
                    setTimeout(() => { box.position.y = 3.0; }, 6000); // Regenerieren nach 6s
                }
            });

            // --- HUD DATA LINK ---
            document.getElementById('speed-indicator').innerText = Math.round(pState.speed * 34);
            const absoluteGap = Math.round(player.pivot.position.distanceTo(ai.pivot.position));
            document.getElementById('gap-indicator').innerText = absoluteGap + "m";

            // --- NEXT-GEN ACTION CHASE CAMERA FOCUS ---
            // Schmeißt eine seidenweiche Verfolgung direkt hinter deine Achse
            const cameraDistance = 24;
            const targetCamX = player.pivot.position.x - Math.sin(pState.angle) * cameraDistance;
            const targetCamZ = player.pivot.position.z - Math.cos(pState.angle) * cameraDistance;
            const targetCamY = 7.5; // Epischer, flacher Blickwinkel direkt auf den Asphalt

            camera.position.x = THREE.MathUtils.lerp(camera.position.x, targetCamX, 0.07);
            camera.position.z = THREE.MathUtils.lerp(camera.position.z, targetCamZ, 0.07);
            camera.position.y = THREE.MathUtils.lerp(camera.position.y, targetCamY, 0.07);
            camera.lookAt(new THREE.Vector3(player.pivot.position.x, 2.5, player.pivot.position.z));

            // --- WINNER DETERMINATION ---
            if (player.pivot.position.z <= -580) {
                gameActive = false;
                document.getElementById('winner-banner').innerText = "DU (SPIELER 1)";
                document.getElementById('victory-screen').style.display = "block";
            } else if (ai.pivot.position.z <= -580) {
                gameActive = false;
                document.getElementById('winner-banner').innerText = "DIE CYBER-KI";
                document.getElementById('victory-screen').style.display = "block";
            }

            renderer.render(scene, camera);
        }
        animate();

        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight; camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight * 0.74);
        });
    </script>
</body>
</html>
"""

st.components.v1.html(engine_code, height=670, scrolling=False)

# --- 3. CONTROLLER GUIDE ---
st.sidebar.markdown("""
### 🛠️ Profi-Setup geladen:
* **Physik-Schräglage:** Wenn du scharf nach links (`A`) oder rechts (`D`) steuerst, legt sich das Rennrad dynamisch in die Kurve. Je schneller du bist, desto spektakulärer wirkt das Kurven-Handling!
* **Item-Kristalle 💎:** Die schwebenden gelben Kristalle geben dir nach dem Einsammeln sofort ein automatisches Nitro-Zündungs-Paket mit Abgasfunken.
* **Gegner-Verhalten:** Die KI passt sich mathematisch glatt an die Kurvenradien an. Nutze den Nitro-Schub weise, um im Schlusssprint vorbeizuziehen!

*Tipp: Browser mit `F5` neuladen, um eine neue Runde zu starten.*
""")
