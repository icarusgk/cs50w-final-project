<script setup lang="ts">
import TaskType from './slots/TaskType.vue';
import SingleTaskIcon from './icons/SingleTaskIcon.vue';
import Task from './Task.vue';
import { useFetch } from '@/composables/useFetch';

const { data, error, retry } = useFetch('/tasks')

function deleteTask(task: any) {
  data.value = data.value.filter((t: any) => t.id !== task)
}


</script>

<template>
  <div>
    <TaskType>
      <template #icon>
        <SingleTaskIcon />
      </template>
      <template #type>
        <h1>Single Tasks</h1>
      </template>
    </TaskType>

    <div v-for="task in data">
      <Task @delete-task="deleteTask" :task="task" />
    </div>
  </div>
</template>

<style lang="scss" scoped>

</style>