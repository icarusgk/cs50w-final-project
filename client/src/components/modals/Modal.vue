<script setup lang="ts">
import CloseIcon from "@/components/icons/CloseIcon.vue";

// Modal is gonna receive the props
defineProps<{
  open: Boolean
  isButton?: Boolean
  isProject?: Boolean
}>()

const emits = defineEmits(['exitModal'])

</script>

<template>
  <Teleport to="html">
    <div v-if="open" class="modal">
      <div class="task-upper-menu">
      
        <div class="tags-and-title-container">

          <div v-if="!isProject" class="tags-container">
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
  position: fixed;
  z-index: 2;
  top: 20%;
  left: 30%;
  width: 700px;

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

  .task-upper-menu {
    display: flex;
    justify-content: space-between;
    

    .tags-and-title-container {
      display: flex;
      flex-direction: column;
      width: 100%;

      .tags-container {
        display: flex;
        height: 25px;
        margin-bottom: 1rem;
      }
    }

    .close-icon {
      &:hover, &:focus {
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
    left: 23%;
    width: 600px;
  }
}

@media (max-width: 768px) {
  .modal {
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
