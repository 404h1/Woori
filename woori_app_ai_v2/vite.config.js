import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

const isCapacitor = process.env.BUILD_TARGET === 'capacitor'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  base: isCapacitor ? './' : '/Woori/after/',
  server: { port: 5174 },
  build: {
    // Capacitor 빌드는 dist/ 로, 웹 배포는 docs/after 로
    outDir: isCapacitor
      ? path.resolve(__dirname, 'dist')
      : path.resolve(__dirname, '../docs/after'),
    emptyOutDir: true,
  },
})
