<script setup lang="ts">
import CloseIcon from '@/components/icons/CloseIcon.vue';

// Modal is gonna receive the props
defineProps<{
  open: Boolean;
  isButton?: Boolean;
  isTask?: Boolean
}>();

const emits = defineEmits(['exitModal']);
</script>

<template>
  <Teleport to="body">
    <div v-if="open" class="modal">
      <div class="task-upper-menu" :class="{ 'align-items': !isTask }">
        <div class="tags-and-title-container">
          <div v-if="isTask" class="tags-container">
            <slot name="tags"></slot>
          </div>

          <div class="title-container">
            <slot name="title"></slot>
          </div>
        </div>

        <div>
          <slot name="delete-icon"></slot>
        </div>

        <div @click="emits('exitModal')" class="close-icon">
          <CloseIcon />
        </div>
      </div>
      <slot></slot>
      <div class="buttons">
        <slot name="save-button"></slot>
      </div>
    </div>
  </Teleport>
</template>

<style lang="scss" scoped>
.modal {
  // Positioning
  position: absolute;
  top: 20%;
  z-index: 10;
  left: 5%;
  right: 0;
  margin-left: auto; 
  margin-right: auto; 
  width: 700px;

  // Color
  background-color: white;
  color: white;

  padding: 2rem;
  border-radius: 10px;

  background: rgba(136, 136, 136, 0.3);
  border-radius: 16px;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(11.2px);
  -webkit-backdrop-filter: blur(11.2px);

  .align-items {
    align-items: center;
  }

  .task-upper-menu {
    display: flex;
    justify-content: space-between;

    .tags-and-title-container {
      display: flex;
      flex-direction: column;
      width: 100%;

      .tags-container {
        display: flex;
        margin-bottom: 1rem;
      }
    }

    .close-icon {
      &:hover,
      &:focus,
      &:active {
        cursor: pointer;
      }
    }
  }

  .buttons {
    display: flex;
    gap: 1rem;
  }
}

@media (max-width: 1160px) {
  .modal {
    position: fixed;
    left: 23%;
    top: 25%;
    width: 600px;
  }
}

@media (max-width: 768px) {
  .modal {
    position: fixed;
    left: 5%;
    right: 5%;
    width: 90%;
    height: 80%;
    top: 5%;

    .buttons {
      flex-direction: column;
    }
  }
}
</style>
