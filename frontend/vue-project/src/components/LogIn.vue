<template>
  <div class="min-h-screen flex flex-col bg-blue-100">
   
    <NavLogin />

    <div class="flex flex-1 items-center justify-center">
      <div class="max-w-md w-full  p-10 bg-white shadow-lg rounded-lg">
        <div class="text-center mb-4">
          <h2 class="text-3xl font-extrabold text-gray-900">Login to Your Account</h2>
        </div>

        <form @submit.prevent="login" class="space-y-6">
          <div class="space-y-4">
            <div>
              <label for="email-address" class="block text-sm font-medium text-gray-700">
                <span>Email address</span>
              </label>
              <input
                v-model="form.email"
                id="email-address"
                name="email"
                type="email"
                autocomplete="email"
                :class="{'border-red-500': errors.email}"
                required
                class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-none shadow-sm placeholder-gray-400"
                placeholder="Email address"
              />
              <span v-if="errors.email" class="text-red-500 text-sm">{{ errors.email }}</span>
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
                :class="{'border-red-500': errors.password}"
                required
                class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-none shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                placeholder="Password"
              />
              <span v-if="errors.password" class="text-red-500 text-sm">{{ errors.password }}</span>
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

     
        <div class="flex flex-col items-center mt-6">
          <span class="text-gray-600 mb-1">Don't have an account?</span>
          <router-link to="/signup" class="text-indigo-600 hover:text-indigo-800 focus:outline-none">
            Sign up here
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { toast } from 'vue3-toastify';
import NavLogin from './NavigationLogin.vue'; 

export default {
  components: {
    NavLogin, 
  },
  data() {
    return {
      form: {
        email: '',
        password: '',
      },
      errors: {
        email: null,
        password: null,
      },
    };
  },
  methods: {
    validateForm() {
      this.errors.email = this.errors.password = null;

      let isValid = true;

      if (!this.form.email) {
        this.errors.email = 'Email is required';
        isValid = false;
      } else if (!/\S+@\S+\.\S+/.test(this.form.email)) {
        this.errors.email = 'Email must be valid';
        isValid = false;
      }

      if (!this.form.password) {
        this.errors.password = 'Password is required';
        isValid = false;
      }

      return isValid;
    },
    login() {
      if (!this.validateForm()) {
        return;
      }

      axios.post('http://127.0.0.1:8000/api/login/', this.form).then(response => {
          localStorage.setItem('access_token', response.data.access);
          localStorage.setItem('refresh_token', response.data.refresh);
          localStorage.setItem('user', JSON.stringify(response.data.user));
          toast.success('Logged in successfully!');

          console.log(response.data);
          if (response.data.user.is_superuser) {
            this.$router.push('/admin');
          } else if (response.data.user.is_artist) {
            this.$router.push('/artist');
          } else {
            toast.error('User role not recognized. Redirecting to login.');
            this.$router.push('/login');
          }
        })
        .catch(error => {
          console.error('Error logging in:', error);
          toast.error('Invalid credentials. Please try again.');
        });
    },
  },
};
</script>


<style>


</style>
