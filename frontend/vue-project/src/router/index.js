import { createRouter, createWebHistory } from 'vue-router'
import SignUp from '../components/SignUp.vue';
import LoginForm from '../components/LogIn.vue';
import AdminDash from '../components/Admin_Dash.vue';
import ArtistDash from '../components/Artist_Dash.vue';
import AdminSongs from '../components/Songs.vue';
import ArtistSongs from '../components/Songs.vue';
import ArtistAccount from '../components/Artist_Account.vue';
import SongAdded from '../components/Artist_song_add.vue';
import AdminAccount from '../components/Admin_Account.vue';
import DisplayArtist from '../components/Display_Artist.vue';
import ManageArtist from '../components/Manage_Artists.vue';
import EditArtist from '../components/Edit_Artist.vue';
const routes= [
    {
      path:'/signup',
      name:'SignUp',
      component:SignUp
    },
    {
      path:'/login',
      name:'LoginForm',
      component:LoginForm
    },
    {
      path:'/admin',
      name:'AdminDash',
      component:AdminDash
    },
    {
      path:'/artist',
      name:'ArtistDash',
      component:ArtistDash
    },
    { 
      path: '/admin/songs',
      name:'AdminSong',
      component: AdminSongs
     },
     {
      path:'/songs',
      name:'ArtistSongs',
      component:ArtistSongs
     },
     {
      path:'/artist_account',
      name:'ArtistAccount',
      component:ArtistAccount
     },
     {
      path:'/song_added',
      name:'SongAdded',
      component:SongAdded
     },
     {
      path:'/admin_account',
      name:'AdminAccount',
      component:AdminAccount
     },
     {
      path:'/display_artists',
      name:'DisplayArtist',
      component:DisplayArtist
     },
     {
      path:'/manage_artists',
      name:'ManageArtist',
      component:ManageArtist
     },
     {
    path: '/edit_artist',
      name:'EditArtist',
      component:EditArtist
     }
]
const router = createRouter({
    history: createWebHistory(),
    routes
  });
  
export default router


