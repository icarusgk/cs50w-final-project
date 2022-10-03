<script setup>
import Login from '@/components/Login.vue';
</script>

<template>
  <div class="login">
    <Login />
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
