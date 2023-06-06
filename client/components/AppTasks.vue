<script setup lang="ts">
const chore = useChoreStore();
const page = usePageStore();

const router = useRouter();

// Back to 1 / 4;
page.taskPagination.page = 1;
page.taskPagination.page_size = 4;
page.taskPagination.added = 1;

chore.fetchTasks();

const tasks = computed(() => chore.tasks.slice(0, 4));
</script>

<template>
  <div class="mt-2">
    <!-- Tasks Title -->
    
    <ChoreTitle class="pointer my-4 mx-3" @click="router.push('/tasks')">
      <template #icon>
        <div class="i-mdi:clipboard-check-multiple scale-300 mr-3"></div>
      </template>
      <template #type>
        <h1 @click="router.push('/tasks')">Your Tasks</h1>
      </template>
      <template #count>
        <span v-if="page.totalTaskPages > 1">
          Page {{ page.taskPagination.page }} of {{ page.totalTaskPages }}
        </span>
      </template>
    </ChoreTitle>
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
      :pages="page.totalTaskPages"
      :page="page.taskPagination.page"
      :added="page.taskPagination.added"
      @prev="page.previousTaskPage"
      @set:page="(p: number) => page.setTaskPage(p)"
      @set:added="(added: number) => page.setTaskAdded(added)"
      @next="page.nextTaskPage"
    />
  </div>
</template>

