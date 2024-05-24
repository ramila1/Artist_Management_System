<template>
  <div class="min-h-screen flex items-center justify-center bg-blue-100">
    <div class="w-full max-w-lg px-8 py-8 bg-white shadow-lg rounded-lg">
      <div class="text-center mb-6">
        <h2 class="text-2xl font-extrabold text-gray-900">Create Account</h2>
      </div>

      <form @submit.prevent="signup" class="space-y-6">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-x-4 gap-y-4">
          <div>
            <label for="first_name" class="block text-sm font-medium text-gray-700">First Name</label>
            <input
              v-model="form.first_name"
              id="first_name"
              name="first_name"
              type="text"
              required
              class="input-field"
              placeholder="First Name"
            />
          </div>
          <div>
            <label for="last_name" class="block text-sm font-medium text-gray-700">Last Name</label>
            <input
              v-model="form.last_name"
              id="last_name"
              name="last_name"
              type="text"
              required
              class="input-field"
              placeholder="Last Name"
            />
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-x-4 gap-y-4">
          <div>
            <label for="email-address" class="block text-sm font-medium text-gray-700">Email address</label>
            <input
              v-model="form.email"
              id="email-address"
              name="email"
              type="email"
              autocomplete="email"
              required
              class="input-field"
              placeholder="Email address"
            />
          </div>
          <div>
            <label for="date_of_birth" class="block text-sm font-medium text-gray-700">Date of Birth</label>
            <input
              v-model="form.date_of_birth"
              id="date_of_birth"
              name="date_of_birth"
              type="date"
              required
              class="input-field"
              placeholder="Date of Birth"
            />
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-x-4 gap-y-4">
          <div>
            <label for="gender" class="block text-sm font-medium text-gray-700">Gender</label>
            <select
              v-model="form.gender"
              id="gender"
              name="gender"
              class="input-field"
              required
            >
              <option value="" disabled>Select your gender</option>
              <option value="male">Male</option>
              <option value="female">Female</option>
              <option value="other">Other</option>
            </select>
          </div>
          <div>
            <label for="address" class="block text-sm font-medium text-gray-700">Address</label>
            <input
              v-model="form.address"
              id="address"
              name="address"
              type="text"
              required
              class="input-field"
              placeholder="Address"
            />
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-x-4 gap-y-4">
          <div>
            <label for="country" class="block text-sm font-medium text-gray-700">Country</label>
            <input
              v-model="form.country"
              id="country"
              name="country"
              type="text"
              required
              class="input-field"
              placeholder="Country"
            />
          </div>
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
            <input
              v-model="form.password"
              id="password"
              name="password"
              type="password"
              required
              class="input-field"
              placeholder="Password"
            />
          </div>
        </div>

        <div>
          <button
            type="submit"
            class="w-full bg-indigo-500 hover:bg-indigo-600 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          >
            Create Account
          </button>
        </div>

        <div class="text-center mt-4">
          <p class="text-sm text-gray-600">
            Already have an account?
            <router-link to="/login" class="text-indigo-500 hover:text-indigo-700 font-medium">
              Log in
            </router-link>
          </p>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      form: {
        email: '',
        first_name: '',
        last_name: '',
        date_of_birth: '',
        gender: '',
        address: '',
        country: '',
        password: ''
      }
    };
  },
  methods: {
    async signup() {
      try {
        const response = await fetch('http://localhost:8000/api/artists/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.form)
        });

        if (response.ok) {
          const data = await response.json();
          console.log('Artist created successfully:', data);
          this.$router.push('/login');
        } else {
          const errorData = await response.json();
          console.error('Error creating artist:', errorData);
        }
      } catch (error) {
        console.error('Network error:', error);
      }
    }
  }
};
</script>

<style scoped>
.input-field {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #d2d6dc;
  border-radius: 0.375rem;
  color: #1a202c;
  background-color: #fff;
  transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}

.input-field:focus {
  border-color: #667eea;
  outline: 0;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.5);
}

.input-field::placeholder {
  color: #a0aec0;
}
</style>
