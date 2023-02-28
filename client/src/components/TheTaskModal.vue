<script setup lang="ts">
import type { ITag, ITask } from '@/types';

const props = defineProps<{
  task: ITask;
  open: boolean;
}>();

// const emit = defineEmits(['exit', 'toggleDone', 'deleteTask']);
const emit = defineEmits<{
  (e: 'exit:modal'): void
  (e: 'toggle:done'): void
  (e: 'delete:task'): void
}>();

let tmpNewTitle = '';
let tmpNewDesc = '';
let tmpEstimated: number;

const chore = useChoreStore();

// Saves task with PUT method
function saveTask() {
  props.task.title = tmpNewTitle !== '' ? tmpNewTitle : props.task.title;
  props.task.description =
    tmpNewDesc !== '' ? tmpNewDesc : props.task.description;
  props.task.estimated =
    tmpEstimated !== null ? tmpEstimated : props.task.estimated;

  chore.saveTask(props.task);

  emit('exit:modal');
}

function deleteTask() {
  emit('delete:task');
  emit('exit:modal');
}

function removeTag(tag: ITag) {
  props.task.tags = props.task.tags.filter((t: ITag) => t.id !== tag.id);
}

function handleInput(event: any) {
  tmpNewTitle = event.target.value;
}

const handleDesc = (desc: any) => (tmpNewDesc = desc);

const handlePomos = (pomos: number) => (tmpEstimated = pomos);

const width = ref(window.innerWidth);

onMounted(() => {
  window.addEventListener('resize', () => (width.value = window.innerWidth));
});

onUnmounted(() => {
  window.removeEventListener('resize', () => (width.value = window.innerWidth));
});
</script>

<template>
  <div class="task-container">
    <!-- Modal -->
    <AppModal :open="open" @exit:modal="$emit('exit:modal')" :is-task="true">
      <!-- Tags -->
      <template #tags>
        <Tags
          :task="props.task"
          :id="props.task.id"
          @remove:tag="(tag: ITag) => removeTag(tag)"
          @close:modal="$emit('exit:modal')"
        />
        <div class="flex items-baseline">
          <div class="pointer" v-auto-animate>
            <DoneIcon @click="$emit('toggle:done')" v-if="!props.task.done" />
            <MarkedDoneIcon @click="$emit('toggle:done')" v-else />
          </div>
          <DeleteIcon @click="deleteTask()" class="my-[0.1rem] mx-2 pointer" />
        </div>
      </template>
      <!-- Title -->
      <template #title>
        <input
          type="text"
          name="title"
          class="border-none bg-transparent text-white text-4xl font-bold w-full focus:outline-none"
          @input="(event) => handleInput(event)"
          :value="props.task.title"
          @keyup.ctrl.enter="saveTask()"
          v-focus
        />
      </template>
      <!-- Body -->
      <TheTaskModalBody
        :task="props.task"
        @input:description="handleDesc"
        @change:pomoCount="handlePomos($event)"
        @save:task="saveTask()"
      />
      <template #save-button>
        <AddToProjectPopup :taskId="props.task.id" />
        <div class="text-center" v-if="width < 480">
          <span class="font-semibold text-xl">Pomos done: {{ task.gone_through }}</span>
        </div>
        <SaveButton @click="saveTask()" />
      </template>
    </AppModal>
  </div>
</template>
