<script setup lang="ts">
import { ref, watch } from 'vue';
import { useModalStore } from '@/stores/modal';
import { useChoreStore } from '@/stores/chore';
import { useAuthStore } from '@/stores/auth';

import TaskModalInfo from '@/components/modals/TaskModalInfo.vue';
import Modal from '@/components/modals/Modal.vue';
import Tags from '@/components/buttons/Tags.vue';
import ChoreButton from '@/components/buttons/ChoreButton.vue';
import SaveButton from '@/components/SaveButton.vue';

import type { TagType, TaskType } from '@/types';

const open = ref(false);
const taskStore = useChoreStore();
const auth = useAuthStore();

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
    taskStore.addTask(initialTask.value);
  }
  resetTask();
}

function removeTag(tag: TagType) {
  initialTask.value.tags = initialTask.value.tags.filter(
    (t: TagType) => t.id !== tag.id
  );
}
</script>

<template>
  <ChoreButton @click="auth.isAuthenticated ? (open = true) : (open = false)">
    <template #type> Add new task </template>
  </ChoreButton>
  <Modal
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
    <TaskModalInfo
      :task="initialTask"
      :isNew="true"
      @saveTask="saveTask()"
      @descriptionInput="initialTask.description = $event"
    />
    <!-- Button -->
    <template #save-button>
      <SaveButton @click="saveTask()">Save!</SaveButton>
    </template>
  </Modal>
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
