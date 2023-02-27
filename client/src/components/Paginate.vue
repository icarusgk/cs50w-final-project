<script setup lang="ts">
const props = defineProps<{
  pages: number;
  page: number;
  added: number;
}>();

const emit = defineEmits<{
  (e: 'prev'): void
  (e: 'next'): void
  (e: 'set:page', page: number): void
  (e: 'set:added', added: number): void
}>();

// Total of pages to display
// Example:
// ... 2, 3, 4 ...
// ... 3, 4, 5 ...
// ... 4, 5, 6 ...
const TOTAL_PAGES = 3;

function increaseCurrentPage(): void {
  if (props.page < props.pages) {
    emit('set:page', props.page + 1);
  }

  if (
    props.page >= TOTAL_PAGES + 1 &&
    props.page < props.pages - (TOTAL_PAGES - 1)
  ) {
    nextMoveBy(1);
  }
}

function setCurrentPage(newPage: number): void {
  if (newPage <= props.pages || newPage >= 1) {
    emit('set:page', newPage);
  }

  if (newPage <= 4) {
    if (newPage === 1 || newPage === 3) emit('set:added', 1);
    if (newPage === 4) emit('set:added', 2);
  } else {
    if (
      newPage > TOTAL_PAGES + 1 &&
      newPage > props.page &&
      newPage !== props.pages
    ) {
      nextMoveBy(1);
    }
    if (newPage < props.page) {
      if (newPage === props.pages - (TOTAL_PAGES - 1)) {
        emit('set:added', props.added);
      } else {
        prevMoveBy(1);
      }
    }
  }

  if (newPage === props.pages - 1) {
    emit('set:added', props.pages - (TOTAL_PAGES + 1));
  }
}

function decreaseCurrentPage(): void {
  if (props.page > 1) {
    emit('set:page', props.page - 1);
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
    emit('set:added', 1);
    return;
  }

  // By 3
  if (decreasedBy > 1) {
    props.added <= TOTAL_PAGES
      ? emit('set:added', 1)
      : emit('set:added', props.added - decreasedBy);

    emit('set:page', props.added - 1);
  }

  // By 1
  if (decreasedBy === 1) {
    emit('set:added', props.added - 1);
  }
}

function nextMoveBy(increasedBy: number): void {
  // By 3
  if (increasedBy > 1) {
    if (props.page >= props.pages - (TOTAL_PAGES + 1)) {
      // Move the range to the final
      emit('set:page', props.pages);
      emit('set:added', props.pages - (TOTAL_PAGES + 1));
    }

    // If added is less than TOTAL_PAGES - 2 move by n
    if (props.added < props.pages - (TOTAL_PAGES + 2)) {
      emit('set:added', props.added + increasedBy - 1);
      emit('set:page', props.added + (TOTAL_PAGES + 1));
    } else {
      // For short pages
      emit('set:added', props.pages - (TOTAL_PAGES + 1));
      emit('set:page', props.pages - (TOTAL_PAGES - 1));
    }
  }

  // By 1
  if (increasedBy === 1 && props.page <= props.pages - (TOTAL_PAGES - 1)) {
    emit('set:added', props.added + 1);
  }
}
</script>

<template>
  <div class="flex justify-center mt-4" v-if="props.pages > 1">
    <!-- Previous Button -->
    <div
      @click="
        $emit('prev');
        decreaseCurrentPage();
      "
      class="paginate-btn"
    >
      Prev
    </div>
    <!-- Container for more than 5 pages -->
    <div v-if="props.pages > 5" class="flex">
      <!-- Single number 1 -->
      <div
        @click="setCurrentPage(1)"
        :class="{ '!bg-white !text-dark-200': props.page === 1, 'paginate-btn': true }"
      >
        1
      </div>
      <!-- Prev ... Dots -->
      <div
        v-if="props.added > 1"
        @click="prevMoveBy(TOTAL_PAGES)"
        class="paginate-btn"
      >
        ...
      </div>
      <!-- 3 pages range -->
      <div
        v-for="page in TOTAL_PAGES"
        :class="{
          '!bg-white !text-dark-200': page + props.added === props.page,
          'paginate-btn': true,
        }"
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
        @click="
          $emit('set:page', props.pages),
            $emit('set:added', props.pages - (TOTAL_PAGES + 1))
        "
        :class="{ '!bg-white !text-dark-200': props.page === props.pages, 'paginate-btn': true }"
      >
        {{ props.pages }}
      </div>
    </div>
    <!-- Normal range less than 5, when there are not other elements -->
    <div
      v-else
      v-for="(_, i) in props.pages"
      @click="setCurrentPage(i + 1)"
      :class="{ '!bg-white !text-dark-200': i + 1 === props.page }"
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
