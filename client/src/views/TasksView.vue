<script setup lang="ts">
import type { ITask } from '@/types';

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

function deleteTask(task: ITask) {
  if (window.confirm('Are you sure you want to delete this task??????')) {
    chore.deleteTask(task);

    if (
      chore.taskPagination.page === chore.totalTaskPages &&
      chore.tasks.length === 1
    ) {
      chore.decreaseTaskPagination();
    }
  }
}
</script>

<template>
  <div class="p-2 lg:p-6 text-white">
    <div class="flex items-center text-white gap-4">
      <BackIcon class="pointer" @click="$router.back()" />
      <span class="font-extrabold text-5xl">Tasks</span>
    </div>
    <Paginate
      class="mt-4"
      :pages="chore.totalTaskPages"
      :page="chore.taskPagination.page"
      :added="chore.taskPagination.added"
      @prev="chore.previousTaskPage()"
      @set:page="(page: number) => setPage(page)"
      @set:added="(added: number) => setAdded(added)"
      @next="chore.nextTaskPage()"
    />
    <div v-if="chore.tasks.length > 0">
      <div class="flex flex-wrap gap-4 mt-4">
        <BaseViewTask
          v-for="task in tasks"
          :task="task"
          :key="task.id"
          @deleteTask="deleteTask($event)"
        />
      </div>
      <Paginate
        :pages="chore.totalTaskPages"
        :page="chore.taskPagination.page"
        :added="chore.taskPagination.added"
        @prev="chore.previousTaskPage()"
        @set:page="(page: number) => setPage(page)"
        @set:added="(added: number) => setAdded(added)"
        @next="chore.nextTaskPage()"
      />
    </div>
    <div class="m-4 flex items-center" v-else>
      <TaskInfoIcon />
      <span class="ml-4 font-semibold text-2xl">No Tasks</span>
    </div>
  </div>
</template>
