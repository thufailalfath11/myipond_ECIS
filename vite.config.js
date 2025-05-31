import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    allowedHosts: ['webecis.mbclaboratory.com'],
    host: true // biar bisa diakses dari luar, penting juga!
  },
})
