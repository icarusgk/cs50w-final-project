import { createApp } from 'vue';
import { createPinia } from 'pinia';
import { plugin, defaultConfig } from '@formkit/vue';
import { autoAnimatePlugin } from '@formkit/auto-animate/vue';
import VueApexCharts from 'vue3-apexcharts';

import App from './App.vue';
import router from './router';
import Popper from 'vue3-popper';
import './axios';

const app = createApp(App);

app.use(createPinia());
app.use(router);
// Formkit
app.use(
  plugin,
  defaultConfig({
    theme: 'genesis',
  })
);

app.use(autoAnimatePlugin);

app.use(VueApexCharts)

app.component('Popper', Popper);

app.mount('#app');
