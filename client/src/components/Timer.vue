<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import dayjs from 'dayjs';

const MINUTES25 = dayjs().set('minutes', 25).set('seconds', 0)

let timerId: number
const timerMinutes = ref(MINUTES25)
let done = ref(false)
let ongoing = ref(false)


watch(timerMinutes, (newMinutes) => {
  const minutes = newMinutes.minute()
  const seconds = newMinutes.second()

  if (minutes === 0 && seconds === 0) {
    done.value = true
    stopTimer()
  }
})

const toggleOngoing = () => ongoing.value = !ongoing.value

function timer() {
  // Clear an existing ID
  if (timerId) { clearInterval(timerId) }
  // Create new ID
  timerId = setInterval(() => {
    timerMinutes.value = timerMinutes.value.subtract(1, 'second')
  }, 1000)
}

function startTimer() {
  // Toggle status
  toggleOngoing()

  // Check if the timer is done
  if (done.value) {
    timerMinutes.value = MINUTES25
    done.value = false
  }

  // Start the timer
  timer()
}

function stopTimer() {
  toggleOngoing()
  clearInterval(timerId)
}
</script>

<template>
  <div id="timer-container">
    <!-- Progress -->
    <div id="red-line"></div>
    <!-- Time -->
    <div>
      <h1 id="timer-count">{{ timerMinutes.format("mm:ss") }}</h1>
      <button @click="startTimer" v-if="!ongoing" id="start-timer-btn">Start</button>
      <button @click="stopTimer" v-else id="stop-timer-btn">Stop</button>
      <h2 v-if="done">DONEEE</h2>
    </div>
  </div>
</template>

<style lang="scss">
#red-line {
  width: 40%;
  height: 15px;
  border-radius: 18px;
  background-color: var(--vivid-red);
}

#timer-count {
  font-size: 8rem;
}

%timer-button {
  padding: 1rem;
  width: 40%;
  border-radius: 18px;
  font-size: 120%;
  font-family: sans-serif;
  color: white;
  font-weight: 900;
  border: none;
  margin-top: 1rem;

  &:hover {
    cursor: pointer;
  }
}


#start-timer-btn {
  @extend %timer-button;
  background-color: var(--vivid-red);
}

#stop-timer-btn {
  @extend %timer-button;
  background-color: var(--light-blue);
}
</style>