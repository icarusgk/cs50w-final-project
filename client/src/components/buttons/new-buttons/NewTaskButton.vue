<script setup lang="ts">
import { ref, watch } from 'vue';
import { useModalStore } from '@/stores/modal';
import { useChoreStore } from '@/stores/chore';

import TaskModal from '@/components/modals/TaskModal.vue';
import Modal from '@/components/modals/Modal.vue';
import Tags from '@/components/buttons/Tags.vue';
import TaskButton from '@/components/buttons/TaskButton.vue';


import type Task from '@/types/TaskType';

const open = ref(false)
const taskStore = useChoreStore()

const initialTask = ref<Task>({
  id: 12,
  tags: [],
  title: '',
  description: '',
  estimated: 1,
  subtasks: []
})

watch(() => open.value, () => {
  useModalStore().toggle()
})

function resetTask() {
  initialTask.value = {
    id: 13,
    tags: [],
    title: '',
    description: '',
    estimated: 1,
    subtasks: []
  }
  open.value = false
}

function saveTask() {
  if (initialTask.value.title) {
    taskStore.addTask(initialTask.value)
  }
  resetTask()
}
</script>

<template>
  <TaskButton @click="open = true">
    <template #type>
      Add new task
    </template>
  </TaskButton>
  <Modal :is-button="true" :open="open" @exit-modal="resetTask()">
    <template #tags>
      <Tags :taskTags="initialTask.tags" :allTags="taskStore.tags" />
    </template>
    <!-- New task title input -->
    <template #title>
      <input 
        type="text" 
        name="title" 
        id="new-task-input-title" 
        placeholder="New task title" 
        v-model="initialTask.title" 
      />
    </template>
    <!-- Rest of modal -->
    <TaskModal :task="initialTask" :isNew="true" />
    <!-- Button -->
    <template #save-button>
      <button
        @click="saveTask()"
        class="close-modal-button"
      >Save!
      </button>
    </template>
  </Modal>
</template>

<style scoped lang="scss">
#new-task-input-title {
  border: none;
  background: transparent;
  color: white;
  font-size: 2rem;
  font-weight: 900;
  font-family: sans-serif;
  width: 100%;

  &:focus, &:hover {
    outline: none;
  }
}

.close-modal-button {
  background-color: var(--vivid-red);
  color: var(--white);

  font: {
    weight: 900;
    family: sans-serif;
  }

  width: 100%;
  border: none;
  border-radius: 10px;
  margin-top: 1rem;
  padding: 0.8rem 0.8rem;

  &:hover, &:focus {
    cursor: pointer;
  }
}
</style>