import { defineStore } from 'pinia';
import { useAuthStore, useChoreStore } from '@/stores';
import { ref, computed } from 'vue';
import { toTimer, local } from '@/utils';
import type { ITimer } from '@/types';

type TimerType = 'pomo' | 'short' | 'long';

// In case the timer object is empty
export const defaultTimer: ITimer = {
  id: 0,
  name: 'Default',
  pomo: 25,
  short: 5,
  long: 15,
};

// If there isn't a timer on the localstorage, set the defaultTimer
if (!local.get('timer')) local.set('timer', defaultTimer)
const localTimer = local.get('timer') as ITimer;

export const useTimerStore = defineStore('timer', () => {
  const auth = useAuthStore();
  const chore = useChoreStore();

  let timerId: number | null;

  const isRunning = ref(false)
  const sessions = ref(0)
  const timerType = ref<TimerType>('pomo')
  const done = ref(false)
  
  const auto_start_pomo = ref(auth.user?.auto_start_pomos || false)
  const auto_start_breaks = ref(auth.user?.auto_start_breaks || false)

  const currentMode = ref<ITimer>({...defaultTimer});

  const currentTimer = ref(currentMode.value[timerType.value as keyof ITimer])
  const activeTimer = ref(toTimer(currentTimer.value as number))

  const displayTimer = computed(() => {
    return activeTimer.value.format(activeTimer.value.hour() ? 'hh:mm:ss' : 'mm:ss')
  })

  function startTimer() {
    if (timerId) return;
    isRunning.value = true;
    done.value = false;
    timerId = window.setInterval(() => {
      activeTimer.value = activeTimer.value.subtract(1, 'second');
    }, 1000);
  }

  // Sets the next timer type based on the current timer type 
  // and number of completed sessions.
  function setNextTimer() {
    if (timerType.value === 'short' || timerType.value === 'long') {
      setTo('pomo');
    } else if (timerType.value === 'pomo') {
      useChoreStore().incrementGoneThrough();
      if (sessions.value === 3) {
        setTo('long'); sessions.value = 0;
      } else {
        setTo('short'); sessions.value++;
      }
    }
  }

  function stopTimer() {
    if (timerId) clearInterval(timerId);
    isRunning.value = false;
    timerId = null;
  }

  function restartTimer() {
    stopTimer();
    activeTimer.value = toTimer(currentTimer.value as number);
  }

  function setTo(timerMode: TimerType) {
    stopTimer();
    timerType.value = timerMode;
    currentTimer.value = currentMode.value[timerMode as keyof ITimer]
    activeTimer.value = toTimer(currentTimer.value as number);
  }

  // From here on, will work with settings
  function setNewTimer(data: ITimer) {
    currentMode.value = data;
  }

  function setToDefault() {
    currentMode.value = {...localTimer};
    timerType.value = 'pomo';
  }

  return { isRunning, done, sessions, timerType, auto_start_pomo, auto_start_breaks, currentMode, currentTimer, activeTimer, displayTimer, startTimer, restartTimer, stopTimer, setTo, setNextTimer, setNewTimer, setToDefault }
});
