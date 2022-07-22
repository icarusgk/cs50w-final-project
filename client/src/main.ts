import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import Popper from "vue3-popper";

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.component("Popper", Popper)

app.mount('#app')
