<script setup>
import { reactive, ref } from 'vue';
import { useChoreStore } from '@/stores/chore';
import VueApexCharts from 'vue3-apexcharts';

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
    categories: [
      '18-oct',
      '19-oct',
      '20-oct',
      '21-oct',
      '22-oct',
      '23-oct',
      '24-oct',
      '25-oct',
      '26-oct',
      '27-oct',
    ],
  },
});
const series = ref([
  {
    name: 'Tasks Done',
    data: [5, 9, 10, 5, 3, 6, 7, 1, 2, 8],
  },
]);
</script>

<template>
  <VueApexCharts
    width="900"
    type="bar"
    :options="options"
    :series="series"
    style="border-radius: 4rem"
  ></VueApexCharts>
</template>
