<script setup lang="ts">
import { ref } from 'vue'
import Task from './Task.vue'
import TaskType from './TaskType.vue'
import ProjectIcon from './icons/ProjectIcon.vue'

const tasks = ref<String[]>([
    'Learn Vue.js', 
    'Study Rails Basics',
]);
</script>

<template>
  <div>
    <!-- Title -->
    <TaskType>
      <template #icon>
        <ProjectIcon />
      </template>
      <template #type>
        <h1>Projects</h1>
      </template>
    </TaskType>
    <div>
      <!-- List of projects -->
      <div v-for="task in tasks">
        <Task :task-title="task" />
      </div>
    </div>
    <div>
      <!-- Icon -->
    </div>
  </div>
</template>

<style>




</style>