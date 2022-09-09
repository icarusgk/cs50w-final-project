<script setup lang="ts">
import { reactive, ref } from "vue";
import { useAuthStore } from "@/stores/auth";

const credentials = reactive({
  username: "",
  password: "",
  passwordConfirmation: "",
});
const message = ref("");

function register() {
  useAuthStore().register(credentials);
}
</script>

<template>
  <div class="register">
    <h1>Register</h1>
    <div>
      {{ message }}
    </div>
    <form @submit.prevent="register()">
      <div>
        <input
          v-model="credentials.username"
          placeholder="Username"
          type="username"
          name="username"
          id="username"
          class="form-input"
        />
      </div>
      <div>
        <input
          v-model="credentials.password"
          placeholder="Password"
          type="password"
          name="password"
          id="password"
          autocomplete="true"
          class="form-input"
        />
      </div>
      <div>
        <input
          v-model="credentials.passwordConfirmation"
          placeholder="Confirm Password"
          type="password"
          name="confirm-password"
          id="confirm-password"
          class="form-input"
        />
      </div>
      <div>
        <input type="submit" value="Register" id="submit" />
      </div>
    </form>
    <div id="route-to-login">
      <span>Already have an account?
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
    border-radius: 8px;
    &:hover,
    &:focus {
      cursor: pointer;
    }
  }

  #route-to-login {
    margin-top: 2rem;
  }
}
</style>
