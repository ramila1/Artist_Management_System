<template>
    <div>
      <h1>Artists and Their Songs</h1>
      <div v-if="loading">Loading...</div>
      <div v-if="error">{{ error }}</div>
      <div v-if="artists.length">
        <div v-for="artist in artists" :key="artist.id" class="artist">
          <h2>{{ artist.first_name }} {{ artist.last_name }}</h2>
          <ul>
            <li v-for="song in artist.songs" :key="song.id">{{ song.title }}</li>
          </ul>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'AdminArtistPanel',
    data() {
      return {
        artists: [],
        loading: false,
        error: null,
      };
    },
    created() {
      this.fetchArtistsAndSongs();
    },
    methods: {
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
  
          // Fetch songs for each artist
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
    },
  };
  </script>
  
  <style scoped>
  .artist {
    margin-bottom: 20px;
  }
  
  .artist h2 {
    margin: 0;
  }
  
  .artist ul {
    list-style-type: none;
    padding: 0;
  }
  
  .artist ul li {
    margin: 5px 0;
  }
  </style>
  