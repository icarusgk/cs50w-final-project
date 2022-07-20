<script setup lang="ts">
import EstimatedIcon from './icons/EstimatedIcon.vue';
import AddPomoIcon from './icons/AddPomoIcon.vue';
import MinusPomoIcon from './icons/MinusPomoIcon.vue';
const props = defineProps(['subtask'])
</script>


<template>
  <div class="timers">
    <!-- Number -->
    <input type="number" class="estimated-timers" :value="subtask.estimated" />
    <MinusPomoIcon @click="$emit('subtract')" class="minus-icon pomo-icon" />
    <AddPomoIcon @click="$emit('add')" class="pomo-icon" />
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
    &:hover, &:focus {
      cursor: pointer;
    }
  }
}
</style>