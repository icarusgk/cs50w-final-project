<script setup lang="ts">
import { ref } from 'vue';
import { useFetch } from '@/composables/useFetch';
import type { TagType } from '@/types';
import BackIcon from '@/components/icons/BackIcon.vue';

const tags = ref<TagType[]>([]);

useFetch('tags', 'get').then((res) => {
  tags.value = res.data;
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
        :key="tag.id" 
        @click="$router.push(`/tags/${tag.name}`)"
        class="tag"
      >
        <span>#{{ tag.name }}</span>
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
      font-size: 2rem;
      font-weight: 800;
    }
  }
  .tags-container {
    color: white;
    display: flex;
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
</style>
