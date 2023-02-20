<template>
  <div class="item">
    <i>
      <slot name="icon"></slot>
    </i>
    <div class="title">
      <h3>
        <slot name="heading"></slot>
      </h3>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.item {
  display: flex;
  align-items: center;
  width: 100%;
  color: white;
  padding: 1rem;
  padding-left: 1.7rem;
  // This transition is being applied to the background color
  transition: all 0.2s ease-in-out;
  position: relative;

  .title {
    opacity: 0;
    position: absolute;
    visibility: hidden;
    transition: opacity 0.4s, visibility 0s ease-in-out 0.1s;
    left: 4rem;
  }

  &:hover {
    background-color: var(--vivid-red);
    border-radius: 0 10px 10px 0;
    width: 180%;

    .title {
      opacity: 1;
      visibility: visible;
      transition-delay: 0s;
    }
  }
}

@media (max-width: 768px) {
  .item {
    // reset the things made on desktop
    transition: none;
    flex-direction: row;

    .title {
      opacity: 1;
      position: static;
      visibility: visible;
      transition: none;
      margin-left: 0.5rem;
    }
    
    &:hover {
      width: 100%;
    }
  }
}
</style>
