<script setup lang="ts">
import LightingIcon from '@/components/icons/LightingIcon.vue'
import TaskButton from '@/components/TaskButton.vue'
import Timer from '@/components/Timer.vue'
import Projects from '@/components/Projects.vue'
import SingleTasks from '@/components/SingleTasks.vue'
import NewProjectModal from '../components/NewProjectModal.vue'
import NewTaskModal from '../components/NewTaskModal.vue'
import { ref } from 'vue'

const isBlurred = ref(false)

</script>
<template>
  <div id="home" :class="{ blur: isBlurred }">
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

          <TaskButton @blur="blur => isBlurred = blur">
            <template #type>
              Add new project
            </template>
            <template #modal-content>
              <NewProjectModal />
            </template>
          </TaskButton>

          <TaskButton @blur="blur => isBlurred = blur">
            <template #type>
              Add new task
            </template>
            <template #modal-content>
              <NewTaskModal />
            </template>
          </TaskButton>

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
