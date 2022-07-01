import { defineStore } from 'pinia'
import dayjs from 'dayjs'

const MINUTES25 = dayjs().set('minutes', 25).set('seconds', 0)
const MINUTESINSECONDS = 1500

export const useTimerStore = defineStore({
  id: 'timer',
  state: () => ({
    timerId: 0,
    timer: MINUTES25,
    done: false,
    ongoing: false,
    percent: 10
  }),
  getters: {
    minutes: state => state.timer.minute(),
    seconds: state => state.timer.second()
  },
  actions: {
    decrementSecond() {
      this.timer = this.timer.subtract(1, 'second')
    },
    toggleOngoing() {
      this.ongoing = !this.ongoing
    },
    markDone() {
      this.done = true
    },
    incrementLine() {
      // Compare the current time with the original time
      const diff = MINUTES25.diff(this.timer, 'seconds')
      this.percent = ((diff / MINUTESINSECONDS) * 80) + 5
      
    },
    setInitialValue() {
      this.timer = MINUTES25
      this.done = false
    }
  }
})
