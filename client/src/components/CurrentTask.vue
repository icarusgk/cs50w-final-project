<script setup lang="ts">
import { ref, watch, computed, onMounted } from 'vue'
import { useChoreStore } from '@/stores/chore';
import axios from 'axios'

const currentTask = computed(() => useChoreStore().currentTask)
const task = ref()

async function getTask() {
  const response = await axios.get(`tasks/${currentTask.value?.id}/`)
  task.value = response?.data
}

onMounted(() => getTask())

watch(() => currentTask.value, (prevTask, curTask) => {
  if (prevTask !== curTask) getTask()
})

</script>

<template>
  <div style="margin-top: 1rem;">
    <h3>Working on task: {{ task?.title }}</h3>
  </div>
</template>