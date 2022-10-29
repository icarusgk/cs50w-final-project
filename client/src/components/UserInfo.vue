<script setup lang="ts">
import { useAuthStore } from '@/stores/auth';

defineEmits(['exitModal']);

const auth = useAuthStore();
</script>

<template>
  <div>
    <h2>Hello there {{ auth.user?.username }}!</h2>
  </div>
</template>

<style scoped lang="scss">

</style>
