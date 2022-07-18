<script setup lang="ts">
import { ref } from 'vue';
import MiniLabel from '../slots/MiniLabel.vue';
import AddTagIcon from "../icons/AddTagIcon.vue";

const props = defineProps(['tags'])

const tagVisible = ref(true)
const newTag = ref("")
const toggleTag = () => tagVisible.value = !tagVisible.value

function addTag() {
  toggleTag()
  
  if (newTag.value) {
    props.tags.push({
      id: props.tags.length + 1,
      name: newTag.value
    })
  }

  newTag.value = ""
}

</script>

<template>
  <MiniLabel v-for="tag in props.tags" :is-tag="true">
    <template #title>
      #{{ tag.name }}
    </template>
  </MiniLabel>
  <MiniLabel v-if="tagVisible && props.tags.length <= 3" @click="toggleTag()" :is-add="true">
    <template #title>
      Add Tag
    </template>
    <template #icon>
      <AddTagIcon />
    </template>
  </MiniLabel>
  <div v-else-if="!tagVisible">
    <input v-model="newTag" type="text" @keyup.enter="addTag()" class="new-tag-name" />
  </div>
</template>

<style scoped lang="scss">
.new-tag-name {
  outline: none;
  border: none;
  border-radius: 6px;
  padding: 1px 6px;
  width: 6rem;
}
</style>