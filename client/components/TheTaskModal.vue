<script setup lang="ts">
import type { ITag, ITask } from '@/types';

const chore = useChoreStore();

const props = defineProps<{
  task: ITask;
  open: boolean;
}>();

const emit = defineEmits<{
  (e: 'exit:modal'): any
  (e: 'newTask', task: ITask): any
}>();

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
  chore.saveTask(props.task, { ...localTask });
  emit('exit:modal');
  emit('newTask', { ...localTask });
}

function deleteTheTask() {
  chore.deleteTask(props.task);
  emit('exit:modal');
}

function exitWithoutSaving() {
  // Copy the props again
  localTask.title = props.task.title;
  localTask.description = props.task.description;
  localTask.estimated = props.task.estimated;
  emit('exit:modal');
}

function addTag(task: ITask, tag: ITag) {
  task.tags.push(tag);
}

function removeTag(task: ITask, tagId?: number) {
  task.tags = task.tags.filter((tag: ITag) => tag.id !== tagId);
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
          <div @click="chore.toggleDone(task)" class="pointer mr-1" v-auto-animate>
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
            Pomos done: {{ task.gone_through }}
          </span>
        </div>
        <SaveButton :enabled="!isFormPristine" @click="saveTheTask()" />
      </template>
    </AppModal>
  </div>
</template>
