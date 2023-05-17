import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useModalStore = defineStore('modal', () => {
  const isOpened = ref(false);
  const open = () => { isOpened.value = true };
  const close = () => { isOpened.value = false };
  const toggle = () => { isOpened.value = !isOpened.value };

  return { isOpened, open, close, toggle }
});
