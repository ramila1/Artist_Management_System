<template>
    <div>
      <h1>My Account</h1>
      <div v-if="loading">Loading...</div>
      <div v-if="error">{{ error }}</div>
      <div v-if="artist">
        <p>Email: {{ artist.email }}</p>
        <!-- <p>First Name: {{ artist.first_name }}</p>
        <p>Last Name: {{ artist.last_name }}</p>
        <p>Date of Birth: {{ artist.date_of_birth }}</p>
        <p>Gender: {{ artist.gender }}</p>
        <p>Address: {{ artist.address }}</p>
        <p>Country: {{ artist.country }}</p> -->
        <p>Created At: {{ artist.created_at }}</p>
        <p>Updated At: {{ artist.updated_at }}</p>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'AdminAccount',
    data() {
      return {
        artist: null,
        loading: false,
        error: null,
      };
    },
    created() {
      this.fetchArtistData();
    },
    methods: {
      async fetchArtistData() {
        this.loading = true;
        this.error = null;
        try {
        const token = localStorage.getItem('access_token');
          const response = await axios.get('http://127.0.0.1:8000/api/only/admin/', {
            headers: {
              Authorization: `Bearer ${token}`
            }
          });
          this.artist = response.data;
        } catch (error) {
          this.error = 'Failed to load artist data';
        } finally {
          this.loading = false;
        }
      }
    }
  };
  </script>
  
  <style scoped>

  </style>
  