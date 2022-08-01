<script setup lang="ts">
import { computed, onMounted } from 'vue';
import { useChoreStore } from '@/stores/chore';

import Project from '@/components/Project.vue'
import TaskType from '@/components/slots/TaskType.vue'
import ProjectIcon from '@/components/icons/ProjectIcon.vue'

const choreStore = useChoreStore()

const projects = computed(() => choreStore.projects)
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