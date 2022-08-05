<script setup lang="ts">
import { watch } from 'vue'
import { useTimerStore } from '@/stores/timer';

import CurrentTask from './CurrentTask.vue';

const timer = useTimerStore()

watch(() => timer.timer, () => {
  // Change the red line percent
  timer.incrementLine()

  if (timer.minutes === 0 && timer.seconds === 0) {
    timer.markDone()
    stopTimer()
  }
})

function timerInitializer() {
  // Clear an existing ID
  if (timer.timerId) { clearInterval(timer.timerId) }
  // Create new ID
  timer.timerId = setInterval(() => {
    timer.decrementSecond()
  }, 1000)
}

function startTimer() {
  // Toggle status
  timer.toggleOngoing()

  // Check if the timer is done
  if (timer.done) {
    timer.setInitialValue()
  }

  // Start the timer
  timerInitializer()
}

function stopTimer() {
  timer.toggleOngoing()
  clearInterval(timer.timerId)
}

function restartTimer() {
  stopTimer()
  timer.setInitialValue()
}
</script>

<template>
  <div id="timer-container">
    <!-- Progress -->
    <div 
      id="red-line"
      :style="{ 'width': timer.percent + '%' }"
    ></div>
    <!-- Time -->
    <div>
      <h1 id="timer-count">{{ timer.timer.format("mm:ss") }}</h1>
      <button @click="startTimer()" v-if="!timer.ongoing" id="start-timer-btn">Start!</button>
      <button @click="stopTimer()" v-else id="stop-timer-btn">Stop!</button>
      <button @click="restartTimer()" v-if="timer.ongoing" id="restart-timer-btn">Restart!</button>
      <h2 v-if="timer.done">DONEEE</h2>
      <CurrentTask />
    </div>
  </div>
</template>

<style lang="scss" scoped>
#red-line {
  height: 15px;
  border-radius: 18px;
  background-color: var(--vivid-red);
  transition: width 0.2s ease-in-out;
}

#timer-count {
  font-size: 8rem;
}

%timer-button {
  padding: 1rem;
  width: 30%;
  border-radius: 18px;
  font-size: 120%;
  font-family: sans-serif;
  color: white;
  font-weight: 900;
  border: none;
  margin-top: 1rem;

  &:hover, &:focus {
    cursor: pointer;
  }
}

h2 {
  margin: 2rem;
}


#start-timer-btn {
  @extend %timer-button;
  background-color: var(--vivid-red);
}

#stop-timer-btn {
  @extend %timer-button;
  background-color: var(--light-blue);
}

#restart-timer-btn {
  @extend %timer-button;
  background-color: darkorange;
  margin-left: 1rem;
}
</style>