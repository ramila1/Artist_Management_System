<template>
  <div class="min-h-screen flex flex-col bg-blue-100">
    <Navigation :admin="admin" :dropdownVisible="dropdownVisible" @toggle-dropdown="toggleDropdown" />
    <div class="flex-1 flex">
      <SideBar class="hidden lg:block" />
      <div class="ml-20 items-end">
        <h1 class="text-3xl font-bold mb-8 mt-11" v-if="artist">Songs by {{ artist.first_name }} {{ artist.last_name }}</h1>
        <div v-if="loading" class="text-center text-gray-600">Loading...</div>
        <div v-if="error" class="text-center text-red-600">{{ error }}</div>
        <div v-if="artist && artist.songs.length" class="w-full max-w-xs mx-auto bg-white shadow-lg rounded-lg p-6">
          <ul>
            <li v-for="song in artist.songs" :key="song.id" class="mb-2">
              <button @click="viewSongDetails(song)" class="font-semibold text-black hover:underline focus:outline-none">{{ song.title }}</button> ({{ song.duration }})
            </li>
          </ul>
        </div>
      </div>
    </div>

    <!-- Song Details Modal -->
    <div v-if="selectedSong" class="fixed inset-0 z-50 flex items-center justify-center overflow-auto bg-gray-800 bg-opacity-50">
      <div class="relative bg-white rounded-lg p-8 max-w-md mx-auto overflow-y-auto max-h-96">
        <button @click="closeModal" class="absolute top-0 right-0 m-4 text-gray-600 hover:text-gray-800 focus:outline-none">&times;</button>
        <h2 class="text-xl font-bold mb-4">{{ selectedSong.title }}</h2>
        <p><strong>Artist:</strong> {{ selectedSong.artist.first_name }} {{ selectedSong.artist.last_name }}</p>
        <p><strong>Release Date:</strong> {{ selectedSong.release_date }}</p>
        <p><strong>Duration:</strong> {{ selectedSong.duration }}</p>
        <p v-if="selectedSong.lyrics"><strong>Lyrics:</strong> {{ selectedSong.lyrics }}</p>
        <p><strong>Language:</strong> {{ selectedSong.language }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Navigation from './NavigationBar.vue';
import SideBar from './SideBar.vue';

export default {
  components: {
    Navigation,
    SideBar,
  },
  name: 'MoreSongs',
  data() {
    return {
      artist: null,
      loading: false,
      error: null,
      dropdownVisible: false,
      selectedSong: null,
    };
  },
  created() {
    this.fetchAdminData();
    this.fetchArtistSongs();
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
    async fetchArtistSongs() {
      this.loading = true;
      this.error = null;
      try {
        const artistId = this.$route.params.artistId;
        const token = localStorage.getItem('access_token');
        
        const artistResponse = await axios.get(`http://127.0.0.1:8000/api/artists/${artistId}/`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (artistResponse.status === 404) {
          this.error = 'Artist not found';
          return;
        }

        const artist = artistResponse.data;

        const songsResponse = await axios.get(`http://127.0.0.1:8000/api/songs/user/${artistId}/`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        artist.songs = songsResponse.data;

        this.artist = artist;
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
    },
    viewSongDetails(song) {
      this.selectedSong = song;
    },
    closeModal() {
      this.selectedSong = null;
    },
  },
};
</script>

<style scoped>
/* Add your scoped styles here */
</style>
