<script setup lang="ts">
import { ref, computed } from 'vue';
import { useChoreStore } from '@/stores/chore';
import type { Tag } from '@/types';

import MiniLabel from '@/components/slots/MiniLabel.vue';
import AddTagIcon from "@/components/icons/AddTagIcon.vue";


const props = defineProps<{
  taskTags: Tag[]
  allTags?: Tag[]
  info?: boolean
}>()

const tagVisible = ref(true)
const newTag = ref("")

// To newly created or existing task
function addTag() {
  if (newTag.value) {
    const existingTag = props.allTags?.find((tag: Tag) => tag.name === newTag.value)

    if (existingTag) {
      props.taskTags.push(existingTag)
    } else {
      const tag = {
        id: 21,
        name: newTag.value
      }
      useChoreStore().addTag(tag)
      props.taskTags.push(tag)
    }
  }
  
  newTag.value = ""
}

const selectedTags = computed(() => {
  return props.allTags?.filter((tag: Tag) => tag.name.includes(newTag.value))
})
</script>

<template>
  <MiniLabel v-for="tag in props.taskTags" :is-tag="true">
    <template #title>
      #{{ tag.name }}
    </template>
  </MiniLabel>
  <Popper arrow placement="right" v-if="!info">
    <MiniLabel v-if="tagVisible && props.taskTags.length <= 3" :is-add="true">
      <template #title>
        Add Tag
      </template>
      <template #icon>
        <AddTagIcon />
      </template>
    </MiniLabel>
    <template #content="{ close }">
      <input v-model="newTag" type="text" @keyup.enter="addTag()" class="new-tag-name" autofocus />
      <div class="tag-results">
        <div class="tag-result" @click="newTag = name; addTag(); close()" v-if="newTag" v-for="{ name } in selectedTags">
          <span>{{ name }}</span>
        </div>
      </div>
    </template>
  </Popper>
  <!-- <div v-else-if="!tagVisible">
    <input v-model="newTag" type="text" @keyup.enter="addTag()" class="new-tag-name" />
  </div> -->
</template>

<style scoped lang="scss">
.new-tag-name {
  outline: none;
  border: none;
  border-radius: 4px;
  padding: 1px 6px;
  width: 6rem;
}

.tag-results {
  .tag-result {
    padding: 0.2rem 0.4rem;
    margin: 0.5rem 0;
    border-radius: 5px;
    background-color: rgba(233, 244, 233, 0.1);

    &:hover, &:focus {
      cursor: pointer;
    }
  }
}
</style>