<script setup>
import {  reactive, ref } from 'vue';
import { useChoreStore } from '@/stores/chore';

const choreStore = useChoreStore();

const options = reactive({
  theme: {
    mode: 'dark',
    palette: 'palette7',
  },
  chart: {
    id: 'vuechart-example',
    fontFamily: 'Poppins',
  },
  xaxis: {
    type: 'datetime',
    categories: choreStore.stats.map((stat) => stat.day),
  },
});
const series = ref([
  {
    name: 'Tasks Done',
    data: choreStore.stats.map((stat) => stat.chores_done),
  },
]);
</script>

<template>
  <apexchart
    width="900"
    type="bar"
    :options="options"
    :series="series"
    style="border-radius: 4rem"
  ></apexchart>
</template>
  