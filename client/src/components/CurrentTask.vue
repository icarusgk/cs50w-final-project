<script setup lang="ts">
import { changeCurrentTask } from '@/utils/taskFns';
const auth = useAuthStore();
const task = ref();
const open = ref(false);

watchEffect(async () => {
  const curId = auth.user?.current_task_id;
  if (curId !== 0 && auth.user) {
    const response = await axios.get(`tasks/${curId}/`);
    task.value = response?.data;
  }
});
// The modal blur
watch(open, () => {
  useModalStore().toggle();
});
</script>

<template>
  <Transition name="slide">
    <div v-if="auth.user?.current_task_id !== 0 && auth.user && task" style="margin-top: 1rem">
      <div class="flex items-center gap-4">
        <div @click="open = true" class="w-84 bg-[#333] text-white p-4 rounded-lg font-semibold depth pointer active:shadow-none active:shadow-dark-gray">
          <div class="flex items-center">
            <div class="i-fluent-info-12-regular scale-150 ml-3" />
            <span class="ml-2">Working on task: {{ task?.title }}</span>
          </div>
        </div>
        <Popper hover>
          <div @click="changeCurrentTask(0)" class="pointer i-fluent-dismiss-circle-32-filled scale-220" />
          <template #content> Remove current task </template>
        </Popper>
      </div>
      <TheTaskModal :open="open" :task="task" @exit:modal="open = false" :key="task.id" />
    </div>
  </Transition>
</template>

<style scoped>
.slide-enter-active,
.slide-leave-active {
  transition: opacity 0.3s ease-in-out;
}

.slide-enter-from,
.slide-leave-to {
  opacity: 0;
}

:deep(.popper) {
  padding: 1rem;
  border-radius: 10px;
  color: #fff;
  font-weight: bold;
}
</style>
