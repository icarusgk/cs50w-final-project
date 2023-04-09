<script setup lang="ts">
import type { ITag, ITask } from '@/types';

const props = defineProps<{
  task: ITask;
  open: boolean;
}>();

// @ts-ignore
const { toggleDone, deleteTask, addTag, removeTag, saveTask } = inject('taskFunctions');
const closeModal = inject<() => void>('closeModal');

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
  closeModal?.();
}

function deleteTheTask() {
  deleteTask(props.task);
  closeModal?.();
}

function exitWithoutSaving() {
  // Copy the props again
  localTask.title = props.task.title;
  localTask.description = props.task.description;
  localTask.estimated = props.task.estimated;
  closeModal?.();
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
        <div class="flex items-baseline">
          <div @click="toggleDone(task)" class="pointer" v-auto-animate>
            <DoneIcon v-if="!task.done" />
            <MarkedDoneIcon v-else />
          </div>
          <DeleteIcon
            @click="deleteTheTask()"
            class="my-[0.1rem] mx-2 pointer"
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
