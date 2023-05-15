<script setup lang="ts">
defineProps<{
  isTask?: Boolean;
  isTag?: Boolean;
  isAdd?: Boolean;
}>();
</script>

<template>
  <div class="flex items-center pointer" :class="{ 
    'py-[0.01rem] px-[0.7rem] rounded-lg bg-lighter-gray text-white h-8': isTask, 
    '<sm:text-xs py-[0.15rem] px-[0.3rem] rounded-[5px] m-[0.2rem] font-medium text-[0.7rem] bg-white text-black': isTag, 
    'py-[0.1rem] px-[0.3rem] rounded-[5px] font-medium text-[0.7rem] bg-[#444] text-white': isAdd 
  }">
    <!-- Title -->
    <div class="title">
      <slot name="title"></slot>
    </div>
    <!-- Icon -->
    <div class="mt-[2px]">
      <slot name="icon"></slot>
    </div>
  </div>
</template>
