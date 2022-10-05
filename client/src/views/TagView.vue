<script setup lang="ts">
import { ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import { useFetch } from '@/composables/useFetch';
import TaskInfo from '../components/TaskInfo.vue';
import BackIcon from '@/components/icons/BackIcon.vue';
import type { TaskType } from '@/types';

const route = useRoute();

const tasks = ref<TaskType[]>([]);

useFetch(`tagInfo/${route.params.name}`, 'get').then((res) => {
  tasks.value = res.data;
});
</script>

<template>
  <div class="tag-info-container">
    <div class="go-back">
      <BackIcon class="button" @click="$router.back()" />
    </div>
    <span class="title">#{{ route.params.name }}</span>
    <div class="all-tasks-container">
      <TaskInfo 
        v-for="task in tasks" 
        :task="task"
        :key="task.id"
      />
    </div>
  </div>
</template>

<style scoped lang="scss">
.tag-info-container {
  padding: 2rem 1.5rem;
  .go-back {
    display: flex;
    align-items: center;
    color: white;
    gap: 1rem;

    .button {
      &:hover,
      &:focus,
      &:active {
        cursor: pointer;
      }
    }
    .title {
      color: white;
      font-size: 3rem;
      font-weight: 800;
    }
  }

  .title {
    color: white;
    font-size: 2rem;
    font-weight: 800;
  }

  .all-tasks-container {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    gap: 1rem;
  }
}
</style>
