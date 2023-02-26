<script setup lang="ts">
const creds = reactive({
  username: '',
  password: '',
  passwordConfirmation: '',
});

const errors = reactive({
  username: '',
  password: '',
  passwordConfirmation: '',
});

const auth = useAuthStore();
const alert = useAlertStore();

function register() {
  // Username empty
  creds.username == ''
    ? (errors.username = 'Username is empty')
    : (errors.username = '');

  // Check for username length
  if (creds.username.length <= 4) {
    errors.username = 'The username has to be longer than 4 characters';
    return;
  } else {
    errors.username = '';
  }

  // Password empty
  creds.password == ''
    ? (errors.password = 'Password is empty')
    : (errors.password = '');

  // Password conf empty
  creds.passwordConfirmation == ''
    ? (errors.passwordConfirmation = 'Password Confirmation is empty')
    : (errors.passwordConfirmation = '');

  // If all fields are filled
  if (creds.username && creds.password && creds.passwordConfirmation) {
    // Reset the errors
    errors.username = '';
    errors.password = '';
    errors.passwordConfirmation = '';

    // The passwords don't match
    if (creds.password !== creds.passwordConfirmation) {
      // Reset the passwords
      creds.password = '';
      creds.passwordConfirmation = '';
      alert.error('Passwords must match');
      return;
    }

    // The password is too short
    if (creds.password.length < 4) {
      errors.password = 'The password must be longer than 4 characters';
      return;
    }

    // When everything goes well then register
    auth.register(creds).then(() => {
      if (auth.error) {
        alert.error('User already exists! Try again');
      }
    });
  }
}
</script>

<template>
  <div class="text-center text-white">
    <h1>Register</h1>
    <form class="mt-4" @submit.prevent="register()">
      <div>
        <input
          v-model="creds.username"
          placeholder="Username"
          type="username"
          name="username"
          id="username"
          class="p-4 bg-[rgba(92,92,92,0.5)] outline-none border-none text-white mb-4 rounded-lg"
        />
        <Transition name="fade">
          <span v-if="errors.username" class="text-vivid-red block">
            {{ errors.username }}
          </span>
        </Transition>
      </div>
      <div>
        <input
          v-model="creds.password"
          placeholder="Password"
          type="password"
          name="password"
          id="password"
          autocomplete="true"
          class="p-4 bg-[rgba(92,92,92,0.5)] outline-none border-none text-white mb-4 rounded-lg"
        />
        <Transition name="fade">
          <span v-if="errors.password" class="text-vivid-red block">
            {{ errors.password }}
          </span>
        </Transition>
      </div>
      <div>
        <input
          v-model="creds.passwordConfirmation"
          placeholder="Confirm password"
          type="password"
          name="passwordConfirmation"
          id="passwordConfirmation"
          autocomplete="true"
          class="p-4 bg-[rgba(92,92,92,0.5)] outline-none border-none text-white mb-4 rounded-lg"
        />
        <Transition name="fade">
          <span class="text-vivid-red block">
            {{ errors.passwordConfirmation }}
          </span>
        </Transition>
      </div>
      <div>
        <input type="submit" value="Submit" class="py-3 px-16 bg-vivid-red text-white border-none rounded-lg transition-all duration-200 ease-in-out pointer hover:bg-[#ff4b4b9f]" />
      </div>
    </form>
    <div class="mt-8">
      <span
        >Already have an account?
        <router-link class="text-vivid-red" to="/login">Login here!</router-link>
      </span>
    </div>
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.7s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
