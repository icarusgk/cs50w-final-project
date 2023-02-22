<script setup lang="ts">
import type { IProject } from '@/types';

const props = defineProps<{
  project: IProject;
  open: boolean;
}>();

const title = ref(props.project.name);
const emit = defineEmits(['exit']);
const chore = useChoreStore();

function deleteProject() {
  if (window.confirm('Are you sure?')) {
    chore.deleteProject(props.project.id as number);
    emit('exit');

    if (chore.projectPagination.page === chore.totalProjectPages && chore.projects.length === 1) {
      chore.decreaseProjectPagination();
    }
  }
}

function saveAndExit() {
  chore.saveProject(props.project, title.value);
  props.project.name = title.value;
  emit('exit');
}

function exitModal() {
  if (title.value !== props.project.name) {
    props.project.name = title.value;
    chore.saveProject(props.project, title.value);
  }
  emit('exit');
}
</script>

<template>
  <div class="project-container">
    <!-- Modal -->
    <AppModal :open="open" @exit-modal="exitModal()">
      <!-- Title -->
      <template #title>
        <input
          type="text"
          name="title"
          id="task-input-title"
          maxlength="30"
          v-model="title"
          @keyup.ctrl.enter="saveAndExit()"
        />
      </template>
      <template #delete-icon>
        <DeleteIcon @click="deleteProject()" class="delete-icon" />
      </template>
      <!-- Modal Info -->
      <TheProjectModalBody :project="project" @close-modal="$emit('exit')" />
    </AppModal>
  </div>
</template>

<style scoped lang="scss">
#task-input-title {
  border: none;
  background: transparent;
  color: white;
  font-size: 2rem;
  font-weight: 700;
  width: 100%;

  &:focus {
    outline: none;
  }
}

.delete-icon {
  margin-right: 10px;
  &:hover,
  &:focus,
  &:active {
    cursor: pointer;
  }
}

@media (max-width: 480px) {
  #task-input-title {
    width: 95%;
  }
}
</style>
