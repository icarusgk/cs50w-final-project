<script setup lang="ts">
import { ref, watch, computed, watchEffect } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { useModalStore } from '@/stores/modal';
import { useChoreStore } from '@/stores/chore';
import axios from 'axios';
import TaskModal from './TaskModal.vue';
import TaskInfoIcon from './icons/TaskInfoIcon.vue';
import CloseIcon from './icons/CloseIcon.vue';
import Popper from 'vue3-popper';


const task = ref();
const auth = useAuthStore();
const chore = useChoreStore();
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
      <div class="current-task-container">        
        <div @click="open = true" class="container">
          <div class="info">
            <TaskInfoIcon />
            <span>Working on task: {{ task?.title }}</span>
          </div>
        </div>
        <Popper hover>
          <CloseIcon @click="chore.changeCurrentTask(0)" class="close-icon" />
          <template #content>
            Remove current task
          </template>
        </Popper>
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

:deep(.popper) {
  padding: 1rem;
  border-radius: 10px;
  color: #fff;
  font-weight: bold;
}

.current-task-container {
  display: flex;
  align-items: center;
  gap: 1rem;
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

  .close-icon {
    &:hover,
    &:focus,
    &:active {
      cursor: pointer;
    }
  }
}
</style>