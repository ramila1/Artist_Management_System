<template>
  <div class="min-h-screen flex flex-col bg-blue-100">

    <Navigation :admin="admin" :dropdownVisible="dropdownVisible" @toggle-dropdown="toggleDropdown" />

 
    <div class="flex-1 flex"> 

      <SideBar class="hidden lg:block" />


    <div class="flex-1 p-6">
      <h1 class="text-3xl font-bold mb-8">Artists and Their Songs</h1>
      <div v-if="loading" class="text-center text-gray-600">Loading...</div>
      <div v-if="error" class="text-center text-red-600">{{ error }}</div>
      
      <div v-if="artists.length" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">

        <div v-for="artist in artists" :key="artist.id" class="bg-white shadow-lg rounded-lg p-6">
          <h2 class="text-xl font-bold mb-4">{{ artist.first_name }} {{ artist.last_name }}</h2>
          <ul>
            <li v-for="(song, index) in artist.songs.slice(0, 2)" :key="song.id" class="mb-2">
              <span class="font-semibold">{{ song.title }}</span> ({{ song.duration }})
            </li>
          </ul>
          <div v-if="artist.songs.length > 2" class="mt-4">
            <router-link :to="{ name: 'MoreSongs', params: { artistId: artist.id } }" class="text-blue-500 hover:underline">More</router-link>
          </div>
        </div>
      </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Navigation from './NavigationBar.vue';
import SideBar from './SideBar.vue';

export default {
  name: 'DisplayArtist',
  components: {
    Navigation,
    SideBar,
  },
  data() {
    return {
      artists: [],
      loading: false,
      error: null,
      dropdownVisible: false,
    };
  },
  created() {
    this.fetchAdminData();
    this.fetchArtistsAndSongs();
  },
  methods: {
    async fetchAdminData() {
      this.loading = true;
      this.error = null;
      try {
        const token = localStorage.getItem('access_token');
        const response = await axios.get('http://127.0.0.1:8000/api/only/admin/', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        this.admin = response.data;
      } catch (error) {
        this.error = 'Failed to load admin data';
      } finally {
        this.loading = false;
      }
    },
    async fetchArtistsAndSongs() {
      this.loading = true;
      this.error = null;
      try {
        const token = localStorage.getItem('access_token');
        const artistsResponse = await axios.get('http://127.0.0.1:8000/api/only/artists/', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        const artists = artistsResponse.data;

        const artistPromises = artists.map(async (artist) => {
          const songsResponse = await axios.get(`http://127.0.0.1:8000/api/songs/user/${artist.id}/`, {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          artist.songs = songsResponse.data;
          return artist;
        });

        this.artists = await Promise.all(artistPromises);
      } catch (error) {
        if (error.response && error.response.status === 403) {
          this.error = 'You do not have permission to view this data.';
        } else {
          this.error = 'Failed to load artist data';
        }
      } finally {
        this.loading = false;
      }
    },
    toggleDropdown() {
      this.dropdownVisible = !this.dropdownVisible;
    }
  },
};
</script>
