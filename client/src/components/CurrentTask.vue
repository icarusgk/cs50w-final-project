<script setup lang="ts">
const task = ref();
const auth = useAuthStore();
const chore = useChoreStore();
const userTaskId = computed(() => auth.user?.current_task_id);
const open = ref(false);

async function getTask(id: any) {
  const response = await axios.get(`tasks/${id}/`);
  task.value = response?.data;
}

watchEffect(() => {
  if (userTaskId.value !== 0 && auth.user) {
    getTask(userTaskId.value);
  }
});

// The modal blur
watch(open, () => {
  useModalStore().toggle();
});
</script>

<template>
  <Transition name="slide">
    <div v-if="userTaskId !== 0 && auth.user" style="margin-top: 1rem">
      <div class="flex items-center gap-4">
        <div @click="open = true" class="w-84 bg-[#333] text-white p-4 rounded-lg font-semibold depth pointer active:shadow-none active:shadow-dark-gray">
          <div class="flex items-center">
            <div class="i-fluent-info-12-regular scale-150 ml-3" />
            <span class="ml-2">Working on task: {{ task?.title }}</span>
          </div>
        </div>
        <Popper hover>
          <CloseIcon @click="chore.changeCurrentTask(0)" class="pointer" />
          <template #content> Remove current task </template>
        </Popper>
      </div>
      <TheTaskModal :open="open" :task="task" @exit:modal="open = false" />
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
