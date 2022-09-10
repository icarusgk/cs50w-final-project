<script setup>
import { useAuthStore } from "@/stores/auth";

async function login(credentials) {
  useAuthStore().login(credentials)
}
</script>

<template>
  <div class="login">
    <h1>Login</h1>
    <div class="wrapper">
      <div>
        <FormKit
        type="form"
        submit-label="Login"
        @submit="login"
        >
          <FormKit
            type="text"
            name="username"
            placeholder="Username"
            input-class="formkit-color-white"
            message-class="formkit-color-red"
            validation="required|length:4"
          />
          <FormKit
            type="password"
            name="password"
            placeholder="Password"
            input-class="formkit-color-white"
            message-class="formkit-color-red"
            validation="required|length:4"
          />
        </FormKit>
      </div>
    </div>
    <div id="route-to-register">
      <span>Don't have an account?
        <router-link to="/register">Register here!</router-link>
      </span>
    </div>
  </div>
</template>

<style scoped lang="scss">
* {
  color: white;
}
.login {
  text-align: center;
  
  .wrapper {
    display: flex;
    justify-content: center;
    margin-top: 2rem;
  }

  #route-to-register {
    margin-top: 2rem;
  }
}


</style>
