<script setup lang="ts">
import { reactive } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { useAlertStore } from '@/stores/alerts';

const creds = reactive({
  username: '',
  password: '',
  passwordConfirmation: '',
});

const errors = reactive({
  username: '',
  password: '',
  passwordConfirmation: ''
})

const auth = useAuthStore();
const alert = useAlertStore();

function register() {
  // Username empty
  creds.username == '' ? errors.username = 'Username is empty' : errors.username = '';

  // Check for username length
  if (creds.username.length <= 4) {
    errors.username = 'The username has to be longer than 4 characters';
    return;
  } else {
    errors.username = '';
  }

  // Password empty
  creds.password == '' ? errors.password = 'Password is empty' : errors.password = '';


  // Password conf empty
  creds.passwordConfirmation == ''
    ? errors.passwordConfirmation = 'Password Confirmation is empty'
    : errors.passwordConfirmation = '';

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
  <div class="register">
    <h1>Register</h1>
    <form @submit.prevent="register()">
      <div>
        <input
          v-model="creds.username"
          placeholder="Username"
          type="username"
          name="username"
          id="username"
          class="form-input"
        />
        <Transition name="fade">
          <span v-if="errors.username" class="error-message">
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
          class="form-input"
        />
        <Transition name="fade">
          <span v-if="errors.password" class="error-message">
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
          class="form-input"
        />
        <Transition name="fade">
          <span class="error-message">
            {{ errors.passwordConfirmation }}
          </span>
        </Transition>
      </div>
      <div>
        <input type="submit" value="Submit" id="submit" />
      </div>
  </form>
    <div id="route-to-login">
      <span
        >Already have an account?
        <router-link to="/login">Login here!</router-link>
      </span>
    </div>
  </div>
</template>

<style scoped lang="scss">
* {
  color: white;
}
.register {
  text-align: center;
  
  form {
    margin-top: 1rem;
  }

  .fade-enter-active,
  .fade-leave-active {
    transition: opacity 0.7s ease;
  }

  .fade-enter-from,
  .fade-leave-to {
    opacity: 0;
  }

  .error-message {
    color:rgb(249, 122, 90);
    display: block;
  }

  .form-input {
    padding: 1rem;
    background-color: rgba(92, 92, 92, 0.5);
    outline: none;
    border: none;
    color: white;
    margin-bottom: 1rem;
    border-radius: 8px;
  }

  #submit {
    padding: 0.6rem 4rem;
    background-color: var(--vivid-red);
    color: white;
    border: none;
    &:hover,
    &:focus,
    &:active {
      cursor: pointer;
    }
  }
  #route-to-login {
    margin-top: 2rem;
  }
}
</style>
