<script setup lang="ts">
import { ref } from 'vue';
import TaskButton from '../TaskButton.vue';
import NewTaskModal from '../../modals/new-modals/NewTaskModal.vue';
import Tags from '../Tags.vue';

const initialTask = ref<{
  tags: string[]
  title: string,
  description: string
  estimated: number,
  subtasks: {
    title: string,
    description: string,
    estimated: number
  }[]
}>({
  tags: [],
  title: '',
  description: '',
  estimated: 0,
  subtasks: []
})

function saveTask() {
  console.log(initialTask)
}
</script>

<template>
  <TaskButton>
    <template #type>
      Add new task
    </template>
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
    <NewTaskModal :task="initialTask" />
    <!-- Button -->
    <template #save-button>
      <button
        @click="saveTask()" 
        class="close-modal-button"
      >Save!
      </button>
    </template>
  </TaskButton>
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