<script setup lang="ts">
import type { ITag } from '@/types';

const tags = ref<ITag[]>([]);
const fetched = ref(false);

const router = useRouter();

useRawFetch<ITag[]>('tags').then((res) => {
  if (res._data) tags.value = res._data;
  fetched.value = true;
});
</script>

<template>
  <div class="<sm:p-4 py-8 px-16">
    <div class="flex items-center gap-4 text-white ml-3">
      <div class="pointer i-bi-arrow-left-square-fill scale-250" @click="router.back()" />
      <span class="text-white font-extrabold text-5xl ml-2">Tags</span>
    </div>
    <div class="text-white flex flex-wrap gap-2.5 pt-4">
      <div
        v-for="tag in tags"
        v-if="fetched"
        :key="tag.id"
        @click="router.push(`/tags/${tag.name}`)"
        class="bg-light-gray p-4 rounded-lg font-semibold transition transition-all duration-200 ease-in-out pointer hover:bg-vivid-red"
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
