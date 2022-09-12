<script setup lang="ts">
defineProps<{
  pages: number;
  page: number;
}>();
</script>

<template>
  <div class="container">
    <div @click="$emit('prev')" class="paginate-btn">Prev</div>
    <div
      v-for="(_, i) in pages"
      @click="$emit('setPage', i + 1)"
      :class="{ active: i + 1 === page }"
      class="paginate-btn"
    >
      {{ i + 1 }}
    </div>
    <div @click="$emit('next')" class="paginate-btn">Next</div>
  </div>
</template>

<style scoped lang="scss">
.container {
  display: flex;
  justify-content: center;
  margin-top: 1rem;

  .active {
    background-color: white !important;
    color: rgb(67, 67, 67) !important;
  }

  .paginate-btn {
    padding: 0.5rem 1rem;
    background-color: rgb(67, 67, 67);
    color: white;
    margin-left: 0.75rem;
    border-radius: 8px;

    &:hover,
    &:focus {
      cursor: pointer;
    }
  }
}
</style>
