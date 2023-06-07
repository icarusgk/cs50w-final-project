<script setup lang="ts">
import { ITask } from '~/types';
const auth = useAuthStore();
const chore = useChoreStore();
const modal = useModalStore();

const { currentTask: task } = storeToRefs(chore)

watchEffect(async () => {
  const currentTaskId = auth.user?.current_task_id;
  
  if (currentTaskId !== 0 && auth.user) {
    const { _data } = await useRawFetch<ITask>(`tasks/${currentTaskId}/`);    
    task.value = _data;
  }
});

function setTask() {
  modal.content = task.value as ITask;
  modal.open();
}
function updateLocal(updatedTask: ITask) {
  task.value = updatedTask;
}
</script>

<template>
  <Transition name="slide">
    <div v-if="auth.user?.current_task_id !== 0 && auth.user && task" style="margin-top: 1rem">
      <div class="flex items-center gap-4">
        <div @click="setTask()" class="w-84 bg-[#333] text-white p-4 rounded-lg font-semibold depth pointer active:shadow-none active:shadow-dark-gray">
          <div class="flex items-center">
            <div class="i-fluent-info-12-regular scale-150 ml-3" />
            <span class="ml-2">Working on task: {{ task?.title }}</span>
          </div>
        </div>
        <Popper hover>
          <div @click="chore.changeCurrentTask(0)" class="pointer i-fluent-dismiss-circle-32-filled scale-220" />
          <template #content> Remove current task </template>
        </Popper>
      </div>
    </div>
  </Transition>
</template>

<style scoped>
.slide-enter-active,
.slide-leave-active {
  transition: opacity 0.3s ease-in-out;
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
</style>
