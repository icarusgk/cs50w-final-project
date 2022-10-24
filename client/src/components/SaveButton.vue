<template>
  <button class="close-modal-button">
    Save!
  </button>
</template>

<style scoped lang="scss">
.close-modal-button {
  $vivid-red: #ed4747;
  background-color: $vivid-red;
  color: var(--white);
  box-shadow: 0 3px 0 1px lighten($vivid-red, 10%);
  transition: box-shadow 0.2s cubic-bezier(0.075, 0.82, 0.165, 1);

  font: {
    weight: 700;
  }

  width: 100%;
  border: none;
  border-radius: 10px;
  margin-top: 1rem;
  padding: 0.8rem 0.8rem;

  &:hover,
  &:focus,
  &:active {
    cursor: pointer;
  }

  &:active {
    box-shadow: 0 0 $vivid-red;
  }
}
</style>
