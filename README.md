# FPS Asset Kit

A curated starter pack of **CC0/public-domain** game assets for building first-person shooter environments. Everything here is **royalty-free, no attribution required** — use it in commercial projects, remix it, redistribute it.

**Contents:** ~1.1GB of PBR textures, 3D weapons, sound effects, and HDRIs.

---

## 📦 Assets

### Textures — ambientCG (24 PBR sets)

2K resolution JPG, PBR-ready. Each set includes Color, Normal (DX/GL), Roughness, Ambient Occlusion, and Displacement maps.

| Category | Assets |
|----------|--------|
| Asphalt  | 3 surfaces |
| Bricks   | 3 surfaces |
| Concrete | 3 surfaces |
| Ground   | 3 surfaces |
| Metal    | 3 surfaces |
| Plaster  | 3 surfaces |
| Rock     | 3 surfaces |
| Wood     | 3 surfaces |

**Source:** [ambientCG](https://ambientcg.com) — CC0 licensed.

### Weapons — Flat Guns (20 models)

20 stylized FPS weapon models in **GLB, FBX (rigged), and OBJ** formats.

| West Pack (10) | East Pack (10) |
|----------------|----------------|
| Assault Rifle  | Assault Rifle  |
| Battle Rifle   | Battle Rifle   |
| Compact Pistol | Compact Pistol |
| Full Pistol    | Full Pistol    |
| SMG Compact    | SMG Compact    |
| SMG Full       | SMG Full       |
| Sniper Rifle   | Sniper Rifle   |
| Shotgun Auto   | Shotgun Auto   |
| Shotgun Pump   | Shotgun Pump   |
| BONUS          | BONUS          |

**Source:** [OpenGameArt - Flat Guns West](https://opengameart.org/content/cc0-flat-guns-west) / [Flat Guns East](https://opengameart.org/content/cc0-flat-guns-east) — CC0 licensed.

### Sound Effects

#### Gunshots — Free Firearm Sound Library (24 weapons)

High-quality field recordings from real firearms. Each weapon folder contains multiple takes.

| Category | Weapons |
|----------|---------|
| Pistols  | 1911, 1917, Bersa, Ruger Mark III, Ruger Single Six, Smith & Wesson 642, Walther PPQ |
| Rifles   | AK-47, AR-15, Arisaka, Marlin 336, Model 1894, Mosin Nagant, Savage 10 |
| SMG      | Carl Gustav M45, PPSh |
| Shotguns | Model 12, Mossberg, Nova |
| Other    | Tikka |

**Source:** [The Free Firearm Sound Library](https://opengameart.org/content/the-free-firearm-sound-library) — CC0 licensed.

#### Footsteps — Fantozzi's Footsteps (12 sounds)

Clean, sliced footstep recordings for game use. Available in FLAC format.

- **Sand:** 6 step sounds (3 left, 3 right)
- **Stone:** 6 step sounds (3 left, 3 right)

**Source:** [OpenGameArt - Fantozzi's Footsteps](https://opengameart.org/content/fantozzis-footsteps-grasssand-stone) — CC0 licensed.

### HDRIs — ambientCG (4 environments)

2K resolution HDR environment maps for image-based lighting.

- Rural Landscape (outdoor day)
- Suburb Night (outdoor night)
- Sunset Valley (golden hour)
- Studio Neutral (interior/studio)

**Source:** [ambientCG](https://ambientcg.com) — CC0 licensed.

---

## 📁 Directory Structure

```
fps-asset-kit/
├── README.md
├── textures/        # 24 PBR texture sets (subdirectories)
├── weapons/
│   ├── flat_guns_west/   # 10 weapons — GLB / FBX / OBJ
│   └── flat_guns_east/   # 10 weapons — GLB / FBX / OBJ
├── sfx/
│   ├── gunshots/         # 24 weapon types — WAV
│   └── footsteps/        # 12 footstep sounds — FLAC
├── hdris/            # 4 HDR environment maps
├── download_textures.py
└── download_hdris.py
```

---

## 🔧 Usage

### In a game engine (Unity, Unreal, Godot)

1. **Textures:** Import the PBR maps from `textures/` using the standard metallic/roughness workflow. Each folder contains color + normal + roughness + AO + displacement.
2. **Weapons:** Import the FBX (rigged) or GLB models from `weapons/`. Both packs share the same rig structure.
3. **SFX:** Import the WAV/FLAC files from `sfx/`. Tag them with the appropriate weapon type.
4. **HDRIs:** Import the HDR images from `hdris/` for skybox/environment lighting.

### In code (Three.js, Babylon, raw WebGL)

```js
// Example: Load a GLB weapon model
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
const loader = new GLTFLoader();
loader.load('weapons/flat_guns_west/GLB/Rifle_Assault_West.glb', (gltf) => {
  scene.add(gltf.scene);
});
```

---

## 📜 License Summary

All assets in this kit are **CC0 (No Rights Reserved)** or equivalent public-domain dedication. You can:

- ✅ Use in commercial games and products
- ✅ Modify and remix
- ✅ Redistribute (including on GitHub)
- ✅ Sub-license
- ❌ No attribution required (but appreciated!)

| Asset | License | Source |
|-------|---------|--------|
| Textures | CC0 | ambientCG.com |
| Weapons | CC0 | OpenGameArt.org |
| Gun SFX | CC0 | The Free Firearm Sound Library |
| Footsteps | CC0 | Fantozzi / OpenGameArt.org |
| HDRIs | CC0 | ambientCG.com |

---

## 🛠️ Regenerating Downloads

The `download_textures.py` and `download_hdris.py` scripts in the root directory will re-download all assets from ambientCG.

```bash
python3 download_textures.py   # Re-download 24 PBR texture sets
python3 download_hdris.py      # Re-download 4 HDR environment maps
```

---

---

## 🤖 For AI Coding Agents

This section is a **system prompt** for LLM coding agents (Claude, ChatGPT, Gemini, Copilot, etc.) tasked with building a playable FPS prototype from this repository.

### Your Context

You are building a first-person shooter game using the assets in this repo. All assets are CC0 — no licensing concerns. The working directory is the repo root (`fps-asset-kit/`). You have ~1.1 GB of ready-to-use art.

### Recommended Stack

- **Runtime:** Node.js + Vite (fast dev server, no build config needed)
- **Engine:** Three.js (via npm: `three`, `@three-ts/gltf-loader`)
- **Physics:** `cannon-es` (lightweight, pairs with Three.js)
- **Audio:** Web Audio API (via Three.js `AudioListener` / `PositionalAudio`)
- **Input:** Pointer Lock API for mouse look + WASD/keyboard events

### Asset Loading Patterns

```js
// --- TEXTURES (PBR metallic-roughness workflow) ---
// Path: textures/<MaterialName>/<MaterialName>_2K-JPG_*.jpg
import { TextureLoader } from 'three';
const loader = new TextureLoader();
const colorMap = loader.load('textures/Concrete048/Concrete048_2K-JPG_Color.jpg');
const normalMap = loader.load('textures/Concrete048/Concrete048_2K-JPG_NormalGL.jpg');
const roughnessMap = loader.load('textures/Concrete048/Concrete048_2K-JPG_Roughness.jpg');
const aoMap = loader.load('textures/Concrete048/Concrete048_2K-JPG_AmbientOcclusion.jpg');

// Apply to material
const material = new THREE.MeshStandardMaterial({
  map: colorMap,
  normalMap: normalMap,
  roughnessMap: roughnessMap,
  aoMap: aoMap,
});
```

```js
// --- WEAPONS (GLB format — rigged FBX also available) ---
// Path: weapons/flat_guns_<west|east>/GLB/<WeaponType>_<West|East>.glb
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
const gltfLoader = new GLTFLoader();
gltfLoader.load('weapons/flat_guns_west/GLB/Rifle_Assault_West.glb', (gltf) => {
  const weapon = gltf.scene;
  weapon.position.set(0.3, -0.25, -0.5); // First-person camera-relative
  camera.add(weapon);                     // Attach to camera
});
```

```js
// --- SFX (WAV / FLAC) ---
// Path: sfx/<category>/<folder>/<file>.wav
import { AudioListener, Audio, AudioLoader } from 'three';
const listener = new AudioListener();
camera.add(listener);
const audioLoader = new AudioLoader();
audioLoader.load('sfx/gunshots/game_gunshot.wav', (buffer) => {
  const sound = new Audio(listener);
  sound.setBuffer(buffer);
  sound.play();
});
```

```js
// --- HDRIs (environment lighting) ---
// Path: hdris/<name>.hdr
import { RGBELoader } from 'three/examples/jsm/loaders/RGBELoader.js';
const rgbeLoader = new RGBELoader();
rgbeLoader.load('hdris/rural_landscape_2k.hdr', (texture) => {
  texture.mapping = THREE.EquirectangularReflectionMapping;
  scene.environment = texture;
  scene.background = texture;
});
```

### Game Architecture (Suggested)

```
src/
├── main.js            # Entry: scene, camera, renderer, game loop
├── player.js          # First-person controller (pointer lock + WASD)
├── world.js           # Level geometry from textures/materials
├── weapons.js         # Weapon switching, firing, animation
├── audio.js           # SFX manager, positional audio
├── hud.js             # Crosshair, ammo, health (DOM overlay)
└── physics.js         # Cannon-es world, collision detection
```

### Iteration Tips for AI

1. **Start minimal:** Get a walking cube in a textured box room before adding weapons.
2. **One weapon first:** Implement `Rifle_Assault_West.glb` end-to-end (load → attach → fire animation → sound) before adding others.
3. **HDRIs for lighting:** Use the HDR environment maps for realistic reflections/shadows without building a lightmap pipeline.
4. **FBX rigs available:** The FBX files in each weapon folder contain a bone rig if you need animated hands/arms. GLB format is simpler for static weapon models.
5. **Test audio early:** Weapon SFX files are field recordings — test at different gain levels and add reverb for distance.

### Constraints

- No `git-lfs` available — all assets are stored as regular blobs.
- No external API calls or network requests for assets (everything is local).
- Keep the first build under 500 lines of JavaScript for prototyping speed.

---

*Curated by Hermes Agent. Built from CC0 sources so you can focus on making games, not clearing rights.*
