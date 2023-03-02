<script setup lang="ts">
// import start from '@/assets/start-timer.mp3';
// import finished from '@/assets/finished-timer.mp3';

const timer = useTimerStore();
// New audios to be found
const startAudio = new Audio();
const finishedAudio = new Audio();

watch(
  () => timer.currentTimer.timer,
  () => {
    // If current timer (pomo, short, long) ended
    if (timer.minutes === 0 && timer.seconds === 0) {
      timer.done = true;
      timer.setNextTimer();
      finishedAudio.play();
      stopTimer();
      document.title = 'Pomo.do - Done!';

      // Auto start pomo
      if (timer.current == 'pomo') {
        timer.auto_start_pomo ? startTimer() : (timer.ongoing = false);
      }

      // Auto start breaks
      if (timer.current == 'short_break' || timer.current == 'long_break') {
        if (timer.auto_start_breaks) {
          startTimer();
        }
      }
    }
  }
);

function initTimer() {
  // Clear an existing ID
  if (timer.timerId) {
    clearInterval(timer.timerId);
  }
  // Create new ID and start a new timer
  timer.timerId = window.setInterval(() => {
    timer.decrementSecond();
  }, 1000);
}

function startTimer() {
  timer.ongoing = true;
  timer.done = false;

  // Restart the timer to the current mode
  initTimer();
}

function stopTimer() {
  timer.ongoing = false;
  clearInterval(timer.timerId);
}

function restartTimer() {
  stopTimer();
  timer.setTimer(timer.current);
}

// Conditionally sets timer
function setTimer(type: string) {
  if (!timer.ongoing) {
    timer.setTimer(type);
    return;
  }

  const message = 'There is a current timer ongoing, are you sure?';
  if (window.confirm(message)) {
    timer.setTimer(type);
    stopTimer();
  }
}
</script>

<template>
  <div>
    <span v-if="!timer.currentMode.includes('Default')" class="block text-2xl font-bold">
      Current Mode: {{ timer.currentMode }}
    </span>
    <!-- Timer buttons -->
    <div class="flex gap-2 mb-8">
      <div class="timer-btn timer-btn-red" @click="setTimer('pomo')">Pomo</div>
      <div class="timer-btn timer-btn-blue" @click="setTimer('short_break')">Short Rest</div>
      <div class="timer-btn timer-btn-green" @click="setTimer('long_break')">Long Rest</div>
    </div>
    <!-- Time -->
    <div>
      <h1 class="font-bold my-4 text-8xl lg:text-9xl">{{ timer.formattedTime }}</h1>
      <button
        @click="
          startTimer();
          startAudio.play();
        "
        v-if="!timer.ongoing"
        :class="timer.current"
      >
        Start!
      </button>
      <button @click="stopTimer()" v-else class="stop-timer-btn">Stop!</button>
      <button
        @click="restartTimer()"
        v-if="timer.ongoing"
        class="restart-timer-btn ml-4"
      >
        Restart!
      </button>
      <!-- TODO: Change style -->
      <div class="block mt-4 font-bold text-4xl" v-if="timer.done && !timer.ongoing">
        <span>Done!</span>
      </div>
      <!-- <CurrentTask /> -->
    </div>
  </div>
</template>
