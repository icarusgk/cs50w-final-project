<script setup lang="ts">
import type { ITask, ITag } from '@/types';

const chore = useChoreStore();

// Back to 1 / 4;
chore.taskPagination.page = 1;
chore.taskPagination.page_size = 4;
chore.taskPagination.added = 1;

chore.fetchTasks();

const tasks = computed(() => chore.tasks.slice(0, 4));

const currentTask = ref();

function addTag(task: ITask, tag: ITag) {
  task.tags.push(tag);
}

function removeTag(task: ITask, tagId: number) {
  task.tags = task.tags.filter((tag: ITag) => tag.id !== tagId);
}

function saveTask(oldTask: ITask, newTask: ITask) {
  chore.saveTask(newTask);
  oldTask = newTask;
}

async function toggleDone(task: ITask) {
  const response = await axios.patch(`tasks/${task.id}/`, {
    obj: 'task',
    action: 'done',
  });
  if (response?.status === 200) {
    task.done = response.data?.done;
    chore.fetchProjects();
  }
}
function deleteTask(task: ITask) {
  if (window.confirm('Are you sure you want to delete this task?')) {
    chore.deleteTask(task);

    if (
      chore.taskPagination.page === chore.totalTaskPages &&
      chore.tasks.length === 1
    ) {
      chore.decreaseTaskPagination();
    }
  }
}

function setCurrentTask(task: ITask) {
  currentTask.value = task.id;
}

provide('taskFunctions', {
  addTag,
  removeTag,
  saveTask,
  toggleDone,
  deleteTask,
  setCurrentTask
})


// // A id debouncer
// watch(currentTask, (prevId, curId) => {
//   if (prevId !== curId) {
//     chore.changeCurrentTask(currentTask.value);
//   }
// });
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

