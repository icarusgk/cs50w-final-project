<script setup lang="ts">
import LightingIcon from '@/components/icons/LightingIcon.vue'
import NewTaskButton from '@/components/NewTaskButton.vue'
import Timer from '@/components/Timer.vue'
import Projects from '@/components/Projects.vue'
import SingleTasks from '@/components/SingleTasks.vue'
import { useModalStore } from '@/stores/modal'
import NewProjectButton from '../components/NewProjectButton.vue'

const modal = useModalStore()
modal.close()

</script>
<template>
  <div id="home" :class="{ blur: modal.isOpened }">
    <!-- Pomo Title -->
    <div id="pomodoro-title-container">
      <!-- Icon -->
      <LightingIcon />
      <!-- Title -->
      <h1>Pomodoro Timer</h1>
    </div>
    <!-- Third box -->
    <div id="timer-and-tasks">
      <!-- Timer -->
      <div id="main-timer">
        <Timer />
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
        <SingleTasks />
      </div>
    </div>
  </div>
</template>

<style lang="scss">
#home {
  color: white;
  display: flex;
  flex-direction: column;
  padding: 0 4rem 0 4rem;
  width: 100%;
  transition: filter 0.1s ease-out;
}

.blur {
  filter: blur(14px);
  pointer-events: none;
}

#pomodoro-title-container {
  display: flex;
  align-items: center;
}

#timer-and-tasks {
  display: flex;
  flex-direction: row;
}

#main-timer {
  width: 50%;
  margin: 4rem 0 0 1rem;
} 

#main-tasks-container {
  width: 40%
}

#task-btn-container {
  display: flex;  
}

</style>
