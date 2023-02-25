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
  <div class="flex justify-center">
    <!-- Number -->
    <input
      type="number"
      class="bg-transparent border-none text-white w-[18%] outline-none font-bold mr-2"
      :min="limits.min"
      :max="limits.max"
      :value="localPomos"
      @input="e => setPomos(((e.target) as HTMLInputElement).value)"
    />
    <button @click="decreasePomos" class="mr-1.25 py-0.5 px-2 border-none outline-none rounded-md bg-lighter-gray text-white pointer">-</button>
    <button @click="increasePomos" class="py-0.5 px-2 border-none outline-none rounded-md bg-lighter-gray text-white pointer">+</button>
  </div>
</template>
