<script setup lang="ts">
import { watch } from 'vue';
import { useTimerStore } from '@/stores/timer';

import CurrentTask from './CurrentTask.vue';

const timer = useTimerStore();

watch(
  () => timer.currentTimer.timer,
  () => {
    // Change the red line percent
    if (timer.ongoing) {
      timer.increasePercent();
    }

    // If current timer (pomo, short, long) ended
    if (timer.minutes === 0 && timer.seconds === 0) {
      timer.done = true;
      timer.setNextTimer();
      stopTimer();

      // Auto start pomo
      if (timer.current == 'pomo') {
        // timer.ongoing or stopTimer()?
        timer.auto_start_pomo ? startTimer() : timer.ongoing = false;
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
  timer.timerId = setInterval(() => {
    timer.decrementSecond();
  }, 1000);
}

function startTimer() {
  // Toggle status
  timer.toggleOngoing();
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
</script>

<template>
  <div id="timer-container">
    <p 
      v-if="!timer.currentMode.includes('Default')"
      id="mode-title"
    >
      Current Mode: {{ timer.currentMode }}
    </p>
    <div id="timer-setters">
      <div
        id="normal-pomo"
        @click="
          timer.setTimer('pomo');
          stopTimer();
        "
      >
        Pomo
      </div>
      <div id="short-rest" @click="timer.setTimer('short_break'); stopTimer();">
        Short Rest
      </div>
      <div id="long-rest" @click="timer.setTimer('long_break'); stopTimer();">
        Long Rest
      </div>
    </div>
    <!-- Progress -->
    <div
      id="line"
      :style="{ width: `${timer.percent - 2}%` }"
      :class="timer.current"
    ></div>
    <!-- Time -->
    <div>
      <h1 id="timer-count">{{ timer.currentTimer.timer.format('mm:ss') }}</h1>
      <button @click="startTimer()" v-if="!timer.ongoing" id="start-timer-btn">
        Start!
      </button>
      <button @click="stopTimer()" v-else id="stop-timer-btn">Stop!</button>
      <button
        @click="restartTimer()"
        v-if="timer.ongoing"
        id="restart-timer-btn"
      >
        Restart!
      </button>
      <!-- TODO: Change style -->
      <div class="done" v-if="timer.done && !timer.ongoing">
        <span>Done!</span>
      </div>
      <CurrentTask />
    </div>
  </div>
</template>

<style lang="scss" scoped>
%btn {
  &:hover,
  &:focus {
    cursor: pointer;
  }
}

@mixin timer-setter($bg-color) {
  background-color: $bg-color;
  padding: 0.5rem 0.8rem;
  border-radius: 8px;
  font-weight: 600;

  @extend %btn;
}

@mixin line($color) {
  height: 15px;
  border-radius: 18px;
  background-color: $color;

  transition: background-color 0.2s ease-in-out;
}

#timer-container {
  #mode-title {
    font-size: 1.5rem;
    font-weight: 700;
  }
  #timer-setters {
    display: flex;
    gap: 0.6rem;
    margin-bottom: 1rem;
  }

  #line {
    transition: width 0.2s ease-in-out;
  }

  .pomo {
    @include line(var(--vivid-red));
  }

  .short_break {
    @include line(var(--short-rest));
  }

  .long_break {
    @include line(var(--long-rest));
  }

  #timer-count {
    font-size: 8rem;
  }

  @mixin timer-button($bg-color) {
    padding: 1rem;
    width: 210px;
    border-radius: 18px;
    font-size: 1.5rem;
    background-color: $bg-color;
    color: white;
    font-weight: 900;
    border: none;
    margin-top: 1rem;

    @extend %btn;
  }

  #normal-pomo {
    @include timer-setter(var(--vivid-red));
  }

  #short-rest {
    @include timer-setter(var(--short-rest));
  }

  #long-rest {
    @include timer-setter(var(--long-rest));
  }

  .done {
    display: block;
    margin-top: 1rem;
    font-weight: 700;
    font-size: 2rem;
  }

  #start-timer-btn {
    @include timer-button(var(--vivid-red));
  }

  #stop-timer-btn {
    @include timer-button(var(--light-blue));
  }

  #restart-timer-btn {
    @include timer-button(darkorange);
    margin-left: 1rem;
  }
}

@media (max-width: 768px) {
  @mixin mobile-btn($width) {
    margin-top: 0;
    width: $width;
  }
  #timer-container {
    width: 82vw;
    #timer-count {
      font-size: 6rem;
    }
    #start-timer-btn {
      @include mobile-btn(200px);
    }

    #stop-timer-btn {
      @include mobile-btn(120px);
    }

    #restart-timer-btn {
      @include mobile-btn(140px);
    }
  }
}
</style>
