import { createRouter, createWebHistory } from 'vue-router'
import SignUp from '../components/SignUp.vue';
import LoginForm from '../components/LogIn.vue';
import AdminDash from '../components/Admin_Dash.vue';
import ArtistDash from '../components/Artist_Dash.vue';
import AdminSongs from '../components/Songs.vue';
import ArtistSongs from '../components/Songs.vue';
import ArtistAccount from '../components/Artist_Account.vue';
import SongAdded from '../components/Admin_song_add.vue';
import AdminAccount from '../components/Admin_Account.vue';
import DisplayArtist from '../components/Display_Artist.vue';
import ManageArtist from '../components/Manage_Artists.vue';
import EditArtist from '../components/Edit_Artist.vue';
import MoreSongs from '../components/More_Songs.vue';
import AllSongs from '../components/AllSongsDetail.vue';
import Navigation from '../components/NavigationBar.vue';
import SideBar from '../components/SideBar.vue';
import NavigationArtist from '../components/NavigationArtist.vue';
import SideBarArtist from '../components/SideBarArtist.vue';
import NavLogin from '../components/NavigationLogin.vue';
import CreateArtistSong from '../components/ArtistSongCreate.vue';
import SongPop from '../components/SongPop.vue'

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
     },
     {
      path: '/artist/:artistId/songs',
      name: 'MoreSongs',
      component: MoreSongs,
      props: true,
     },

     {
      path: '/all_songs_detail',
      name: 'AllSongs',
      component: AllSongs,
   
     },
     {
      path:'/nav',
      name:'Navigation',
      component:Navigation
     },
     {
      path:'/sidebar',
      name:'SideBar',
      component:SideBar
     },
     {
      path:'/navigation',
      name:'NavigationArtist',
      component:NavigationArtist
     },
     {
      path:'/sidebar',
      name:'SideBarArtist',
      component:SideBarArtist
     },
     {
      path:'/navlogin',
      name:'NavLogin',
      component:NavLogin
     },
     {
      path:'/createartistsong',
      name:'CreateArtistSong',
      component:CreateArtistSong
     },
     {
      path:'/songpop',
      name:'SongPop',
      component:SongPop
     }

   
]

const router = createRouter({
  history: createWebHistory(),
  routes
});


function isAuthenticated() {
  return !!localStorage.getItem('access_token'); 
}


router.beforeEach((to, from, next) => {

  const publicPages = ['LoginForm', 'SignUp'];
  
 
  if (publicPages.includes(to.name) || isAuthenticated()) {
    next();
  } else {
    next({ name: 'LoginForm' });
  }
});
export default router


