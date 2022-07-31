<script setup lang="ts">
import { useModalStore } from '@/stores/modal';
import { useChoreStore } from '@/stores/chore';
import { ref, watch } from 'vue';
import TaskButton from '../TaskButton.vue';
import ProjectModal from '../../modals/ProjectModal.vue';
import Modal from '@/components/modals/Modal.vue';
import type Project from '@/types/ProjectType';

const newProject = ref<Project>({
  id: 11,
  title: '',
  tasks: [],
})

const open = ref(false)

watch(() => open.value, () => {
  useModalStore().toggle()
})

function resetProject() {
  newProject.value = {
    id: 12,
    title: '',
    tasks: []
  }
  open.value = false
}

function saveProject() {
  useChoreStore().addProject(newProject.value)
  resetProject()
}
</script>

<template>
  <TaskButton @click="open = true">
    <template #type>
      Add new project
    </template>
  </TaskButton>

  <Modal :is-project="true" :is-button="true" :open="open" @exit-modal="resetProject()">
    <template #title>
      <input 
        type="text" 
        name="title" 
        id="new-task-input-title" 
        placeholder="New project name"
        v-model="newProject.title" 
      />
    </template>
    
    <!-- Rest of modal -->
    <ProjectModal :project="newProject" :isNew="true" />
    <template #save-button>
      <button
        @click="saveProject()" 
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

  &:hover, &:focus {
    cursor: pointer;
  }
}
</style>