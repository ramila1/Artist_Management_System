<template>
    <div>
      <h1>Manage Artists</h1>
      
      <div v-if="loading">Loading...</div>
      <div v-if="error">{{ error }}</div>
  
      <table v-if="artists.length" class="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Email</th>
            <th>First Name</th>
            <th>Last Name</th>
            <th>Date of Birth</th>
            <th>Gender</th>
            <th>Address</th>
            <th>Country</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="artist in artists" :key="artist.id">
            <td>{{ artist.id }}</td>
            <td>{{ artist.email }}</td>
            <td>{{ artist.first_name }}</td>
            <td>{{ artist.last_name }}</td>
            <td>{{ artist.date_of_birth }}</td>
            <td>{{ artist.gender }}</td>
            <td>{{ artist.address }}</td>
            <td>{{ artist.country }}</td>
            <td>
              <router-link :to="'/edit_artist/' + artist.id">Edit</router-link>
              <button @click="deleteArtist(artist.id)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'ManageArtists',
    data() {
      return {
        artists: [],
        loading: false,
        error: null,
      };
    },
    created() {
      this.fetchArtists();
    },
    methods: {
      async fetchArtists() {
        this.loading = true;
        this.error = null;
        try {
          const token = localStorage.getItem('access_token'); 
          const response = await axios.get('http://127.0.0.1:8000/api/only/artists/', {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          this.artists = response.data;
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
      async deleteArtist(artistId) {
        if (confirm('Are you sure you want to delete this artist?')) {
          try {
            const token = localStorage.getItem('access_token'); 
            await axios.delete(`http://127.0.0.1:8000/api/artists/${artistId}/`, {
              headers: {
                Authorization: `Bearer ${token}`,
              },
            });
          
            this.artists = this.artists.filter(artist => artist.id !== artistId);
            alert('Artist deleted successfully');
          } catch (error) {
            alert('Failed to delete artist');
          }
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .table {
    width: 100%;
    border-collapse: collapse;
  }
  
  .table th,
  .table td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
  }
  
  .table th {
    background-color: #f2f2f2;
  }
  </style>
  