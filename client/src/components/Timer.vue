<template>
  <div id="timer-container">
    <!-- Progress -->
    <div id="red-line"></div>
    <!-- Time -->
    <div>
      <h1 id="timer-count">25:00</h1>
      <button id="start-timer-btn">Start</button>
    </div>
  </div>
</template>

<style lang="scss">
#red-line {
  width: 40%;
  height: 15px;
  border-radius: 18px;
  background-color: var(--vivid-red);
}

#timer-count {
  font-size: 8rem;
}

#start-timer-btn {
  padding: 1rem;
  width: 40%;
  border-radius: 18px;
  font-size: 120%;
  font-family: sans-serif;
  background-color: var(--vivid-red);
  color: white;
  font-weight: 900;
  border: none;
  margin-top: 1rem;

  &:hover {
    cursor: pointer;
  }
}
</style>