<script setup lang="ts">
import { ref, watch } from 'vue';
import { useModalStore } from '@/stores/modal';
import type { ProjectType } from '@/types';

import ProjectModal from '@/components/ProjectModal.vue';

defineProps<{
  project: ProjectType;
}>();

const open = ref(false);

watch(open, () => {
  useModalStore().toggle();
});
</script>

<template>
  <div class="single-project" @click="open = true">
    <h1>{{ project.name }}</h1>
  </div>
  <ProjectModal :project="project" :open="open" @exit="open = false" />
</template>

<style scoped lang="scss">
.single-project {
  padding: 1rem;
  background-color: #3d3d3d;
  border-radius: 8px;

  &:hover,
  &:focus,
  &:active {
    cursor: pointer;
  }
}

@media (max-width: 480px) {
  .single-project {
    width: 100%;
  }
}
</style>
