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
    if (chore.projectPagination.count > 1 && newProjectPage !== oldProjectPage) {
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
  <div class="body">
    <div class="menu-and-content" :class="{ blur: modal.isOpened }">
      <TheUpperMenu class="upper-menu" />
      <RouterView @vnodeUpdated="modal.close()"></RouterView>
    </div>
    <TheAlerts />
  </div>
</template>

<style lang="scss">
/* variables */
@import "./assets/base.css";

/* Popper theme */
@import "./assets/popper-theme.css";

/* Fonts */
@import url('https://fonts.googleapis.com/css2?family=Lexend:wght@100;200;300;400;500;600;700;800;900&display=swap');

* {
  font-family: "Lexend", sans-serif;
}

/* Chrome, Safari, Edge, Opera */
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  appearance: none;
  -webkit-appearance: none;
  margin: 0;
}

/* Firefox */
input[type="number"] {
  appearance: textfield;
  -moz-appearance: textfield;
}

/* Resets */
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
  transition: filter 0.15s ease-out;
}

html {
  background-color: #212121;
}

.blur {
  filter: blur(14px);
  pointer-events: none;
}

.body {
  display: flex;
  margin-left: 130px;
  position: relative;

  .menu-and-content {
    width: 100%;
    display: flex;
    flex-direction: column;

    .upper-menu {
      padding: 1.5rem 3rem 0 3rem;
      color: white;
    }
  }
}

@media (max-width: 768px) {
  .body {
    margin-left: 0;
    margin-bottom: 140px;

    .menu-and-content {
      padding: 0.5rem;
      .upper-menu {
        padding: 0;
      }
    }
  }

  .blur {
    filter: blur(60px);
  }

  * {
    touch-action: manipulation;
  }
}
</style>
