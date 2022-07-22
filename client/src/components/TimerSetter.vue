<script setup lang="ts">
import { ref } from 'vue'

const props = defineProps(['subtask'])

const pomoLimits = ref({ min: 1, max: 99 })

function decreasePomos() {
  if (props.subtask.estimated > pomoLimits.value.min) props.subtask.estimated--
}

function increasePomos() {
  props.subtask.estimated < pomoLimits.value.max
    ? props.subtask.estimated++
    : props.subtask.estimated = pomoLimits.value.max
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
      v-model="subtask.estimated" />
    <button @click="decreasePomos" class="minus-icon pomo-icon">-</button>
    <button @click="increasePomos" class="pomo-icon">+</button>
  </div>
</template>


<style scoped lang="scss">
.timers {
  display: flex;
  justify-content: flex-end;

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
    
    &:hover, &:focus {
      cursor: pointer;
    }
  }
}
</style>