<script setup lang="ts">
import { ref, watch } from 'vue';
import { useModalStore } from '@/stores/modal';
import type { ProjectType } from '@/types';

import ProjectModal from './ProjectModal.vue';
import TaskInfoIcon from '@/components/icons/TaskInfoIcon.vue';

defineProps<{
  project: ProjectType;
}>();

const open = ref(false);

watch(
  () => open.value,
  () => {
    useModalStore().toggle();
  }
);
</script>

<template>
  <div class="task-container">
    <!-- Checkbox -->
    <div class="task-checkbox"></div>
    <!-- Name -->
    <div class="task-title-container">
      <div class="title-container">
        <span>{{ project.name }}</span>
      </div>
      <div @click="open = true" class="task-info-icon">
        <TaskInfoIcon />
      </div>
    </div>

    <ProjectModal :project="project" :open="open" @exit="open = false" />
  </div>
</template>

<style scoped lang="scss">
.task-container {
  display: flex;
  align-items: center;
  margin: 0 0.2rem 0.5rem 0.2rem;

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
      &:hover,
      &:focus,
      &:active {
        cursor: pointer;
      }
    }
  }
}
</style>
