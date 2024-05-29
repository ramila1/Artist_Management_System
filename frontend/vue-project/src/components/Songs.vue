<template>
  <div class="min-h-screen flex flex-col bg-blue-100">
    <!-- Navigation Bar Component -->
    <NavigationArtist :artist="artist" :dropdownVisible="dropdownVisible" @toggle-dropdown="toggleDropdown" />

    <div class="flex-1 flex">
      <!-- Sidebar Component (Hidden on Large Screens) -->
      <SideBarArtist class="hidden lg:block" />

      <!-- Main Content Area -->
      <div class="flex-1 p-6">
        <!-- Section Title -->
        <h2 class="text-center text-xl font-bold mb-4">My Songs</h2>

        <!-- Grid for Songs -->
        <div v-if="mySongs.length" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          <!-- Song Card -->
          <div v-for="song in mySongs" :key="song.id" class="song-card bg-white p-4 rounded shadow-md relative">
            <!-- Song Details -->
            <div class="mb-2">
              <strong class="font-bold">Title:</strong> {{ song.title }}
            </div>
            <div class="mb-2">
              <strong class="font-bold">Release Date:</strong> {{ song.release_date }}
            </div>
            <div class="mb-2">
              <strong class="font-bold">Duration:</strong> {{ song.duration }}
            </div>
            <div class="mb-2">
              <strong class="font-bold">Language:</strong> {{ song.language }}
            </div>
            <div>
              <!-- Shortened Lyrics with 'Show More' Button -->
              <p class="text-gray-700">{{ getShortenedLyrics(song.lyrics) }}</p>
              <button @click="showLyricsModal(song)" class="text-blue-500 hover:underline focus:outline-none">
                Show More
              </button>
            </div>

            <!-- Song Actions (Edit and Delete) -->
            <div class="absolute top-2 right-2 flex space-x-2 items-center">
              <!-- Edit Icon -->
              <svg @click="editSong(song)" class="h-6 w-6 cursor-pointer text-gray-500 hover:text-green-600"
                fill="none" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24"
                stroke="currentColor">
                <path
                  d="M15 3a2 2 0 012 2v14a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h10zm4 5a2 2 0 11-4 0 2 2 0 014 0zM8 9a2 2 0 100 4 2 2 0 000-4z">
                </path>
              </svg>

              <!-- Delete Icon -->
              <svg @click="deleteSong(song.id)" class="h-6 w-6 cursor-pointer text-gray-500 hover:text-red-600"
                fill="none" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24"
                stroke="currentColor">
                <path d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </div>
          </div>
        </div>

        <!-- Message when no songs are found -->
        <p v-else class="text-center">No songs found.</p>

        <!-- Lyrics Modal -->
        <div v-if="lyricsModalVisible" class="fixed inset-0 flex items-center justify-center bg-gray-800 bg-opacity-50">
          <div class="bg-white p-6 rounded-md w-96 max-h-96 overflow-y-auto relative">
            <button @click="closeLyricsModal"
              class="absolute top-2 right-2 text-gray-600 hover:text-gray-800 focus:outline-none">
              &times;
            </button>
            <h3 class="text-lg font-bold mb-4">{{ currentSong.title }}</h3>
            <div v-html="formatLyrics(currentSong.lyrics)"></div>
          </div>
        </div>

        <!-- Editing Modal -->
        <div v-if="editingSong" class="fixed inset-0 flex items-center justify-center bg-gray-800 bg-opacity-50">
          <div class="bg-white p-6 rounded-md w-96 relative">
            <button @click="cancelEdit"
              class="absolute top-2 right-2 text-gray-600 hover:text-gray-800 focus:outline-none">
              &times;
            </button>
            <h3 class="text-lg font-bold mb-4">Edit Song</h3>
            <form @submit.prevent="updateSong">
              <!-- Title Input -->
              <div class="mb-4">
                <label for="title" class="block mb-1 font-bold">Title</label>
                <input type="text" id="title" v-model="editingSong.title" required
                  class="w-full border-gray-300 rounded-md px-3 py-2 focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50"
                  :class="{ 'border-red-500': formErrors.title }">
                <span v-if="formErrors.title" class="text-red-500 text-sm">{{ formErrors.title }}</span>
              </div>
              <!-- Release Date Input -->
              <div class="mb-4">
                <label for="release_date" class="block mb-1 font-bold">Release Date</label>
                <input type="date" id="release_date" v-model="editingSong.release_date" required
                  class="w-full border-gray-300 rounded-md px-3 py-2 focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50"
                  :class="{ 'border-red-500': formErrors.release_date }">
                <span v-if="formErrors.release_date" class="text-red-500 text-sm">{{ formErrors.release_date }}</span>
              </div>
              <!-- Duration Input -->
              <div class="mb-4">
                <label for="duration" class="block mb-1 font-bold">Duration</label>
                <input type="text" id="duration" v-model="editingSong.duration" required
                  class="w-full border-gray-300 rounded-md px-3 py-2 focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50"
                  :class="{ 'border-red-500': formErrors.duration }">
                <span v-if="formErrors.duration" class="text-red-500 text-sm">{{ formErrors.duration }}</span>
              </div>
              <!-- Lyrics Input -->
              <div class="mb-4">
                <label for="lyrics" class="block mb-1 font-bold">Lyrics</label>
                <textarea id="lyrics" v-model="editingSong.lyrics" required
                  class="w-full border-gray-300 rounded-md px-3 py-2 focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50"
                  :class="{ 'border-red-500': formErrors.lyrics }"></textarea>
                <span v-if="formErrors.lyrics" class="text-red-500 text-sm">{{ formErrors.lyrics }}</span>
              </div>
              <!-- Language Input -->
              <div class="mb-4">
                <label for="language" class="block mb-1 font-bold">Language</label>
                <input type="text" id="language" v-model="editingSong.language" required
                  class="w-full border-gray-300 rounded-md px-3 py-2 focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50"
                  :class="{ 'border-red-500': formErrors.language }">
                <span v-if="formErrors.language" class="text-red-500 text-sm">{{ formErrors.language }}</span>
              </div>
              <!-- Submit Button -->
              <button type="submit"
                class="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600 focus:outline-none focus:ring focus:ring-blue-500 focus:ring-opacity-50">
                Update Song
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import NavigationArtist from './NavigationArtist.vue';
import SideBarArtist from './SideBarArtist.vue';
import { toast } from 'vue3-toastify';

export default {
  components: {
    NavigationArtist,
    SideBarArtist,
  },
  data() {
    return {
      mySongs: [],
      editingSong: null,
      currentSong: null,
      lyricsModalVisible: false,
      artist: null,
      dropdownVisible: false,
      formErrors: {},
    };
  },
  created() {
    this.fetchArtistDetails();
    this.fetchMySongs();
  },
  methods: {
    async fetchArtistDetails() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/artists/me/', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`
          }
        });
        this.artist = response.data;
      } catch (error) {
        console.error('Error fetching artist details:', error);
      }
    },
    toggleDropdown() {
      this.dropdownVisible = !this.dropdownVisible;
    },
    async fetchMySongs() {
      const user = JSON.parse(localStorage.getItem('user'));
      const token = localStorage.getItem('access_token');
      try {
        const response = await axios.get(`http://127.0.0.1:8000/api/song/${user.id}/`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        this.mySongs = response.data;
      } catch (error) {
        console.error('Error fetching my songs:', error);
      }
    },
    getShortenedLyrics(lyrics) {
      const lines = lyrics.split('\n').slice(0, 4);
      return lines.join('\n');
    },
    formatLyrics(lyrics) {
      const lines = lyrics.split('\n');
      return lines.map(line => `<p class="text-gray-700">${line}</p>`).join('');
    },
    showLyricsModal(song) {
      this.currentSong = song;
      this.lyricsModalVisible = true;
    },
    closeLyricsModal() {
      this.lyricsModalVisible = false;
      this.currentSong = null;
    },
    editSong(song) {
      this.editingSong = { ...song };
    },
    cancelEdit() {
      this.editingSong = null;
      this.formErrors = {};
    },
    async updateSong() {
      if (!this.validateForm()) {
        return;
      }

      const token = localStorage.getItem('access_token');
      try {
        await axios.put(`http://127.0.0.1:8000/api/song/${this.editingSong.id}/`, this.editingSong, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        this.fetchMySongs();
        this.editingSong = null;
        this.formErrors = {};
        toast.success('Song updated successfully!');
      } catch (error) {
        if (error.response && error.response.data) {
          this.formErrors = error.response.data;
        } else {
          console.error('Error updating song:', error);
          toast.error('Failed to update song. Please try again.');
        }
      }
    },
    async deleteSong(songId) {
      const token = localStorage.getItem('access_token');
      try {
        await axios.delete(`http://127.0.0.1:8000/api/song/${songId}/`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        this.fetchMySongs();
        toast.success('Song deleted successfully!');
      } catch (error) {
        console.error('Error deleting song:', error);
        toast.error('Failed to delete song. Please try again.');
      }
    },
    validateForm() {
      this.formErrors = {};
      let isValid = true;
      if (!this.editingSong.title) {
        this.$set(this.formErrors, 'title', 'Title is required');
        isValid = false;
      }
      if (!this.editingSong.release_date) {
        this.$set(this.formErrors, 'release_date', 'Release Date is required');
        isValid = false;
      }
      if (!this.editingSong.duration) {
        this.$set(this.formErrors, 'duration', 'Duration is required');
        isValid = false;
      }
      if (!this.editingSong.lyrics) {
        this.$set(this.formErrors, 'lyrics', 'Lyrics are required');
        isValid = false;
      }
      if (!this.editingSong.language) {
        this.$set(this.formErrors, 'language', 'Language is required');
        isValid = false;
      }
      return isValid;
    },
  }
};
</script>

<style scoped>
/* No scoped styles necessary as we are using Tailwind CSS classes */
</style>

