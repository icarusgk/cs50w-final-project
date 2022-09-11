<script setup lang="ts">
import { watch } from 'vue';
import { useTimerStore } from '@/stores/timer';

// import CurrentTask from './CurrentTask.vue';

const timer = useTimerStore();

watch(
  () => timer.timer,
  () => {
    // Change the red line percent
    timer.incrementLine();

    if (timer.minutes === 0 && timer.seconds === 0) {
      timer.markDone();
      stopTimer();
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
  switch (timer.current) {
    case 'pomo':
      timer.setPomo();
      break;
    case 'short':
      timer.setShortRest();
      break;
    case 'long':
      timer.setLongRest();
  }
}
</script>

<template>
  <div id="timer-container">
    <div id="timer-setters">
      <div
        id="normal-pomo"
        @click="
          timer.setPomo();
          stopTimer();
        "
      >
        Pomo
      </div>
      <div id="short-rest" @click="timer.setShortRest(), stopTimer()">
        Short Rest
      </div>
      <div id="long-rest" @click="timer.setLongRest(), stopTimer()">
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
      <h1 id="timer-count">{{ timer.timer.format('mm:ss') }}</h1>
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
      <div class="done" v-if="timer.done">
        <span>Done!</span>
      </div>
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

  .short {
    @include line(var(--short-rest));
  }

  .long {
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
