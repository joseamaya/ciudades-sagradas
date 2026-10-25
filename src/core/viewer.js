import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

const TIME_PRESETS = {
  morning: {
    offset: [120, 70, -100],
    sun: 0xfff0dc,
    sunIntensity: 4.2,
    hemiSky: 0xcfe4f2,
    hemiGround: 0x8a7550,
    hemiIntensity: 0.22,
    fill: 0.12,
    skyTop: 0x2f5a86,
    skyHorizon: 0x6d90b0,
    skyGround: 0xb08a58,
    fog: 0xb9c5c9,
    exposure: 0.78,
  },
  noon: {
    offset: [50, 125, 10],
    sun: 0xfff4e0,
    sunIntensity: 4.0,
    hemiSky: 0xdfeeff,
    hemiGround: 0x7a6748,
    hemiIntensity: 0.2,
    fill: 0.12,
    skyTop: 0x2c6ba8,
    skyHorizon: 0x80a8c8,
    skyGround: 0xb89660,
    fog: 0xc4d2da,
    exposure: 0.72,
  },
  dusk: {
    offset: [-110, 40, 20],
    sun: 0xff9a5a,
    sunIntensity: 2.8,
    hemiSky: 0xf0b48b,
    hemiGround: 0x4a3624,
    hemiIntensity: 0.22,
    fill: 0.1,
    skyTop: 0x33365f,
    skyHorizon: 0xd98e66,
    skyGround: 0x6a4630,
    fog: 0xc98f6a,
    exposure: 0.7,
  },
  night: {
    offset: [25, 90, -65],
    sun: 0x8fb0ff,
    sunIntensity: 0.45,
    hemiSky: 0x2a3a5a,
    hemiGround: 0x1a1410,
    hemiIntensity: 0.14,
    fill: 0.04,
    skyTop: 0x080e1a,
    skyHorizon: 0x18243a,
    skyGround: 0x0d0c0a,
    fog: 0x101827,
    exposure: 0.55,
  },
};

function materialKey(material) {
  return (material?.name || '').split('.')[0];
}

function makeSkyTexture(topHex, horizonHex, groundHex) {
  const canvas = document.createElement('canvas');
  canvas.width = 1024;
  canvas.height = 512;
  const context = canvas.getContext('2d');
  const gradient = context.createLinearGradient(0, 0, 0, canvas.height);
  gradient.addColorStop(0, new THREE.Color(topHex).getStyle());
  gradient.addColorStop(0.46, new THREE.Color(horizonHex).getStyle());
  gradient.addColorStop(0.58, new THREE.Color(horizonHex).getStyle());
  gradient.addColorStop(1, new THREE.Color(groundHex).getStyle());
  context.fillStyle = gradient;
  context.fillRect(0, 0, canvas.width, canvas.height);
  const texture = new THREE.CanvasTexture(canvas);
  texture.mapping = THREE.EquirectangularReflectionMapping;
  texture.colorSpace = THREE.SRGBColorSpace;
  return texture;
}

function makeSandTexture() {
  const size = 512;
  const canvas = document.createElement('canvas');
  canvas.width = size;
  canvas.height = size;
  const context = canvas.getContext('2d');
  const image = context.createImageData(size, size);
  for (let i = 0; i < image.data.length; i += 4) {
    let value = 0.82 + Math.random() * 0.18;
    if (Math.random() < 0.025) value *= 0.82;
    const tone = Math.round(value * 255);
    image.data[i] = tone;
    image.data[i + 1] = tone;
    image.data[i + 2] = tone;
    image.data[i + 3] = 255;
  }
  context.putImageData(image, 0, 0);
  const texture = new THREE.CanvasTexture(canvas);
  texture.wrapS = THREE.RepeatWrapping;
  texture.wrapT = THREE.RepeatWrapping;
  texture.colorSpace = THREE.SRGBColorSpace;
  texture.anisotropy = 4;
  return texture;
}

function classify(name = '') {
  if (
    name.startsWith('GEO-Caral_Terrain_') ||
    name.startsWith('GEO-Caral_Field_') ||
    name.startsWith('GEO-Caral_Hill_') ||
    name.startsWith('GEO-Caral_Tree_') ||
    name.startsWith('GEO-Caral_Reed_') ||
    name.startsWith('GEO-Caral_Rock_') ||
    name.startsWith('GEO-Caral_Path_') ||
    name.startsWith('GEO-Caral_SiteApron')
  ) {
    return 'terrain';
  }
  if (name.startsWith('GEO-Caral_HumanScale')) return 'reference';
  if (name.startsWith('GEO-Caral_Shicra') || name.startsWith('GEO-Caral_StoneBlock')) return 'props';
  if (
    name.startsWith('GEO-Caral_Pyramide') ||
    name.startsWith('GEO-Caral_Piramide') ||
    name.startsWith('GEO-Caral_Anfiteatro') ||
    name.startsWith('GEO-Caral_AltarCircular') ||
    name.startsWith('GEO-Caral_TemploBanqueta') ||
    name.startsWith('GEO-Caral_EdificiosE2E3') ||
    name.startsWith('GEO-Caral_PlazaMayor') ||
    name.startsWith('GEO-Caral_PlazaCentral') ||
    name.startsWith('GEO-Caral_PlazuelaHuanca') ||
    name.startsWith('GEO-Caral_Residencial') ||
    name.startsWith('GEO-Caral_Residencia') ||
    name.startsWith('GEO-Caral_Elite') ||
    name.startsWith('GEO-Caral_Taller') ||
    name.startsWith('GEO-Caral_Periferia')
  ) {
    return 'city';
  }
  return 'props';
}

export class CityViewer {
  constructor(container, { onProgress, onReady, onError } = {}) {
    this.container = container;
    this.onProgress = onProgress;
    this.onReady = onReady;
    this.onError = onError;
    this.city = null;
    this.model = null;
    this.meshes = [];
    this.flight = null;
    this.timeOfDay = 'morning';
    this.flatSand = null;
    this.stars = null;
    this.sandTexture = makeSandTexture();

    this.renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance' });
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.5));
    this.renderer.setSize(container.clientWidth, container.clientHeight, false);
    this.renderer.outputColorSpace = THREE.SRGBColorSpace;
    this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
    this.renderer.toneMappingExposure = 0.74;
    this.renderer.shadowMap.enabled = true;
    this.renderer.shadowMap.type = THREE.PCFShadowMap;
    container.appendChild(this.renderer.domElement);

    this.scene = new THREE.Scene();
    this.scene.fog = new THREE.Fog(0xb9c5c9, 110, 260);

    this.camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 500);
    this.camera.position.set(24, 17, -26);

    this.controls = new OrbitControls(this.camera, this.renderer.domElement);
    this.controls.target.set(2, 4, -5);
    this.controls.enableDamping = true;
    this.controls.dampingFactor = 0.07;
    this.controls.screenSpacePanning = false;
    this.controls.minDistance = 5;
    this.controls.maxDistance = 180;
    this.controls.maxPolarAngle = Math.PI * 0.495;
    this.controls.update();

    this._buildLights();
    this._buildGround();
    this._buildStars();
    this._applyTime('morning');
    this._onResize = () => this.resize();
    window.addEventListener('resize', this._onResize);
    this._animate = this._animate.bind(this);
    this.renderer.setAnimationLoop(this._animate);
  }

  _buildLights() {
    this.scene.add(new THREE.AmbientLight(0xffffff, 0.08));

    this.hemi = new THREE.HemisphereLight(0xcfe4f2, 0x8a7550, 0.22);
    this.scene.add(this.hemi);

    this.sun = new THREE.DirectionalLight(0xfff0dc, 4.2);
    this.sun.position.set(120, 70, -100);
    this.sun.castShadow = true;
    this.sun.shadow.mapSize.set(2048, 2048);
    this.sun.shadow.camera.near = 1;
    this.sun.shadow.camera.far = 260;
    this.sun.shadow.camera.left = -50;
    this.sun.shadow.camera.right = 50;
    this.sun.shadow.camera.top = 50;
    this.sun.shadow.camera.bottom = -50;
    this.sun.shadow.bias = -0.0005;
    this.sun.shadow.normalBias = 0.035;
    this.scene.add(this.sun);

    this.sunTarget = new THREE.Object3D();
    this.scene.add(this.sunTarget);
    this.sun.target = this.sunTarget;

    this.fill = new THREE.DirectionalLight(0x9fc4ff, 0.12);
    this.fill.position.set(-40, 45, -30);
    this.scene.add(this.fill);
  }

  _buildGround() {
    const groundSand = this.sandTexture.clone();
    groundSand.needsUpdate = true;
    groundSand.repeat.set(80, 80);
    const material = new THREE.MeshStandardMaterial({
      color: 0xc7a877,
      map: groundSand,
      roughness: 1,
      metalness: 0,
    });
    this.ground = new THREE.Mesh(new THREE.PlaneGeometry(400, 400), material);
    this.ground.rotation.x = -Math.PI / 2;
    this.ground.position.y = -0.3;
    this.ground.receiveShadow = true;
    this.scene.add(this.ground);
  }

  _buildStars() {
    const positions = [];
    for (let i = 0; i < 1400; i += 1) {
      const radius = 180;
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(THREE.MathUtils.randFloat(0.05, 0.75));
      positions.push(
        radius * Math.sin(phi) * Math.cos(theta),
        radius * Math.cos(phi),
        radius * Math.sin(phi) * Math.sin(theta),
      );
    }
    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
    this.stars = new THREE.Points(
      geometry,
      new THREE.PointsMaterial({ color: 0xffffff, size: 0.55, transparent: true, opacity: 0.8, depthWrite: false }),
    );
    this.stars.visible = false;
    this.scene.add(this.stars);
  }

  _applyTime(name) {
    const preset = TIME_PRESETS[name] || TIME_PRESETS.morning;
    this.timeOfDay = name;
    this.sun.position.set(...preset.offset);
    this.sun.color.setHex(preset.sun);
    this.sun.intensity = preset.sunIntensity;
    this.hemi.color.setHex(preset.hemiSky);
    this.hemi.groundColor.setHex(preset.hemiGround);
    this.hemi.intensity = preset.hemiIntensity;
    this.fill.intensity = preset.fill;
    if (this.scene.background?.isTexture) this.scene.background.dispose();
    this.scene.background = makeSkyTexture(preset.skyTop, preset.skyHorizon, preset.skyGround);
    if (this.scene.fog) this.scene.fog.color.setHex(preset.fog);
    this.renderer.toneMappingExposure = preset.exposure;
    this.stars.visible = name === 'night';
  }

  setTimeOfDay(name) {
    this._applyTime(name);
  }

  setLayer(id, visible) {
    for (const mesh of this.meshes) {
      if (mesh.userData.layer === id) mesh.visible = visible;
    }
  }

  setCamera(data, immediate = true) {
    if (!data) return;
    if (data.fov) {
      this.camera.fov = data.fov;
      this.camera.updateProjectionMatrix();
    }
    const position = new THREE.Vector3(...data.position);
    const target = new THREE.Vector3(...data.target);
    if (immediate) {
      this.camera.position.copy(position);
      this.controls.target.copy(target);
      this.controls.update();
      return;
    }
    this.flyTo(data);
  }

  flyTo(data, duration = 1600) {
    if (!data) return;
    if (data.fov) {
      this.camera.fov = data.fov;
      this.camera.updateProjectionMatrix();
    }
    this.flight = {
      start: performance.now(),
      duration,
      fromPosition: this.camera.position.clone(),
      toPosition: new THREE.Vector3(...data.position),
      fromTarget: this.controls.target.clone(),
      toTarget: new THREE.Vector3(...data.target),
    };
    this.controls.enabled = false;
  }

  _updateFlight(now) {
    if (!this.flight) return;
    const t = Math.min(1, (now - this.flight.start) / this.flight.duration);
    const eased = t < 0.5 ? 4 * t * t * t : 1 - (-2 * t + 2) ** 3 / 2;
    this.camera.position.lerpVectors(this.flight.fromPosition, this.flight.toPosition, eased);
    this.controls.target.lerpVectors(this.flight.fromTarget, this.flight.toTarget, eased);
    if (t >= 1) {
      this.flight = null;
      this.controls.enabled = true;
    }
  }

  async load(city) {
    this.city = city;
    if (!city.model) return;
    const loader = new GLTFLoader();
    const url = new URL(city.model, document.baseURI).href;
    const gltf = await new Promise((resolve, reject) => {
      loader.load(
        url,
        resolve,
        (event) => {
          if (event.total && this.onProgress) this.onProgress(event.loaded / event.total);
        },
        (error) => {
          if (this.onError) this.onError(error);
          reject(error);
        },
      );
    });

    const model = gltf.scene;
    model.scale.setScalar(city.scale ?? 1);
    model.traverse((object) => {
      if (!object.isMesh) return;
      object.castShadow = true;
      object.receiveShadow = true;
      object.userData.layer = classify(object.name);
      const materials = Array.isArray(object.material) ? object.material : [object.material];
      for (const material of materials) this._prepareMaterial(material, object);
      this.meshes.push(object);
    });
    this.model = model;
    this.scene.add(model);
    this.setCamera(city.camera || { position: [24, 17, -26], target: [2, 4, -5], fov: 45 });
    if (this.onReady) this.onReady();
  }

  _prepareMaterial(material, mesh) {
    if (!material) return;
    const key = materialKey(material);

    if (key === 'MAT-Caral_Sand') {
      this.flatSand ??= new THREE.MeshStandardMaterial({ color: 0xd4b184, map: this.sandTexture, roughness: 1, metalness: 0 });
      mesh.material = this.flatSand;
      return;
    }

    if (key === 'MAT-Caral_Fire' && material.emissive) {
      material.emissive.setHex(0xff5a10);
      material.emissiveIntensity = 1.3;
      material.color.setHex(0x2a0a02);
      material.roughness = 0.6;
      material.needsUpdate = true;
    }

    if (key === 'MAT-Caral_Water') {
      material.transparent = true;
      material.opacity = 0.84;
      material.roughness = 0.1;
      material.metalness = 0.08;
      material.needsUpdate = true;
    }
  }

  resize() {
    const width = this.container.clientWidth;
    const height = this.container.clientHeight;
    if (!width || !height) return;
    this.camera.aspect = width / height;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(width, height, false);
  }

  _animate(now) {
    this._updateFlight(now);
    this.controls.update();
    this.renderer.render(this.scene, this.camera);
  }

  dispose() {
    this.renderer.setAnimationLoop(null);
    window.removeEventListener('resize', this._onResize);
    this.controls.dispose();
    if (this.scene.background?.isTexture) this.scene.background.dispose();
    this.scene.traverse((object) => {
      if (object.geometry) object.geometry.dispose();
      const materials = Array.isArray(object.material) ? object.material : [object.material];
      for (const material of materials) {
        if (!material) continue;
        for (const value of Object.values(material)) {
          if (value?.isTexture) value.dispose();
        }
        material.dispose();
      }
    });
    this.renderer.dispose();
    this.renderer.domElement.remove();
    this.meshes = [];
    this.model = null;
  }
}
