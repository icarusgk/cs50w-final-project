<script setup lang="ts">
import { computed } from 'vue';
import { useChoreStore } from '@/stores/chore';

import Project from '@/components/buttons/Project.vue';
import TaskType from '@/components/slots/TaskType.vue';
import ProjectIcon from '@/components/icons/ProjectIcon.vue';
import Paginate from '@/components/Paginate.vue';

const chore = useChoreStore();

chore.projectPagination.page = 1;
chore.projectPagination.page_size = 2;
chore.projectPagination.added = 1;

const projects = computed(() => chore.projects.slice(0, 2));
</script>

<template>
  <div>
    <!-- Title -->
    <TaskType class="projects-button">
      <template #icon>
        <ProjectIcon />
      </template>
      <template #type>
        <h1 @click="$router.push('/projects')">Projects</h1>
      </template>
      <template #count>
        <span v-if="chore.totalProjectPages > 1">
          Page {{ chore.projectPagination.page }} of
          {{ chore.totalProjectPages }}
        </span>
      </template>
    </TaskType>
    <div>
      <div v-if="projects.length === 0">
        <span>There are no projects</span>
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
      @setAdded="(number) => (chore.projectPagination.added = number)"
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
