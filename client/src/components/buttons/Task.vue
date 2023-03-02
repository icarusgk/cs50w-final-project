<script setup lang="ts">
import type { ITag, ITask } from '@/types';

const props = defineProps<{
  task: ITask;
}>();

// @ts-ignore
const { toggleDone, deleteTask, setCurrentTask } = inject('taskFunctions');
const chore = useModalStore();

const open = ref(false);

watch(open, () => {
  chore.toggle();
});

const closeModal = () => open.value = false;
provide('closeModal', closeModal);
</script>

<template>
  <div class="flex items-center my-2 mb-2">
    <div @click="toggleDone(task)" class="pointer mr-4" v-auto-animate>
      <DoneIcon v-if="!task.done" />
      <MarkedDoneIcon v-else />
    </div>
    <!-- Name -->
    <div
      :class="[
        'flex items-center justify-between py-1.5 px-4 bg-vivid-red w-full rounded-lg transition duration-200 ease',
        { 'opacity-40': task.done },
      ]"
    >
      <div
        @click="setCurrentTask(task)"
        class="title-container"
      >
        <Popper hover arrow placement="bottom" openDelay="1000">
          <span class="title pointer">{{ props.task.title }}</span>
          <template #content> Click to set it to current </template>
        </Popper>
      </div>
      <div class="flex items-center">
        <div class="mr-4">
          <span class="hidden ml-20 xs:block"
            >{{ task.gone_through }} / {{ task.estimated }}</span
          >
        </div>
        <div class="pointer mr-1" @click="deleteTask(task)">
          <DeleteIcon />
        </div>
        <div class="pointer" @click="open = true">
          <TaskInfoIcon />
        </div>
      </div>
    </div>
    <TheTaskModal
      :task="props.task"
      :open="open"
      @exit:modal="open = false"
    />
  </div>
</template>
