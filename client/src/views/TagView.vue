<script setup lang="ts">
import { ref } from 'vue';
import { useRoute } from 'vue-router';
import { useFetch } from '@/composables/useFetch';
import TaskInfo from '../components/TaskInfo.vue';

const route = useRoute();

const tasks = ref([]);

useFetch(`tagInfo/${route.params.name}`, 'get').then((res) => {
  tasks.value = res.data;
})
</script>

<template>
  <TaskInfo v-for="task in tasks" :task="task" />
</template>

<style lang="scss">

</style>
