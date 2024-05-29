<template>
  <div class="min-h-screen flex flex-col bg-blue-100">
    <Navigation :admin="admin" :dropdownVisible="dropdownVisible" @toggle-dropdown="toggleDropdown" />

    <div class="flex-1 flex"> 
      <SideBar class="hidden lg:block" />
      <div class="w-full max-w-md mx-auto bg-white shadow-lg rounded-lg p-6 mt-10 mb-14">
        <div class="flex justify-between items-center mb-6">
          <h1 class="text-3xl font-bold text-center">My Account</h1>
          <div class="flex space-x-4">
            <button @click="editProfile" class="bg-gray-500 text-white px-4 py-2 rounded-md hover:bg-gray-500">Edit</button>
            <button @click="deleteProfile" class="bg-gray-500 text-white px-4 py-2 rounded-md hover:bg-gray-500">Delete</button>
          </div>
        </div>
      
        <div v-if="loading" class="text-center text-gray-600">Loading...</div>
        <div v-if="error" class="text-center text-red-600">{{ error }}</div>
        
        <div v-if="admin" class="space-y-4">
          <div class="text-lg"><strong>Email:</strong> {{ admin.email }}</div>
          <div class="text-lg"><strong>First Name:</strong> {{ admin.first_name }}</div>
          <div class="text-lg"><strong>Last Name:</strong> {{ admin.last_name }}</div>
          <div class="text-lg"><strong>Date of Birth:</strong> {{ admin.date_of_birth }}</div>
          <div class="text-lg"><strong>Gender:</strong> {{ admin.gender }}</div>
          <div class="text-lg"><strong>Address:</strong> {{ admin.address }}</div>
          <div class="text-lg"><strong>Country:</strong> {{ admin.country }}</div>
          <div class="text-lg"><strong>Created At:</strong> {{ admin.created_at }}</div>
          <div class="text-lg"><strong>Updated At:</strong> {{ admin.updated_at }}</div>
        </div>

        <div v-if="editing" class="fixed inset-0 flex items-center justify-center bg-gray-800 bg-opacity-50">
          <div class="bg-white p-6 rounded-md w-full max-w-md shadow-lg relative">
            <span @click="cancelEdit" class="absolute top-2 right-2 text-gray-600 cursor-pointer text-xl">&times;</span>
            <h3 class="text-2xl font-bold mb-4">Edit Profile</h3>
            <form @submit.prevent="updateProfile">
              <div class="mb-4">
                <label for="email" class="block mb-1 font-bold">Email</label>
                <input
                  type="email"
                  v-model="editedAdmin.email"
                  class="w-full border-gray-300 rounded-md px-3 py-2"
                  :class="{'border-red-500': errors.email}"
                  required
                />
                <div v-if="errors.email" class="text-red-600 text-sm">{{ errors.email }}</div>
              </div>
              <div class="mb-4">
                <label for="first_name" class="block mb-1 font-bold">First Name</label>
                <input
                  type="text"
                  v-model="editedAdmin.first_name"
                  class="w-full border-gray-300 rounded-md px-3 py-2"
                  :class="{'border-red-500': errors.first_name}"
                  required
                />
                <div v-if="errors.first_name" class="text-red-600 text-sm">{{ errors.first_name }}</div>
              </div>
              <div class="mb-4">
                <label for="last_name" class="block mb-1 font-bold">Last Name</label>
                <input
                  type="text"
                  v-model="editedAdmin.last_name"
                  class="w-full border-gray-300 rounded-md px-3 py-2"
                  :class="{'border-red-500': errors.last_name}"
                  required
                />
                <div v-if="errors.last_name" class="text-red-600 text-sm">{{ errors.last_name }}</div>
              </div>
              <div class="mb-4">
                <label for="date_of_birth" class="block mb-1 font-bold">Date of Birth</label>
                <input
                  type="date"
                  v-model="editedAdmin.date_of_birth"
                  class="w-full border-gray-300 rounded-md px-3 py-2"
                  :class="{'border-red-500': errors.date_of_birth}"
                  required
                />
                <div v-if="errors.date_of_birth" class="text-red-600 text-sm">{{ errors.date_of_birth }}</div>
              </div>
              <div class="mb-4">
                <label for="gender" class="block mb-1 font-bold">Gender</label>
                <input
                  type="text"
                  v-model="editedAdmin.gender"
                  class="w-full border-gray-300 rounded-md px-3 py-2"
                  :class="{'border-red-500': errors.gender}"
                  required
                />
                <div v-if="errors.gender" class="text-red-600 text-sm">{{ errors.gender }}</div>
              </div>
              <div class="mb-4">
                <label for="address" class="block mb-1 font-bold">Address</label>
                <input
                  type="text"
                  v-model="editedAdmin.address"
                  class="w-full border-gray-300 rounded-md px-3 py-2"
                  :class="{'border-red-500': errors.address}"
                  required
                />
                <div v-if="errors.address" class="text-red-600 text-sm">{{ errors.address }}</div>
              </div>
              <div class="mb-4">
                <label for="country" class="block mb-1 font-bold">Country</label>
                <input
                  type="text"
                  v-model="editedAdmin.country"
                  class="w-full border-gray-300 rounded-md px-3 py-2"
                  :class="{'border-red-500': errors.country}"
                  required
                />
                <div v-if="errors.country" class="text-red-600 text-sm">{{ errors.country }}</div>
              </div>
              <button type="submit" class="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600 w-full">Update Profile</button>
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
  name: 'AdminAccount',
  data() {
    return {
      admin: null,
      editedAdmin: null,
      loading: false,
      error: null,
      editing: false,
      dropdownVisible: false,
      errors: {},
    };
  },
  created() {
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
    editProfile() {
      this.editedAdmin = { ...this.admin };
      this.editing = true;
      this.errors = {};
    },
    cancelEdit() {
      this.editing = false;
      this.editedAdmin = null;
      this.fetchAdminData();
    },
    validateForm() {
      this.errors = {};
      if (!this.editedAdmin.email) {
        this.errors.email = 'Email is required';
      } else if (!this.validEmail(this.editedAdmin.email)) {
        this.errors.email = 'Invalid email format';
      }
      if (!this.editedAdmin.first_name) {
        this.errors.first_name = 'First name is required';
      }
      if (!this.editedAdmin.last_name) {
        this.errors.last_name = 'Last name is required';
      }
      if (!this.editedAdmin.date_of_birth) {
        this.errors.date_of_birth = 'Date of birth is required';
      }
      if (!this.editedAdmin.gender) {
        this.errors.gender = 'Gender is required';
      }
      if (!this.editedAdmin.address) {
        this.errors.address = 'Address is required';
      }
      if (!this.editedAdmin.country) {
        this.errors.country = 'Country is required';
      }
      return Object.keys(this.errors).length === 0;
    },
    validEmail(email) {
      const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@(([^<>()[\]\\.,;:\s@"]+\.)+[^<>()[\]\\.,;:\s@"]{2,})$/i;
      return re.test(email);
    },
    async updateProfile() {
      if (this.validateForm()) {
        const token = localStorage.getItem('access_token');
        try {
          await axios.put(`http://127.0.0.1:8000/api/artists/${this.admin.id}/`, this.editedAdmin, {
            headers: {
              Authorization: `Bearer ${token}`
            }
          });
          this.admin = { ...this.editedAdmin };
          this.editing = false;
          this.fetchAdminData();
          this.$toast.success('Profile updated successfully!');
        } catch (error) {
          console.error('Error updating profile:', error);
          this.$toast.error('Failed to update profile. Please try again.');
        }
      } else {
        this.$toast.error('Please correct the errors in the form.');
      }
    },
    async deleteProfile() {
      const token = localStorage.getItem('access_token');
      if (confirm('Are you sure you want to delete your profile? This action cannot be undone.')) {
        try {
          await axios.delete(`http://127.0.0.1:8000/api/artists/${this.admin.id}/`, {
            headers: {
              Authorization: `Bearer ${token}`
            }
          });
          this.$toast.success('Profile deleted successfully!');
          this.$router.push('/login');
        } catch (error) {
          console.error('Error deleting profile:', error);
          this.$toast.error('Failed to delete profile. Please try again.');
        }
      }
    },
    toggleDropdown() {
      this.dropdownVisible = !this.dropdownVisible;
    }
  }
};
</script>
