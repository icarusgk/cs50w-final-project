<script setup lang="ts">
import type { Task } from '@/types';

import Tags from './buttons/Tags.vue';
import TasksDoneIcon from './icons/TasksDoneIcon.vue';
import TotalTasksIcon from './icons/TotalTasksIcon.vue';

defineProps<{
  task: Task
}>()
</script>

<template>
<div class="single-task-info">
  <div class="tags-and-counters">
    <div class="tags">
      <Tags :taskTags="task.tags" :info="true"  />
    </div>
    <div class="counters">
      <div class="counter-in-container">
        <TasksDoneIcon />
        <span class="single-counter">{{ task.gone_through }}</span>
      </div>
      <div>
        <TotalTasksIcon />
        <span class="single-counter">{{ task.estimated }}</span>
      </div>
    </div>
  </div>
  
  <div class="task-info">
    <span class="title">{{ task.title }}</span>
    <span>{{ task.description }}</span>
  </div>
</div>
</template>

<style scoped lang="scss">
.single-task-info {
  width: 500px;
  background-color: #3D3D3D;
  color: white;
  margin: 0 1rem 1rem 0rem;
  padding: 1rem;
  border-radius: 8px;

  margin: 0 1rem 1rem 0;
  flex: 1 0 auto;
  
  .tags-and-counters {
    display: flex;
    justify-content: space-between;    

    .tags {
      display: flex;
      margin-right: 2rem;
    }
    .counters {
      display: flex;

      .counter-in-container {
        margin-right: 10px;
      }

      .single-counter {
        margin-left: 5px;
      }      
    }
  }

  .task-info {
    display: flex;
    flex-direction: column;
    .title {
      font-weight: 700;
      font-size: larger;
    }
  }
}
</style>