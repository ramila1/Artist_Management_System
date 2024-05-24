<template>
    <div class="artist-songs">

      <h2 class="text-center text-xl font-bold mb-4">My Songs</h2>
      <ul v-if="mySongs.length" class="space-y-4">
        <li v-for="song in mySongs" :key="song.id" class="bg-white p-4 rounded shadow-md">
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
          <button @click="toggleLyrics(song)" class="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600">Show Lyrics</button>
          <p v-if="song.showLyrics" class="mt-2"><strong class="font-bold">Lyrics:</strong> {{ song.lyrics }}</p>
          <button @click="editSong(song)" class="bg-green-500 text-white px-4 py-2 rounded-md hover:bg-green-600">Edit</button>
          <button @click="deleteSong(song.id)" class="bg-red-500 text-white px-4 py-2 rounded-md hover:bg-red-600">Delete</button>
        </li>
      </ul>
      <p v-else class="text-center">No songs found.</p>
  

      <div v-if="editingSong" class="fixed inset-0 flex items-center justify-center bg-gray-800 bg-opacity-50">
        <div class="bg-white p-4 rounded-md w-96">
          <span @click="cancelEdit" class="absolute top-0 right-0 cursor-pointer p-2">&times;</span>
          <h3 class="text-lg font-bold mb-4">Edit Song</h3>
          <form @submit.prevent="updateSong">
            <div class="mb-4">
              <label for="title" class="block mb-1 font-bold">Title</label>
              <input type="text" v-model="editingSong.title" required class="w-full border-gray-300 rounded-md px-3 py-2">
            </div>
            <div class="mb-4">
              <label for="release_date" class="block mb-1 font-bold">Release Date</label>
              <input type="date" v-model="editingSong.release_date" required class="w-full border-gray-300 rounded-md px-3 py-2">
            </div>
            <div class="mb-4">
              <label for="duration" class="block mb-1 font-bold">Duration</label>
              <input type="text" v-model="editingSong.duration" required class="w-full border-gray-300 rounded-md px-3 py-2">
            </div>
            <div class="mb-4">
              <label for="lyrics" class="block mb-1 font-bold">Lyrics</label>
              <textarea v-model="editingSong.lyrics" class="w-full border-gray-300 rounded-md px-3 py-2"></textarea>
            </div>
            <div class="mb-4">
              <label for="language" class="block mb-1 font-bold">Language</label>
              <input type="text" v-model="editingSong.language" required class="w-full border-gray-300 rounded-md px-3 py-2">
            </div>
            <button type="submit" class="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600">Update Song</button>
          </form>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        mySongs: [],
        editingSong: null,
      };
    },
    created() {
      this.fetchMySongs();
    },
    methods: {
      fetchMySongs() {
        const user = JSON.parse(localStorage.getItem('user'));
        const token = localStorage.getItem('access_token');
        axios
          .get(`http://127.0.0.1:8000/api/songs/user/${user.id}/`, {
            headers: {
              Authorization: `Bearer ${token}`
            }
          })
          .then(response => {
            this.mySongs = response.data.map(song => ({ ...song, showLyrics: false }));
          })
          .catch(error => {
            console.error('Error fetching my songs:', error);
          });
      },
      toggleLyrics(song) {
        song.showLyrics = !song.showLyrics;
      },
      editSong(song) {
        this.editingSong = { ...song };
      },
      cancelEdit() {
        this.editingSong = null;
      },
      updateSong() {
        const token = localStorage.getItem('access_token');
        axios
          .put(`http://127.0.0.1:8000/api/song/${this.editingSong.id}/`, this.editingSong, {
            headers: {
              Authorization: `Bearer ${token}`
            }
          })
          .then(response => {
            this.fetchMySongs();
            this.editingSong = null;
            alert('Song updated successfully!');
          })
          .catch(error => {
            console.error('Error updating song:', error);
            alert('Failed to update song. Please try again.');
          });
      },
      deleteSong(songId) {
        const token = localStorage.getItem('access_token');
        axios
          .delete(`http://127.0.0.1:8000/api/song/${songId}/`, {
            headers: {
              Authorization: `Bearer ${token}`
            }
          })
          .then(response => {
            this.fetchMySongs();
            alert('Song deleted successfully!');
          })
          .catch(error => {
            console.error('Error deleting song:', error);
            alert('Failed to delete song. Please try again.');
          });
      }
    }
  };
  </script>
  
  <style scoped>

  </style>