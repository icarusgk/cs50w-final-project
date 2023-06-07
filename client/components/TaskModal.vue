<script setup lang="ts">
defineProps<{
  open: boolean
}>();
defineEmits<{
  (e: 'exit:modal'): any
}>();
</script>


<template>
  <AppModal :open="open" @exit:modal="$emit('exit:modal')">
    <slot></slot>
  </AppModal>
</template>


<style scoped>

</style>
