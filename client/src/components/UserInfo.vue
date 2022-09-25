<script setup lang="ts">
import { useAuthStore } from '@/stores/auth';

defineEmits(['exitModal'])

const auth = useAuthStore();
</script>

<template>
  <div>
    <h1>Logout</h1>
    <h2>Hello there {{ auth.user?.username }}</h2>
    <button
      id="logout-btn"
      @click="
        auth.logout();
        $emit('exitModal')
      "
    >
      Logout
    </button>
  </div>
</template>

<style scoped lang="scss">
#logout-btn {
  padding: 0.5rem 1rem;
  border-radius: 8px;
  border: none;
  background-color: var(--vivid-red);
  color: white;
  font-weight: 500;
  transition: background-color 0.15s ease-in;

  &:hover {
    cursor: pointer;
    background-color: #ff4b4b9f;
  }
}
</style>