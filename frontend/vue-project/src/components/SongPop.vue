<template>
    <div class="fixed inset-0 overflow-y-auto z-50 flex items-center justify-center bg-black bg-opacity-50">
      <div class="bg-white p-8 max-w-2xl mx-auto rounded-lg shadow-lg">
        <h2 class="text-2xl font-bold mb-4">{{ song.title }}</h2>
        <p><strong>Artist:</strong> {{ song.artist.first_name }} {{ song.artist.last_name }}</p>
        <p><strong>Release Date:</strong> {{ song.release_date }}</p>
        <p><strong>Duration:</strong> {{ song.duration }}</p>
        <p v-if="song.lyrics"><strong>Lyrics:</strong> {{ song.lyrics }}</p>
        <p><strong>Language:</strong> {{ song.language }}</p>
        <div class="mt-4">
          <button @click="close" class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">Close</button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      song: {
        type: Object,
        required: true,
      },
    },
    methods: {
      close() {
        this.$emit('close');
      },
    },
  };
  </script>
  
  <style scoped>
  /* Styling for the popup */
  </style>
  