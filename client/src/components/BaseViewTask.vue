<script setup lang="ts">
import type { ITask } from '@/types';

defineProps<{
  task: ITask;
}>();

defineEmits<{
  (e: 'delete:task', task: ITask): void
}>();

const open = ref(false);

watch(open, () => {
  useModalStore().toggle();
});
</script>

<template>
  <!-- w-[320px] -->
  <div class="w-full p-4 bg-[#3d3d3d] rounded-lg pointer md:w-[320px] pointer h-min text-white">
    <div class="flex justify-between">
      <div class="flex mr-8 h-min">
        <Tags :task="task" :info="true" />
      </div>
      <div class="flex">
        <div class="flex items-center mr-2.5">
          <TasksDoneIcon />
          <span class="ml-1.25">{{ task.gone_through }}</span>
        </div>
        <div class="flex items-center">
          <TotalTasksIcon />
          <span class="ml-1.25">{{ task.estimated }}</span>
        </div>
      </div>
    </div>
    <div class="flex flex-col h-[85%] justify-center" @click="open = true">
      <span class="font-bold">{{ task.title }}</span>
      <span>{{ task.description }}</span>
    </div>
    <TheTaskModal
      :task="task"
      :open="open"
      @exit:modal="open = false"
      @delete:task="$emit('delete:task', task)"
    />
  </div>
</template>
