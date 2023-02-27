<script setup lang="ts">
import type { IProject } from '@/types';

const newProject = ref<IProject>({
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

  <AppModal :open="open" @exit:modal="resetProject()">
    <template #title>
      <input
        type="text"
        name="title"
        class="border-none outline-none bg-transparent text-white text-4xl font-bold w-[90%] placeholder-[rgb(190,190,190)]"
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

