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
  <div class="w-full p-4 bg-[#3d3d3d] rounded-lg pointer md:w-auto" @click="open = true">
    <h1>{{ project.name }}</h1>
  </div>
  <TheProjectModal :project="project" :open="open" @exit:modal="open = false" />
</template>
