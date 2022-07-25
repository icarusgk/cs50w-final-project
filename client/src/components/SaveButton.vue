<template>
  <button
    class="close-modal-button"
  >Save!
</button>

</template>

<style scoped lang="scss">
.close-modal-button {
  background-color: var(--vivid-red);
  color: var(--white);

  font: {
    weight: 900;
    family: sans-serif;
  }

  width: 100%;
  border: none;
  border-radius: 10px;
  margin-top: 1rem;
  padding: 0.8rem 0.8rem;

  &:hover {
    cursor: pointer;
  }
}
</style>