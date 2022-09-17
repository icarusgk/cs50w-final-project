<script setup lang="ts">
import { computed } from 'vue';
import { useChoreStore } from '@/stores/chore';

import TaskType from '@/components/slots/TaskType.vue';
import SingleTaskIcon from '@/components/icons/SingleTaskIcon.vue';
import Task from '@/components/buttons/Task.vue';
import Paginate from './Paginate.vue';

const choreStore = useChoreStore();

const tasks = computed(() => choreStore.tasks);
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
        Page {{ choreStore.taskPagination.page }} of {{ choreStore.totalTaskPages}}
      </template>
    </TaskType>
    <div v-if="tasks.length === 0">
      <h2>No tasks</h2>
    </div>
    <div v-auto-animate>
      <Task v-for="task in tasks" :task="task" :key="task.id" />
    </div>
    
    <Paginate
      :pages="choreStore.totalTaskPages"
      v-model:page="choreStore.taskPagination.page"
      :added="choreStore.taskPagination.added"
      @prev="choreStore.previousTaskPage"
      @setPage="(page) => choreStore.setTaskPage(page)"
      @next="choreStore.nextTaskPage"
    />
  </div>
</template>

<style lang="scss" scoped>
.button {
  &:hover,
  &:focus {
    cursor: pointer;
  }
}
</style>
