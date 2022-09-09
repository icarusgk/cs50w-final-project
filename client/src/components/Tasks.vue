<script setup lang="ts">
import { computed } from 'vue';
import { useChoreStore } from '@/stores/chore';

import TaskType from '@/components/slots/TaskType.vue';
import SingleTaskIcon from '@/components/icons/SingleTaskIcon.vue';
import Task from '@/components/buttons/Task.vue';

const choreStore = useChoreStore()

const tasks = computed(() => choreStore.tasks)
</script>

<template>
  <div>
    <TaskType class="button" @click="$router.push('/tasks')">
      <template #icon>
        <SingleTaskIcon />
      </template>
      <template #type>
        <h1>Single Tasks</h1>
      </template>
    </TaskType>
    <div v-if="tasks.length === 0">
      <h2>No tasks</h2>
    </div>
    <div v-for="task in tasks">
      <Task :task="task" />
    </div>
  </div>
</template>

<style lang="scss" scoped>
.button {
  &:hover, &:focus {
    cursor: pointer;
  }
}
</style>