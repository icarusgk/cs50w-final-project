<script setup lang="ts">
import TaskType from './slots/TaskType.vue';
import SingleTaskIcon from './icons/SingleTaskIcon.vue';
import Task from './Task.vue';
import { useFetch } from '@/composables/useFetch';
import tasks from '@/mocks/tasks';

// const tasksURL = new URL('http://127.0.0.1:8000/api/tasks/?format=json')
// const { data, error, retry } = useFetch(tasksURL)

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