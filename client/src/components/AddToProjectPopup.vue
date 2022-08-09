<script setup lang="ts">
import { ref } from 'vue';
import { useChoreStore } from '@/stores/chore';
import type { Project } from '@/types';

const projects = useChoreStore().projects

const allMyProjects = ref<Project[]>([])

// TODO: Connect to back-end
function addToProject(project: Project) {
  if (!allMyProjects.value.includes(project)) {
    allMyProjects.value.push(project)
  }
}
</script>

<template>
<!-- Add to project -->
  <div class="add-to-project-dropdown">
    <Popper arrow placement="bottom">
    <div>
      <span class="text">Add to Project</span>
    </div>
    <template #content="{ close }">
      <div class="project-select">
        <div class="project" 
          :class="{ inside: allMyProjects.includes(project) }" 
          v-for="project in projects" 
          @click="addToProject(project)"
        >
          {{ project.title }}
        </div>
      </div>
    </template>
    </Popper>
  </div>

</template>


<style scoped lang="scss">
.add-to-project-dropdown {
  padding: 0.5rem;
  margin-top: 1rem;
  border-radius: 8px;
  width: 60%;
  text-align: center;
  background-color: rgb(58, 58, 58);

  &:hover, &:focus {
    cursor: pointer;
  }

  .text {
    font-weight: 500;
  }

  .project-select { 
    width: 10rem;

    .project {
      background-color: rgb(92, 92, 92);
      padding: 0.5rem;
      border-radius: 8px;
      margin-bottom: 0.4rem;
      &:last-child {
        margin: 0;
      }
    }

    .inside {
      background-color: rgb(251, 105, 105);
      transition: background-color 0.3s ease-in-out;
    }
  }
}

@media (max-width: 768px) {
  .add-to-project-dropdown {
    width: 100%;
  }
}
</style>