<script setup lang="ts">
import { computed } from '@vue/reactivity';
import BackIcon from '@/components/icons/BackIcon.vue';
import ProjectInfo from '@/components/ProjectInfo.vue';
import projects from '@/mocks/projects';
import { useChoreStore } from '@/stores/chore';

// const projects = computed(() => useChoreStore().projects)
</script>

<template>
  <div class="projects-view">
    <div class="go-back">
      <BackIcon class="button" @click="$router.back()" />
      <span class="title">All Projects</span>
    </div>
    <div class="all-projects-container">
      <ProjectInfo v-for="project in projects" :project="project" />
    </div>
  </div>
</template>

<style scoped lang="scss">
.projects-view {
  padding: 1.5rem;
  .go-back {
    display: flex;
    align-items: center;
    gap: 1rem;
    color: white;
  
    .button {
      &:hover, &:focus {
        cursor: pointer;
      }
    }
  }

  .title {
    color: white;
    font-size: 2rem;
    font-weight: 800;
  }

  .all-projects-container {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    color: white;
    margin-top: 1rem;
    gap: 1rem;
  }
}

@media (max-width: 768px) {
  .projects-view {
    padding: 0.5rem;
  }
}
</style>