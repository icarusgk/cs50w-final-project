<script setup lang="ts">
import { ref, watch } from "vue";
import TaskInfoIcon from "./icons/TaskInfoIcon.vue";
import Modal from "./Modal.vue";
import TaskInfoModal from "@/components/TaskInfoModal.vue";
import type TypeTask from "@/types/TaskType"
import { useModalStore } from "@/stores/modal";

defineProps<{
  task: TypeTask
}>()

const open = ref(false)

// When open.value changes, toggle
watch(() => open.value, () => {
  useModalStore().toggle()
})

</script>

<template>
  <div @click="open = true" class="task-container">
    <!-- Checkbox -->
    <div class="task-checkbox"></div>
    <!-- Name -->
    <div class="task-title-container">
      <div>
        <p>{{ task.title }}</p>
      </div>
      <div class="task-info-icon">
        <TaskInfoIcon />
      </div>
    </div>
    <Modal :open="open" @close-modal="(close) => open = close">
      <TaskInfoModal />
    </Modal>
  </div>
</template>

<style lang="scss" scoped>
.task-container {
  display: flex;
  align-items: center;
  margin: 0 0.2rem 0.5rem 0.2rem;

  &:hover {
    cursor: pointer;
  } 

  .task-checkbox {
    height: 20px;
    width: 20px;
    background-color: var(--white);
    border-radius: 10px;
    margin-right: 1rem;
  }
  
  .task-title-container {
    padding: 0.2rem 1rem;
    border-radius: 8px;
    background-color: var(--vivid-red);
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    
    .task-info-icon {
      &:hover {
        cursor: pointer;
      }
    }
  }
}

</style>