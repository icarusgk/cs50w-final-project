<script setup lang="ts">
import type { ITag, ITask } from '@/types';

const open = ref(false);
const chore = useChoreStore();
const auth = useAuthStore();
const alert = useAlertStore();

watch(open, () => {
  useModalStore().toggle();
});

const taskModel: ITask = {
  tags: [],
  title: '',
  description: '',
  estimated: 1,
  subtasks: [],
}

const initialTask = reactive<ITask>({...taskModel});

const hasTitle = computed(() => initialTask.title !== '')

function resetTask() {
  Object.assign(initialTask, taskModel);
  initialTask.tags = [];
  initialTask.subtasks = [];
  open.value = false;
}

function saveTask() {
  if (initialTask.title) {
    chore.addTask(initialTask).then(() => chore.fetchTags());
    resetTask();
  } else {
    alert.error('Your task must have a title');
  }
}

function addTag(tag: ITag) {
  initialTask.tags.push(tag);
}

function removeTag(tag: ITag) {
  initialTask.tags = initialTask.tags.filter(
    (t: ITag) => t.name !== tag.name
  );
}
</script>

<template>
  <ChoreButton @click="open = auth.isAuthed ? true : false">
    <template #type> Add new task </template>
  </ChoreButton>
  <AppModal :open="open" @exit:modal="resetTask()" :is-task="true">
    <template #tags>
      <Tags
        :task="initialTask"
        :new="true"
        @add:tag="(tag: ITag) => addTag(tag)"
        @remove:tag="(tag: ITag) => removeTag(tag)"
      />
    </template>
    <!-- New task title input -->
    <template #title>
      <input
        type="text"
        name="title"
        class="border-none bg-transparent text-white font-bold text-[2rem] w-full outline-none placeholder-[rgb(190,190,190)]"
        placeholder="New task title"
        @keyup.ctrl.enter="saveTask()"
        v-model="initialTask.title"
        v-focus
      />
    </template>
    <!-- Rest of modal -->
    <TheTaskModalBody
      :task="initialTask"
      :isNew="true"
      @save:task="saveTask()"
      @change:pomoCount="(pomos: number) => initialTask.estimated = pomos"
      @input:description="(desc: string) => initialTask.description = desc"
    />
  <!-- Button -->
    <template #save-button>
      <SaveButton :enabled="hasTitle" @click="saveTask()">Save!</SaveButton>
    </template>
  </AppModal>
</template>
