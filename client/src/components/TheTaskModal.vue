<script setup lang="ts">
import type { ITag, ITask } from '@/types';
import { toggleDone, deleteTask, addTag, removeTag, saveTask } from '@/utils/taskFns';

const props = defineProps<{
  task: ITask;
  open: boolean;
}>();

const emit = defineEmits<{
  (e: 'exit:modal'): any
}>()

// @ts-ignore
// const { toggleDone, deleteTask, addTag, removeTag, saveTask } = inject('taskFunctions');

// This way it prevents from mutating the original object
// inside props.task by reference
const width = ref(window.innerWidth);
let localTask = reactive<ITask>({ ...props.task });

const isFormPristine = computed(() => {
  return localTask.title === props.task.title
    && localTask.description === props.task.description
    && localTask.estimated === props.task.estimated
});

function saveTheTask() {
  saveTask(props.task, { ...localTask });
  emit('exit:modal');
}

function deleteTheTask() {
  deleteTask(props.task);
  emit('exit:modal');
}

function exitWithoutSaving() {
  // Copy the props again
  localTask.title = props.task.title;
  localTask.description = props.task.description;
  localTask.estimated = props.task.estimated;
  emit('exit:modal');
}

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
    <AppModal :open="open" @exit:modal="exitWithoutSaving()" :is-task="true">
      <!-- Tags -->
      <template #tags>
        <Tags
          :id="props.task.id"
          :task="props.task"
          @add:tag="(tag: ITag) => addTag(props.task, tag)"
          @remove:tag="(tag: ITag) => removeTag(props.task, tag.id)"
          @close:modal="$emit('exit:modal')"
        />
        <div class="flex items-baseline items-center">
          <div @click="toggleDone(task)" class="pointer mr-1" v-auto-animate>
            <div class="i-fluent:checkmark-circle-32-regular scale-130" v-if="!task.done" />
            <div class="i-fluent:checkmark-circle-32-filled scale-130 bg-vivid-red" v-else />
          </div>
          <div
            @click="deleteTheTask()"
            class="my-[0.1rem] mx-2 mr-5 pointer i-fluent:delete-20-filled scale-150"
          />
        </div>
      </template>
      <!-- Title -->
      <template #title>
        <input
          type="text"
          name="title"
          class="border-none bg-transparent text-white text-4xl font-bold w-full focus:outline-none"
          @keyup.ctrl.enter="saveTheTask()"
          v-model="localTask.title"
          v-focus
        />
      </template>
      <!-- Body -->
      <TheTaskModalBody
        :task="localTask"
        @input:description="(desc: string) => localTask.description = desc"
        @change:pomoCount="(pomos: number) => localTask.estimated = pomos"
        @save:task="saveTheTask()"
      />
      <template #save-button>
        <AddToProjectPopup :taskId="props.task.id" />
        <div class="text-center" v-if="width < 480">
          <span class="font-semibold text-xl"
            >Pomos done: {{ task.gone_through }}</span
          >
        </div>
        <SaveButton :enabled="!isFormPristine" @click="saveTheTask()" />
      </template>
    </AppModal>
  </div>
</template>
