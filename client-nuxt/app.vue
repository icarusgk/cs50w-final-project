<script setup lang="ts">
import '@unocss/reset/tailwind.css';
const auth = useAuthStore();
const chore = useChoreStore();
const modal = useModalStore();
const timer = useTimerStore();
const page = usePageStore();

// Close any previously opened modal
modal.close();

auth.getUser();

useHead({ title: 'Pomo.do' })

if (auth.isAuthed) {
  watch(
    [
      () => page.projectPagination.page,
      () => page.taskPagination.page,
      () => page.projectPagination.page_size,
      () => page.taskPagination.page_size,
    ],
    ([newProjectPage, newTaskPage], [oldProjectPage, oldTaskPage]) => {
      if (
        page.projectPagination.count > 1 &&
        newProjectPage !== oldProjectPage
      ) {
        chore.fetchProjects();
      }
      if (page.taskPagination.count > 1 && newTaskPage !== oldTaskPage) {
        chore.fetchTasks();
      }
    }
  );
  chore.fetchModes();
  chore.fetchStats();
}
window.onbeforeunload = () => (timer.isRunning ? true : null)
</script>

<template>
  <NuxtLayout>
    <NuxtPage />
  </NuxtLayout>
</template>

<style>
/* variables */
@import './assets/base.css';
/* Popper theme */
@import './assets/popper-theme.css';

/* Lexend font */
@import url('https://fonts.googleapis.com/css2?family=Lexend:wght@100;200;300;400;500;600;700;800;900&display=swap');

* {
  transition: filter 0.15s ease-out;
}
</style>
