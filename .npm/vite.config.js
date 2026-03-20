import { defineConfig } from 'vite'
import legacy from '@vitejs/plugin-legacy'

export default defineConfig({
  plugins: [
    legacy({ targets: ['defaults', 'not IE 11'] }),
  ],
  
  build: {
    outDir: '../app/static/js',   // naik satu level ke root, lalu masuk app/static/js
    emptyOutDir: true,
    reportCompressedSize: false,  // Matikan warning plugin timings
    rollupOptions: {
      input: {
        main: './src/main.js',    // relatif dari frontend/
      },

      output: {
        entryFileNames: '[name].js',
        chunkFileNames: '[name].js',
        assetFileNames: '[name].[ext]',
      },
    },
  },
})