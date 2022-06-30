<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import dayjs from 'dayjs';

const MINUTES25 = dayjs().set('minutes', 25).set('seconds', 0)
const MOCK = dayjs().set('minutes', 0).set('seconds', 4)
const MINUTESINSECONDS = 1500

let timerId: number
const timerMinutes = ref(MINUTES25)
let done = ref(false)
let ongoing = ref(false)
let percent = ref(10)

watch(timerMinutes, (newMinutes) => {
  const minutes = newMinutes.minute()
  const seconds = newMinutes.second()

  const diff = MINUTES25.diff(newMinutes, 'seconds')
  percent.value = ((diff / MINUTESINSECONDS) * 80) + 5

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
    timerMinutes.value = MOCK
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
    <div 
      id="red-line"
      :style="{ 'width': percent + '%' }"
    ></div>
    <!-- Time -->
    <div>
      <h1 id="timer-count">{{ timerMinutes.format("mm:ss") }}</h1>
      <button @click="startTimer" v-if="!ongoing" id="start-timer-btn">Start!</button>
      <button @click="stopTimer" v-else id="stop-timer-btn">Stop!</button>
      <h2 v-if="done">DONEEE</h2>
    </div>
  </div>
</template>

<style lang="scss">
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
</style>