<script setup>
import { useAlertStore } from '@/stores/alerts';
import DoneIcon from './icons/DoneIcon.vue';
const alerts = useAlertStore();
</script>
<template>
  <div class="alert-container">
    <TransitionGroup name="alerts">
      <div
        v-for="alert in alerts.items"
        :key="alert.id"
        :class="`alert ${alert.style}`"
      >
        <div class="flex">
          <div class="close-icon">
            <div @click="alerts.remove(alert.id)">
              <DoneIcon />
            </div>
          </div>
          <div class="message">{{ alert.message }}</div>
        </div>
      </div>
    </TransitionGroup>
  </div>
</template>
<style scoped lang="scss">
.alert-container {
  position: fixed;
  overflow: hidden;
  z-index: 5;
  top: 5.5rem;
  right: -10px;
}

.alert {
  width: 250px;
  margin-bottom: 0.5rem;
  padding: 1rem 1.5rem;
  border-radius: 10px;
}

.close-icon {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-right: 10px;

  &:hover, &:focus {
    cursor: pointer;
  }
}

.message {
  color: white;
}

.error {
  background-color: rgb(249, 71, 31);
}

.flex {
  display: flex;
}


.success {
  background-color: rgb(52, 169, 94);
}

.info {
  background-color: rgb(0, 140, 255);
}
.alerts-enter-active,
.alerts-leave-active {
  transition: all 0.5s cubic-bezier(0.6, 0.2, 0.4, 1);
}
.alerts-enter-from,
.alerts-leave-to {
  opacity: 0;
  transform: translateX(1rem);
}
</style>
  