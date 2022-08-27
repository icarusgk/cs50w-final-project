<script setup lang="ts">
import { computed } from 'vue';
import { useChoreStore } from '@/stores/chore';

import Project from '@/components/Project.vue'
import TaskType from '@/components/slots/TaskType.vue'
import ProjectIcon from '@/components/icons/ProjectIcon.vue'
// import projects from '@/mocks/projects';
const choreStore = useChoreStore()

const projects = computed(() => choreStore.projects)

</script>

<template>
  <div v-if="projects.length > 0">
    <!-- Title -->
    <TaskType
      class="projects-button"
      @click="$router.push('/projects')"
    >
      <template #icon>
        <ProjectIcon />
      </template>
      <template #type>
        <h1>Projects</h1>
      </template>
    </TaskType>
    <div>
      <div v-if="!projects">
        <h2>No Projects</h2>
      </div>
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

<style scoped lang="scss">
.projects-button {
  &:hover, &:focus {
    cursor: pointer;
  }
}

</style>