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
    <div>
      <div>
        <!-- Icon -->
        <!-- Title -->
        <h1>Pomodoro Timer</h1>
      </div>
    </div>
    <!-- Third box -->
    <div>
      <!-- Timer -->
      <div>
        <!-- Progress -->
        <div></div>
        <!-- Time -->
        <div>
          <h1>25:00</h1>
          <button>Start</button>
        </div>
      </div>
      <!-- Add Tasks -->
      <div>
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

<style>
#home {
  color: white;
  display: flex;
  flex-direction: column;
}

#icons ul li {
  display: inline-block;
}
</style>
