<script setup lang="ts">
import { computed } from '@vue/reactivity';
import BackIcon from '@/components/icons/BackIcon.vue';
import ProjectInfo from '@/components/ProjectInfo.vue';
import Paginate from '@/components/Paginate.vue';
import { useChoreStore } from '@/stores/chore';

const chore = useChoreStore();

chore.projectPagination.page = 1;
chore.projectPagination.page_size = 10;
chore.projectPagination.added = 1;

const projects = computed(() => chore.projects);
</script>

<template>
  <div class="projects-view">
    <Paginate
      :pages="chore.totalProjectPages"
      v-model:page="chore.projectPagination.page"
      :added="chore.projectPagination.added"
      @prev="chore.previousProjectPage"
      @setPage="(page: number) => chore.setProjectPage(page)"
      @setAdded="(number: number) => chore.projectPagination.added = number"
      @next="chore.nextProjectPage"
    />
    <div class="go-back">
      <BackIcon class="button" @click="$router.back()" />
      <span class="title">Projects</span>
    </div>
    <div v-if="chore.projects.length > 0" class="all-projects-container">
      <ProjectInfo v-for="project in projects" :project="project" />
    </div>
    <div v-else>
      <h1 class="white">No Projects</h1>
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
      &:hover,
      &:focus,
      &:active {
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

.white {
  color: white;
}

@media (max-width: 768px) {
  .projects-view {
    padding: 0.5rem;
  }
}
</style>
