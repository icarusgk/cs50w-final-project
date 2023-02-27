<script setup lang="ts">
const auth = useAuthStore();
const chore = useChoreStore();
const modal = useModalStore();

// Close any previously opened modal
modal.close();

auth.getUser();

if (auth.isAuthed) {
  chore.fetchProjects();
  chore.fetchTasks();
}

watch(
  [
    () => chore.projectPagination.page,
    () => chore.taskPagination.page,
    () => chore.projectPagination.page_size,
    () => chore.taskPagination.page_size,
  ],
  ([newProjectPage, newTaskPage], [oldProjectPage, oldTaskPage]) => {
    if (
      chore.projectPagination.count > 1 &&
      newProjectPage !== oldProjectPage
    ) {
      chore.fetchProjects();
    }
    if (chore.taskPagination.count > 1 && newTaskPage !== oldTaskPage) {
      chore.fetchTasks();
    }
  }
);
</script>

<template>
  <TheSidebar />
  <div class="flex ml-0 mb-[140px] lg:ml-[130px] lg:mb-0 relative">
    <div :class="[{ '<sm:p-4 filter blur-md pointer-events-none duration-150 ease-out': modal.isOpened }, 'w-full flex flex-col']">
      <TheUpperMenu class="pt-6 py-12 pb-0" />
      <RouterView @vnodeUpdated="modal.close()"></RouterView>
    </div>
    <TheAlerts />
  </div>
</template>

<style>
/* variables */
@import './assets/base.css';

/* Popper theme */
@import './assets/popper-theme.css';

/* Lexend font */
@import url('https://fonts.googleapis.com/css2?family=Lexend:wght@100;200;300;400;500;600;700;800;900&display=swap');
</style>
