<template>
  <div id="projects-container">
    <!-- Icon -->
    <div class="task-title-icon">
      <slot name="icon"></slot>
    </div>
    <!-- Title -->
    <div class="title">
      <slot name="type"></slot>
      <div>
        <slot name="count"></slot>
      </div>
    </div>
    
  </div>
</template>

<style scoped lang="scss">
#projects-container {
  display: flex;
  align-items: center;
  padding: 1rem 0;
  width: 100%;
  .task-title-icon {
    margin-right: 1rem;
  }

  .title {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 85%;
  }
}

@media (max-width: 420px) {
  #projects-container {
    .title {
      font-size: 0.9rem;
    }
  }
}
</style>
