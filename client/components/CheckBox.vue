<script setup lang="ts">
defineProps<{
  checked?: boolean
  label: string
  id: string
}>();

defineEmits<{
  (e: 'change', checked: boolean): void
}>();
</script>

<template>
  <div class="flex gap-2 my-2 items-center">
    <input :checked="checked" @change="$emit('change', !checked)" type="checkbox" :id="id">
    <label :for="id" class="toggleSwitch"></label>
    <span class="text-lg font-medium">{{ label }}</span>
  </div>
</template>

<style scoped>
/* To hide the checkbox */
input[type="checkbox"] {
  display: none;
}

.toggleSwitch {
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  width: 50px;
  height: 30px;
  background-color: rgb(115, 115, 115);
  border-radius: 20px;
  cursor: pointer;
  transition-duration: .2s;
}

.toggleSwitch::after {
  content: "";
  position: absolute;
  height: 20px;
  width: 20px;
  left: 5px;
  background-color: transparent;
  border-radius: 50%;
  transition-duration: .2s;
  box-shadow: 5px 2px 7px rgba(8, 8, 8, 0.26);
  border: 5px solid white;
}

input[type="checkbox"]:checked+.toggleSwitch::after {
  transform: translateX(100%);
  transition-duration: .2s;
  background-color: white;
}
/* Switch background change */
input[type="checkbox"]:checked+.toggleSwitch {
  background-color: var(--vivid-red);
  transition-duration: .2s;
}
</style>
