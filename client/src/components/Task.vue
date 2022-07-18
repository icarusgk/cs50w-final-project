<script setup lang="ts">
import { ref, watch } from "vue";
import Tags from "./buttons/Tags.vue";
import TaskInfoIcon from "./icons/TaskInfoIcon.vue";
import Modal from "./modals/Modal.vue";
import NewTaskModal from "./modals/new-modals/NewTaskModal.vue";
import type TypeTask from "@/types/TaskType"
import { useModalStore } from "@/stores/modal";

const props = defineProps<{
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
      <div class="title-container">
        <p>{{ props.task.title }}</p>
      </div>
      <div class="task-info-icon">
        <TaskInfoIcon />
      </div>
    </div>
    <!-- Modal -->
    <Modal :open="open" @close-modal="(close) => open = close">
      <!-- Tags -->
      <template #tags>
        <Tags :tags="task.tags" />
      </template>
      <!-- Title -->
      <template #title>
        <input type="text" name="title" id="task-input-title" v-model="props.task.title" />
      </template>
      <!-- Modal -->
      <NewTaskModal :task="task" />
    </Modal>
  </div>
</template>

<style lang="scss" scoped>
.task-container {
  display: flex;
  align-items: center;
  margin: 0 0.2rem 0.5rem 0.2rem;

  &:hover, &:focus {
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
      margin-top: 0.2rem;
      &:hover, &:focus {
        cursor: pointer;
      }
    }
  }
}

#task-input-title {
  border: none;
  background: transparent;
  color: white;
  font-size: 2rem;
  font-weight: 900;
  font-family: sans-serif;
  width: 100%;

  &:focus {
    outline: none;
  }

}



</style>
