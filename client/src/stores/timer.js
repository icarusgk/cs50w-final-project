import { defineStore } from 'pinia';
import { useChoreStore } from './chore';
import dayjs from 'dayjs';

// In case the timer object is empty
export const defaultTimer = {
  name: 'Local Default',
  pomo: 25,
  short_break: 5,
  long_break: 15,
};

const storageTimer = localStorage.getItem('timer');
const localTimer = storageTimer ? JSON.parse(storageTimer) : defaultTimer;

const minutes = minutes => {
  return dayjs().set('minutes', minutes).set('seconds', 0);
}

const seconds = minutes => minutes * 60;

const n = 5;
export const useTimerStore = defineStore({
  id: 'timer',
  state: () => ({
    timerId: 0,
    currentTimer: {
      timer: minutes(localTimer.pomo),
      seconds: seconds(localTimer.pomo),
    },
    pomo: {
      timer: minutes(localTimer.pomo),
      seconds: seconds(localTimer.pomo),
    },
    short_break: {
      timer: minutes(localTimer.short_break),
      seconds: seconds(localTimer.short_break),
    },
    long_break: {
      timer: minutes(localTimer.long_break),
      seconds: seconds(localTimer.short_break),
    },
    currentMode: localTimer.name,
    done: false,
    ongoing: false,
    current: 'pomo',
    percent: 5,
    sessions: 0,
    auto_start_pomo: true,
    auto_start_breaks: true,
  }),
  getters: {
    minutes: (state) => state.currentTimer.timer.minute(),
    seconds: (state) => state.currentTimer.timer.second(),
  },
  actions: {
    setTo(data) {
      const { pomo, short_break, long_break } = data;
      this.currentTimer.timer = minutes(pomo);
      this.currentTimer.seconds = pomo;
      this.pomo.timer = minutes(pomo);
      this.pomo.seconds = seconds(pomo);

      this.short_break.timer = minutes(short_break);
      this.short_break.seconds = seconds(short_break);

      this.long_break.timer = minutes(long_break);
      this.long_break.seconds = seconds(long_break);
      this.currentMode = data.name;
    },
    setNewTimer(data) {
      this.setTo(data);
      const timer = JSON.stringify(data);
      localStorage.setItem('timer', timer);
    },
    decrementSecond() {
      this.currentTimer.timer = this.currentTimer.timer.subtract(1, 'second');
    },
    toggleOngoing() {
      this.ongoing = !this.ongoing;
    },
    setNextTimer() {
      // set next timer
      if (this.current === 'short_break' || this.current === 'long_break') {
        this.setTimer('pomo');
      } else if (this.current === 'pomo') {
        useChoreStore().incrementGoneThrough();
        if (this.sessions === 3) {
          this.setTimer('long_break');
          this.sessions = 0;
        } else {
          this.setTimer('short_break');
          this.sessions++;
        }
      }
    },
    setToDefault() {
      this.setTo(defaultTimer);
      localStorage.removeItem('timer');
    },
    increasePercent() {
      this.percent =
        (this[this.current].timer.diff(this.currentTimer.timer, 'seconds') /
          this.currentTimer.seconds) *
        100;
    },
    setTimer(name) {
      this.currentTimer.timer = this[name].timer;
      this.currentTimer.seconds = this[name].seconds;
      this.current = name;
      this.percent = 5;
    },
  },
});
