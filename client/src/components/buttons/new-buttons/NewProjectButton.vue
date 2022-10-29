<script setup lang="ts">
import { ref, watch } from 'vue';
import { useModalStore } from '@/stores/modal';
import { useChoreStore } from '@/stores/chore';
import { useAuthStore } from '@/stores/auth';
import type { ProjectType } from '@/types';

import ProjectModalInfo from '@/components/modals/ProjectModalInfo.vue';
import Modal from '@/components/modals/Modal.vue';
import ChoreButton from '@/components/buttons/ChoreButton.vue';
import SaveButton from '@/components/SaveButton.vue';

const newProject = ref<ProjectType>({
  name: '',
  tasks: [],
});

const open = ref(false);
const auth = useAuthStore();

watch(open, () => {
  useModalStore().toggle();
});

function resetProject() {
  newProject.value = {
    name: '',
    tasks: [],
  };
  open.value = false;
}

function saveProject() {
  useChoreStore().addProject(newProject.value);
  resetProject();
}
</script>

<template>
  <ChoreButton @click="auth.isAuthenticated ? (open = true) : (open = false)">
    <template #type> Add new project </template>
  </ChoreButton>

  <Modal :open="open" @exit-modal="resetProject()">
    <template #title>
      <input
        type="text"
        name="title"
        id="new-project-input-title"
        placeholder="New project"
        @keyup.ctrl.enter="saveProject()"
        v-model="newProject.name"
      />
    </template>

    <!-- Rest of modal -->
    <ProjectModalInfo :project="newProject" :isNew="true" />
    <template #save-button>
      <SaveButton @click="saveProject()" />
    </template>
  </Modal>
</template>

<style scoped lang="scss">
#new-project-input-title {
  border: none;
  background: transparent;
  color: white;
  font-size: 2rem;
  font-weight: 700;
  width: 90%;

  &:focus,
  &:hover,
  &:active {
    outline: none;
  }
}
</style>
