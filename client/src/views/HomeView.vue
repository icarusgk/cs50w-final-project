<script setup lang="ts">
import LightingIcon from '@/components/icons/LightingIcon.vue'
import TaskButton from '@/components/TaskButton.vue'
import Timer from '@/components/Timer.vue'
import Projects from '@/components/Projects.vue'
import SingleTasks from '@/components/SingleTasks.vue'
import UpperMenu from '@/components/UpperMenu.vue'
import NewProjectModal from '../components/NewProjectModal.vue'
import NewTaskModal from '../components/NewTaskModal.vue'
</script>
<template>
  <div id="home">
    <!-- Upper Icons -->
    <UpperMenu />
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

          <TaskButton>
            <template #type>
              Add new project
            </template>
            <template #modal-content>
              <NewProjectModal />
            </template>
          </TaskButton>

          <TaskButton>
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
  padding: 2rem 4rem;
  width: 100%;
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
