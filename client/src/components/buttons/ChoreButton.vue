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

  &:hover {
    cursor: pointer;
  }

  .add-icon {
    width: 2rem;
    margin-right: 0.4rem;
  }
}

.modal {
  position: fixed;
  z-index: 2;
  top: 20%;
  left: 30%;
  width: 40%;
  background-color: white;
  color: black;
  padding: 2rem;
}
</style>