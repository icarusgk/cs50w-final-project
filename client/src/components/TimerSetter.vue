<script setup lang="ts">
import { ref, reactive } from 'vue';

const props = defineProps(['chore']);
const emit = defineEmits(['decreasePomos', 'increasePomos']);

const pomoLimits = reactive({ min: 1, max: 99 });

const localPomos = ref(props.chore.estimated);

function increasePomos() {
  if (props.chore.estimated < pomoLimits.max) {
    localPomos.value++;
  } else {
    localPomos.value = pomoLimits.max;
  }
  emit('increasePomos', localPomos.value);
}

function decreasePomos() {
  if (props.chore.estimated > pomoLimits.min) {
    localPomos.value--;
  }
  emit('decreasePomos', localPomos.value);
}
</script>

<template>
  <div class="timers">
    <!-- Number -->
    <input
      type="number"
      class="estimated-timers"
      :min="pomoLimits.min"
      :max="pomoLimits.max"
      :value="localPomos"
      @input="e => localPomos = ((e.target) as HTMLInputElement).value"
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
