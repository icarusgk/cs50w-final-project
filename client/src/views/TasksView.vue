<script setup lang="ts">
import { computed } from '@vue/reactivity';
import { useChoreStore } from '@/stores/chore';

import TaskInfo from '@/components/TaskInfo.vue';
import BackIcon from '@/components/icons/BackIcon.vue';
import Paginate from '../components/Paginate.vue';

const chore = useChoreStore();

// Back to 1 / 10
chore.taskPagination.page = 1;
chore.taskPagination.page_size = 10;
chore.taskPagination.added = 1;

const tasks = computed(() => chore.tasks);
</script>

<template>
  <div class="tasks-view">
    <div class="go-back">
      <BackIcon class="button" @click="$router.back()" />
      <span class="title">Tasks</span>
    </div>
    <div v-if="chore.tasks.length > 0">
      <div class="all-tasks-container">
        <TaskInfo v-for="task in tasks" :task="task" :key="task.id" />
      </div>
      <Paginate
        :pages="chore.totalTaskPages"
        :page="chore.taskPagination.page"
        :added="chore.taskPagination.added"
        @prev="chore.previousTaskPage"
        @setPage="(page) => chore.setTaskPage(page)"
        @next="chore.nextTaskPage"
      />
    </div>
    <div v-else>
      <h1 class="white">No tasks</h1>
    </div>
  </div>
  
</template>

<style scoped lang="scss">
.tasks-view {
  padding: 1.5rem;
  .go-back {
    display: flex;
    align-items: center;
    color: white;
    gap: 1rem;

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
    font-size: 3rem;
    font-weight: 800;
  }
  .all-tasks-container {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    gap: 1rem;
  }
}

.white {
  color: white;
}

@media (max-width: 768px) {
  .tasks-view {
    padding: 0.5rem;
  }
}
</style>
