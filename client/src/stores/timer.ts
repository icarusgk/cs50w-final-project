import { defineStore } from 'pinia';
import { useAlertStore, useChoreStore } from '@/stores';
import { ref, computed } from 'vue';
import { toTimer, local } from '@/utils';
import type { ITimer } from '@/types';

type TimerType = 'pomo' | 'short_break' | 'long_break';

// In case the timer object is empty
export const defaultTimer: ITimer = {
  id: 0,
  name: 'Default',
  pomo: 25,
  short_break: 5,
  long_break: 15,
};

// If there isn't a timer on the localstorage, set the defaultTimer
if (!local.get('timer')) local.set('timer', defaultTimer)

export const useTimerStore = defineStore('timer', () => {
  const alert = useAlertStore();

  let timerId: number | null;

  const isRunning = ref(false)
  const sessions = ref(0)
  const timerType = ref<TimerType>('pomo')
  const done = ref(false)

  const modes = ref<ITimer[]>(local.get('modes'))

  const currentMode = ref(local.get('timer') || modes.value[0]);

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
      document.title = `Pomo.do - ${displayTimer.value}`
    }, 1000);
  }

  // Sets the next timer type based on the current timer type 
  // and number of completed sessions.
  function setNextTimer() {
    if (timerType.value === 'short_break' || timerType.value === 'long_break') {
      setTo('pomo');
    } else if (timerType.value === 'pomo') {
      useChoreStore().incrementGoneThrough();
      if (sessions.value === 3) {
        setTo('long_break'); sessions.value = 0;
      } else {
        setTo('short_break'); sessions.value++;
      }
    }
  }

  function stopTimer() {
    if (timerId) clearInterval(timerId);
    isRunning.value = false;
    timerId = null;
    document.title = 'Pomo.do';
  }

  function restartTimer() {
    stopTimer();
    activeTimer.value = toTimer(currentTimer.value as number);
  }

  function changeTimer(timerMode: TimerType = 'pomo') {
    local.set('timer', currentMode.value);
    currentTimer.value = currentMode.value[timerMode];
    activeTimer.value = toTimer(currentTimer.value as number);
  }

  function setTo(timerMode: TimerType) {
    stopTimer();
    timerType.value = timerMode;
    changeTimer(timerMode);
  }

  // From here on, will work with settings
  function setNewTimer(data: ITimer) {
    currentMode.value = { ...data };
    timerType.value = 'pomo';
    alert.success(`Mode changed to ${data.name}`)
    changeTimer();
  }

  function setToDefault() {
    currentMode.value = { ...defaultTimer };
    alert.info('Back to default')
    changeTimer();
  }

  return { isRunning, done, sessions, timerType, modes, currentMode, currentTimer, activeTimer, displayTimer, startTimer, restartTimer, stopTimer, setTo, setNextTimer, setNewTimer, setToDefault }
});
