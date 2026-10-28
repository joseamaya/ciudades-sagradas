import * as THREE from 'three';
import { DRACOLoader } from 'three/addons/loaders/DRACOLoader.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

const TIME_PRESETS = {
  morning: {
    offset: [-120, 70, 100],
    sun: 0xffd2a0,
    sunIntensity: 5.0,
    hemiSky: 0xd8d8d8,
    hemiGround: 0x6a5a48,
    hemiIntensity: 0.05,
    fill: 0.08,
    skyTop: 0x4a7fb5,
    skyHorizon: 0x9fc2dc,
    skyGround: 0xaec4d2,
    fog: 0xc8d2d8,
    exposure: 1.05,
    envIntensity: 0.18,
    backgroundIntensity: 1.0,
  },
  noon: {
    offset: [50, 125, 10],
    sun: 0xfff2dc,
    sunIntensity: 3.8,
    hemiSky: 0xdfeeff,
    hemiGround: 0x7a6748,
    hemiIntensity: 0.08,
    fill: 0.25,
    skyTop: 0x2c6ba8,
    skyHorizon: 0x80a8c8,
    skyGround: 0xb89660,
    fog: 0xc4d2da,
    exposure: 0.85,
    envIntensity: 0.8,
  },
  dusk: {
    offset: [-110, 40, 20],
    sun: 0xff9a5a,
    sunIntensity: 2.4,
    hemiSky: 0xf0b48b,
    hemiGround: 0x4a3624,
    hemiIntensity: 0.12,
    fill: 0.2,
    skyTop: 0x33365f,
    skyHorizon: 0xd98e66,
    skyGround: 0x6a4630,
    fog: 0xc98f6a,
    exposure: 0.95,
    envIntensity: 0.65,
  },
  night: {
    offset: [25, 90, -65],
    sun: 0x8fb0ff,
    sunIntensity: 0.45,
    hemiSky: 0x2a3a5a,
    hemiGround: 0x1a1410,
    hemiIntensity: 0.1,
    fill: 0.05,
    skyTop: 0x080e1a,
    skyHorizon: 0x18243a,
    skyGround: 0x0d0c0a,
    fog: 0x101827,
    exposure: 0.7,
    envIntensity: 0.35,
  },
};

const DOUBLE_SIDED_MATERIALS = new Set([
  'MAT-Caral_Fire',
  'MAT-Caral_Cotton',
  'MAT-Caral_Remaster_Thatch',
  'MAT-Caral_Remaster_Leaves',
  'MAT-Caral_Remaster_Grass',
]);

const SHADOW_MAP_SIZE = {
  desktop: 2048,
  mobile: 1024,
};

function materialKey(material) {
  return (material?.name || '').split('.')[0];
}

function isDoubleSided(material) {
  const key = materialKey(material);
  if (key === 'MAT-Caral_Water') return false;
  if (key.startsWith('MAT-Caral_LOD1_')) return false;
  return DOUBLE_SIDED_MATERIALS.has(key);
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

function deviceProfile() {
  const userAgent = navigator.userAgent || '';
  const uaMobile = navigator.userAgentData?.mobile === true;
  const mobileUA = /Android|iPhone|iPad|iPod|Mobile|Tablet/i.test(userAgent);
  const iPadDesktop = /Macintosh/i.test(userAgent) && (navigator.maxTouchPoints ?? 0) > 1;
  const memory = navigator.deviceMemory ?? 8;
  const cores = navigator.hardwareConcurrency ?? 8;
  const small = Math.min(window.screen.width, window.screen.height) <= 600;
  const coarse = window.matchMedia?.('(pointer: coarse)').matches === true;
  const lowPower = Boolean(
    uaMobile ||
    mobileUA ||
    iPadDesktop ||
    memory <= 4 ||
    cores <= 4 ||
    (small && coarse),
  );
  return { lowPower, uaMobile, mobileUA, iPadDesktop, memory, cores, small, coarse };
}

function selectLodLevel(city, lowPower) {
  const levels = city.lod?.levels ?? {};
  const override = new URLSearchParams(window.location.search).get('lod');
  if (override && levels[override]) return override;
  const preferred = city.lod?.default;
  if (preferred && preferred !== 'auto' && levels[preferred]) return preferred;
  if (lowPower && levels['1']) return '1';
  if (levels['0']) return '0';
  return Object.keys(levels)[0] ?? null;
}

function buildModelCandidates(city, lowPower) {
  const levels = city.lod?.levels ?? {};
  const selected = selectLodLevel(city, lowPower);
  const candidates = [];
  const add = (level, url) => {
    if (!url || candidates.some((candidate) => candidate.url === url)) return;
    candidates.push({ level, url });
  };
  if (selected && levels[selected]) add(selected, levels[selected]);

  if (lowPower && selected === '1') {
    // En un dispositivo modesto, el fallback v1 pesa menos que LOD0.
    add('v1', city.fallbackModel);
    for (const [level, url] of Object.entries(levels)) add(level, url);
    add(null, city.model);
    return candidates;
  }

  for (const [level, url] of Object.entries(levels)) add(level, url);
  add(null, city.model);
  add('v1', city.fallbackModel);
  return candidates;
}

function classify(name = '') {
  if (name.includes('_Infra_Terrain')) return 'terrain';
  if (name.includes('_Infra_Props')) return 'props';
  if (name.includes('_Infra_Reference')) return 'reference';
  if (
    name.startsWith('GEO-Caral_HighPoly_') ||
    name.startsWith('GEO-Caral_LOD0_') ||
    name.startsWith('GEO-Caral_LOD1_') ||
    name.startsWith('MESH-Caral_HighPoly_') ||
    name.startsWith('MESH-Caral_LOD0_') ||
    name.startsWith('MESH-Caral_LOD1_')
  ) {
    return 'city';
  }
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
    this.cityLights = [];
    this.model = null;
    this.meshes = [];
    this.flight = null;
    this.timeOfDay = 'morning';
    this.baseFov = 45;
    this.flatSand = null;
    this.stars = null;
    this.sandTexture = makeSandTexture();
    this.profile = deviceProfile();
    this.lowPower = this.profile.lowPower;
    const params = new URLSearchParams(window.location.search);
    this.flags = {
      noGround: params.has('noground'),
      noShadows: params.has('noshadows'),
    };
    this.lodLevel = null;
    this.modelUrl = null;
    this.modelTriangles = 0;
    this.modelBytes = null;
    this.loadStartedAt = performance.now();
    this.loadMs = null;
    this.stats = { fps: 0, frameMs: 0, calls: 0, trianglesDrawn: 0 };
    this._frameCount = 0;
    this._frameAccum = 0;
    this._lastFrame = 0;
    this.skyCache = new Map();
    this.envCache = new Map();
    this._destroyed = false;

    this.renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance' });
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, this.lowPower ? 1.25 : 1.5));
    this.renderer.setSize(container.clientWidth, container.clientHeight, false);
    this.renderer.outputColorSpace = THREE.SRGBColorSpace;
    this.renderer.toneMapping = THREE.AgXToneMapping;
    this.renderer.toneMappingExposure = 0.9;
    this.renderer.shadowMap.enabled = !this.flags.noShadows;
    this.renderer.shadowMap.type = THREE.PCFShadowMap;
    this.renderer.shadowMap.autoUpdate = false;
    this.renderer.shadowMap.needsUpdate = true;
    container.appendChild(this.renderer.domElement);

    this._onContextRestored = () => {
      this.renderer.shadowMap.needsUpdate = true;
    };
    this.renderer.domElement.addEventListener('webglcontextrestored', this._onContextRestored);

    this.pmrem = new THREE.PMREMGenerator(this.renderer);
    this.pmrem.compileEquirectangularShader();

    this.dracoLoader = new DRACOLoader();
    this.dracoLoader.setDecoderPath(new URL('draco/', document.baseURI).href);

    this.scene = new THREE.Scene();
    this.scene.fog = new THREE.Fog(0xb9c5c9, 110, 260);

    this.camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.05, 500);
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
    this.scene.add(new THREE.AmbientLight(0xffffff, 0.04));

    this.hemi = new THREE.HemisphereLight(0xcfe4f2, 0x8a7550, 0.1);
    this.scene.add(this.hemi);

    this.sun = new THREE.DirectionalLight(0xffdcb3, 3.6);
    this.sun.position.set(120, 70, -100);
    this.sun.castShadow = !this.flags.noShadows;
    const shadowSize = this.lowPower ? SHADOW_MAP_SIZE.mobile : SHADOW_MAP_SIZE.desktop;
    this.sun.shadow.mapSize.set(shadowSize, shadowSize);
    this.sun.shadow.camera.near = 1;
    this.sun.shadow.camera.far = 400;
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

    this.fill = new THREE.DirectionalLight(0xd8d8d8, 0.08);
    this.fill.position.set(35, 40, -25);
    this.scene.add(this.fill);
  }

  _buildGround() {
    const groundSand = this.sandTexture.clone();
    groundSand.needsUpdate = true;
    groundSand.repeat.set(80, 80);
    const material = new THREE.MeshStandardMaterial({
      color: 0xd0b892,
      map: groundSand,
      roughness: 1,
      metalness: 0,
      polygonOffset: true,
      polygonOffsetFactor: 1,
      polygonOffsetUnits: 1,
    });
    this.ground = new THREE.Mesh(new THREE.PlaneGeometry(400, 400), material);
    this.ground.rotation.x = -Math.PI / 2;
    // El terreno del GLB llega a ~-0.32 tras la escala 0.08. El plano queda
    // debajo y con polygonOffset para evitar z-fighting con las capas de suelo.
    this.ground.position.y = -0.36;
    this.ground.receiveShadow = true;
    this.ground.visible = !this.flags.noGround;
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
      new THREE.PointsMaterial({ color: 0xffffff, size: 0.55, transparent: true, opacity: 0.8, depthWrite: false, fog: false }),
    );
    this.stars.visible = false;
    this.scene.add(this.stars);
  }

  _skyFor(name) {
    if (!this.skyCache.has(name)) {
      const preset = TIME_PRESETS[name];
      const sky = makeSkyTexture(preset.skyTop, preset.skyHorizon, preset.skyGround);
      const envTarget = this.pmrem.fromEquirectangular(sky);
      this.skyCache.set(name, sky);
      this.envCache.set(name, envTarget);
    }
    return { sky: this.skyCache.get(name), envTarget: this.envCache.get(name) };
  }

  _positionSun() {
    const preset = TIME_PRESETS[this.timeOfDay] || TIME_PRESETS.morning;
    this.sun.position.set(
      this.sunTarget.position.x + preset.offset[0],
      this.sunTarget.position.y + preset.offset[1],
      this.sunTarget.position.z + preset.offset[2],
    );
  }

  _applyTime(name) {
    const key = TIME_PRESETS[name] ? name : 'morning';
    const preset = TIME_PRESETS[key];
    this.timeOfDay = key;
    this._positionSun();
    this.sun.color.setHex(preset.sun);
    this.sun.intensity = preset.sunIntensity;
    this.hemi.color.setHex(preset.hemiSky);
    this.hemi.groundColor.setHex(preset.hemiGround);
    this.hemi.intensity = preset.hemiIntensity;
    this.fill.intensity = preset.fill;
    const { sky, envTarget } = this._skyFor(key);
    this.scene.background = sky;
    this.scene.environment = envTarget.texture;
    this.scene.environmentIntensity = preset.envIntensity ?? 0.8;
    this.scene.backgroundIntensity = preset.backgroundIntensity ?? 1;
    if (this.scene.fog) this.scene.fog.color.setHex(preset.fog);
    this.renderer.toneMappingExposure = preset.exposure;
    this.renderer.shadowMap.needsUpdate = true;
    this.stars.visible = key === 'night';
  }

  setTimeOfDay(name) {
    this._applyTime(name);
  }

  setLayer(id, visible) {
    for (const mesh of this.meshes) {
      if (mesh.userData.layer === id) mesh.visible = visible;
    }
    this.renderer.shadowMap.needsUpdate = true;
  }

  setCamera(data, immediate = true) {
    if (!data) return;
    if (data.fov) {
      this.baseFov = data.fov;
      this._applyFov();
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
      this.baseFov = data.fov;
      this._applyFov();
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

  _loadGltf(loader, url) {
    return new Promise((resolve, reject) => {
      loader.load(
        url,
        resolve,
        (event) => {
          if (event.total && this.onProgress) this.onProgress(event.loaded / event.total);
        },
        reject,
      );
    });
  }

  async load(city) {
    this._clearCityLights();
    this.city = city;
    if (Number.isFinite(city.minDistance)) this.controls.minDistance = city.minDistance;
    if (Number.isFinite(city.maxDistance)) this.controls.maxDistance = city.maxDistance;
    this.loadStartedAt = performance.now();
    const candidates = buildModelCandidates(city, this.lowPower);
    if (!candidates.length) return;

    const loader = new GLTFLoader();
    loader.setDRACOLoader(this.dracoLoader);
    let gltf = null;
    let loadedLevel = null;
    let lastError = null;
    for (const candidate of candidates) {
      try {
        gltf = await this._loadGltf(loader, new URL(candidate.url, document.baseURI).href);
        loadedLevel = candidate.level;
        this.modelUrl = candidate.url;
        break;
      } catch (error) {
        lastError = error;
        console.warn(`No se pudo cargar ${candidate.url}`, error);
      }
    }
    if (!gltf) {
      if (this.onError) this.onError(lastError);
      throw lastError;
    }

    this.lodLevel = loadedLevel;
    const model = gltf.scene;
    const scale = city.scale ?? 1;
    const verticalScale = city.verticalScale ?? 1;
    model.scale.set(scale, scale * verticalScale, scale);
    model.traverse((object) => {
      if (!object.isMesh) return;
      const parentLayer = typeof object.parent?.userData?.layer === 'string' ? object.parent.userData.layer : '';
      const declaredLayer = typeof object.userData.layer === 'string' ? object.userData.layer : parentLayer;
      object.userData.layer = declaredLayer || classify(object.name);
      object.castShadow = object.userData.layer !== 'terrain';
      object.receiveShadow = true;
      const materials = Array.isArray(object.material) ? object.material : [object.material];
      for (const material of materials) this._prepareMaterial(material, object);
      this.meshes.push(object);
    });
    this.model = model;
    this.scene.add(model);
    this._buildCityLights(city);
    this._collectModelStats();
    for (const layer of city.layers || []) {
      if (layer.default === false) this.setLayer(layer.id, false);
    }
    this.setCamera(city.camera || { position: [24, 17, -26], target: [2, 4, -5], fov: 45 });
    this._fitShadowsToModel();
    this.renderer.shadowMap.needsUpdate = true;
    this.renderer.render(this.scene, this.camera);
    this.loadMs = performance.now() - this.loadStartedAt;
    this.modelBytes = this._resourceBytes(this.modelUrl);
    if (this.onReady) this.onReady();
  }

  _clearCityLights() {
    for (const light of this.cityLights.splice(0)) {
      this.scene.remove(light);
      light.dispose?.();
    }
  }

  _buildCityLights(city) {
    for (const spec of city.lights || []) {
      if (spec.type !== 'point') continue;
      const light = new THREE.PointLight(
        new THREE.Color(spec.color || 0xffd8a8),
        spec.intensity ?? 6,
        spec.distance ?? 2.2,
        spec.decay ?? 2,
      );
      light.position.fromArray(spec.position || [0, 1, 0]);
      this.scene.add(light);
      this.cityLights.push(light);
    }
  }

  _prepareMaterial(material, mesh) {
    if (!material) return;
    const key = materialKey(material);

    if (key === 'MAT-Caral_Sand') {
      this.flatSand ??= new THREE.MeshStandardMaterial({
        color: 0xd4b184,
        map: this.sandTexture,
        roughness: 1,
        metalness: 0,
        side: THREE.FrontSide,
      });
      mesh.material = this.flatSand;
      return;
    }

    if (material.userData.__caralPrepared) return;
    material.userData.__caralPrepared = true;

    if (key === 'MAT-Caral_Fire' && material.emissive) {
      material.emissive.setHex(0xff5a10);
      material.emissiveIntensity = 1.3;
      material.color.setHex(0x2a0a02);
      material.roughness = 0.6;
    }

    if (key === 'MAT-Caral_Water') {
      // La transmisión fuerza una pasada extra de toda la escena en Three.js.
      material.transmission = 0;
      material.transparent = true;
      material.opacity = 0.84;
      material.roughness = 0.1;
      material.metalness = 0.08;
      material.side = THREE.FrontSide;
      material.forceSinglePass = true;
      material.depthWrite = false;
    } else {
      material.side = isDoubleSided(material) ? THREE.DoubleSide : THREE.FrontSide;
    }

    material.needsUpdate = true;
  }

  _collectModelStats() {
    if (!this.model) return;
    const materials = new Set();
    const textures = new Set();
    const images = new Set();
    let meshes = 0;
    let triangles = 0;
    let textureBytes = 0;
    this.model.traverse((object) => {
      if (!object.isMesh) return;
      meshes += 1;
      const geometry = object.geometry;
      if (geometry?.index) triangles += geometry.index.count / 3;
      else if (geometry?.attributes?.position) triangles += geometry.attributes.position.count / 3;
      const objectMaterials = Array.isArray(object.material) ? object.material : [object.material];
      for (const material of objectMaterials) {
        if (!material) continue;
        materials.add(material.uuid);
        for (const value of Object.values(material)) {
          if (!value?.isTexture || textures.has(value.uuid)) continue;
          textures.add(value.uuid);
          const image = value.image;
          if (image?.width && image?.height && !images.has(image)) {
            images.add(image);
            textureBytes += image.width * image.height * 4;
          }
        }
      }
    });
    this.meshCount = meshes;
    this.materialCount = materials.size;
    this.textureCount = textures.size;
    this.textureMB = +(textureBytes * 4 / 3 / 1024 / 1024).toFixed(1);
    this.modelTriangles = Math.round(triangles);
  }

  _fitShadowsToModel() {
    if (!this.model) return;
    this.model.updateMatrixWorld(true);
    const box = new THREE.Box3();
    const temp = new THREE.Box3();
    for (const mesh of this.meshes) {
      if (!mesh.castShadow) continue;
      temp.setFromObject(mesh);
      box.union(temp);
    }
    if (box.isEmpty()) box.setFromObject(this.model);
    const center = box.getCenter(new THREE.Vector3());
    const size = box.getSize(new THREE.Vector3());
    const maxShadow = Math.max(
      ...Object.values(TIME_PRESETS).map((preset) => {
        const horizontal = Math.hypot(preset.offset[0], preset.offset[2]);
        return (size.y * horizontal) / Math.max(10, preset.offset[1]);
      }),
    );
    const radius = Math.max(20, Math.max(size.x, size.z) / 2 + maxShadow + 4);
    this.sunTarget.position.set(center.x, 0, center.z);
    this.sun.shadow.camera.left = -radius;
    this.sun.shadow.camera.right = radius;
    this.sun.shadow.camera.top = radius;
    this.sun.shadow.camera.bottom = -radius;
    this.sun.shadow.camera.near = 1;
    this.sun.shadow.camera.far = 400;
    this.sun.shadow.camera.updateProjectionMatrix();
    this._positionSun();
    this.renderer.shadowMap.needsUpdate = true;
  }

  _resourceBytes(url) {
    if (!url) return null;
    const absolute = new URL(url, document.baseURI).href;
    const entry = performance
      .getEntriesByType('resource')
      .filter((item) => item.name === absolute)
      .at(-1);
    if (!entry) return null;
    return entry.encodedBodySize || entry.transferSize || null;
  }

  getMetrics() {
    return {
      ready: Boolean(this.model),
      lod: this.lodLevel,
      modelUrl: this.modelUrl,
      lowPower: this.lowPower,
      profile: this.profile,
      viewport: {
        width: this.renderer.domElement.width,
        height: this.renderer.domElement.height,
      },
      cssViewport: {
        width: this.container.clientWidth,
        height: this.container.clientHeight,
      },
      pixelRatio: this.renderer.getPixelRatio(),
      shadowMapSize: [this.sun?.shadow?.mapSize?.x ?? null, this.sun?.shadow?.mapSize?.y ?? null],
      shadowAutoUpdate: this.renderer.shadowMap.autoUpdate,
      flags: this.flags,
      meshes: this.meshCount ?? this.meshes.length,
      materials: this.materialCount ?? null,
      textures: this.textureCount ?? null,
      textureMB: this.textureMB ?? null,
      modelTriangles: this.modelTriangles,
      calls: this.stats.calls,
      trianglesDrawn: this.stats.trianglesDrawn,
      fps: this.stats.fps,
      frameMs: this.stats.frameMs,
      loadMs: this.loadMs == null ? null : Math.round(this.loadMs),
      modelBytes: this.modelBytes,
      timeOfDay: this.timeOfDay,
      layers: Object.fromEntries(
        [...new Set(this.meshes.map((mesh) => mesh.userData.layer))]
          .filter(Boolean)
          .map((layer) => [layer, this.meshes.some((mesh) => mesh.userData.layer === layer && mesh.visible)]),
      ),
    };
  }

  _applyFov() {
    const aspect = this.container.clientWidth / Math.max(1, this.container.clientHeight);
    const fov = aspect < 0.8 ? Math.min(60, this.baseFov * 2.2) : this.baseFov;
    if (this.camera.fov !== fov) {
      this.camera.fov = fov;
      this.camera.updateProjectionMatrix();
    }
  }

  resize() {
    const width = this.container.clientWidth;
    const height = this.container.clientHeight;
    if (!width || !height) return;
    this.camera.aspect = width / height;
    this._applyFov();
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(width, height, false);
  }

  _animate(now) {
    this._updateFlight(now);
    this.controls.update();
    this.renderer.render(this.scene, this.camera);

    const render = this.renderer.info.render;
    this.stats.calls = render.calls;
    this.stats.trianglesDrawn = render.triangles;

    if (this._lastFrame) {
      const delta = now - this._lastFrame;
      if (delta > 0 && delta < 1000) {
        this._frameAccum += delta;
        this._frameCount += 1;
        if (this._frameAccum >= 500) {
          this.stats.fps = +((this._frameCount * 1000) / this._frameAccum).toFixed(1);
          this.stats.frameMs = +(this._frameAccum / this._frameCount).toFixed(2);
          this._frameAccum = 0;
          this._frameCount = 0;
        }
      }
    }
    this._lastFrame = now;
  }

  dispose() {
    this._clearCityLights();
    if (this._destroyed) return;
    this._destroyed = true;
    this.renderer.setAnimationLoop(null);
    window.removeEventListener('resize', this._onResize);
    this.renderer.domElement.removeEventListener('webglcontextrestored', this._onContextRestored);
    this.controls.dispose();
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
    for (const target of this.envCache.values()) target.dispose();
    for (const sky of this.skyCache.values()) sky.dispose();
    this.envCache.clear();
    this.skyCache.clear();
    this.dracoLoader.dispose();
    this.pmrem.dispose();
    this.renderer.dispose();
    this.renderer.domElement.remove();
    this.meshes = [];
    this.model = null;
  }
}
