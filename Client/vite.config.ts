import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from 'tailwindcss'
import dotenv from 'dotenv'

// load environment variables
dotenv.config()

export default defineConfig(({ mode }) => {
  return {
    plugins: [react()],
    css: {
      postcss: {
        plugins: [
          tailwindcss(),
        ],
      },
    },
    server: {
      proxy: mode === 'development' ? {
        '/api': {
          target: process.env.SERVER_API_URL,
          changeOrigin: true,
        },
        '/socket.io': {
          target: process.env.SERVER_API_URL,
        },
      } : undefined,
    },
  }
})
