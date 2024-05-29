<template>
    <nav class="bg-cyan-100 text-black p-4 flex justify-between items-center">
      <span class="text-xl font-bold"></span>
      <div @click="toggleDropdown" class="relative cursor-pointer">
        <span v-if="artist" class="text-xl font-bold">{{ artist.first_name }} {{ artist.last_name }}</span>
        <ul v-if="dropdownVisible" class="absolute right-0 mt-2 bg-white border border-gray-300 rounded shadow-lg w-48">
          <li>
            <router-link to="/artist_account" class="block px-4 py-2 text-black hover:bg-gray-200">My Account</router-link>
          </li>
          <li>
            <a @click="logout" class="block px-4 py-2 text-black hover:bg-gray-200 cursor-pointer">Logout</a>
          </li>
        </ul>
      </div>
    </nav>
  </template>
  
  <script>
  import axios from 'axios';
  export default {
    props: ['artist', 'dropdownVisible'],
    methods: {
      toggleDropdown() {
        this.$emit('toggle-dropdown');
      },
      async logout() {
        localStorage.removeItem('access_token');
        this.$router.push('/login');
      }
    }
  };
  </script>
  
  <style scoped>

  </style>
  