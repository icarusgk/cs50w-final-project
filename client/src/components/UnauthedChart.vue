<script setup>
import { ref, onMounted } from 'vue';
import ApexChart from 'apexcharts';

// a template ref
const unauthedChart = ref(null);

const widthSize = () => window.innerWidth;
const heightSize = () => window.innerWidth;

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
    text: 'Tasks done',
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
      name: 'Tasks Done',
      data: [5, 9, 10, 5, 3, 6, 7, 1, 2, 8],
    },
  ],
  xaxis: {
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
    ]
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
  const chart = new ApexChart(unauthedChart.value, options.value);
  chart.render();
})
</script>

<template>
  <div id="unauthedChart" ref="unauthedChart"></div>
</template>

<style>
#unauthedChart {
  max-width: 760px;
  margin: 35px auto;
}
</style>
