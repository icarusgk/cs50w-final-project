import { fileURLToPath, URL } from 'url';

import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import AutoImport from 'unplugin-auto-import/vite';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue(), AutoImport({
    include: [
      /\.vue$/, /\.vue\?vue/, // .vue
    ],
    imports: [
      'vue',
      {
        'axios': [
          // default imports
          ['default', 'axios'], // import { default as axios } from 'axios',
        ],
      }
    ],
    dirs: ['./src/stores'],
    vueTemplate: true,
    dts: 'auto-imports.d.ts',
    eslintrc: {
      enabled: true
    }
  })],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
});
