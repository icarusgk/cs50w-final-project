<template>
  <div id="projects-container">
    <!-- Icon -->
    <div class="task-title-icon">
      <slot name="icon"></slot>
    </div>
    <!-- Title -->
    <div>
      <slot name="type"></slot>
    </div>
  </div>
</template>

<style>
#projects-container {
  display: flex;
  align-items: center;
  padding: 1rem 0;
}

.task-title-icon {
  margin-right: 1rem;
}
</style>
