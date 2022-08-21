<script setup lang="ts">
import { useChoreStore } from '@/stores/chore';
import type { Project } from '@/types';

import Modal from '@/components/modals/Modal.vue';
import ProjectModalInfo from '@/components/modals/ProjectModalInfo.vue';
import DeleteIcon from '@/components/icons/DeleteIcon.vue';

const props = defineProps<{
  project: Project
  open: boolean
}>()

const emit = defineEmits(['exit'])

// Works
function deleteProject() {
  useChoreStore().deleteProject(props.project.id as number)
  emit('exit')
}

</script>

<template>
  <div class="project-container">
    <!-- Modal -->
    <Modal :is-project="true" :open="open" @exit-modal="$emit('exit')">
      <!-- Title -->
      <template #title>
        <input type="text" name="title" id="task-input-title" v-model="props.project.name" />
      </template>
      <template #delete-icon>
        <DeleteIcon @click="deleteProject()" class="delete-icon" />
      </template>
      <!-- Modal Info -->
      <ProjectModalInfo :project="project" @close-modal="$emit('exit')" />
    </Modal>
  </div>
</template>

<style scoped lang="scss">
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