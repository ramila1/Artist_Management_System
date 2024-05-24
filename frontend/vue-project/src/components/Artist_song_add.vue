<template>
  <div class="flex justify-center items-center h-screen bg-gradient-to-br from-purple-500 via-pink-500 to-red-500">
    <div class="artist-page max-w-3xl w-full sm:w-3/4 lg:w-1/2 xl:w-1/3 p-8 bg-white shadow-lg rounded-lg">
      <h1 class="text-3xl font-bold text-center mb-8">Create New Song</h1>
      <form @submit.prevent="createSong" class="space-y-4">
        <div class="flex flex-col sm:flex-row sm:space-x-4">
          <div class="w-full sm:w-1/2">
            <label for="title" class="font-semibold text-gray-800 mb-1">Title</label>
            <input type="text" v-model="newSong.title" required placeholder="Enter song title" class="w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:border-blue-500">
          </div>
          <div class="w-full sm:w-1/2">
            <label for="release_date" class="font-semibold text-gray-800 mb-1">Release Date</label>
            <input type="date" v-model="newSong.release_date" required class="w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:border-blue-500">
          </div>
        </div>
        <div class="flex flex-col sm:flex-row sm:space-x-4">
          <div class="w-full sm:w-1/2">
            <label for="duration" class="font-semibold text-gray-800 mb-1">Duration</label>
            <input type="text" v-model="newSong.duration" required placeholder="Enter duration" class="w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:border-blue-500">
          </div>
          <div class="w-full sm:w-1/2">
            <label for="language" class="font-semibold text-gray-800 mb-1">Language</label>
            <input type="text" v-model="newSong.language" required placeholder="Enter language" class="w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:border-blue-500">
          </div>
        </div>
        <div>
          <label for="lyrics" class="font-semibold text-gray-800 mb-1">Lyrics</label>
          <textarea v-model="newSong.lyrics" placeholder="Enter lyrics" class="w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:border-blue-500"></textarea>
        </div>
        <button type="submit" class="w-full px-6 py-3 bg-purple-500 text-white rounded hover:bg-purple-600 focus:outline-none focus:bg-purple-600">Create Song</button>
      </form>

      <button @click="showMySongs" class="w-full mt-4 px-6 py-3 bg-pink-500 text-white rounded hover:bg-pink-600 focus:outline-none focus:bg-pink-600">Show My Songs</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      newSong: {
        title: '',
        release_date: '',
        duration: '',
        lyrics: '',
        language: ''
      }
    };
  },
  methods: {
    createSong() {
      const user = JSON.parse(localStorage.getItem('user'));
      const token = localStorage.getItem('access_token');
      this.newSong.artist = user.id;

      axios
        .post('http://127.0.0.1:8000/api/song/create/', this.newSong, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        })
        .then(response => {
          this.newSong = {
            title: '',
            release_date: '',
            duration: '',
            lyrics: '',
            language: ''
          };
          alert('Song created successfully!');
        })
        .catch(error => {
          console.error('Error creating song:', error);
          alert('Failed to create song. Please try again.');
        });
    },
    showMySongs() {
      this.$router.push({ name: 'ArtistSongs' });
    }
  }
};
</script>

<style scoped>

</style>
