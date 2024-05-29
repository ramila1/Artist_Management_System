<template>
  <div class="min-h-screen flex flex-col bg-blue-100">
    <Navigation :admin="admin" :dropdownVisible="dropdownVisible" @toggle-dropdown="toggleDropdown" />
    <div class="flex-1 flex">
      <SideBar class="hidden lg:block" />
      <div class="flex-1 flex flex-col items-center justify-start">
        <h1 class="text-3xl font-bold mb-8 text-gray-700 text-center mt-10">Manage Artists</h1>
        <div v-if="loading" class="text-center text-gray-600">Loading...</div>
        <div v-if="error" class="text-center text-red-500">{{ error }}</div>
        <div class="max-w-screen-lg w-full mt-10">
          <table v-if="artists.length" class="table-auto bg-white shadow-md rounded-lg overflow-hidden w-full mx-auto">
            <thead>
              <tr class="bg-gray-100">
                <th class="px-4 py-2 text-left">ID</th>
                <th class="px-4 py-2 text-left">Email</th>
                <th class="px-4 py-2 text-left">First Name</th>
                <th class="px-4 py-2 text-left">Last Name</th>
                <th class="px-4 py-2 text-left">Date of Birth</th>
                <th class="px-4 py-2 text-left">Gender</th>
                <th class="px-4 py-2 text-left">Address</th>
                <th class="px-4 py-2 text-left">Country</th>
                <th class="px-4 py-2 text-left">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="artist in artists" :key="artist.id" class="border-b border-gray-200">
                <td class="px-4 py-2">{{ artist.id }}</td>
                <td class="px-4 py-2">{{ artist.email }}</td>
                <td class="px-4 py-2">{{ artist.first_name }}</td>
                <td class="px-4 py-2">{{ artist.last_name }}</td>
                <td class="px-4 py-2">{{ artist.date_of_birth }}</td>
                <td class="px-4 py-2">{{ artist.gender }}</td>
                <td class="px-4 py-2">{{ artist.address }}</td>
                <td class="px-4 py-2">{{ artist.country }}</td>
                <td class="px-4 py-2 flex space-x-2">
                  <button @click="openEditModal(artist)" class="bg-gray-800 hover:bg-gray-700 text-white py-1 px-4 rounded">Edit</button>
                  <button @click="deleteArtist(artist.id)" class="bg-gray-800 hover:bg-gray-700 text-white py-1 px-4 rounded">Delete</button>
                </td>
              </tr>
            </tbody>
          </table>
          <p v-else class="text-center text-gray-600 mt-4">No artists found</p>
        </div>
        <div v-if="showEditModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
          <div class="bg-white shadow-md rounded-lg overflow-hidden w-full max-w-lg mx-auto p-6 relative">
            <span @click="closeEditModal" class="absolute top-3 right-3 cursor-pointer text-gray-800 text-2xl">&times;</span>
            <h2 class="text-2xl font-bold mb-4 text-gray-700">Edit Artist</h2>
            <form @submit.prevent="updateArtist" class="space-y-4">
              <div class="space-y-4">
                <div>
                  <label for="email" class="text-gray-700">Email:</label>
                  <input type="email" v-model="editForm.email" required class="w-full px-3 py-1 border border-gray-300 rounded">
                  <span v-if="errors.email" class="text-red-500 text-sm">{{ errors.email }}</span>
                </div>
                <div>
                  <label for="first_name" class="text-gray-700">First Name:</label>
                  <input type="text" v-model="editForm.first_name" required class="w-full px-3 py-1 border border-gray-300 rounded">
                  <span v-if="errors.first_name" class="text-red-500 text-sm">{{ errors.first_name }}</span>
                </div>
                <div>
                  <label for="last_name" class="text-gray-700">Last Name:</label>
                  <input type="text" v-model="editForm.last_name" required class="w-full px-3 py-1 border border-gray-300 rounded">
                  <span v-if="errors.last_name" class="text-red-500 text-sm">{{ errors.last_name }}</span>
                </div>
                <div>
                  <label for="date_of_birth" class="text-gray-700">Date of Birth:</label>
                  <input type="date" v-model="editForm.date_of_birth" required class="w-full px-3 py-1 border border-gray-300 rounded">
                  <span v-if="errors.date_of_birth" class="text-red-500 text-sm">{{ errors.date_of_birth }}</span>
                </div>
                <div>
                  <label for="gender" class="text-gray-700">Gender:</label>
                  <select v-model="editForm.gender" required class="w-full px-3 py-1 border border-gray-300 rounded">
                    <option value="" disabled>Select your gender</option>
                    <option value="male">Male</option>
                    <option value="female">Female</option>
                    <option value="other">Other</option>
                  </select>
                  <span v-if="errors.gender" class="text-red-500 text-sm">{{ errors.gender }}</span>
                </div>
                <div>
                  <label for="address" class="text-gray-700">Address:</label>
                  <input type="text" v-model="editForm.address" required class="w-full px-3 py-1 border border-gray-300 rounded">
                  <span v-if="errors.address" class="text-red-500 text-sm">{{ errors.address }}</span>
                </div>
                <div>
                  <label for="country" class="text-gray-700">Country:</label>
                  <input type="text" v-model="editForm.country" required class="w-full px-3 py-1 border border-gray-300 rounded">
                  <span v-if="errors.country" class="text-red-500 text-sm">{{ errors.country }}</span>
                </div>
              </div>
              <div class="flex justify-end">
                <button type="submit" class="bg-gray-800 hover:bg-gray-700 text-white py-2 px-4 rounded">Update</button>
              </div>
            </form>
          </div>
        </div>
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
  name: 'ManageArtists',
  data() {
    return {
      artists: [],
      loading: false,
      error: null,
      showEditModal: false,
      dropdownVisible: false,
      editForm: {
        id: '',
        email: '',
        first_name: '',
        last_name: '',
        date_of_birth: '',
        gender: '',
        address: '',
        country: ''
      },
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
    this.fetchArtists();
    this.fetchAdminData();
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

    async openEditModal(artist) {
      this.editForm = { ...artist };
      this.showEditModal = true;
    },

    closeEditModal() {
      this.showEditModal = false;
    },

    async updateArtist() {
      if (!this.validateForm()) {
        return;
      }

      try {
        const token = localStorage.getItem('access_token');
        const response = await axios.put(`http://127.0.0.1:8000/api/artists/${this.editForm.id}/`, this.editForm, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        const updatedArtist = response.data;
        this.artists = this.artists.map((artist) => (artist.id === updatedArtist.id ? updatedArtist : artist));
        this.closeEditModal();
        alert('Artist updated successfully');
      } catch (error) {
        alert('Failed to update artist');
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

          this.artists = this.artists.filter((artist) => artist.id !== artistId);
          alert('Artist deleted successfully');
        } catch (error) {
          alert('Failed to delete artist');
        }
      }
    },

    toggleDropdown() {
      this.dropdownVisible = !this.dropdownVisible;
    },

    validateForm() {
      this.errors.email = this.errors.first_name = this.errors.last_name = this.errors.date_of_birth = this.errors.gender = this.errors.address = this.errors.country = null;

      let isValid = true;

      if (!this.editForm.email) {
        this.errors.email = 'Email is required';
        isValid = false;
      } else if (!/\S+@\S+\.\S+/.test(this.editForm.email)) {
        this.errors.email = 'Email must be valid';
        isValid = false;
      }

      if (!this.editForm.first_name) {
        this.errors.first_name = 'First Name is required';
        isValid = false;
      }

      if (!this.editForm.last_name) {
        this.errors.last_name = 'Last Name is required';
        isValid = false;
      }

      if (!this.editForm.date_of_birth) {
        this.errors.date_of_birth = 'Date of Birth is required';
        isValid = false;
      }

      if (!this.editForm.gender) {
        this.errors.gender = 'Gender is required';
        isValid = false;
      }

      if (!this.editForm.address) {
        this.errors.address = 'Address is required';
        isValid = false;
      }

      if (!this.editForm.country) {
        this.errors.country = 'Country is required';
        isValid = false;
      }

      return isValid;
    },
  },
};
</script>
<style></style>