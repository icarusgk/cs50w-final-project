<script setup lang="ts">
// import start from '@/assets/start-timer.mp3';
// import finished from '@/assets/finished-timer.mp3';
const timer = useTimerStore();
const auth = useAuthStore();
const { startTimer, stopTimer, restartTimer, setTo } = timer;
// New audios to be found
const startAudio = new Audio();
const finishedAudio = new Audio();

type TimerType = 'pomo' | 'short_break' | 'long_break';

watch(() => timer.activeTimer, (newMinutes) => {
  // If current timer (pomo, short,long) ended
  if (newMinutes.minute() === 0 && newMinutes.second() === 0) {
    timer.done = true;
    stopTimer();
    // finishedAudio.play();
    timer.setNextTimer();
    document.title = 'Pomo.do - Done!';

    if (timer.timerType == 'pomo' && auth.user?.auto_start_pomos) {
      startTimer();
    }

    if ((timer.timerType == 'short_break' || timer.timerType == 'long_break') && auth.user?.auto_start_breaks) {
      startTimer();
    }
  }
});

function setTimer(type: TimerType) {
  if (!timer.isRunning) setTo(type)
  if (timer.isRunning && window.confirm('yes?')) {
      setTo(type)
  }
}
</script>

<template>
  <div>
    <!-- <span class="block text-2xl font-bold">
      Current Mode: {{ timer.currentMode }}
    </span> -->
    <!-- Timer buttons -->
    <div class="flex gap-2 mb-8">
      <div class="timer-btn timer-btn-red" @click="setTimer('pomo')">Pomo</div>
      <div class="timer-btn timer-btn-blue" @click="setTimer('short_break')">Short Rest</div>
      <div class="timer-btn timer-btn-green" @click="setTimer('long_break')">Long Rest</div>
    </div>
    <!-- Time -->
    <div>
      <h1 class="font-bold my-4 text-8xl lg:text-9xl">{{ timer.displayTimer }}</h1>
      <button
        @click="startTimer(); startAudio.play();"
        v-if="!timer.isRunning"
        :class="timer.timerType"
      >
        Start!
      </button>
      <button @click="stopTimer()" v-else class="stop-timer-btn">Stop!</button>
      <button
        @click="restartTimer()"
        v-if="timer.isRunning"
        class="restart-timer-btn ml-4"
      >
        Restart!
      </button>
      <!-- TODO: Change style -->
      <div class="block mt-4 font-bold text-4xl" v-if="timer.done && !timer.isRunning">
        <span>Done!</span>
      </div>
      <CurrentTask />
    </div>
  </div>
</template>
