<script setup lang="ts">
import type { ITag, ITask } from '@/types';

defineProps<{
  task: ITask;
}>();

const emit = defineEmits<{
  (e: 'delete:task', task: ITask): void
  (e: 'remove:tag', task: ITask, tag?: ITag): void
}>();

const modal = useModalStore();
const open = ref(false);

watch(open, () => modal.toggle());

const deleteTask = (task: ITask) => emit('delete:task', task);

function removeTag(task: ITask, tag?: ITag) {
  emit('remove:tag', task, tag);
  modal.close();
}
</script>

<template>
  <div class="w-full p-4 bg-[#3d3d3d] rounded-lg pointer md:w-[320px] pointer h-min text-white">
    <div class="flex justify-between">
      <div class="flex mr-8 h-min">
        <Tags info :task="task" />
      </div>
      <div class="flex">
        <div class="flex items-center mr-2.5">
          <div class="i-fluent-arrow-clockwise-28-filled" />
          <span class="ml-1.25">{{ task.gone_through }}</span>
        </div>
        <div class="flex items-center">
          <div class="i-fluent-clock-28-filled" />
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
      @delete:task="deleteTask"
      @remove:tag="removeTag"
    />
  </div>
</template>
