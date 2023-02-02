<script setup lang="ts">
import type { ProjectType } from '@/types';

import TheProjectModalBody from '@/components/TheProjectModalBody.vue';
import AppModal from '@/components/AppModal.vue';
import ChoreButton from '@/components/buttons/ChoreButton.vue';
import SaveButton from '@/components/buttons/SaveButton.vue';

const newProject = ref<ProjectType>({
  name: '',
  tasks: [],
});

const open = ref(false);
const auth = useAuthStore();
const alert = useAlertStore();

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
  if (newProject.value.name) {
    useChoreStore().addProject(newProject.value);
    resetProject();
  } else {
    alert.error('Your project must have a name');
  }
}
</script>

<template>
  <ChoreButton @click="auth.isAuthed ? (open = true) : (open = false)">
    <template #type> Add new project </template>
  </ChoreButton>

  <AppModal :open="open" @exit-modal="resetProject()">
    <template #title>
      <input
        type="text"
        name="title"
        id="new-project-input-title"
        placeholder="New project"
        maxlength="30"
        @keyup.ctrl.enter="saveProject()"
        v-model="newProject.name"
      />
    </template>

    <!-- Rest of modal -->
    <TheProjectModalBody :project="newProject" :isNew="true" />
    <template #save-button>
      <SaveButton @click="saveProject()" />
    </template>
  </AppModal>
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
