import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  optimizeDeps: {
    exclude: [
      '/home/ketiovv/studia/projekty/sentiment_analysis/frontend/node_modules/.vite/deps/chunk-LJ6NGG6B.js?v=e3843cd2'
    ]
  }
})


