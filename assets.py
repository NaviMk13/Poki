# assets.py - Prozedurale 3D-Generierungs-Funktionen für die WebGL-Engine
def get_asset_pipeline():
    return """
    // --- ADVANCED ASSET PIPELINE ---
    function createDetailedTree() {
        const tree = new THREE.Group();
        const trunkGeo = new THREE.CylinderGeometry(0.2, 0.4, 3, 8);
        const trunkMat = new THREE.MeshStandardMaterial({ color: 0x4a2f13, roughness: 0.9 });
        const trunk = new THREE.Mesh(trunkGeo, trunkMat);
        trunk.position.y = 1.5;
        trunk.castShadow = true;
        tree.add(trunk);

        // Mehrschichtige Tannenspitze
        for(let i = 0; i < 3; i++) {
            const leavesGeo = new THREE.ConeGeometry(2.2 - (i*0.5), 4 - (i*0.5), 6);
            const leavesMat = new THREE.MeshStandardMaterial({ 
                color: new THREE.Color(0x0f4d2a).multiplyScalar(1 - (i*0.15)), 
                roughness: 0.8 
            });
            const leaves = new THREE.Mesh(leavesGeo, leavesMat);
            leaves.position.y = 3.5 + (i * 1.8);
            leaves.castShadow = true;
            tree.add(leaves);
        }
        return tree;
    }

    function createSpectator(shirtColorHex) {
        const person = new THREE.Group();
        const bodyMat = new THREE.MeshStandardMaterial({ color: shirtColorHex });
        const skinMat = new THREE.MeshStandardMaterial({ color: 0xffdbac });

        const legs = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.2, 1.5), new THREE.MeshStandardMaterial({color: 0x111111}));
        legs.position.y = 0.75;
        
        const torso = new THREE.Mesh(new THREE.BoxGeometry(0.8, 1.2, 0.4), bodyMat);
        torso.position.y = 2.1;
        
        const head = new THREE.Mesh(new THREE.SphereGeometry(0.35, 8, 8), skinMat);
        head.position.y = 2.9;

        person.add(legs, torso, head);
        person.castShadow = true;
        return person;
    }

    function createSpectatorBarrier() {
        const barrier = new THREE.Group();
        const mat = new THREE.MeshStandardMaterial({ color: 0xdddddd, metalness: 0.5 });
        const postGeo = new THREE.CylinderGeometry(0.05, 0.05, 1.5);
        const barGeo = new THREE.CylinderGeometry(0.04, 0.04, 4);
        barGeo.rotateZ(Math.PI / 2);

        const p1 = new THREE.Mesh(postGeo, mat); p1.position.set(-2, 0.75, 0);
        const p2 = new THREE.Mesh(postGeo, mat); p2.position.set(2, 0.75, 0);
        const bar = new THREE.Mesh(barGeo, mat); bar.position.set(0, 1.3, 0);

        barrier.add(p1, p2, bar);
        return barrier;
    }
    """
