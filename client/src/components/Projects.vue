<script setup lang="ts">
import { computed, onMounted } from 'vue';
import { useChoreStore } from '@/stores/chore';

import Project from './Project.vue'
import TaskType from './slots/TaskType.vue'
import ProjectIcon from './icons/ProjectIcon.vue'

const choreStore = useChoreStore()

const projects = computed(() => choreStore.projects)

onMounted(() => choreStore.fetchProjects())

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
      <div v-for="project in projects">
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