<script setup lang="ts">
import { ref, watch } from 'vue';
import { useModalStore } from '@/stores/modal';
import type { Task } from '@/types';

import Tags from '@/components/buttons/Tags.vue';
import TasksDoneIcon from '@/components/icons/TasksDoneIcon.vue';
import TotalTasksIcon from '@/components/icons/TotalTasksIcon.vue';
import TaskModal from '@/components/TaskModal.vue';

defineProps<{
  task: Task;
}>();

const open = ref(false);

watch(
  () => open.value,
  () => {
    useModalStore().toggle();
  }
);
</script>

<template>
  <div class="single-task-info" @click="open = true">
    <div class="tags-and-counters">
      <div class="tags">
        <Tags :taskTags="task.tags" :info="true" />
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

    <TaskModal :task="task" :open="open" @exit="open = false" />
  </div>
</template>

<style scoped lang="scss">
.single-task-info {
  width: 500px;
  background-color: #3d3d3d;
  color: white;
  height: 250px;
  padding: 1rem;
  border-radius: 8px;

  &:hover,
  &:focus {
    cursor: pointer;
  }

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
    height: 85%;
    justify-content: center;
    .title {
      font-weight: 700;
      font-size: larger;
    }
  }
}

@media (max-width: 768px) {
  .single-task-info {
    height: min-content;
  }
}
</style>
