<script setup lang="ts">
const auth = useAuthStore();
</script>
<template>
  <div id="home">
    <!-- Third box -->
    <div id="timer-and-tasks">
      <!-- Timer -->
      <div id="main-timer">
        <TheTimer />
      </div>
    </div>
    <!-- Add Tasks -->
    <div id="main-tasks-container">
      <!-- Buttons -->
      <div id="task-btn-container" :class="{ opaque: !auth.isAuthed }">
        <!-- New Task -->
        <NewTaskButton />
        <!-- New Project -->
        <NewProjectButton />
      </div>
      <div id="message" v-if="!auth.isAuthed">
        <UnauthedLogin> To add tasks and projects </UnauthedLogin>
      </div>
      <!-- Projects and Tasks if user is authed -->
      <div v-if="auth.isAuthed">
        <AppProjects />
        <AppTasks />
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
#home {
  color: white;
  display: flex;
  flex-direction: row;
  justify-content: center;

  padding: 0 4rem 0 4rem;
  width: 100%;
}

#pomodoro-title-container {
  display: flex;
  align-items: center;
}

#timer-and-tasks {
  display: flex;
  flex-direction: row;
  width: 550px;
  margin-top: 3rem;
}

#main-tasks-container {
  width: 500px;

  #message {
    width: 80%;
    margin-top: 8rem;
  }
}

#task-btn-container {
  display: flex;
}

.opaque {
  opacity: 0.1;
}

@media (max-width: 1160px) {
  #home {
    flex-direction: column;
  }

  #main-tasks-container {
    margin: 2rem 0 2rem 0;
    width: 600px;
  }
}

@media (max-width: 768px) {
  #home {
    padding: 0 0 0 1rem;
    align-items: unset;
    flex-direction: column;
  }
  #timer-and-tasks {
    flex-wrap: wrap;
    width: 110px;
  }

  #main-timer {
    margin-left: 0;
  }

  #title {
    font-size: 1.5rem;
  }

  #main-tasks-container {
    margin: 0;
    width: 85vw;

    #task-btn-container {
      margin: 2rem 0 2rem 0;
    }
  }
}
</style>
