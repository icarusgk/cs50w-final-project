<script setup lang="ts">
import { reactive } from 'vue';
import { useAuthStore } from '@/stores/auth';

const credentials = reactive({
  username: '',
  password: '',
  passwordConfirmation: '',
});

function register() {
  useAuthStore().register(credentials);
}
</script>

<template>
  <div class="register">
    <h1>Register</h1>
    <div class="wrapper">

    </div>
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

  .wrapper {
    display: flex;
    justify-content: center;
    margin-top: 2rem;
  }
  #route-to-login {
    margin-top: 2rem;
  }
}

.text-color {
  color: white;
}
</style>
