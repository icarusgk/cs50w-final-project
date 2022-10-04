<script setup lang="ts">
import { computed } from 'vue';
import { useChoreStore } from '@/stores/chore';

import TaskType from '@/components/slots/TaskType.vue';
import SingleTaskIcon from '@/components/icons/SingleTaskIcon.vue';
import Task from '@/components/buttons/Task.vue';
import Paginate from './Paginate.vue';

const chore = useChoreStore();

// Back to 1 / 4;
chore.taskPagination.page = 1;
chore.taskPagination.page_size = 4;

const tasks = computed(() => chore.tasks.slice(0, 4));
</script>

<template>
  <div>
    <TaskType class="button" @click="$router.push('/tasks')">
      <template #icon>
        <SingleTaskIcon />
      </template>
      <template #type>
        <h1>Single Tasks</h1>
      </template>
      <template #count>
        Page {{ chore.taskPagination.page }} of {{ chore.totalTaskPages}}
      </template>
    </TaskType>
    <div v-if="tasks.length === 0">
      <h2>No tasks</h2>
    </div>
    <div v-auto-animate>
      <Task v-for="task in tasks" :task="task" :key="task.id" />
    </div>
    
    <Paginate
      :pages="chore.totalTaskPages"
      v-model:page="chore.taskPagination.page"
      :added="chore.taskPagination.added"
      @prev="chore.previousTaskPage"
      @setPage="(page) => chore.setTaskPage(page)"
      @next="chore.nextTaskPage"
    />
  </div>
</template>

<style lang="scss" scoped>
.button {
  &:hover,
  &:focus,
  &:active {
    cursor: pointer;
  }
}
</style>
