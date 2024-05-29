<template>
    <nav class="bg-cyan-100">
      <div class="max-w-7xl mx-auto">
        <div class="flex items-center justify-between h-16">
          <div class="flex items-center">
            <router-link to="/login" class="text-xl font-bold text-indigo-600">Home</router-link>
          </div>
          <div>
            <router-link to="/login" class="text-gray-800 hover:text-indigo-600 mx-8">Login</router-link>
            <router-link to="/signup" class="text-gray-800 hover:text-indigo-600 mx-9">Signup</router-link>
          </div>
        </div>
      </div>
    </nav>
  </template>
  <script>
  export default {
    name: 'NavLogin',
  };
  </script>
  
  <style scoped>

  </style>
  