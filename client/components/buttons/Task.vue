<script setup lang="ts">
import type { ITask } from '@/types';

const modal = useModalStore();
const chore = useChoreStore();
const auth = useAuthStore();

const props = defineProps<{
  task: ITask;
}>();

function openTask() {
  modal.content = props.task;
  modal.isOpened = true;
}

function changeCurrentTask(task: ITask) {
  // Debouncer
  if (auth.user?.current_task_id != task.id) {
    chore.changeCurrentTask(task.id);
  }
}
</script>

<template>
  <div class="flex items-center mb-2">
    <div @click="chore.toggleDone(task)" class="pointer mr-4" v-auto-animate>
      <div class="i-fluent:checkmark-circle-32-regular scale-130" v-if="!task.done" />
      <div class="i-fluent:checkmark-circle-32-filled scale-130 bg-vivid-red" v-else />
    </div>
    <!-- Container -->
    <div class="flex items-center justify-between px-4 bg-vivid-red w-full rounded-lg transition duration-200 ease" :class="{ 'opacity-40': task.done }">
      <!-- Title -->
      <div @click="openTask()" class="w-70 pointer py-2">
        <span class="font-bold">{{ props.task.title }}</span>
        <p class="text-xs">{{ props.task.description }}</p>
      </div>
      <div class="flex items-center">
        <span class="hidden mr-4 xs:block">
          {{ task.gone_through }} / {{ task.estimated }}
        </span>
        <div @click="chore.deleteTask(task)" class="pointer i-fluent:delete-20-filled scale-135 mr-2" />
        <div @click="changeCurrentTask(task)" class="pointer i-fluent:info-24-regular scale-135" />
      </div>
    </div>
  </div>
</template>
