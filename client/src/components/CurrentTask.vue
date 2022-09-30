<script setup lang="ts">
import { ref, watch, computed, onMounted } from 'vue';
import { useChoreStore } from '@/stores/chore';
import { useAuthStore } from '@/stores/auth';
import axios from 'axios';

const task = ref();
const currentTask = computed(() => useChoreStore().currentTaskId);

async function getTask() {  
  const response = await axios.get(`tasks/${currentTask.value}/`);
  task.value = response?.data;
}

onMounted(() => {
  if (useAuthStore().isAuthenticated) {
    getTask();
  }
});

// A kind of debouncer?
watch(
  () => currentTask.value,
  (prevTask, curTask) => {
    if (prevTask !== curTask) getTask();
  }
);
</script>

<template>
  <div 
    v-if="useAuthStore().isAuthenticated && useChoreStore().currentTaskId" 
    style="margin-top: 1rem"
  >
    <h3>Working on task: {{ task?.title }}</h3>
  </div>
</template>
