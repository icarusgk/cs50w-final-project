<script setup lang="ts">
import Title from '@/components/slots/Title.vue';
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
  <div class="mt-2">
    <!-- Tasks Title -->
    <Title class="pointer" @click="$router.push('/tasks')">
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
    </Title>
    <!-- Task List Container -->
    <div>
      <div class="flex items-center bg-light-gray w-full p-4 rounded-xl lg:w-4/5" v-if="tasks.length === 0">
        <TaskInfoIcon />
        <span>There are no tasks</span>
      </div>
      <!-- List of Tasks -->
      <div v-auto-animate>
        <Task
          v-for="task in tasks"
          :task="task"
          :key="task.id"
          @set:currentTask="(id: number) => setCurrent(id)"
        />
      </div>
    </div>
    <!-- Pagination -->
    <Paginate
      :pages="chore.totalTaskPages"
      :page="chore.taskPagination.page"
      :added="chore.taskPagination.added"
      @prev="chore.previousTaskPage"
      @set:page="(page: number) => setPage(page)"
      @set:added="(added: number) => setAdded(added)"
      @next="chore.nextTaskPage"
    />
  </div>
</template>

