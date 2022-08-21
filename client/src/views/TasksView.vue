<script setup lang="ts">
import { computed } from '@vue/reactivity';
import { useChoreStore } from '@/stores/chore';

import TaskInfo from '@/components/TaskInfo.vue';
import BackIcon from '@/components/icons/BackIcon.vue';
// import tasks from '@/mocks/tasks';


const tasks = computed(() => useChoreStore().tasks)
</script>

<template>
<div class="tasks-view">
  <div class="go-back">
    <BackIcon class="button" @click="$router.back()" />
    <span class="title">Tasks</span>
  </div>
  <div class="all-tasks-container">
    <TaskInfo v-for="task in tasks" :task="task"/>
  </div>
</div>
</template>


<style scoped lang="scss">
.tasks-view {
  padding: 1.5rem;
  .go-back {
    display: flex;
    align-items: center;
    color: white;
    gap: 1rem;
    
    .button {
      &:hover, &:focus {
        cursor: pointer;
      }
    }
  }
  .title {
    color: white;
    font-size: 3rem;
    font-weight: 800;
  }
  .all-tasks-container {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    gap: 1rem;
  }
}

@media (max-width: 768px) {
  .tasks-view {
    padding: 0.5rem;
  }
}
</style>