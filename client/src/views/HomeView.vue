<script setup lang="ts">
import { useModalStore } from '@/stores/modal'
import LightingIcon from '@/components/icons/LightingIcon.vue'
import NewTaskButton from '@/components/buttons/new-buttons/NewTaskButton.vue'
import Timer from '@/components/Timer.vue'
import Projects from '@/components/Projects.vue'
import Tasks from '@/components/Tasks.vue'
import NewProjectButton from '@/components/buttons/new-buttons/NewProjectButton.vue'

</script>
<template>
  <div id="home">
    <!-- Third box -->
    <div id="timer-and-tasks">
      <!-- Timer -->
      <div id="main-timer">
        <Timer />
      </div>
    </div>
    
    <!-- Add Tasks -->
    <div id="main-tasks-container">
      <!-- Buttons -->
      <div id="task-btn-container">
        <!-- New Task -->
        <NewTaskButton />
        <!-- New Project -->
        <NewProjectButton />
      </div>
      <!-- Projects -->
      <Projects />
      <!-- Tasks -->
      <Tasks />
    </div>
  </div>
</template>

<style lang="scss">
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
}

#task-btn-container {
  display: flex;
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
