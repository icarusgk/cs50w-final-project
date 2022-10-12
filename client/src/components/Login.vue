<script setup>
import { reactive } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { useAlertStore } from '@/stores/alerts';

const creds = reactive({
  username: '',
  password: '',
});
const errors = reactive({
  username: null,
  password: null,
});

const auth = useAuthStore();

function login() {
  creds.username == '' ? errors.username = 'Username is empty' : null;
  creds.password == '' ? errors.password = 'Password is empty' : null;
    

  if (creds.username && creds.password) {
    // clear errors
    errors.username = '';
    errors.password = '';

    auth.login(creds).then(() => {
      if (auth.error) {
        useAlertStore().error('Your username or password is incorrect.')
      }
    });
  }
}
</script>

<template>
  <div class="login">
    <h1>Login</h1>
    <div>
      <span class="error-message">{{ errors.general }}</span>
    </div>
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
        <span class="error-message">{{ errors.username }}</span>
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
        <span class="error-message">{{ errors.password }}</span>
      </div>
      <div>
        <input type="submit" value="Submit" id="submit" />
      </div>
  </form>
  </div>
</template>

<style scoped lang="scss">
.login {
  text-align: center;

  form {
    margin-top: 1rem;
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
}
</style>
