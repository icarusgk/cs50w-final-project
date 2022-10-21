<script setup>
import AboutIcon from '@/components/icons/AboutIcon.vue'
</script>

<template>
  <div class="about">
    <div class="title">
      <AboutIcon />
      <h1>About</h1>
    </div>

    <div class="info">
      <h1>What is Pomodoro?</h1>
      <p>Pomodoro is a technique for productivity.</p>
    </div>

    <div class="final-project">
      <h1>CS50w Final Project</h1>
      <p>This is my CS50's Web Programming with Python and JavaScript final project.</p>
    </div>
  </div>
</template>

<style scoped lang="scss">
.about {
  color: white;
  margin: 2rem 4rem;

  .title {
    display: flex;
    align-items: center;
    margin-left: -0.5rem;
    margin-bottom: 1rem;
    h1 {
      margin-left: 1rem;
    }
  }

  .final-project {
    margin-top: 2rem;
  }
}
</style>
