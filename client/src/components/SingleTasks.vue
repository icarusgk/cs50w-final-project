<script setup lang="ts">
import { ref } from 'vue';
import TaskType from './TaskType.vue';
import SingleTaskIcon from './icons/SingleTaskIcon.vue';
import Task from './Task.vue';

const tasks = ref<String[]>([
  'Learn Refs from Vue.js',
  'Study Controller from Rails',
  'Read Nuxt.js 3',
  'Put my strips on'
]);
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
      <Task :task-title="task" />
    </div>
  </div>
</template>

<style lang="scss" scoped>

</style>