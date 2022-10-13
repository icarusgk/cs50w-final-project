<script setup lang="ts">
import { ref, watch, computed, watchEffect } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { useModalStore } from '@/stores/modal';
import axios from 'axios';
import TaskModal from './TaskModal.vue';
import TaskInfoIcon from './icons/TaskInfoIcon.vue';

const task = ref();
const auth = useAuthStore();
const userTaskId = computed(() => auth.user?.current_task_id);
const open = ref(false);

async function getTask(id: any) {
  const response = await axios.get(`tasks/${id}/`);
  task.value = response?.data;
}

watchEffect(
  () => {
    if (userTaskId.value !== 0 && auth.user) {
      getTask(userTaskId.value);
    }
  }
);

// The modal blur
watch(open, () => {
  useModalStore().toggle();
});
</script>

<template>
  <Transition name="slide">
    <div 
      v-if="userTaskId !== 0 && auth.user" 
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
  </Transition>
</template>


<style scoped lang="scss">
.slide-enter-active,
.slide-leave-active {
  transition: opacity 0.7s ease-in-out;
}

.slide-enter-from,
.slide-leave-to {
  opacity: 0;
}

.container {
  width: 21rem;
  background: #333;
  color: white;
  padding: 1rem;
  border-radius: 10px;
  font-weight: 600;
  box-shadow: 3px 4px rgb(71, 71, 71);
  transition: box-shadow 0.1s cubic-bezier(0.075, 0.82, 0.165, 1);

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
  &:active {
    box-shadow: 0 0 #333;
  }
}
</style>