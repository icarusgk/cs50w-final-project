<script setup lang="ts">
import type { TagType } from '@/types';

const tags = ref<TagType[]>([]);

const fetched = ref(false);

useFetch('tags', 'get').then((res) => {
  tags.value = res.data;
  fetched.value = true;
});
</script>

<template>
  <div class="tags-view">
    <div class="go-back">
      <BackIcon class="button" @click="$router.back()" />
      <span class="title">Tags</span>
    </div>
    <div class="tags-container">
      <div
        v-for="tag in tags"
        v-if="fetched"
        :key="tag.id" 
        @click="$router.push(`/tags/${tag.name}`)"
        class="tag"
      >
        <span>#{{ tag.name }}</span>
      </div>
      <div v-else>
        <span>Loading...</span>
      </div>
      <div v-if="fetched && tags.length === 0">
        <p>Currently there are no tags.</p>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.tags-view {
  padding: 2rem 4rem;

  .go-back {
    display: flex;
    align-items: center;
    gap: 1rem;
    color: white;

    .button {
      &:hover,
      &:focus,
      &:active {
        cursor: pointer;
      }
    }
    .title {
      color: white;
      font-size: 3rem;
      font-weight: 800;
    }
  }
  .tags-container {
    color: white;
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    padding-top: 1rem;
  
    .tag {
      background-color: var(--light-gray);
      padding: 1rem;
      border-radius: 8px;
      font-weight: 600;
      transition: background-color 0.2s ease-in-out;
  
      &:hover,
      &:focus,
      &:active {
        cursor: pointer;
      }
  
      &:hover {
        background-color: var(--vivid-red);
      }
    }
  }
}

@media (max-width: 480px) {
  .tags-view {
    padding: 1rem;
  }
}
</style>
