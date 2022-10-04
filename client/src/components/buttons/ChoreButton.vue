<script setup lang="ts">
import AddIcon from '@/components/icons/AddIcon.vue';
</script>

<template>
  <div class="add-item-btn">
    <!-- Icon -->
    <AddIcon class="add-icon" />
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
  padding: 0.1rem 0.5rem;
  // Add depth to the button
  box-shadow: 3px 4px rgba(208, 208, 208);
  transition: box-shadow 0.1s cubic-bezier(0.075, 0.82, 0.165, 1);

  &:hover,
  &:focus,
  &:active {
    cursor: pointer;
  }

  &:active {
    box-shadow: 0 0 var(--white);
  }
  
  .add-icon {
    width: 2rem;
    margin-right: 0.4rem;
  }
}

@media (max-width: 768px) {
  .add-item-btn {
    font-size: 0.7rem;
    font-weight: 600;
  }
}
</style>
