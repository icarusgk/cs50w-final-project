<script setup lang="ts">
import { reactive, ref } from 'vue';
import { useAuthStore } from '@/stores/auth';

const credentials = reactive({
  username: '',
  password: '',
  passwordConfirmation: '',
});
const message = ref('');

function register() {
  useAuthStore().register(credentials);
}
</script>

<template>
  <div class="register">
    <h1>Register</h1>
    <div class="wrapper">
      <FormKit type="form" submit-label="Register" @submit="register">
        <FormKit
          type="text"
          name="username"
          id="username"
          input-class="formkit-color-white"
          message-class="formkit-color-red"
          placeholder="Username"
          validation="required"
        />
        <FormKit
          type="password"
          name="password"
          id="password"
          input-class="formkit-color-white"
          message-class="formkit-color-red"
          placeholder="Password"
          validation="required"
        />
        <FormKit
          type="password"
          name="confirm-password"
          id="confirm-password"
          input-class="formkit-color-white"
          message-class="formkit-color-red"
          placeholder="Confirm Password"
          validation="required"
        />
      </FormKit>
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
