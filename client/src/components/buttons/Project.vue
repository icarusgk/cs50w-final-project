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
  <div class="flex items-center my-1 mb-2">
    <!-- Checkbox -->
    <div class="h-5 w-5 rounded-xl bg-white mr-4"></div>
    <!-- Name -->
    <div class="flex items-center justify-between py-1.5 px-4 bg-light-blue w-full rounded-lg">
      <div class="title-container">
        <span>{{ project.name }}</span>
      </div>
      <div @click="open = true" class="i-fluent:info-24-regular scale-135 mt-0.5 pointer" />
    </div>

    <TheProjectModal
      :project="project"
      :open="open"
      @exit:modal="open = false"
      @update:name="(newName: string) => project.name = newName"
    />
  </div>
</template>
