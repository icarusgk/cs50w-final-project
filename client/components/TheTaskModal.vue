<script setup lang="ts">
import type { ITag, ITask } from '@/types';

const emit = defineEmits<{
  (e: 'exit:modal'): any
  (e: 'delete:task', task: ITask): any
  (e: 'newTask', task: ITask): any
  (e: 'remove:tag', task: ITask, tag?: ITag): any
}>();

const chore = useChoreStore();
const modal = useModalStore();

// This way it prevents from mutating the original object
// inside props.task by reference
const width = ref(window.innerWidth);
let localTask = reactive<ITask>({ ...modal.content });

const isFormPristine = computed(() => {
  return localTask.title === modal.content.title
    && localTask.description === modal.content.description
    && localTask.estimated === modal.content.estimated
});

function saveTheTask() {
  chore.saveTask(modal.content, { ...localTask });
  modal.close();
  emit('newTask', { ...localTask });
}

function deleteTheTask() {
  chore.deleteTask(modal.content);
  modal.close();
}

function exitWithoutSaving() {
  // Copy the props again
  localTask.title = modal.content.title;
  localTask.description = modal.content.description;
  localTask.estimated = modal.content.estimated;
  modal.close()
}

function exitModal() {
  // if (!isFormPristine.value) {
  //   if (!window.confirm('Are you sure? You have unsaved changes.')) return;
  // }
  exitWithoutSaving();
}

function addTag(task: ITask, tag: ITag) {
  task.tags.push(tag);
}

function removeTag(task: ITask, tag?: ITag) {
  task.tags = task.tags.filter((t: ITag) => t.id !== tag?.id);
  emit('remove:tag', task, tag);
  modal.close();
}

function resize() {
  width.value = window.innerWidth
}

onMounted(() => {
  window.addEventListener('resize', resize);
});

onUnmounted(() => {
  window.removeEventListener('resize', resize);
});
</script>

<template>
  <div class="task-container">
    <!-- Modal -->
    <AppModal :open="modal.isOpened" @exit:modal="exitModal" :is-task="true">
      <!-- Tags -->
      <template #tags>
        <Tags
          :id="modal.content.id"
          :task="modal.content"
          @add:tag="(tag: ITag) => addTag(modal.content, tag)"
          @remove:tag="(tag: ITag) => removeTag(modal.content, tag)"
          @close:modal="$emit('exit:modal')"
        />
        <div class="flex items-baseline items-center">
          <div @click="chore.toggleDone(modal.content)" class="pointer mr-1" v-auto-animate>
            <div class="i-fluent:checkmark-circle-32-regular scale-130" v-if="!modal.content.done" />
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
          class="border-none bg-transparent text-white text-4xl font-bold w-full h-full focus:outline-none"
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
        <div class="text-center" v-if="width < 480">
          <span class="font-semibold text-xl">
            Pomos done: {{ modal.content.gone_through }}
          </span>
        </div>
        <SaveButton :enabled="!isFormPristine" @click="saveTheTask()" />
      </template>
    </AppModal>
  </div>
</template>
