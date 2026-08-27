import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'
import { resolve } from 'path'

export default defineConfig({
  plugins: [react()],

  define: {
    'process.env.NODE_ENV': JSON.stringify('production'),
  },

  build: {
    lib: {
      entry: resolve(__dirname, 'src/widget.jsx'),
      name: 'HotelChatbot',
      fileName: 'chatbot',
      formats: ['iife'],
    },

    rollupOptions: {
      output: {
        inlineDynamicImports: true,
      },
    },
  },
})