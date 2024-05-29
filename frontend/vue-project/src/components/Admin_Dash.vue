<template>
  <div class="min-h-screen flex flex-col">
    <Navigation :admin="admin" :dropdownVisible="dropdownVisible" @toggle-dropdown="toggleDropdown" />
    <div class="flex flex-1">
      <SideBar />
      <div class="flex-1 p-6 bg-blue-100">
        <h1 class="text-3xl font-bold mb-8">Admin Dashboard</h1>
        <div v-if="loading" class="text-center text-gray-600">Loading...</div>
        <div v-if="error" class="text-center text-red-600">{{ error }}</div>
        <div v-if="artists.length" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-5">
          <div v-for="artist in artists" :key="artist.id" class="bg-white shadow-lg rounded-lg p-6 artist-card">
            <h2 class="text-xl font-bold mb-4">{{ artist.first_name }} {{ artist.last_name }}</h2>
            <ul>
              <li v-for="(song, index) in artist.songs.slice(0, 2)" :key="song.id" class="mb-2">
                <button @click="viewSongDetails(song)" class="font-semibold text-black hover:underline focus:outline-none">{{ song.title }}</button> ({{ song.duration }})
              </li>
            </ul>
            <div v-if="artist.songs.length < 1" class="mt-4">
              <p>No Songs Found</p>
            </div>
            <div v-if="artist.songs.length > 2" class="mt-4">
              <router-link :to="{ name: 'MoreSongs', params: { artistId: artist.id } }" class="text-blue-500 hover:underline">More</router-link>
            </div>
          </div>
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
  data() {
    return {
      admin: null,
      dropdownVisible: false,
      artists: [],
      loading: false,
      error: null,
      selectedSong: null,
    };
  },
  created() {
    this.fetchAdminDetails();
    this.fetchArtistsAndSongs();
  },
  methods: {
    async fetchAdminDetails() {
      try {
        const token = localStorage.getItem('access_token');
        const response = await axios.get('http://127.0.0.1:8000/api/only/admin/', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        this.admin = response.data;
      } catch (error) {
        console.error('Error fetching admin details:', error);
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
.artist-card {
  width: 300px; 
  height: 200px; 
}


.modal {
  display: none;
  position: fixed;
  z-index: 1000;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgba(0, 0, 0, 0.5);
}

.modal-content {
  background-color: #fefefe;
  margin: 15% auto;
  padding: 20px;
  border: 1px solid #888;
  width: 80%;
}

.close {
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
}

.close:hover,
.close:focus {
  color: black;
  text-decoration: none;
  cursor: pointer;
}
</style>
