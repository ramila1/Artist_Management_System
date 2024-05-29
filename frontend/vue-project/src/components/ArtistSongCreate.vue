<template>
  <div class="min-h-screen flex flex-col bg-blue-100">
    <NavigationArtist :artist="artist" :dropdownVisible="dropdownVisible" @toggle-dropdown="toggleDropdown" />

    <div class="flex-1 flex">
      <SideBarArtist class="hidden lg:block" />

      <div class="flex-1 flex items-center justify-center">
        <div class="max-w-md w-full p-8 bg-white shadow-lg rounded-lg">
          <h1 class="text-3xl font-bold text-center mb-8">Create New Song</h1>

          <form @submit.prevent="createSong" class="space-y-4">
            <div class="flex flex-col sm:flex-row sm:space-x-4">
              <div class="w-full sm:w-1/2">
                <label for="title" class="font-semibold text-gray-800 mb-1">Title</label>
                <input
                  type="text"
                  v-model="newSong.title"
                  :class="{'border-red-500': errors.title}"
                  required
                  placeholder="Enter song title"
                  class="w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:border-blue-500"
                />
                <span v-if="errors.title" class="text-red-500 text-sm">{{ errors.title }}</span>
              </div>
              <div class="w-full sm:w-1/2">
                <label for="release_date" class="font-semibold text-gray-800 mb-1">Release Date</label>
                <input
                  type="date"
                  v-model="newSong.release_date"
                  :class="{'border-red-500': errors.release_date}"
                  required
                  class="w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:border-blue-500"
                />
                <span v-if="errors.release_date" class="text-red-500 text-sm">{{ errors.release_date }}</span>
              </div>
            </div>
            <div class="flex flex-col sm:flex-row sm:space-x-4">
              <div class="w-full sm:w-1/2">
                <label for="duration" class="font-semibold text-gray-800 mb-1">Duration</label>
                <input
                  type="text"
                  v-model="newSong.duration"
                  :class="{'border-red-500': errors.duration}"
                  required
                  placeholder="Enter duration"
                  class="w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:border-blue-500"
                />
                <span v-if="errors.duration" class="text-red-500 text-sm">{{ errors.duration }}</span>
              </div>
              <div class="w-full sm:w-1/2">
                <label for="language" class="font-semibold text-gray-800 mb-1">Language</label>
                <input
                  type="text"
                  v-model="newSong.language"
                  :class="{'border-red-500': errors.language}"
                  required
                  placeholder="Enter language"
                  class="w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:border-blue-500"
                />
                <span v-if="errors.language" class="text-red-500 text-sm">{{ errors.language }}</span>
              </div>
            </div>
            <div>
              <label for="lyrics" class="font-semibold text-gray-800 mb-1">Lyrics</label>
              <textarea
                v-model="newSong.lyrics"
                :class="{'border-red-500': errors.lyrics}"
                placeholder="Enter lyrics"
                class="w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:border-blue-500"
              ></textarea>
              <span v-if="errors.lyrics" class="text-red-500 text-sm">{{ errors.lyrics }}</span>
            </div>
            <button type="submit" class="w-full px-6 py-3 bg-sky-500 text-white rounded hover:bg-sky-600 focus:outline-none focus:bg-sky-600">
              Create Song
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import NavigationArtist from './NavigationArtist.vue';
import SideBarArtist from './SideBarArtist.vue';

export default {
  components: {
    NavigationArtist,
    SideBarArtist,
  },
  data() {
    return {
      artist: null,
      newSong: {
        title: '',
        release_date: '',
        duration: '',
        lyrics: '',
        language: '',
      },
      dropdownVisible: false,
      errors: {
        title: null,
        release_date: null,
        duration: null,
        lyrics: null,
        language: null,
      },
    };
  },
  created() {
    this.fetchArtistData();
  },
  methods: {
    async fetchArtistData() {
      try {
        const token = localStorage.getItem('access_token');
        const response = await axios.get('http://127.0.0.1:8000/api/artists/me/', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        this.artist = response.data;
      } catch (error) {
        console.error('Error fetching artist data:', error);
      }
    },
    async createSong() {
      if (!this.validateForm()) {
        return;
      }
      const token = localStorage.getItem('access_token');
      try {
        await axios.post('http://127.0.0.1:8000/api/song/create/', this.newSong, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        this.newSong = {
          title: '',
          release_date: '',
          duration: '',
          lyrics: '',
          language: ''
        };
        alert('Song created successfully!');
        this.$router.push({ name: 'ArtistSongs' });
      } catch (error) {
        console.error('Error creating song:', error);
        if (error.response && error.response.data) {
          this.errors = error.response.data;
        } else {
          alert('Failed to create song. Please try again.');
        }
      }
    },
    toggleDropdown() {
      this.dropdownVisible = !this.dropdownVisible;
    },
    validateForm() {
      this.errors = {
        title: null,
        release_date: null,
        duration: null,
        lyrics: null,
        language: null,
      };

      let isValid = true;

      if (!this.newSong.title) {
        this.errors.title = 'Title is required';
        isValid = false;
      }

      if (!this.newSong.release_date) {
        this.errors.release_date = 'Release date is required';
        isValid = false;
      }

      if (!this.newSong.duration) {
        this.errors.duration = 'Duration is required';
        isValid = false;
      }

      if (!this.newSong.language) {
        this.errors.language = 'Language is required';
        isValid = false;
      }

      if (!this.newSong.lyrics) {
        this.errors.lyrics = 'Lyrics are required';
        isValid = false;
      }

      return isValid;
    },
  },
};
</script>

<style scoped>
/* Add your styles here */
</style>

