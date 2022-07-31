<script setup lang="ts">
import { ref, watch } from 'vue';
import { useChoreStore } from '@/stores/chore';
import { useModalStore } from '@/stores/modal';
import TaskInfoIcon from './icons/TaskInfoIcon.vue';
import Modal from './modals/Modal.vue';
import ProjectModal from './modals/ProjectModal.vue';
import DeleteIcon from './icons/DeleteIcon.vue';

const props = defineProps(['project'])

const open = ref(false)

// When open.value changes, toggle
watch(() => open.value, () => {
  useModalStore().toggle()
})

function deleteProject() {
  useChoreStore().deleteProject(props.project.id)
  open.value = false
}
</script>

<template>
  <div @click="open = true" class="task-container">
    <!-- Checkbox -->
    <div class="task-checkbox"></div>
    <!-- Name -->
    <div class="task-title-container">
      <div class="title-container">
        <p>{{ project.title }}</p>
      </div>
      <div class="task-info-icon">
        <TaskInfoIcon />
      </div>
    </div>
    <!-- Modal -->
    <Modal :is-project="true" :open="open" @exit-modal="open = false">
      <!-- Title -->
      <template #title>
        <input type="text" name="title" id="task-input-title" v-model="props.project.title" />
      </template>
      <template #delete-icon>
        <DeleteIcon @click="deleteProject()" class="delete-icon" />
      </template>
      <!-- Modal Info -->
      <ProjectModal :project="project" @close-modal="open = false" />
    </Modal>
  </div>
</template>

<style scoped lang="scss">
.task-container {
  display: flex;
  align-items: center;
  margin: 0 0.2rem 0.5rem 0.2rem;

  &:hover, &:focus {
    cursor: pointer;
  } 

  .task-checkbox {
    height: 20px;
    width: 20px;
    background-color: var(--white);
    border-radius: 10px;
    margin-right: 1rem;
  }
  
  .task-title-container {
    padding: 0.2rem 1rem;
    border-radius: 8px;
    background-color: var(--light-blue);
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;

    
    .task-info-icon {
      margin-top: 0.2rem;
      &:hover, &:focus {
        cursor: pointer;
      }
    }
  }
}

#task-input-title {
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

.delete-icon {
  &:hover, &:focus {
    cursor: pointer;
  }
}
</style>