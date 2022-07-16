<script setup lang="ts">
import TaskButton from '../TaskButton.vue';
import NewProjectModal from '../../modals/new-modals/NewProjectModal.vue';
</script>

<template>
  <TaskButton>
    <template #type>
      Add new project
    </template>
    <template #title>
      <h1>New Project</h1>
    </template>
    <template #modal-content>
      <NewProjectModal />
    </template>
  </TaskButton>
</template>