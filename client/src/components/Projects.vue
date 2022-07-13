<script setup lang="ts">
import { ref } from 'vue'
import Task from './Task.vue'
import TaskType from './TaskType.vue'
import ProjectIcon from './icons/ProjectIcon.vue'
import type TypeTask from '@/types/TaskType'

const mockProjects = ref([
  {
    "id": 1,
    "user": 1,
    "title": "Learn Vue.js",
    "description": "Vue refs. Updated from drf",
    "subtasks": [
      
    ]
  },
  {

    "id": 2,
    "user": 1,
    "title": "Study Rails Basics",
    "description": "Here’s a brief description of this task. It’ll continue for I don’t know for how long. Vue is a really good front-end framework, it is the first one that I’m learning before React and Svelte.",
    "subtasks": [

    ]
  },
])


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
      <div v-for="task in mockProjects">
        <Task :task="task" />
      </div>
    </div>
    <div>
      <!-- Icon -->
    </div>
  </div>
</template>

<style>




</style>