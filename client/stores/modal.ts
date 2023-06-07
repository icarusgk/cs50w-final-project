import type { ITask } from "~/types";

export const useModalStore = defineStore('modal', () => {
  const chore = useChoreStore();
  const isOpened = ref(false);
  const isOpenedNew = ref(false);
  const content = ref<ITask>(chore.tasks[0]);
  
  const open = () => { isOpened.value = true };
  const close = () => { isOpened.value = false };
  const toggle = () => { isOpened.value = !isOpened.value };

  return { isOpened, isOpenedNew, content, open, close, toggle }
});
