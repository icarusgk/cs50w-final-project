import { createApp } from 'vue';
import { createPinia } from 'pinia';
import { autoAnimatePlugin } from '@formkit/auto-animate/vue';
import { useChoreStore } from './stores/chore';
import piniaPluginPersistedState from "pinia-plugin-persistedstate"
import 'virtual:windi.css'

import App from './App.vue';
import router from './router';
import Popper from 'vue3-popper';
import './axios';

const app = createApp(App);

const pinia = createPinia();
pinia.use(piniaPluginPersistedState)
app.use(pinia);
app.use(router);

app.use(autoAnimatePlugin);

app.component('Popper', Popper);

app.mount('#app');

useChoreStore().fetchAll();
