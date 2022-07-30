<script setup lang="ts">
import Subtasks from "../Subtasks.vue"
import { useChoreStore } from '@/stores/chore';
import DeleteIcon from '../icons/DeleteIcon.vue';

const props = defineProps<{
  project: any,
  isNew?: boolean
}>()

const emits = defineEmits(['closeModal'])

function deleteProject() {
  useChoreStore().deleteProject(props.project.id)
  emits('closeModal')
}
</script>

<template>
  <div class="project-modal">
    <!-- Tasks heading -->
    <div>
      <DeleteIcon @click="deleteProject()" class="delete-icon" />
    </div>
    <div>
      <p class="task-heading">Tasks</p>
    </div>
    
    <!-- Add tasks button -->
    <div>
      <Subtasks :is-project="true" :subtasks="project.tasks" :project="project" :isNew="isNew" />
    </div>
  </div>
</template>

<style lang="scss" scoped>
.project-modal {
  margin-top: 1rem;

  .delete-icon {
    &:hover, &:focus {
      cursor: pointer;
    }
  }
  .task-container {
    display: flex;
    flex-wrap: wrap;
    margin: 0.5rem 0;
    height: 33px;

    .add-task {
      padding: 0 1rem;
    }
    
    .icon {
      margin-left: 1rem;
      margin-top: 2px;
    }

    .new-subtask {
      width: 15px;
      height: 15px;
      margin-top: 2px;
      margin-left: 0.5rem;
    }
  }
}
</style>