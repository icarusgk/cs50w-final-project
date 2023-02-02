<script setup lang="ts">
import { ref, watch } from 'vue';
import { useModalStore } from '@/stores/modal';
import { useChoreStore } from '@/stores/chore';
import { useAuthStore } from '@/stores/auth';
import { useAlertStore } from '@/stores/alerts';

import TheTaskModalBody from '@/components/TheTaskModalBody.vue';
import AppModal from '@/components/AppModal.vue';
import Tags from '@/components/buttons/Tags.vue';
import ChoreButton from '@/components/buttons/ChoreButton.vue';
import SaveButton from '@/components/buttons/SaveButton.vue';

import type { TagType, TaskType } from '@/types';

const open = ref(false);
const chore = useChoreStore();
const auth = useAuthStore();
const alert = useAlertStore();

watch(open, () => {
  useModalStore().toggle();
});

const initialTask = ref<TaskType>({
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

function removeTag(tag: TagType) {
  initialTask.value.tags = initialTask.value.tags.filter(
    (t: TagType) => t.name !== tag.name
  );
}

const handlePomos = (pomos: number) => (initialTask.value.estimated = pomos);
</script>

<template>
  <ChoreButton @click="auth.isAuthed ? (open = true) : (open = false)">
    <template #type> Add new task </template>
  </ChoreButton>
  <AppModal
    :open="open"
    @exit-modal="resetTask()"
    :is-task="true"
  >
    <template #tags>
      <Tags
        :task="initialTask"
        :new="true"
        @remove-tag="(tag) => removeTag(tag)"
      />
    </template>
    <!-- New task title input -->
    <template #title>
      <input
        type="text"
        name="title"
        id="new-task-input-title"
        placeholder="New task title"
        v-model="initialTask.title"
        @keyup.ctrl.enter="saveTask()"
      />
    </template>
    <!-- Rest of modal -->
    <TheTaskModalBody
      :task="initialTask"
      :isNew="true"
      @saveTask="saveTask()"
      @newPomoCount="handlePomos($event)"
      @descriptionInput="initialTask.description = $event"
    />
    <!-- Button -->
    <template #save-button>
      <SaveButton @click="saveTask()">Save!</SaveButton>
    </template>
  </AppModal>
</template>

<style scoped lang="scss">
#new-task-input-title {
  border: none;
  background: transparent;
  color: white;
  font-size: 2rem;
  font-weight: 700;
  width: 100%;

  &:focus,
  &:hover,
  &:active {
    outline: none;
  }
}
</style>
