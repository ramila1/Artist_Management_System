
  <template>
    <div class="min-h-screen flex">
      <div class="w-1/4 bg-gray-800 text-white p-6">
        <nav>
          <ul class="space-y-4">
            <li>
              <router-link to="/home" class="block text-xl font-bold">Home</router-link>
            </li>
            <li>
              <router-link to="/admin_account" class="block text-xl font-bold">My Account</router-link>
            </li>
            <li>
              <router-link to="/display_artists" class="block text-xl font-bold">Artists</router-link>
            </li>
            <li>
              <router-link to="/signup" class="block text-xl font-bold">Add new Artist</router-link>
            </li>
            <li>
              <router-link to="/manage_artists" class="block text-xl font-bold">Manage Artist</router-link>
            </li>
            <li>
              <router-link to="/songs" class="block text-xl font-bold">Manage Songs</router-link>
            </li>
            <li>
              <router-link to="/song_added" class="block text-xl font-bold">Add new Song</router-link>
            </li>
            <li>
              <router-link to="/logout" class="block text-xl font-bold">LogOut</router-link>
            </li>
          </ul>
        </nav>
      </div>
  
 
      <div class="w-3/4 p-6 bg-blue-100">
        <h1 class="text-3xl font-bold mb-6">My Songs</h1>
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          <div v-for="song in songs" :key="song.id" class="bg-white p-4 rounded shadow">
            <h2 class="text-xl font-bold mb-2">{{ song.title }}</h2>
            <p class="text-gray-700">{{ song.artist }}</p>
       
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        songs: [
          { id: 1, title: 'Song 1', artist: 'Artist 1' },
          { id: 2, title: 'Song 2', artist: 'Artist 2' },
          { id: 3, title: 'Song 3', artist: 'Artist 3' },
   
        ]
      };
    }
  };
  </script>
  
  <style scoped>

  </style>
  