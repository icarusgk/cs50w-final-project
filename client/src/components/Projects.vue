<script setup lang="ts">
import Project from './Project.vue'
import TaskType from './slots/TaskType.vue'
import ProjectIcon from './icons/ProjectIcon.vue'
import { useFetch } from '@/composables/useFetch'

const { data, error, retry } = useFetch('/projects')

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
      <div v-for="project in data">
        <Project :project="project" />
      </div>
    </div>
    <div>
      <!-- Icon -->
    </div>
  </div>
</template>

<style>




</style>