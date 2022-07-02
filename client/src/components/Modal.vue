<script setup lang="ts">
// Modal is gonna receive the props
defineProps<{
  open: Boolean
}>()

const emit = defineEmits(['closeModal', 'unblur'])

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
      >Save!
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
  color: white;

  padding: 2rem;
  border-radius: 10px;

  background: rgba(136, 136, 136, 0.30);
  border-radius: 16px;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(11.2px);
  -webkit-backdrop-filter: blur(11.2px);

  .close-modal-button {
    background-color: var(--vivid-red);
    color: var(--white);
    font: {
      weight: 900;
      family: sans-serif;
    }
    width: 100%;
    border: none;
    border-radius: 10px;
    margin-top: 1rem;
    padding: 0.8rem 0.8rem;

    &:hover {
      cursor: pointer;
    }
  }
}
</style>