import { createHash } from 'node:crypto';
import { readFile } from 'node:fs/promises';

export function trianglesOf(json) {
  let triangles = 0;
  for (const mesh of json.meshes ?? []) {
    for (const primitive of mesh.primitives ?? []) {
      const mode = primitive.mode ?? 4;
      const count = primitive.indices != null
        ? json.accessors?.[primitive.indices]?.count
        : json.accessors?.[primitive.attributes?.POSITION]?.count;
      if (!Number.isFinite(count)) continue;
      if (mode === 4) triangles += count / 3;
      else if (mode === 5) triangles += Math.max(0, count - 2);
    }
  }
  return Math.round(triangles);
}

export async function inspectGlb(file) {
  const buffer = await readFile(file);
  if (buffer.length < 20) throw new Error(`${file}: GLB demasiado pequeño`);
  if (buffer.toString('ascii', 0, 4) !== 'glTF') throw new Error(`${file}: cabecera GLB inválida`);
  if (buffer.readUInt32LE(4) !== 2) throw new Error(`${file}: versión GLB distinta de 2`);
  if (buffer.readUInt32LE(8) !== buffer.length) throw new Error(`${file}: longitud GLB declarada no coincide`);
  const jsonLength = buffer.readUInt32LE(12);
  const jsonType = buffer.toString('ascii', 16, 20);
  if (jsonType !== 'JSON' || 20 + jsonLength > buffer.length) {
    throw new Error(`${file}: primer chunk GLB no es JSON`);
  }
  const json = JSON.parse(buffer.toString('utf8', 20, 20 + jsonLength));
  const primitives = (json.meshes ?? []).reduce(
    (total, mesh) => total + (mesh.primitives?.length ?? 0),
    0,
  );
  const meshNodes = (json.nodes ?? []).filter((node) => node.mesh !== undefined);
  const layers = [
    ...new Set(
      meshNodes
        .map((node) => node.extras?.layer)
        .filter((layer) => typeof layer === 'string' && layer),
    ),
  ];
  const missingLayers = meshNodes
    .filter((node) => typeof node.extras?.layer !== 'string' || !node.extras.layer)
    .map((node) => node.name || '(sin nombre)');
  return {
    triangles: trianglesOf(json),
    bytes: buffer.length,
    images: json.images?.length ?? 0,
    materials: json.materials?.length ?? 0,
    primitives,
    layers,
    missingLayers,
    sha256: createHash('sha256').update(buffer).digest('hex'),
  };
}
