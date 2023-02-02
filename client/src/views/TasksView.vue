<script setup lang="ts">
import { computed } from '@vue/reactivity';
import { useChoreStore } from '@/stores/chore';
import type { TaskType } from '@/types';

import BaseViewTask from '@/components/BaseViewTask.vue';
import BackIcon from '@/components/icons/BackIcon.vue';
import TaskInfoIcon from '@/components/icons/TaskInfoIcon.vue';
import Paginate from '../components/Paginate.vue';

const chore = useChoreStore();

// Back to 1 / 10
chore.taskPagination.page = 1;
chore.taskPagination.page_size = 10;
chore.taskPagination.added = 1;

chore.fetchTasks();

const tasks = computed(() => chore.tasks);

function setPage(newPage: number) {
  chore.setTaskPage(newPage);
}

function setAdded(newAdded: number) {
  chore.setTaskAdded(newAdded);
}

function deleteTask(task: TaskType) {
  if (window.confirm('Are you sure you want to delete this task??????')) {
    chore.deleteTask(task);

    if (chore.taskPagination.page === chore.totalTaskPages && chore.tasks.length === 1) {
      chore.decreaseTaskPagination();
    }
  }
}
</script>

<template>
  <div class="tasks-view">
    <div class="go-back">
      <BackIcon class="button" @click="$router.back()" />
      <span class="title">Tasks</span>
    </div>
    <Paginate
      class="top-paginate"
      :pages="chore.totalTaskPages"
      :page="chore.taskPagination.page"
      :added="chore.taskPagination.added"
      @prev="chore.previousTaskPage()"
      @setPage="setPage($event)"
      @setAdded="setAdded($event)"
      @next="chore.nextTaskPage()"
    />
    <div v-if="chore.tasks.length > 0">
      <div class="all-tasks-container">
        <BaseViewTask v-for="task in tasks" :task="task" :key="task.id" @deleteTask="deleteTask($event)"/>
      </div>
      <Paginate
        :pages="chore.totalTaskPages"
        :page="chore.taskPagination.page"
        :added="chore.taskPagination.added"
        @prev="chore.previousTaskPage()"
        @setPage="setPage($event)"
        @setAdded="setAdded($event)"
        @next="chore.nextTaskPage()"
      />
    </div>
    <div class="no-tasks" v-else>
      <TaskInfoIcon />
      <span class="white">No Tasks</span>
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
  .top-paginate {
    margin-bottom: 1rem;
  }
  .all-tasks-container {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    gap: 1rem;
    margin-top: 1rem;
  }

  .no-tasks {
    margin: 1rem;
    display: flex;
    align-items: center;
    span {
      margin-left: 1rem;
      font-weight: 600;
      font-size: 1.5rem;
    }
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
