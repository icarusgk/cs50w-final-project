<script setup lang="ts">
import { ref } from "vue";

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
const totalPages = 3;

// Emitters
const emit = defineEmits(["prev", "next", "setPage", "setAdded"]);

// Reactive Variables
const added = ref(props.added);
const currentPage = ref(props.page);

// Increase CurrentPage
function increaseCurrentPage(): void {
  if (currentPage.value < props.pages) {
    currentPage.value += 1;
  }

  if (currentPage.value >= 4) {
    nextMoveBy(1);
  }
}

// Set current Page
function setCurrentPage(page: number): void {
  if (page <= 4) {
    emit("setPage", page);
  } else {
    // Move the added pages
    if (page > 4 && page > currentPage.value && page !== props.pages) {
      // Move next
      emit("setPage", page);
      nextMoveBy(1);
    }
    if (page < currentPage.value) {
      // Move prev
      emit("setPage", page);
      prevMoveBy(1);
    }
  }

  // added.value setters
  if (page === props.pages) {
    added.value = props.pages - 4;
    emit('setPage', page);
  }

  if (page === props.pages - 1) {
    added.value = props.pages - 4;
  }

  currentPage.value = page;

  // Movers
  // Reset to 2
  if (currentPage.value === 4) {
    added.value = 2;
  }
  // Reset back to 1
  if (currentPage.value <= 3) {
    added.value = 1;
  }

  emit("setAdded", added.value);
}

// Decrease Current Page
function decreaseCurrentPage(): void {
  if (currentPage.value > 1) {
    currentPage.value -= 1;
  }

  if (currentPage.value <= props.pages - 3) {
    prevMoveBy(1);
  }
}

function prevMoveBy(decreasedBy: number): void {  
  // Edge case when '...' is pressed when currentPage is <= 3
  // Resets added back to 1

  // Reset range
  if (currentPage.value <= 4) {
    added.value = 1;
    emit("setAdded", added.value);
    return;
  }

  // By 3
  if (decreasedBy > 1) {
    added.value <= 3 ? added.value = 1 : added.value -= decreasedBy; 
    currentPage.value = added.value + 2;
    emit('setPage', currentPage.value);
  }

  // By 1
  if (decreasedBy === 1) {
    added.value -= 1;
  }

  emit('setAdded', added.value);
}

function nextMoveBy(increasedBy: number): void {
  // By 3
  if (increasedBy > 1) {
    // Check if currentPage value is 7 or more
    if (currentPage.value >= props.pages - 4) {
      currentPage.value = props.pages;
      // Move the range to the final
      added.value = props.pages - 4;
    }
    // If added is less than 6 move by n (3)
    if (added.value < props.pages - 5) {
      added.value += increasedBy - 1;
      currentPage.value = added.value + 2;
    } else {
      // For short pages
      added.value = props.pages - 4
      currentPage.value = props.pages - 2;      
    }
    emit("setPage", currentPage.value);
  }

  // By 1
  // Check the increasedBy value
  if (increasedBy === 1 && currentPage.value <= props.pages - 2) {
    added.value += 1;
  }
  
  emit("setAdded", added.value);
}
</script>

<template>
  <div class="container" v-if="pages > 1">
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
    <div v-if="pages > 5" class="flex">
      <!-- Single number 1 -->
      <div
        @click="setCurrentPage(1)"
        :class="{ active: currentPage === 1, 'paginate-btn': true }"
      >
        1
      </div>
      <!-- Prev ... Dots -->
      <div v-if="added > 1" @click="prevMoveBy(3)" class="paginate-btn">...</div>
      <!-- 3 pages range -->
      <div
        v-for="page in totalPages"
        :class="{ active: page + added === currentPage, 'paginate-btn': true }"
        @click="setCurrentPage(page + added)"
      >
        {{ page + added }}
      </div>
      <!-- Next ... Dots -->
      <div v-if="added + 4 !== pages" @click="nextMoveBy(3)" class="paginate-btn">
        ...
      </div>
      <!-- Last page -->
      <div
        @click="setCurrentPage(pages)"
        :class="{ active: currentPage === pages, 'paginate-btn': true }"
      >
        {{ pages }}
      </div>
    </div>
    <!-- Normal range less than 5 -->
    <div
      v-else
      v-for="(_, i) in pages"
      @click="setCurrentPage(i + 1)"
      :class="{ active: i + 1 === currentPage }"
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
