<script setup lang="ts">
import { computed } from '@vue/reactivity';
import { useChoreStore } from '@/stores/chore';

import TaskInfo from '@/components/TaskInfo.vue';

const tasks = computed(() => useChoreStore().tasks)
</script>

<template>
<p @click="$router.back()" style="color: white">Go back</p>
<h1 style="color: white">Tasks</h1>

<div class="all-tasks-container">
  <TaskInfo v-for="task in tasks" :task="task"/>
</div>

</template>


<style scoped lang="scss">
.all-tasks-container {
  display: flex;
  flex-wrap: wrap;

  margin-left: 1rem;
}
</style>