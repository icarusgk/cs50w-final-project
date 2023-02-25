<template>
  <div class="add-item-btn bg-white text-black flex items-center pointer rounded-lg mr-4 py-[0.1rem] px-2 w-full text-sm font-semibold md:font-normal xl:text-base xl:w-auto">
    <!-- Icon -->
    <AddIcon class="w-8 mr-2" />
    <slot name="type"></slot>
  </div>
</template>
