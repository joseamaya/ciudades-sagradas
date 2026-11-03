import { defineConfig } from 'vite';

function dropUnusedDracoAssets() {
  return {
    name: 'drop-unused-draco-assets',
    apply: 'build',
    generateBundle(_options, bundle) {
      for (const file of Object.keys(bundle)) {
        if (/^assets\/draco_(?:decoder|wasm_wrapper)-.*\.(?:js|wasm)$/.test(file)) {
          delete bundle[file];
        }
      }
    },
  };
}

export default defineConfig({
  base: './',
  plugins: [dropUnusedDracoAssets()],
  server: {
    host: '127.0.0.1',
    port: 5173,
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    sourcemap: false,
    target: 'es2022',
    chunkSizeWarningLimit: 700,
    rolldownOptions: {
      output: {
        codeSplitting: {
          groups: [
            { name: 'three', test: /node_modules[\\/]three[\\/]build/ },
            { name: 'three-addons', test: /node_modules[\\/]three[\\/]examples[\\/]jsm/ },
          ],
        },
      },
    },
  },
});
