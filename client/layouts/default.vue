<script setup lang="ts">
const modal = useModalStore();
</script>

<template>
  <div>
    <TheTaskModal :key="modal.content?.id" />
    <TheSidebar />
    <div class="flex ml-0 mb-[140px] lg:ml-[130px] lg:mb-0 relative lg:h-screen">
      <div class="w-full flex flex-col" :class="{ '<sm:p-4 filter blur-md pointer-events-none duration-150 ease-out': modal.isOpened || modal.isOpenedNew }">
        <TheUpperMenu class="pt-6 py-12 pb-0" />
        <slot />
      </div>
      <TheAlerts />
    </div>
  </div>
</template>

