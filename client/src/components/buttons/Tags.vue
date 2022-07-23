<script setup lang="ts">
import { ref, computed } from 'vue';
import MiniLabel from '../slots/MiniLabel.vue';
import AddTagIcon from "../icons/AddTagIcon.vue";
import tags from "@/mocks/tags"

const props = defineProps(['tags'])

const tagVisible = ref(true)
const newTag = ref("")

function addTag() {  
  if (newTag.value) {
    props.tags.push({
      id: props.tags.length + 1,
      name: newTag.value
    })
  }

  newTag.value = ""
}

const selectedTags = computed(() => {
  return tags.filter(t => t.includes(newTag.value))
})
</script>

<template>
  <MiniLabel v-for="tag in props.tags" :is-tag="true">
    <template #title>
      #{{ tag.name }}
    </template>
  </MiniLabel>
  <Popper arrow placement="right">
    <MiniLabel v-if="tagVisible && props.tags.length <= 3" :is-add="true">
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
        <div class="tag-result" @click="newTag = tag; addTag(); close()" v-if="newTag" v-for="tag in selectedTags">
          <span>{{ tag }}</span>
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