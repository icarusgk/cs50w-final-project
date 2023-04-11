<script setup lang="ts">
import type { IProject } from '@/types';

const props = defineProps<{
  project: IProject;
  open: boolean;
}>();

const emit = defineEmits<{
  (e: 'exit:modal'): void;
  (e: 'update:name', name: string): void;
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
  emit('update:name', title.value);
  emit('exit:modal');
}

function exitModal() {
  if (title.value !== props.project.name) {
    emit('update:name', title.value);
    chore.saveProject(props.project, title.value);
  }
  emit('exit:modal');
}
</script>

<template>
  <div>
    <!-- Modal -->
    <AppModal :open="open" @exit:modal="exitModal()">
      <!-- Title -->
      <template #title>
        <input
          type="text"
          name="title"
          class="w-[95%] border-none bg-transparent text-white font-bold text-[2rem] lg:w-full outline-none"
          maxlength="30"
          v-model="title"
          @keyup.ctrl.enter="saveAndExit()"
          v-focus
        />
      </template>
      <template #delete-icon>
        <div @click="deleteProject()" class="i-fluent:delete-20-filled scale-150 pointer mr-5" />
      </template>
      <!-- Modal Info -->
      <TheProjectModalBody :project="project" />
    </AppModal>
  </div>
</template>
