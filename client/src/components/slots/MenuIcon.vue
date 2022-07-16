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
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 30px;
  border-radius: 10px;
  color: white;
  transition: background-color 0.1s ease-in-out;

  &:hover {
    background-color: var(--vivid-red);
    cursor: pointer;
  }
}


</style>