<script setup lang="ts">
import { watch, computed } from 'vue';
import { useTimerStore } from '@/stores/timer';

import CurrentTask from '@/components/CurrentTask.vue';

const timer = useTimerStore();
const currentLine = computed(() => `line-${timer.current}`)

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
        @click="setTimer('pomo')"
      >
        Pomo
      </div>
      <div id="short-rest" @click="setTimer('short_break')">
        Short Rest
      </div>
      <div id="long-rest" @click="setTimer('long_break')">
        Long Rest
      </div>
    </div>
    <!-- Progress -->
    <div
      id="line"
      :style="{ width: `${timer.percent - 2}%` }"
      :class="currentLine"
    ></div>
    <!-- Time -->
    <div>
      <h1 id="timer-count">{{ timer.currentTimer.timer.format('mm:ss') }}</h1>
      <button @click="startTimer()" v-if="!timer.ongoing" :class="timer.current">
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
@mixin btn($bg-color) {
  box-shadow: 0 4px 0 0 lighten($bg-color, 10%);
  transition: box-shadow 0.2s cubic-bezier(0.075, 0.82, 0.165, 1);
  &:hover,
  &:focus,
  &:active {
    cursor: pointer;
  }

  &:active {
    box-shadow: 0 0 $bg-color;
  }
}

@mixin timer-setter($bg-color) {
  @include btn($bg-color);

  background-color: $bg-color;
  padding: 0.5rem 0.8rem;
  border-radius: 8px;
  font-weight: 600;  
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

  .line-pomo {
    @include line(var(--vivid-red));
  }

  .line-short_break {
    @include line(var(--short-rest));
  }

  .line-long_break {
    @include line(var(--long-rest));
  }

  #timer-count {
    font-size: 8rem;
  }

  @mixin timer-button($bg-color) {
    @include btn($bg-color);

    padding: 1rem;
    width: 160px;
    border-radius: 18px;
    font-size: 1.5rem;
    background-color: $bg-color;
    color: white;
    font-weight: 900;
    border: none;
    margin-top: 1rem;
  }

  #normal-pomo {
    @include timer-setter(#ed4747);
  }

  #short-rest {
    @include timer-setter(#1ba7b1);
  }

  #long-rest {
    @include timer-setter(#1eaf58);
  }

  .pomo {
    @include timer-button(#ed4747);
  }

  .short_break {
    @include timer-button(#1ba7b1);
  }

  .long_break {
    @include timer-button(#1eaf58);
  }

  .done {
    display: block;
    margin-top: 1rem;
    font-weight: 700;
    font-size: 2rem;
  }

  #start-timer-btn {
    @include timer-button(#ed4747);
  }

  #stop-timer-btn {
    @include timer-button(#1b6eb1);
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
