<script setup>
import { ref } from 'vue';
import { useFetch } from '@/composables/useFetch';


const tags = ref([]);

useFetch('tags', 'get').then((res) => {
  tags.value = res.data;
})
</script>

<template>
  <div class="tags-container">
    <div v-for="{ name } in tags" @click="$router.push(`/tags/${name}`)">
      {{ name }}
    </div>
  </div>
</template>

<style>
.tags-container {
  color: white;
}
</style>