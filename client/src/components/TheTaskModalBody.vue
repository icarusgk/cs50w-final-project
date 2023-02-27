<script setup lang="ts">
import type { ITask } from '@/types';

defineProps<{
  task: ITask;
  isNew?: boolean;
}>();

defineEmits<{
  (e: 'input:description', description: string): void
  (e: 'change:pomoCount', count: number): void
  (e: 'save:task'): void
}>();
</script>

<template>
  <div>
    <!-- Description -->
    <div class="mt-2 mb-0 lg:my-4 lg:mx-0">
      <textarea
        @input="event => $emit('input:description', (event.target as HTMLInputElement).value)"
        @keyup.ctrl.enter="$emit('save:task')"
        :value="task.description"
        placeholder="Description"
        class="h-[80px] placeholder-gray-300 w-full outline-none border-b-gray-400 border-b-[1px] bg-transparent lg:h-[50px]"
      >
      </textarea>
    </div>
    <!-- Subtasks -->
    <div class="my-4 mx-0">
      <h2>Subtasks</h2>
      <!-- Add subtask button -->
      <div>
        <!-- Subtasks list -->
        <Subchores
          :is-project="false"
          :chores="task.subtasks"
          :task="task"
          :isNew="isNew"
        />
      </div>
    </div>
    <!-- Bottom container -->
    <div class="flex flex-col">
      <!-- Estimated Pomos -->
      <div class="flex">
        <div>
          <span class="font-extrabold">Estimated pomos</span>
        </div>
        <!-- Counter -->
        <PomoCountSetter
          :chore="task"
          @change:pomoCount="(count: number) => $emit('change:pomoCount', count)"
        />
      </div>
    </div>
  </div>
</template>
