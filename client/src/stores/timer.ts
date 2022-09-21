import { defineStore } from 'pinia';
import { useChoreStore } from './chore';
import type { ModeType } from '@/types';
import dayjs from 'dayjs';

type TimerType = {
  minutes: dayjs.Dayjs;
  seconds: number;
};

// In case the timer object is empty
const defaultTimer = {
  name: 'default',
  pomo: 25,
  short_break: 5,
  long_break: 15
}

let timer: ModeType = JSON.parse(localStorage.getItem('timer') || '{}');

if (Object.keys(timer).length === 0) {
  timer = defaultTimer;
}

const POMO: TimerType = {
  minutes: dayjs().set('minutes', timer.pomo).set('seconds', 0),
  seconds: 1500,
};
const LONG_REST: TimerType = {
  minutes: dayjs().set('minutes', timer.long_break).set('seconds', 0),
  seconds: 900,
};
const SHORT_REST: TimerType = {
  minutes: dayjs().set('minutes', timer.short_break).set('seconds', 0),
  seconds: 300,
};

function calculatePercent(time: TimerType, timer: dayjs.Dayjs) {
  return (time.minutes.diff(timer, 'seconds') / time.seconds) * 100;
}

export const useTimerStore = defineStore({
  id: 'timer',
  state: () => ({
    timerId: 0,
    timer: POMO.minutes,
    done: false,
    ongoing: false,
    current: 'pomo',
    percent: 5,
    sessions: 0,
    minutesInSeconds: 1500,
  }),
  getters: {
    minutes: (state) => state.timer.minute(),
    seconds: (state) => state.timer.second(),
  },
  actions: {
    decrementSecond() {
      this.timer = this.timer.subtract(1, 'second');
    },
    toggleOngoing() {
      this.ongoing = !this.ongoing;
    },
    markDone() {
      this.done = true;
      // set next timer
      if (this.current === 'short' || this.current === 'long') {
        this.setPomo();
      } else if (this.current === 'pomo') {
        useChoreStore().incrementGoneThrough();
        if (this.sessions === 3) {
          this.setLongRest();
          this.sessions = 0;
        } else {
          this.setShortRest();
          this.sessions++;
        }
      }
    },
    incrementLine() {
      // Compare the current time with the original time
      switch (this.current) {
        case 'pomo':
          this.percent = calculatePercent(POMO, this.timer) + 5;
          break;
        case 'short':
          this.percent = calculatePercent(SHORT_REST, this.timer) + 5;
          break;
        case 'long':
          this.percent = calculatePercent(LONG_REST, this.timer) + 5;
      }
    },
    setPomo() {
      this.timer = POMO.minutes;
      this.current = 'pomo';
    },
    setShortRest() {
      this.timer = SHORT_REST.minutes;
      this.current = 'short';
    },
    setLongRest() {
      this.timer = LONG_REST.minutes;
      this.current = 'long';
    },
  },
});
