<script setup lang="ts">
import Subtasks from '@/components/Subtasks.vue';

defineProps<{
  project: any;
  isNew?: boolean;
}>();
</script>

<template>
  <div class="project-modal">
    <!-- Tasks heading -->
    <div>
      <p class="task-heading">Tasks</p>
    </div>
    <!-- Add tasks button -->
    <div>
      <Subtasks
        :is-project="true"
        :chores="project.tasks"
        :project="project"
        :isNew="isNew"
      />
    </div>
  </div>
</template>

<style lang="scss" scoped>
.project-modal {
  margin-top: 1rem;

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
