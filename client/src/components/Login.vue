<script setup>
import { reactive } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { useAlertStore } from '@/stores/alerts';

const creds = reactive({
  username: '',
  password: '',
});
const errors = reactive({
  username: '',
  password: '',
});

const auth = useAuthStore();

function login() {
  creds.username == '' ? errors.username = 'Username is empty' : errors.username = '';
  creds.password == '' ? errors.password = 'Password is empty' : errors.password = '';
    

  if (creds.username && creds.password) {
    // clear errors
    errors.username = '';
    errors.password = '';

    auth.login(creds).then(() => {
      if (auth.error) {
        useAlertStore().error('Your username or password is incorrect.');
      }
    });
  }
}
</script>

<template>
  <div class="login">
    <h1>Login</h1>
    <form @submit.prevent="login()">
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
        <input type="submit" value="Submit" id="submit" />
      </div>
    </form>
    <div id="route-to-register">
      <span>Don't have an account yet? </span>
      <RouterLink to="/register">Register here!</RouterLink>
    </div>
  </div>
</template>

<style scoped lang="scss">
.login {
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

  #route-to-register {
    margin-top: 2rem;
  }
}
</style>
