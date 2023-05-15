<script setup lang="ts">
defineProps<{
  enabled?: boolean;
}>();
</script>

<template>
  <button
    :class="[
      { '!opacity-100': enabled },
      'opacity-40 w-full timer-btn timer-btn-red font-bold border-none mt-4 transition duration-150 ease-in-out',
    ]"
    :disabled="!enabled"
  >
    Save!
  </button>
</template>
