<script setup lang="ts">
import type { IProject } from '@/types';

const props = defineProps<{
  project: IProject;
  open: boolean;
}>();

const emit = defineEmits<{
  (e: 'exit:modal'): void;
  (e: 'update:title', title: string): void; // TODO: To be used in the future
}>();

const chore = useChoreStore();

const { name: title } = toRefs(props.project);

function deleteProject() {
  const shouldDelete = window.confirm('Are you sure?');

  if (!shouldDelete) {
    return;
  }

  chore.deleteProject(props.project.id as number);
  emit('exit:modal');

  const isLastProjectOnPage =
    chore.projectPagination.page === chore.totalProjectPages &&
    chore.projects.length === 1;

  if (isLastProjectOnPage) {
    chore.decreaseProjectPagination();
  }
}

function saveAndExit() {
  chore.saveProject(props.project, title.value);
  props.project.name = title.value;
  emit('exit:modal');
}

function exitModal() {
  if (title.value !== props.project.name) {
    props.project.name = title.value;
    chore.saveProject(props.project, title.value);
  }
  emit('exit:modal');
}
</script>

<template>
  <div class="project-container">
    <!-- Modal -->
    <AppModal :open="open" @exit:modal="exitModal()">
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
      <TheProjectModalBody :project="project" />
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
