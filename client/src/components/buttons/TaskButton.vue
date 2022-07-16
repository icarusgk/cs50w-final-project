<script setup lang="ts">
import { useModalStore } from '@/stores/modal';
import { ref, watch } from 'vue';
import AddIcon from '../icons/AddIcon.vue';
import Modal from '../modals/Modal.vue';

const open = ref(false)

watch(() => open.value, () => {
  useModalStore().toggle()
})
</script>

<template>
  <div @click="open = true" class="add-item-btn">
    <!-- Icon -->
    <AddIcon class="add-icon" />
    <slot name="type"></slot>
    <Modal :is-button="true" :open="open" @close-modal="(close) => open = close">
      <template #tags>
        <slot name="tags"></slot>
      </template>
      <template #title>
        <slot name="title"></slot>
      </template>
      <slot></slot>
      <template #save-button>
        <slot name="save-button"></slot>
      </template>

    </Modal>
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