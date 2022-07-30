<script setup lang="ts">
import { computed, onMounted } from 'vue';
import { useTaskStore } from '@/stores/task';

import TaskType from './slots/TaskType.vue';
import SingleTaskIcon from './icons/SingleTaskIcon.vue';
import Task from './Task.vue';

const taskStore = useTaskStore()

const tasks = computed(() => taskStore.tasks)

onMounted(() => {
  taskStore.fetchTasks()  
})

</script>

<template>
  <div>
    <TaskType>
      <template #icon>
        <SingleTaskIcon />
      </template>
      <template #type>
        <h1>Single Tasks</h1>
      </template>
    </TaskType>

    <div v-for="task in tasks">
      <Task :task="task" />
    </div>
  </div>
</template>

<style lang="scss" scoped>

</style>