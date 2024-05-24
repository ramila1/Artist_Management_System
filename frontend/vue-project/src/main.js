import './assets/index.css'
import { createApp } from 'vue'
import App from './App.vue'
import LoginForm from './components/LogIn.vue'
import SignUp from './components/SignUp.vue'
import AdminDash from './components/Admin_Dash.vue'
import ArtistDash from './components/Artist_Dash.vue'
import router from './router'
import axios from './axios' 
import ArtistAccount from './components/Artist_Account.vue'
import DisplayArtist from './components/Display_Artist.vue';
import ManageArtist from './components/Manage_Artists.vue';

const app = createApp(App)

app.config.globalProperties.$axios = axios


app.use(router)

app.component('LoginForm', LoginForm)
app.component('SignUp', SignUp)
app.component('AdminDash', AdminDash)
app.component('ArtistDash', ArtistDash)
app.component('ArtistAccount',ArtistAccount)
app.component('DisplayArtist',DisplayArtist)
app.component('ManageArtists',ManageArtist)

app.mount('#app')
