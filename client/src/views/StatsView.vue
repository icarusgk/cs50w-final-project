<script setup>
import { useAuthStore } from '@/stores/auth';
import AppChart from '@/components/AppChart.vue';
import UnauthedChart from '@/components/UnauthedChart.vue';
import UnauthedLogin from '../components/UnauthedLogin.vue';

const auth = useAuthStore();
</script>

<template>
  <div class="stats">
    <h1 v-if="auth.isAuthed">Stats</h1>
    <div class="fake-chart-container" v-if="!auth.isAuthed">
      <div class="message">
        <UnauthedLogin> To see your stats! </UnauthedLogin>
      </div>
      <UnauthedChart class="blur" />
    </div>
    <div v-else class="chart-container">
      <Suspense>
        <AppChart id="the-chart" />
      </Suspense>
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
  width: 100%;

  .fake-chart-container {
    position: relative;
    width: 100%;
    .message {
      // Above the graph
      position: absolute;
      top: 40%;
      right: 40%;
      z-index: 4;

      font-size: 2rem;
    }
  }

  .chart-container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width: 100%;

    #the-chart {
      width: 70%;
      color: black;
    }
  }
}

.blur {
  filter: blur(10px);
}

@media (max-width: 1000px) {
  .stats {
    .fake-chart-container {
      .message {
        right: 30%;
      }
    }
    .chart-container {
      #the-chart {
        width: 100%;
      }
    }
  }
}

@media (max-width: 500px) {
  .stats {
    .fake-chart-container {
      .message {
        right: 18%;
      }
    }
  }
}
</style>
