// vite.config.js
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'), // 👈 设置 @ 为 src 路径别名
    },
  },
  server: {
    host: true,
    allowedHosts: ['chenfeiyu.asuscomm.com'],
    port: 5173
  }
})
