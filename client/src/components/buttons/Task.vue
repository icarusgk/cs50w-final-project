<script setup lang="ts">
import type { ITask } from '@/types';

const modal = useModalStore();
const chore = useChoreStore();
const auth = useAuthStore();

const props = defineProps<{
  task: ITask;
}>();

const open = ref(false);

watch(open, () => {
  modal.toggle();
});

function changeTask(task: ITask) {
  // Debouncer
  if (auth.user?.current_task_id != task.id) {
    chore.changeCurrentTask(task.id);
  }
}
</script>

<template>
  <div class="flex items-center my-2 mb-2">
    <div @click="chore.toggleDone(task)" class="pointer mr-4" v-auto-animate>
      <div class="i-fluent:checkmark-circle-32-regular scale-130" v-if="!task.done" />
      <div class="i-fluent:checkmark-circle-32-filled scale-130 bg-vivid-red" v-else />
    </div>
    <!-- Name -->
    <div
      :class="[
        'flex items-center justify-between py-1.5 px-4 bg-vivid-red w-full rounded-lg transition duration-200 ease',
        { 'opacity-40': task.done },
      ]"
    >
      <div
        class="title-container"
      >
        <Popper hover arrow placement="bottom" openDelay="1000">
          <span @click="changeTask(task)" class="title pointer">{{ props.task.title }}</span>
          <template #content> Click to set it to current </template>
        </Popper>
      </div>
      <div class="flex items-center">
        <div class="mr-4">
          <span class="hidden ml-20 xs:block"
            >{{ task.gone_through }} / {{ task.estimated }}</span
          >
        </div>
        <div class="pointer i-fluent:delete-20-filled scale-135 mr-2" @click="chore.deleteTask(task)" />
        <div class="pointer i-fluent:info-24-regular scale-135" @click="open = true" />
      </div>
    </div>
    <TheTaskModal
      :task="props.task"
      :open="open"
      @exit:modal="open = false"
    />
  </div>
</template>
