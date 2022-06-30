<script setup lang="ts">
import LightingIcon from '../components/icons/LightingIcon.vue'
</script>
<template>
  <div id="home">
    <!-- Upper Icons -->
    <div id="icons">
      <ul>
        <!-- Four icons -->
        <!-- Streaks -->
        <li>Streaks</li>
        <!-- Dark Theme -->
        <li>Theme</li>
        <!-- User -->
        <li>User</li>
        <!-- Settings -->
        <li>Settings</li>
      </ul>
    </div>
    <!-- Pomo Title -->
    <div id="pomodoro-container">
      <!-- Icon -->
      <LightingIcon />
      <!-- Title -->
      <h1>Pomodoro Timer</h1>
    </div>
    <!-- Third box -->
    <div id="third-box">
      <!-- Timer -->
      <div id="timer-container">
        <!-- Progress -->
        <div id="red-line"></div>
        <!-- Time -->
        <div>
          <h1 id="timer-count">25:00</h1>
          <button id="start-timer-btn">Start</button>
        </div>
      </div>
      <!-- Add Tasks -->
      <div id="tasks-container">
        <!-- Buttons -->
        <div>
          <button>Add new project</button>
          <button>Add new task</button>
        </div>
        <!-- Projects -->
        <div>
          <!-- Title -->
          <div>
            <!-- Icon -->
            <!-- Title -->
            <h3>Projects</h3>
            <!-- List of projects -->
            <div>
              <div>
                <!-- Checkbox -->
                <!-- Name -->
                <h2>Learn Vue.js</h2>
              </div>
              <div>
                <!-- Checkbox -->
                <!-- Name -->
                <h2>Study Rails Basics</h2>
              </div>
            </div>
          </div>
          <div>
            <!-- Icon -->
          </div>
        </div>
        <!-- Tasks -->
        <div>
          <div>
            <!-- Icon -->
            <!-- Title -->
            <h3>Tasks</h3>
            <!-- List of tasks -->
            <div>
              <div>
                <!-- Checkbox -->
                <!-- Name -->
                <h2>Learn Refs from Vue.js</h2>
              </div>
              <div>
                <!-- Checkbox -->
                <!-- Name -->
                <h2>Learn Controller from Rails</h2>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss">
#home {
  color: white;
  display: flex;
  flex-direction: column;
  padding: 4rem;
  width: 100%;
}

#icons {
  ul {
    text-align: right;
    li {
      display: inline-block;
    }
  }
}

#third-box {
  display: flex;
  flex-direction: row;
  margin-top: 4rem;
}

#pomodoro-container {
  display: flex;
  align-items: center;
  
}

#red-line {
  width: 40%;
  height: 15px;
  border-radius: 18px;
  background-color: var(--vivid-red);
}

#timer-container {
  width: 50%;
  margin: 2rem 0 0 1rem;
}

#tasks-container {
  width: 50%
}

#timer-count {
  font-size: 8rem;
}

#start-timer-btn {
  padding: 1rem;
  width: 20%;
  border-radius: 18px;
  font-size: 120%;
  font-family: sans-serif;
  background-color: var(--vivid-red);
  color: white;
  font-weight: 900;
  border: none;
  margin-top: 1rem;
}

</style>
