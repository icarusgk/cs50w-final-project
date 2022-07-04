<script setup lang="ts">
import { ref } from 'vue';
import TaskType from './TaskType.vue';
import SingleTaskIcon from './icons/SingleTaskIcon.vue';
import Task from './Task.vue';
import { useFetch } from '@/composables/useFetch';


const { data, error, retry } = useFetch('http://127.0.0.1:8000/api/tasks/?format=json')

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

    <div v-for="task in data">
      <Task :task-title="task.title" />
    </div>
  </div>
</template>

<style lang="scss" scoped>

</style>