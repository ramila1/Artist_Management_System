import './assets/index.css'
import { createApp } from 'vue'
import Vue3Toasity from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'
import App from './App.vue'

import router from './router'
import axios from './axios' 

import Toast from 'vue-toastification';
import 'vue-toastification/dist/index.css';


const app = createApp(App)

app.config.globalProperties.$axios = axios

app.use(Vue3Toasity)
app.use(Toast);
app.use(router)




app.mount('#app')



