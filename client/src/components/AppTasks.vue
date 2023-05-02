<script setup lang="ts">
const chore = useChoreStore();

// Back to 1 / 4;
chore.taskPagination.page = 1;
chore.taskPagination.page_size = 4;
chore.taskPagination.added = 1;

chore.fetchTasks();

const tasks = computed(() => chore.tasks.slice(0, 4));
</script>

<template>
  <div class="mt-2">
    <!-- Tasks Title -->
    <Title class="pointer my-4 mx-3" @click="$router.push('/tasks')">
      <template #icon>
        <div class="i-mdi:clipboard-check-multiple scale-350 mr-3"></div>
      </template>
      <template #type>
        <h1 @click="$router.push('/tasks')">Single Tasks</h1>
      </template>
      <template #count>
        <span v-if="chore.totalTaskPages > 1">
          Page {{ chore.taskPagination.page }} of {{ chore.totalTaskPages }}
        </span>
      </template>
    </Title>
    <!-- Task List Container -->
    <div>
      <div class="flex items-center bg-light-gray w-full p-4 rounded-xl lg:w-4/5" v-if="tasks.length === 0">
        <div class="i-fluent-info-12-regular scale-150 ml-3" />
        <span class="ml-4">There are no tasks</span>
      </div>
      <!-- List of Tasks -->
      <div v-auto-animate>
        <Task
          v-for="task in tasks"
          :task="task"
          :key="task.id"
        />
      </div>
    </div>
    <!-- Pagination -->
    <Paginate
      :pages="chore.totalTaskPages"
      :page="chore.taskPagination.page"
      :added="chore.taskPagination.added"
      @prev="chore.previousTaskPage"
      @set:page="(page: number) => chore.setTaskPage(page)"
      @set:added="(added: number) => chore.setTaskAdded(added)"
      @next="chore.nextTaskPage"
    />
  </div>
</template>

