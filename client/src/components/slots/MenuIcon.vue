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
  padding: 30px 20px;
  border-radius: 10px;
  color: white;
  transition: background-color 0.1s ease-in-out;
}


@media (max-width: 768px) {
  .item {
    transform: scale(0.5);
    flex-direction: row;
    padding: 0;
    margin: 0;
  }
  .title {
    font-size: 2rem;
    margin-left: 1rem;
  }
}

</style>