<script setup lang="ts">
import { useModalStore } from '@/stores/modal';
import { ref, watch } from 'vue';
import TaskButton from '../TaskButton.vue';
import NewProjectModal from '../../modals/new-modals/NewProjectModal.vue';
import Modal from '@/components/modals/Modal.vue';

const project = ref({
  title: '',
  tasks: []
})

const open = ref(false)

watch(() => open.value, () => {
  useModalStore().toggle()
})

function saveProject() {
  // TODO: Save with axios
  console.log(project.value)
  open.value = false
}
</script>

<template>
  <TaskButton @click="open = true">
    <template #type>
      Add new project
    </template>
  </TaskButton>

  <Modal :is-project="true" :is-button="true" :open="open" @exit-modal="open = false">
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
    <NewProjectModal :project="project" />
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

  &:hover {
    cursor: pointer;
  }
}
</style>