<script setup>
const chore = useChoreStore();
await chore.fetchStats();

// A template ref
const responsiveChart = ref(null);

const widthSize = () => window.innerWidth;
const heightSize = () => window.innerWidth;

// options
const options = ref({
  chart: {
    width: '100%',
    height: widthSize() < 768 ? heightSize() : 600,
    type: 'bar',
    fontFamily: 'Poppins',
  },
  theme: {
    mode: 'light',
    monochrome: {
      enabled: true,
      color: '#ed4747',
      shadeTo: 'light',
      shadeIntensity: 0.65,
    },
  },
  fill: {
    type: 'solid',
  },
  title: {
    text:
      chore.stats.length > 0
        ? 'Tasks done'
        : "You don't have any tasks done yet!",
    align: 'center',
    margin: 10,
    style: {
      fontSize: '16px',
      fontWeight: 'bold',
      color: '#fff',
    },
  },
  plotOptions: {
    bar: {
      horizontal: false,
    },
  },
  dataLabels: {
    enabled: false,
  },
  stroke: {
    width: 1,
    colors: ['#fff'],
  },
  series: [
    {
      name: 'Tasks done',
      data: chore.stats.map((stat) => stat.chores_done),
    },
  ],
  xaxis: {
    categories: chore.stats.map((stat) => stat.day),
  },
  legend: {
    position: 'right',
    verticalAlign: 'top',
    containerMargin: {
      left: 35,
      right: 60,
    },
  },
  responsive: [
    {
      breakpoint: 1000,
      options: {
        plotOptions: {
          bar: {
            horizontal: true,
          },
        },
        legend: {
          position: 'bottom',
        },
      },
    },
  ],
});

onMounted(() => {
  // Here we can have access to the elements
  // That are in the DOM
  const chart = new ApexChart(responsiveChart.value, options.value);
  chart.render();
});
</script>

<template>
  <div id="responsiveChart" ref="responsiveChart"></div>
</template>

<style scoped lang="scss">
#responsiveChart {
  max-width: 760px;
  margin: 35px auto;
}
</style>
