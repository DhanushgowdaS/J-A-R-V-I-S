import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  // GitHub Pages project-site path; Vite dev server still works locally.
  base: '/J-A-R-V-I-S/',
  server: { host: '127.0.0.1' },
});
