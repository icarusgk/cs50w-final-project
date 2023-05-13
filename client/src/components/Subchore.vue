<script setup lang="ts">
import type { ITag, ITask } from '@/types';
const props = defineProps<{
  chore: ITask;
  newChore?: boolean;
  isProject: boolean;
  parentNew?: boolean;
}>();

defineEmits<{
  (e: 'save:project'): void;
  (e: 'save:task'): void;
  (e: 'close:details'): void;
  (e: 'delete:chore'): void;
  (e: 'remove:chore'): void;
  (e: 'remove:tag', tag: ITag): void;
  (e: 'change:title', newTitle: string): void;
  (e: 'change:description', newDescription: string): void;
  (e: 'change:pomoCount', pomoCount: number): void;
}>();
</script>

<template>
  <!-- Blur -->
  <div class="p-4 bg-[#3a3a3a66] transform rounded-xl">
    <!-- Flex row -->
    <div class="flex flex-col justify-between h-full">
      <div v-if="props.isProject" class="flex">
        <Tags
          :id="props.chore.id"
          :task="props.chore"
          :new="newChore"
          @remove:tag="$emit('remove:tag', $event)"
        />
      </div>
      <!-- Title and description -->
      <div class="flex flex-col">
        <!-- Title -->
        <input
          :value="props.chore.title"
          @input="event => $emit('change:title', (event.target as HTMLInputElement).value)"
          placeholder="Title"
          type="text"
          autofocus
          class="border-none bg-transparent text-white text-2xl font-bold w-full focus:outline-none"
          @keyup.ctrl.enter="
            isProject ? $emit('save:task') : $emit('save:project')
          "
        />
        <!-- Description -->
        <textarea
          :value="props.chore.description"
          @input="event => $emit('change:description', (event.target as HTMLInputElement).value)"
          class="w-full h-12.5 outline-none bg-transparent text-white border-none resize-none"
          placeholder="Description"
          @keyup.ctrl.enter="
            isProject ? $emit('save:task') : $emit('save:project')
          "
        >
        </textarea>
      </div>
      <div class="flex items-center justify-end">
        <div class="mr-4">
          <div
            class="pointer i-fluent:delete-20-filled"
            v-if="!newChore"
            @click="$emit('delete:chore')"
          />
          <div class="pointer i-fluent:delete-20-filled" v-if="newChore && parentNew" @click="$emit('remove:chore')" />
        </div>
        <div v-if="props.isProject">
          <PomoCountSetter
            :chore="chore"
            @change:pomoCount="(count: number) => $emit('change:pomoCount', count)"
          />
        </div>
        <!-- Estimated Timers and save button -->
        <div class="flex flex-col self-end">
          <!-- Buttons -->
          <div class="flex justify-end">
            <!-- Emit the close event -->
            <!-- Cancel -->
            <button @click="$emit('close:details')" class="cancel-btn mr-2 pointer">Close</button>
            <!-- Save -->
            <button
              v-if="!isProject"
              @click="$emit('save:project')"
              class="timer-btn save-btn pointer"
            >
              Save!
            </button>
            <button v-else class="save-btn pointer" @click="$emit('save:task')">
              Save!
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
