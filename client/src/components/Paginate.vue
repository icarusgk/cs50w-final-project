<script setup lang="ts">
const props = defineProps<{
  pages: number;
  page: number;
  added: number;
}>();

// Total of pages to display
// Example:
// ... 2, 3, 4 ...
// ... 3, 4, 5 ...
// ... 4, 5, 6 ...
const TOTAL_PAGES = 3;

const emit = defineEmits(['prev', 'next', 'setPage', 'setAdded']);

function increaseCurrentPage(): void {
  if (props.page < props.pages) {
    emit('setPage', props.page + 1);
  }

  if (props.page >= (TOTAL_PAGES + 1) && props.page < props.pages - (TOTAL_PAGES - 1)) {
    nextMoveBy(1);
  }
}

function setCurrentPage(newPage: number): void {
  if (newPage <= props.pages || newPage >= 1) {
    emit('setPage', newPage);
  }

  if (newPage <= 4) {
    if (newPage === 1 || newPage === 3) emit('setAdded', 1);
    if (newPage === 4) emit('setAdded', 2);
  } else {
    if (newPage > (TOTAL_PAGES + 1) && newPage > props.page && newPage !== props.pages) {
      nextMoveBy(1);
    }
    if (newPage < props.page) {
      if (newPage === props.pages - (TOTAL_PAGES - 1)) {
        emit('setAdded', props.added)
      } else {
        prevMoveBy(1);
      }
    }
  }

  if (newPage === props.pages - 1) {
    emit('setAdded', props.pages - (TOTAL_PAGES + 1));
  }
}

function decreaseCurrentPage(): void {
  if (props.page > 1) {
    emit('setPage', props.page - 1);
  }

  if (props.page <= props.pages - TOTAL_PAGES) {
    prevMoveBy(1);
  }
}

function prevMoveBy(decreasedBy: number): void {
  // Edge case when '...' is pressed when currentPage is <= 3
  // Resets added back to 1

  // Reset range
  if (props.page <= 4) {
    emit('setAdded', 1);
    return;
  }

  // By 3
  if (decreasedBy > 1) {
    props.added <= TOTAL_PAGES
      ? emit('setAdded', 1)
      : emit('setAdded', props.added - decreasedBy);

    emit('setPage', props.added - 1);
  }

  // By 1
  if (decreasedBy === 1) {
    emit('setAdded', props.added - 1);
  }
}

function nextMoveBy(increasedBy: number): void {
  // By 3
  if (increasedBy > 1) {
    if (props.page >= props.pages - (TOTAL_PAGES + 1)) {
      // Move the range to the final
      emit('setPage', props.pages);
      emit('setAdded', props.pages - (TOTAL_PAGES + 1));
    }
    
    // If added is less than TOTAL_PAGES - 2 move by n
    if (props.added < props.pages - (TOTAL_PAGES + 2)) {
      emit('setAdded', props.added + increasedBy - 1);
      emit('setPage', props.added + (TOTAL_PAGES + 1));
    } else {
      // For short pages
      emit('setAdded', props.pages - (TOTAL_PAGES + 1));
      emit('setPage', props.pages - (TOTAL_PAGES - 1));
    }
  }

  // By 1
  if (increasedBy === 1 && props.page <= props.pages - (TOTAL_PAGES - 1)) {
    emit('setAdded', props.added + 1);
  }
}
</script>

<template>
  <div class="container" v-if="props.pages > 1">
    <!-- Previous Button -->
    <div
      @click="
        $emit('prev');
        decreaseCurrentPage();
      "
      class="paginate-btn action-btn"
    >
      Prev
    </div>
    <!-- Container for more than 5 pages -->
    <div v-if="props.pages > 5" class="flex">
      <!-- Single number 1 -->
      <div
        @click="setCurrentPage(1)"
        :class="{ active: props.page === 1, 'paginate-btn': true }"
      >
        1
      </div>
      <!-- Prev ... Dots -->
      <div v-if="props.added > 1" @click="prevMoveBy(TOTAL_PAGES)" class="paginate-btn">
        ...
      </div>
      <!-- 3 pages range -->
      <div
        v-for="page in TOTAL_PAGES"
        :class="{ active: page + props.added === props.page, 'paginate-btn': true }"
        @click="setCurrentPage(page + props.added)"
      >
        {{ page + props.added }}
      </div>
      <!-- Next ... Dots -->
      <div
        v-if="props.added + (TOTAL_PAGES + 1) !== props.pages"
        @click="nextMoveBy(TOTAL_PAGES)"
        class="paginate-btn"
      >
        ...
      </div>
      <!-- Last page -->
      <div
        @click="$emit('setPage', props.pages), $emit('setAdded', props.pages - (TOTAL_PAGES + 1))"
        :class="{ active: props.page === props.pages, 'paginate-btn': true }"
      >
        {{ props.pages }}
      </div>
    </div>
    <!-- Normal range less than 5, when there are not other elements -->
    <div
      v-else
      v-for="(_, i) in props.pages"
      @click="setCurrentPage(i + 1)"
      :class="{ active: i + 1 === props.page }"
      class="paginate-btn"
    >
      {{ i + 1 }}
    </div>
    <!-- Next Button -->
    <div
      @click="
        $emit('next');
        increaseCurrentPage();
      "
      class="paginate-btn action-btn"
    >
      Next
    </div>
  </div>
</template>

<style scoped lang="scss">
.container {
  display: flex;
  justify-content: center;
  margin-top: 1rem;

  .flex {
    display: flex;
  }

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
    transition: background-color 0.2s ease-in-out;

    &:hover,
    &:focus,
    &:active {
      cursor: pointer;
    }
  }

  .action-btn {
    transition: all 0.1s ease-in-out;
    &:hover,
    &:active,
    &:active {
      background-color: var(--white);
      color: var(--black);
    }
  }

  @media (max-width: 480px) {
    .paginate-btn {
      padding: 0.25rem 0.55rem;
    }
  }
}
</style>
