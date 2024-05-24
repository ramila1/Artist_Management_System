<template>
  <div class="min-h-screen flex items-center justify-center bg-blue-100">
    <div class=" max-w-md w-full space-y-8 p-10 bg-white shadow-lg rounded-lg">
      <div class="text-center mb-4">
        <!-- <img src="@/assets/logo.png" alt="Logo" class="h-16 w-16 mx-auto mb-4"> -->
        <h2 class="text-3xl font-extrabold text-gray-900">Login to Your Account</h2>
        
      </div>

      <form @submit.prevent="login" class="space-y-6">
        <div class="space-y-4">
          <div>
            <label for="email-address" class="block text-sm font-medium text-gray-700">
              <i class="fas fa-envelope mr-2"></i>
              <span>Email address</span>
            </label>
            <input
              v-model="form.email"
              id="email-address"
              name="email"
              type="email"
              autocomplete="email"
              required
              class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-none shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              placeholder="Email address"
            />
          </div>

          <div>
            <label for="password" class="block text-sm font-medium text-gray-700">
              <i class="fas fa-lock mr-2"></i>
              <span>Password</span>
            </label>
            <input
              v-model="form.password"
              id="password"
              name="password"
              type="password"
              required
              class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-none shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              placeholder="Password"
            />
          </div>
        </div>

        <div>
          <button
            type="submit"
            class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            <i class="fas fa-arrow-right mr-2"></i>
            Login
          </button>
        </div>
      </form>

      <div class="flex justify-center text-sm text-gray-600 mt-2">
        <router-link to="/signup" class="text-indigo-600 hover:text-indigo-800 focus:outline-none">
          Don't have an account? Sign up here.
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      form: {
        email: '',
        password: '',
      },
    };
  },
  methods: {
    login() {
      axios
        .post('http://127.0.0.1:8000/api/login/', this.form)
        .then(response => {
          localStorage.setItem('access_token', response.data.access);
          localStorage.setItem('refresh_token', response.data.refresh);
          
          
          alert('Logged in successfully!');
          console.log(response.data);
          if (response.data.user.is_superuser) {
            this.$router.push('/admin');
          } else if (response.data.user.is_artist) {
            this.$router.push('/artist');
          } else {
            alert('User role not recognized. Redirecting to login.');
            this.$router.push('/login');
          }
          
        })
        .catch(error => {
          console.error('Error logging in:', error);
          alert('Invalid credentials. Please try again.');
        });
    },
  },
};
</script>

<style>
.fas {
  font-size: 16px;
}

.bg-custom-color {
  background-color: #ecfeff;
}
</style>

