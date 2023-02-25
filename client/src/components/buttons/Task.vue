<script setup lang="ts">
import type { ITask } from '@/types';

const props = defineProps<{
  task: ITask;
}>();

defineEmits<{
  (e: 'set:currentTask', id: number): void
}>();

const open = ref(false);
const chore = useChoreStore();

watch(open, () => {
  useModalStore().toggle();
});

async function toggleDone() {
  const response = await axios.patch(`tasks/${props.task.id}/`, {
    obj: 'task',
    action: 'done',
  });
  if (response?.status === 200) {
    props.task.done = response.data?.done;
    chore.fetchProjects();
  }
}

function deleteTask() {
  if (window.confirm('Are you sure you want to delete this task?')) {
    chore.deleteTask(props.task);

    if (
      chore.taskPagination.page === chore.totalTaskPages &&
      chore.tasks.length === 1
    ) {
      chore.decreaseTaskPagination();
    }
  }
}
</script>

<template>
  <div class="flex items-center my-2 mb-2">
    <div @click="toggleDone()" class="pointer mr-4" v-auto-animate>
      <DoneIcon v-if="!task.done" />
      <MarkedDoneIcon v-else />
    </div>
    <!-- Name -->
    <div :class="[{ 'opacity-40': task.done }, 'flex items-center justify-between py-1.5 px-4 bg-vivid-red w-full rounded-lg transition druation-200 ease']">
      <div @click="$emit('set:currentTask', task.id as number)" class="title-container">
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
        <div class="pointer mr-1" @click="deleteTask()">
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
      @toggle:done="toggleDone()"
      @delete:Task="deleteTask()"
    />
  </div>
</template>
