<script setup lang="ts">
import { useModalStore } from '@/stores/modal';
import { useChoreStore } from '@/stores/chore';
import { ref, watch } from 'vue';
import TaskButton from '../TaskButton.vue';
import TaskModal from '../../modals/TaskModal.vue';
import Tags from '../Tags.vue';
import Modal from '@/components/modals/Modal.vue';

import axios from 'axios'
import type Task from '@/types/TaskType';

const open = ref(false)
const taskStore = useChoreStore()

const initialTask = ref<Task>({
  id: 8,
  tags: [],
  title: '',
  description: '',
  estimated: 0,
  subtasks: []
})

watch(() => open.value, () => {
  useModalStore().toggle()
})

async function saveTask() {
  if (initialTask.value.title) {
    const response = await axios.post(`http://127.0.0.1:3001/tasks/`, initialTask.value)
    if (response.status === 200) { console.log("Saved!") }
  }
  taskStore.addTask(initialTask.value)
  open.value = false;
}
</script>

<template>
  <TaskButton @click="open = true">
    <template #type>
      Add new task
    </template>
  </TaskButton>
  <Modal :is-button="true" :open="open" @exit-modal="open = false">
    <template #tags>
      <Tags :tags="initialTask.tags" />
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

  &:focus {
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

  &:hover {
    cursor: pointer;
  }
}
</style>