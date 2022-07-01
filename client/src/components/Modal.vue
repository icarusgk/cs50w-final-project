<script setup lang="ts">
// Modal is gonna receive the props
const props = defineProps<{
  open: Boolean
}>()

const emit = defineEmits(['closeModal'])

const closeModal = () => emit('closeModal', false)
</script>

<template>
  <Teleport to="body">
    <div v-if="open" class="modal">
      <slot></slot>
      <!-- Close modal -->
      <button 
        @click="closeModal()"
        class="close-modal-button"
      >Close
      </button>
    </div>
  </Teleport>
</template>

<style lang="scss" scoped>
.modal {
  // Positioning
  position: fixed;
  z-index: 2;
  top: 20%;
  left: 30%;
  width: 40%;

  // Color
  background-color: white;
  color: black;

  padding: 2rem;
  border-radius: 10px;

  .close-modal-button {
    background-color: var(--white);
    color: var(--black);
    display: flex;
    align-items: center;
    border-radius: 10px;
    margin-right: 1rem;
    padding: 0.5rem 0.5rem;
  }
}
</style>