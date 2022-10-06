<script setup lang="ts">
import { ref, watch, computed, onMounted } from 'vue';
import { useChoreStore } from '@/stores/chore';
import { useAuthStore } from '@/stores/auth';
import { useModalStore } from '@/stores/modal';
import axios from 'axios';
import TaskModal from './TaskModal.vue';
import TaskInfoIcon from './icons/TaskInfoIcon.vue';

const task = ref();
const chore = useChoreStore();
const currentTask = computed(() => chore.currentTaskId);
const open = ref(false);


async function getTask() {  
  const response = await axios.get(`tasks/${currentTask.value}/`);
  task.value = response?.data;
}

onMounted(() => {
  if (useAuthStore().isAuthenticated) {
    getTask();
  }
});

// A kind of debouncer?
watch(
  () => currentTask.value,
  (prevTask, curTask) => {
    if (prevTask !== curTask) getTask();
  }
);
watch(open, () => {
  useModalStore().toggle();
});
</script>

<template>
  <div 
    v-if="useAuthStore().isAuthenticated && chore.currentTaskId" 
    style="margin-top: 1rem"
  >
    <div @click="open = true" class="container">
      <div class="info">
        <TaskInfoIcon />
        <span>Working on task: {{ task?.title }}</span>
      </div>
    </div>
    <TaskModal :open="open" :task="task" @exit="open = false" />
  </div>
</template>


<style scoped lang="scss">
  .container {
    background: #333;
    color: white;
    padding: 1rem;
    border-radius: 10px;
    font-weight: 600;

    .info {
      display: flex;
      align-items: center;

      span {
        margin-left: 0.5rem;
      }
    }

    &:hover,
    &:focus,
    &:active {
      cursor: pointer;
    }
  }
</style>