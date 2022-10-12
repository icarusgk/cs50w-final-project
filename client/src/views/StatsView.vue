<script setup>
import { useAuthStore } from '@/stores/auth';
import Chart from '@/components/Chart.vue';
import FakeChart from '@/components/FakeChart.vue'
import UnauntheticatedLogin from '../components/UnauntheticatedLogin.vue'

const auth = useAuthStore();
</script>

<template>
  <div class="stats">
    <h1>Stats</h1>
    <div class="fake-chart-container" v-if="!auth.isAuthenticated">
      <div class="message">
        <UnauntheticatedLogin>
          To see your stats!
        </UnauntheticatedLogin>
      </div>
      <FakeChart class="blur" />
    </div>
    <div v-else>
      <Chart />
    </div>
  </div>
</template>

<style scoped lang="scss">
.stats {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  color: white;

  .fake-chart-container {
    position: relative;
    .message  {
      // Above the graph
      position: absolute;
      top: 40%;
      right: 35%;
      z-index: 4;

      font-size: 2rem;
    }
  }
}

.blur {
  filter: blur(10px);
}
</style>
