<script setup lang="ts">
import type { IProject } from '@/types';

defineProps<{
  project: IProject;
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
  <TheProjectModal :project="project" :open="open" @exit:modal="open = false" />
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
