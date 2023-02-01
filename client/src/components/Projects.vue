<script setup lang="ts">
import { ref, computed } from 'vue';
import { useChoreStore } from '@/stores/chore';

import Project from '@/components/buttons/Project.vue';
import TaskType from '@/components/slots/TaskType.vue';
import ProjectIcon from '@/components/icons/ProjectIcon.vue';
import TaskInfoIcon from './icons/TaskInfoIcon.vue';
import Paginate from '@/components/Paginate.vue';

const chore = useChoreStore();

chore.projectPagination.page = 1;
chore.projectPagination.page_size = 2;
chore.projectPagination.added = 1;

chore.fetchProjects();

const projects = computed(() => chore.projects.slice(0, 2));

function setPage(newPage: number) {
  chore.setProjectPage(newPage);
}

function setAdded(newAdded: number) {
  chore.setProjectAdded(newAdded);
}
</script>

<template>
  <div id="projects-container">
    <!-- Projects Title -->
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
    <!-- Project List Container -->
    <div>
      <div class="no-projects" v-if="projects.length === 0">
        <TaskInfoIcon />
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
    <!-- Paginator -->
    <Paginate
      :pages="chore.totalProjectPages"
      :page="chore.projectPagination.page"
      :added="chore.projectPagination.added"
      @prev="chore.previousProjectPage()"
      @setPage="setPage($event)"
      @setAdded="setAdded($event)"
      @next="chore.nextProjectPage()"
    />
  </div>
</template>

<style scoped lang="scss">
#projects-container {
  margin-top: 0.5rem;
}

.projects-button {
  &:hover,
  &:focus,
  &:active {
    cursor: pointer;
  }
}

.no-projects {
  display: flex;
  align-items: center;
  background-color: var(--light-gray);
  width: 80%;
  padding: 1rem;
  border-radius: 10px;
  span {
    margin-left: 1rem;
  }
}

@media (max-width: 768px) {
  .no-projects {
    width: 100%;
  }
}
</style>
