<script setup lang="ts">
import LightingIcon from '@/components/icons/LightingIcon.vue';
</script>

<template>
  <!-- Pomo Title -->
  <div @click="$router.push('/')" id="pomodoro-title-container">
    <!-- Icon -->
    <LightingIcon id="pomo-icon" />
    <!-- Title -->
    <h1 id="title">Pomodoro Timer</h1>
  </div>
</template>

<style scoped lang="scss">
#pomodoro-title-container {
  cursor: pointer;
  display: flex;
  align-items: center;
  #title {
    font-size: 2rem;
  }
}

@media (max-width: 768px) {
  #pomodoro-title-container {
    margin: 0;

    #pomo-icon {
      transform: scale(0.7);
    }
    #title {
      margin-left: -8px;
      font-size: 1.2rem;
    }
  }
}

@media (max-width: 460px) {
  #pomodoro-title-container {
    #title {
      font-size: 0.8rem;
    }
  }
}
</style>
