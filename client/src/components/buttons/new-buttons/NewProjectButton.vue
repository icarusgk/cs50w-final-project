<script setup lang="ts">
import { ref } from 'vue';
import TaskButton from '../TaskButton.vue';
import NewProjectModal from '../../modals/new-modals/NewProjectModal.vue';

const project = ref({
  title: '',
  tasks: []
})

function saveProject() {
  console.log(project.value)
}
</script>

<template>
  <TaskButton :is-project="true">
    <template #type>
      Add new project
    </template>
    <template #title>
      <input 
        type="text" 
        name="title" 
        id="new-task-input-title" 
        placeholder="New project name" 
        v-model="project.title" 
      />
    </template>
    <!-- Rest of modal -->
    <NewProjectModal :tasks="project.tasks" />
    <template #save-button>
      <button
        @click="saveProject()" 
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