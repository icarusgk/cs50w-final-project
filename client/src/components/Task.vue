<script setup lang="ts">
import TaskInfoIcon from "./icons/TaskInfoIcon.vue";
import type TypeTask from "@/types/TaskType"
defineProps<{
  task: TypeTask
}>()
</script>

<template>
  <div class="task-container">
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
  </div>
</template>

<style lang="scss" scoped>
.task-container {
  display: flex;
  align-items: center;
  margin: 0 0.2rem 0.5rem 0.2rem;
  

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