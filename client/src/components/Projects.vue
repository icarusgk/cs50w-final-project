<script setup lang="ts">
import { computed } from 'vue';
import { useChoreStore } from '@/stores/chore';
import { useAutoAnimate } from '@formkit/auto-animate/vue';

import Project from '@/components/Project.vue';
import TaskType from '@/components/slots/TaskType.vue';
import ProjectIcon from '@/components/icons/ProjectIcon.vue';
import Paginate from './Paginate.vue';

const chore = useChoreStore();

chore.projectPagination.page = 1;
chore.projectPagination.page_size = 4;

const projects = computed(() => chore.projects.slice(0, 2));
</script>

<template>
  <div>
    <!-- Title -->
    <TaskType class="projects-button" @click="$router.push('/projects')">
      <template #icon>
        <ProjectIcon />
      </template>
      <template #type>
        <h1>Projects</h1>
      </template>
      <template #count>
        Page {{ chore.projectPagination.page }} of
        {{ chore.totalProjectPages }}
      </template>
    </TaskType>
    <div>
      <div v-if="projects.length === 0">
        <h2>No Projects</h2>
      </div>
      <!-- List of projects -->
      <div v-auto-animate>
        <Project
          v-for="project in projects"
          :project="project"
          :key="project.id"
        />
      </div>
    </div>
    <Paginate
      :pages="chore.totalProjectPages"
      v-model:page="chore.projectPagination.page"
      :added="chore.projectPagination.added"
      @prev="chore.previousProjectPage"
      @setPage="(page) => chore.setProjectPage(page)"
      @setAdded="(number) => chore.projectPagination.added = number"
      @next="chore.nextProjectPage"
    />
  </div>
</template>

<style scoped lang="scss">
.projects-button {
  &:hover,
  &:focus,
  &:active {
    cursor: pointer;
  }
}
</style>
