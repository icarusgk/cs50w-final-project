<script setup>
import { reactive, ref } from "vue";
import { useAuthStore } from "@/stores/auth";

const credentials = reactive({
  username: "",
  password: "",
});
const message = ref("");

function login() {
  useAuthStore().login(credentials);
}
</script>

<template>
  <div class="login">
    <h1>Login</h1>
    <div>
      {{ message }}
    </div>
    <form @submit.prevent="login()">
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
        <input type="submit" value="Submit" id="submit" />
      </div>
    </form>
  </div>
</template>

<style scoped lang="scss">
* {
  color: white;
}
.login {
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
    &:hover,
    &:focus {
      cursor: pointer;
    }
  }
}
</style>
