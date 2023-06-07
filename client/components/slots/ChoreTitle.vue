<template>
  <div class="flex items-center py-4 w-full">
    <!-- Icon -->
    <div class="mr-4">
      <slot name="icon"></slot>
    </div>
    <!-- Title -->
    <div class="flex justify-between items-center w-105">
    <div class="font-semibold xs:text-2xl sm:text-3xl">
        <slot name="type"></slot>
      </div>
      <slot name="count"></slot>
    </div>
  </div>
</template>