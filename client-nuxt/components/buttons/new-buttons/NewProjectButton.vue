<script setup lang="ts">
import type { IProject } from '@/types';

const open = ref(false);
const auth = useAuthStore();
const alert = useAlertStore();

const newProject = reactive<IProject>({
  name: '',
  tasks: []
});

const hasTitle = computed(() => newProject.name !== '');

watch(open, () => {
  useModalStore().toggle();
});

function resetProject() {
  Object.assign(newProject, {
    name: '',
    tasks: []
  })
  open.value = false;
}

function saveProject() {
  if (newProject.name) {
    useChoreStore().addProject(newProject);
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
        v-focus
      />
    </template>

    <!-- Rest of modal -->
    <TheProjectModalBody :project="newProject" :isNew="true" />
    <template #save-button>
      <SaveButton :enabled="hasTitle" @click="saveProject()" />
    </template>
  </AppModal>
</template>

