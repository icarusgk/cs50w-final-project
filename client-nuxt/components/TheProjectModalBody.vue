<script setup lang="ts">
import type { IProject } from '@/types';
defineProps<{
  project: IProject;
  isNew?: boolean;
}>();
</script>

<template>
  <div class="mt-4">
    <!-- Tasks heading -->
    <span>Tasks</span>
    <!-- Add tasks button -->
    <div>
      <Subchores
        :is-project="true"
        :chores="project.tasks"
        :project="project"
        :isNew="isNew"
      />
    </div>
  </div>
</template>
