<script setup lang="ts">
import type { ITag, ITask } from '@/types';

const open = ref(false);
const chore = useChoreStore();
const auth = useAuthStore();
const alert = useAlertStore();

watch(open, () => {
  useModalStore().toggle();
});

const initialTask = ref<ITask>({
  tags: [],
  title: '',
  description: '',
  estimated: 1,
  subtasks: [],
});

function resetTask() {
  initialTask.value = {
    tags: [],
    title: '',
    description: '',
    estimated: 1,
    subtasks: [],
  };
  open.value = false;
}

function saveTask() {
  if (initialTask.value.title) {
    chore.addTask(initialTask.value).then(() => chore.fetchTags());
    resetTask();
  } else {
    alert.error('Your task must have a title');
  }
}

function removeTag(tag: ITag) {
  initialTask.value.tags = initialTask.value.tags.filter(
    (t: ITag) => t.name !== tag.name
  );
}

const handlePomos = (pomos: number) => (initialTask.value.estimated = pomos);
</script>

<template>
  <ChoreButton @click="auth.isAuthed ? (open = true) : (open = false)">
    <template #type> Add new task </template>
  </ChoreButton>
  <AppModal :open="open" @exit:modal="resetTask()" :is-task="true">
    <template #tags>
      <Tags
        :task="initialTask"
        :new="true"
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
        v-model="initialTask.title"
        @keyup.ctrl.enter="saveTask()"
      />
    </template>
    <!-- Rest of modal -->
    <TheTaskModalBody
      :task="initialTask"
      :isNew="true"
      @save:task="saveTask()"
      @change:pomoCount="handlePomos($event)"
      @input:description="initialTask.description = $event"
    />
  <!-- Button -->
    <template #save-button>
      <SaveButton @click="saveTask()">Save!</SaveButton>
    </template>
  </AppModal>
</template>
