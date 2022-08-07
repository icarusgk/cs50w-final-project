<script setup lang="ts">
import { computed } from '@vue/reactivity';
import BackIcon from '@/components/icons/BackIcon.vue';
import ProjectInfo from '@/components/ProjectInfo.vue';

import { useChoreStore } from '@/stores/chore';

const projects = computed(() => useChoreStore().projects)
</script>

<template>
  <div class="projects-view">
    <div>
      <div class="go-back">
        <BackIcon class="button" @click="$router.back()" />
        <span>Go back</span>
      </div>
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
    color: white;
    
    .button {
      &:hover, &:focus {
        cursor: pointer;
      }
    }
  }

  .title {
    color: white;
    margin-bottom: 1rem;
    font-size: 6rem;
    font-weight: 800;
  }

  .all-projects-container {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    color: white;
    margin-top: 1rem;
  }
}
</style>