<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import { useChoreStore } from '@/stores/chore';

import TaskType from '@/components/slots/TaskType.vue';
import SingleTaskIcon from '@/components/icons/SingleTaskIcon.vue';
import Task from '@/components/buttons/Task.vue';
import Paginate from './Paginate.vue';

const chore = useChoreStore();

// Back to 1 / 4;
chore.taskPagination.page = 1;
chore.taskPagination.page_size = 4;
chore.taskPagination.added = 1;

const tasks = computed(() => chore.tasks.slice(0, 4));

const currentTask = ref();

const setCurrent = (id: number) => currentTask.value = id;

// A id debouncer
watch(currentTask, (prevId, curId) => {
  if (prevId !== curId) {
    chore.changeCurrentTask(currentTask.value);
  }
})
</script>

<template>
  <div>
    <TaskType class="button" @click="$router.push('/tasks')">
      <template #icon>
        <SingleTaskIcon />
      </template>
      <template #type>
        <h1 @click="$router.push('/tasks')">Single Tasks</h1>
      </template>
      <template #count>
        <span v-if="chore.totalTaskPages > 1">
          Page {{ chore.taskPagination.page }} of {{ chore.totalTaskPages}}
        </span>
      </template>
    </TaskType>
    <div v-if="tasks.length === 0">
      <span>The are no tasks</span>
    </div>
    <div v-auto-animate>
      <Task
        v-for="task in tasks"
        :task="task"
        :key="task.id"
        @setCurrent="setCurrent"
      />
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
