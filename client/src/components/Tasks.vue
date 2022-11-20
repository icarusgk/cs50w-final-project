<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import { useChoreStore } from '@/stores/chore';

import TaskType from '@/components/slots/TaskType.vue';
import SingleTaskIcon from '@/components/icons/SingleTaskIcon.vue';
import TaskInfoIcon from './icons/TaskInfoIcon.vue';
import Task from '@/components/buttons/Task.vue';
import Paginate from '@/components/Paginate.vue';

const chore = useChoreStore();

// Back to 1 / 4;
chore.taskPagination.page = 1;
chore.taskPagination.page_size = 4;
chore.taskPagination.added = 1;

chore.fetchTasks();

const tasks = computed(() => chore.tasks.slice(0, 4));

const currentTask = ref();

const setCurrent = (id: number) => (currentTask.value = id);

// A id debouncer
watch(currentTask, (prevId, curId) => {
  if (prevId !== curId) {
    chore.changeCurrentTask(currentTask.value);
  }
});

function setPage(newPage: number) {
  chore.setTaskPage(newPage);
}

function setAdded(newAdded: number) {
  chore.setTaskAdded(newAdded);
}
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
          Page {{ chore.taskPagination.page }} of {{ chore.totalTaskPages }}
        </span>
      </template>
    </TaskType>
    <div class="no-tasks" v-if="tasks.length === 0">
      <TaskInfoIcon />
      <span>There are no tasks</span>
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
      :page="chore.taskPagination.page"
      :added="chore.taskPagination.added"
      @prev="chore.previousTaskPage"
      @setPage="setPage($event)"
      @setAdded="setAdded($event)"
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

.no-tasks {
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
  .no-tasks {
    width: 100%;
  }
}
</style>
