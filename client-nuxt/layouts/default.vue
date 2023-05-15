<script setup lang="ts">
const modal = useModalStore();
</script>

<template>
  <div>
    <TheSidebar />
    <div class="flex ml-0 mb-[140px] lg:ml-[130px] lg:mb-0 relative">
      <div :class="[{ '<sm:p-4 filter blur-md pointer-events-none duration-150 ease-out': modal.isOpened },
          'w-full flex flex-col',]"
      >
        <TheUpperMenu class="pt-6 py-12 pb-0" />
        <slot />
      </div>
    </div>
  </div>
</template>


<style scoped>

</style>
