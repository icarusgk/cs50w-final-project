<script setup lang="ts">
import { ref, watch } from 'vue';
import { useModalStore } from '@/stores/modal';
import type { Project } from '@/types';

import ProjectModal from '@/components/ProjectModal.vue'


defineProps<{
  project: Project
}>()

const open = ref(false)

watch(() => open.value, () => {
  useModalStore().toggle()
})

</script>

<template>
<div class="single-project" @click="open = true">
  <h1>{{ project.title }}</h1>
</div>
<ProjectModal :project="project" :open="open" @exit="open = false" />
</template>

<style scoped lang="scss">
.single-project {
  padding: 1rem;
  background-color: #3D3D3D;
  margin: 0 1rem 1rem 0;
  border-radius: 8px;

  &:hover, &:focus {
    cursor: pointer;
  }
}
</style>