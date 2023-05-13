<script setup lang="ts">
import type { ITask } from '@/types';

const chore = useChoreStore();
const page = usePageStore();

// Back to 1 / 10
page.taskPagination.page = 1;
page.taskPagination.page_size = 10;
page.taskPagination.added = 1;

chore.fetchTasks();

const tasks = computed(() => chore.tasks);

function setPage(newPage: number) {
  page.setTaskPage(newPage);
}

function setAdded(newAdded: number) {
  page.setTaskAdded(newAdded);
}

function deleteTask(task: ITask) {
  if (window.confirm('Are you sure you want to delete this task??????')) {
    chore.deleteTask(task);

    if (
      chore.taskPagination.page === chore.totalTaskPages &&
      chore.tasks.length === 1
    ) {
      page.decreaseTaskPagination();
    }
  }
}
</script>

<template>
  <div class="p-2 lg:p-6 text-white">
    <div class="flex items-center text-white gap-4 ml-3">
      <div class="pointer i-bi-arrow-left-square-fill scale-250" @click="$router.back()" />
      <span class="font-extrabold text-5xl">Tasks</span>
    </div>
    <Paginate
      class="mt-4"
      :pages="page.totalTaskPages"
      :page="page.taskPagination.page"
      :added="page.taskPagination.added"
      @prev="page.previousTaskPage()"
      @set:page="(page: number) => setPage(page)"
      @set:added="(added: number) => setAdded(added)"
      @next="page.nextTaskPage()"
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
        :pages="page.totalTaskPages"
        :page="page.taskPagination.page"
        :added="page.taskPagination.added"
        @prev="page.previousTaskPage()"
        @set:page="(page: number) => setPage(page)"
        @set:added="(added: number) => setAdded(added)"
        @next="page.nextTaskPage()"
      />
    </div>
    <div class="m-4 flex items-center" v-else>
      <div class="i-fluent-info-12-regular scale-150 ml-3" />
      <span class="ml-4 font-semibold text-2xl">No Tasks</span>
    </div>
  </div>
</template>
