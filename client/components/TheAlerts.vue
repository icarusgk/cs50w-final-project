<script setup>
const alerts = useAlertStore();
</script>
<template>
  <div class="fixed overflow-hidden z-15 lg:z-5 top-[5.5rem] right-[-10px]">
    <TransitionGroup name="alerts">
      <div
        v-for="alert in alerts.items"
        :key="alert.id"
        :class="`w-[150px] p-3 lg:w-[250px] mb-2 lg:py-4 lg:px-6 rounded-lg ${alert.style}`"
      >
        <div class="flex">
          <div class="flex justify-center items-center mr-2.5 pointer">
            <div class="i-fluent:checkmark-circle-32-filled scale-130 bg-white" @click="alerts.remove(alert.id)" />
          </div>
          <div class="text-[0.9rem] lg:text-base text-white">{{ alert.message }}</div>
        </div>
      </div>
    </TransitionGroup>
  </div>
</template>
<style scoped>
.alerts-enter-active,
.alerts-leave-active {
  transition: all 0.5s cubic-bezier(0.6, 0.2, 0.4, 1);
}
.alerts-enter-from,
.alerts-leave-to {
  opacity: 0;
  transform: translateX(1rem);
}

.error {
  background-color: rgb(249, 71, 31);
}

.success {
  background-color: rgb(52, 169, 94);
}

.info {
  background-color: rgb(0, 140, 255);
}
</style>
