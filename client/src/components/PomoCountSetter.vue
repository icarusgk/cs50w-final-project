<script setup lang="ts">
import type { ITask } from '@/types';

const props = defineProps<{
  chore: ITask;
}>();

const { estimated: localPomos } = toRefs(props.chore)
const emit = defineEmits<{
  (e: 'change:pomoCount', newValue: number): void
}>();

const limits = reactive({ min: 1, max: 99 });

function increasePomos() {
  localPomos.value = Math.min(localPomos.value + 1, limits.max)
  emit('change:pomoCount', localPomos.value);
}

function decreasePomos() {
  localPomos.value = Math.max(localPomos.value - 1, limits.min)
  emit('change:pomoCount', localPomos.value);
}

function setPomos(count: string) {
  localPomos.value = Math.min(parseInt(count), limits.max);
  emit('change:pomoCount', localPomos.value);
}
</script>

<template>
  <div class="timers">
    <!-- Number -->
    <input
      type="number"
      class="estimated-timers"
      :min="limits.min"
      :max="limits.max"
      :value="localPomos"
      @input="e => setPomos(((e.target) as HTMLInputElement).value)"
    />
    <button @click="decreasePomos" class="minus-icon pomo-icon">-</button>
    <button @click="increasePomos" class="pomo-icon">+</button>
  </div>
</template>

<style scoped lang="scss">
.timers {
  display: flex;
  justify-content: center;

  .estimated-timers {
    background: transparent;
    border: none;
    color: white;
    width: 18%;
    outline: none;
    font-weight: 700;
    margin-right: 0.5rem;
  }

  .minus-icon {
    margin-right: 5px;
  }

  .pomo-icon {
    padding: 2px 7px;
    border-radius: 4px;
    border: none;
    outline: none;
    background-color: rgba(255, 255, 255, 0.25);
    color: white;

    &:hover,
    &:focus,
    &:active {
      cursor: pointer;
    }
  }
}
</style>
