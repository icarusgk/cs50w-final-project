<script setup lang="ts">
const modal = useModalStore();
</script>

<template>
  <AppModal :open="false" @exit:modal="modal.close()">
    
  </AppModal>
</template>

<style scoped>

</style>
