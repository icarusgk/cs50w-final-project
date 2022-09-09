<script setup>
import Projects from "@/components/Projects.vue";
import Tasks from "@/components/Tasks.vue";
import { useAuthStore } from "@/stores/auth";
</script>

<template>
  <div v-if="useAuthStore().isAuthenticated">
    <Projects />
    <Tasks />
  </div>
</template>
