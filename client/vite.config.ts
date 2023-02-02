import { fileURLToPath, URL } from 'url';

import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import AutoImport from 'unplugin-auto-import/vite';
import Components from 'unplugin-vue-components/vite';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue(),
    AutoImport({
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
          'vue3-popper': [
            ['default', 'Popper']
          ],
          'apexcharts': [
            ['default', 'ApexChart']
          ]
        }
      ],
      dirs: ['./src/stores'],
      vueTemplate: true,
      dts: 'auto-imports.d.ts',
      eslintrc: {
        enabled: true
      }
    }),
    Components({
      dirs: ['./src/components'],
      extensions: ['vue'],
      deep: true,
      dts: true,
      types: [{
        from: 'vue-router',
        names: ['RouterLink', 'RouterView'],
      }],
      include: [/\.vue$/, /\.vue\?vue/],
      exclude: [/[\\/]node_modules[\\/]/, /[\\/]\.git[\\/]/, /[\\/]\.nuxt[\\/]/],      
    })
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
});
