<template>
  <div class="min-h-screen flex flex-col bg-blue-100">
    <NavigationArtist :artist="artist" :dropdownVisible="dropdownVisible" @toggle-dropdown="toggleDropdown" />

    <div class="flex-1 flex">
      <SideBarArtist class="hidden lg:block" />

      <div class="flex-1 justify-center items-center mt-10">
        <div class="w-full max-w-md p-6 bg-white shadow-lg rounded-lg mx-auto">
          <div class="flex justify-between items-center mb-4">
            <h1 class="text-2xl font-bold">My Account</h1>
            <div>
              <button @click="editProfile" class="bg-gray-500 text-white px-3 py-1 rounded-md hover:bg-gray-600">Edit</button>
              <button @click="deleteProfile(artist.id)" class="bg-gray-500 text-white px-3 py-1 rounded-md hover:bg-gray-600 ml-2">Delete</button>
            </div>
          </div>
          <div v-if="loading" class="text-center text-gray-600 mt-4">Loading...</div>
          <div v-if="error" class="text-center text-red-600 mt-4">{{ error }}</div>

          <div v-if="artist" class="space-y-2 mt-4">
            <div class="text-lg"><strong>Email:</strong> {{ artist.email }}</div>
            <div class="text-lg"><strong>First Name:</strong> {{ artist.first_name }}</div>
            <div class="text-lg"><strong>Last Name:</strong> {{ artist.last_name }}</div>
            <div class="text-lg"><strong>Date of Birth:</strong> {{ artist.date_of_birth }}</div>
            <div class="text-lg"><strong>Gender:</strong> {{ artist.gender }}</div>
            <div class="text-lg"><strong>Address:</strong> {{ artist.address }}</div>
            <div class="text-lg"><strong>Country:</strong> {{ artist.country }}</div>
          </div>
          <div v-if="editing" class="fixed inset-0 flex items-center justify-center bg-gray-800 bg-opacity-50">
            <div class="bg-white p-4 rounded-md w-full max-w-md shadow-lg relative">
              <span @click="cancelEdit" class="absolute top-2 right-2 text-gray-600 cursor-pointer text-xl">&times;</span>
              <h3 class="text-2xl font-bold mb-2">Edit Profile</h3>
              <form @submit.prevent="updateProfile">
                <div class="mb-3">
                  <label for="email" class="block mb-1 font-bold">Email</label>
                  <input type="email" v-model="editedArtist.email" required class="w-full border-gray-300 rounded-md px-2 py-1" :class="{ 'border-red-500': errors.email }">
                  <p v-if="errors.email" class="text-red-500 text-sm mt-1">{{ errors.email }}</p>
                </div>
                <div class="mb-3">
                  <label for="first_name" class="block mb-1 font-bold">First Name</label>
                  <input type="text" v-model="editedArtist.first_name" required class="w-full border-gray-300 rounded-md px-2 py-1" :class="{ 'border-red-500': errors.first_name }">
                  <p v-if="errors.first_name" class="text-red-500 text-sm mt-1">{{ errors.first_name }}</p>
                </div>
                <div class="mb-3">
                  <label for="last_name" class="block mb-1 font-bold">Last Name</label>
                  <input type="text" v-model="editedArtist.last_name" required class="w-full border-gray-300 rounded-md px-2 py-1" :class="{ 'border-red-500': errors.last_name }">
                  <p v-if="errors.last_name" class="text-red-500 text-sm mt-1">{{ errors.last_name }}</p>
                </div>
                <div class="mb-3">
                  <label for="date_of_birth" class="block mb-1 font-bold">Date of Birth</label>
                  <input type="date" v-model="editedArtist.date_of_birth" required class="w-full border-gray-300 rounded-md px-2 py-1" :class="{ 'border-red-500': errors.date_of_birth }">
                  <p v-if="errors.date_of_birth" class="text-red-500 text-sm mt-1">{{ errors.date_of_birth }}</p>
                </div>
                <div class="mb-3">
                  <label for="gender" class="block mb-1 font-bold">Gender</label>
                  <input type="text" v-model="editedArtist.gender" required class="w-full border-gray-300 rounded-md px-2 py-1" :class="{ 'border-red-500': errors.gender }">
                  <p v-if="errors.gender" class="text-red-500 text-sm mt-1">{{ errors.gender }}</p>
                </div>
                <div class="mb-3">
                  <label for="address" class="block mb-1 font-bold">Address</label>
                  <input type="text" v-model="editedArtist.address" required class="w-full border-gray-300 rounded-md px-2 py-1" :class="{ 'border-red-500': errors.address }">
                  <p v-if="errors.address" class="text-red-500 text-sm mt-1">{{ errors.address }}</p>
                </div>
                <div class="mb-3">
                  <label for="country" class="block mb-1 font-bold">Country</label>
                  <input type="text" v-model="editedArtist.country" required class="w-full border-gray-300 rounded-md px-2 py-1" :class="{ 'border-red-500': errors.country }">
                  <p v-if="errors.country" class="text-red-500 text-sm mt-1">{{ errors.country }}</p>
                </div>
                <button type="submit" class="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600 w-full">Update</button>
              </form>
            </div>
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
import router from '../router';  

export default {
  components: {
    NavigationArtist,
    SideBarArtist,
  },
  name: 'ArtistAccount',
  data() {
    return {
      artist: null,
      editedArtist: null,
      loading: false,
      error: null,
      editing: false,
      dropdownVisible: false,
      errors: {
        email: null,
        first_name: null,
        last_name: null,
        date_of_birth: null,
        gender: null,
        address: null,
        country: null,
      },
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
        const response = await axios.get('http://127.0.0.1:8000/api/artists/me/', {
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
    },
    editProfile() {
      this.editedArtist = { ...this.artist };
      this.editing = true;
    },
    cancelEdit() {
      this.editing = false;
      this.editedArtist = null;
      this.fetchArtistData();
    },
    async updateProfile() {
      if (!this.validateForm()) {
        return;
      }

      const token = localStorage.getItem('access_token');
      try {
        await axios.put(`http://127.0.0.1:8000/api/artists/${this.artist.id}/`, this.editedArtist, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        this.artist = { ...this.editedArtist };
        this.editing = false;
        this.fetchArtistData();
        alert('Profile updated successfully!');
      } catch (error) {
        console.error('Error updating profile:', error);
        alert('Failed to update profile. Please try again.');
      }
    },
    async deleteProfile(artistId) {
      if (confirm('Are you sure you want to delete this artist?')) {
        try {
          const token = localStorage.getItem('access_token');
          await axios.delete(`http://127.0.0.1:8000/api/artists/${artistId}/`, {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          alert('Artist deleted successfully');
          localStorage.removeItem('access_token');
          localStorage.removeItem('user');  
    
          router.push('/login');
        } catch (error) {
          console.error('Failed to delete artist:', error);
          this.error = 'Failed to delete artist'; 
        }
      }
    },
    toggleDropdown() {
      this.dropdownVisible
    },
    toggleDropdown() {
      this.dropdownVisible = !this.dropdownVisible;
    },
    validateForm() {
      this.errors = {
        email: null,
        first_name: null,
        last_name: null,
        date_of_birth: null,
        gender: null,
        address: null,
        country: null,
      };

      let isValid = true;

      if (!this.editedArtist.email) {
        this.errors.email = 'Email is required';
        isValid = false;
      }
      if (!this.editedArtist.first_name) {
        this.errors.first_name = 'First name is required';
        isValid = false;
      }
      if (!this.editedArtist.last_name) {
        this.errors.last_name = 'Last name is required';
        isValid = false;
      }
      if (!this.editedArtist.date_of_birth) {
        this.errors.date_of_birth = 'Date of birth is required';
        isValid = false;
      }
      if (!this.editedArtist.gender) {
        this.errors.gender = 'Gender is required';
        isValid = false;
      }
      if (!this.editedArtist.address) {
        this.errors.address = 'Address is required';
        isValid = false;
      }
      if (!this.editedArtist.country) {
        this.errors.country = 'Country is required';
        isValid = false;
      }

      return isValid;
    },
  },
};
</script>

<style scoped>

</style>







