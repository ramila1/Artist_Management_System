<template>
    <div class="w-full sm:w-1/4 lg:w-1/6 bg-cyan-950 text-white p-4">
      <nav>
        <ul class="space-y-4">
          <li>
            <router-link to="/admin" class="block text-lg font-bold">Home</router-link>
          </li>

          <li>
            <router-link to="/manage_artists" class="block text-lg font-bold">Manage Artist</router-link>
          </li>
          <li>
            <router-link to="/all_songs_detail" class="block text-lg font-bold">All Songs Detail</router-link>
          </li>
          <!-- <li>
            <router-link to="/song_added" class="block text-lg font-bold">Add new Song</router-link>
          </li> -->
        </ul>
      </nav>
    </div>
  </template>
  
  <script>
  export default {

  };
  </script>
  
  <style scoped>

  </style>
  