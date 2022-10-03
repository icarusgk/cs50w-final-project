import { createApp } from 'vue';
import { createPinia } from 'pinia';
import { autoAnimatePlugin } from '@formkit/auto-animate/vue';

import App from './App.vue';
import router from './router';
import Popper from 'vue3-popper';
import './axios';

const app = createApp(App);

app.use(createPinia());
app.use(router);

app.use(autoAnimatePlugin);

app.component('Popper', Popper);

app.mount('#app');
