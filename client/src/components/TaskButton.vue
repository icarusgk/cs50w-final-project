<script setup lang="ts">
import AddIcon from './icons/AddIcon.vue';
</script>

<template>
  <div class="add-item-btn">
    <!-- Icon -->
    <AddIcon class="add-icon"/>
    <slot name="type"></slot>
  </div>
</template>

<style lang="scss">
.add-item-btn {
  background-color: var(--white);
  color: var(--black);
  display: flex;
  align-items: center;
  border-radius: 10px;
  margin-right: 1rem;
  padding: 0.1rem 1.25rem;
  &:hover {
    cursor: pointer;
  }
}

.add-icon {
  width: 2rem;
  margin-right: 0.4rem;
}
</style>