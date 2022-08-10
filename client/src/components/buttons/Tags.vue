<script setup lang="ts">
import { ref, computed } from 'vue';
import { useChoreStore } from '@/stores/chore';
import type { Tag } from '@/types';
import tags from '@/mocks/tags';


import MiniLabel from '@/components/slots/MiniLabel.vue';
import AddTagIcon from "@/components/icons/AddTagIcon.vue";
import DeleteTagIcon from "../icons/DeleteTagIcon.vue";


const props = defineProps<{
  taskTags: Tag[]
  allTags?: Tag[]
  info?: boolean
}>()

const newTagVisible = ref(true)
const newTag = ref("")
const taskTags = ref(props.taskTags)

// To newly created or existing task
// function addTag() {
//   if (newTag.value) {
//     const existingTag = props.allTags?.find((tag: Tag) => tag.name === newTag.value)

//     if (existingTag) {
//       props.taskTags.push(existingTag)
//     } else {
//       const tag = {
//         id: 21,
//         name: newTag.value
//       }
//       useChoreStore().addTag(tag)
//       props.taskTags.push(tag)
//     }
//   }
  
//   newTag.value = ""
// }

// const selectedTags = computed(() => {
//   return props.allTags?.filter((tag: Tag) => tag.name.includes(newTag.value))
// })

const selectedTags = computed(() => {
  return tags.filter((tag: Tag) => tag.name.includes(newTag.value.toLowerCase()))
})


function addMockTag() {
  if (newTag.value) {
    taskTags.value.push({
      id: 91,
      name: newTag.value
    })
  }
  newTag.value = ""
  newTagVisible.value = true
}

function deleteTag(tag: Tag) {
  taskTags.value = taskTags.value.filter((t: Tag) => t.id !== tag.id)
}

</script>

<template>
  <MiniLabel v-for="tag in taskTags" :is-tag="true">
    <template #title>
      #{{ tag.name }}
    </template>
    <template #icon>
      <DeleteTagIcon v-if="!info" @click="deleteTag(tag)" class="delete-tag-icon" />
    </template>
  </MiniLabel>
  <MiniLabel v-if="!info && taskTags.length === 0 && newTagVisible" @click="newTagVisible = false" :is-add="true">
    <template #title>
      <span class="task-title">Add tag</span>
    </template>
    <template #icon>
      <AddTagIcon />
    </template>
  </MiniLabel>
  <!-- Replace the button with input -->
  <MiniLabel v-if="(!info && taskTags.length > 0 && taskTags.length < 3) && newTagVisible" @click="newTagVisible = false" :is-add="true">
    <template #icon>
      <AddTagIcon />
    </template>
  </MiniLabel>
  <!-- Form -->
  <div v-if="!newTagVisible">
    <Popper>
      <div class="new-tag-container">
        <input type="text" class="new-tag-name" v-model="newTag" @keydown.enter="addMockTag()" />
        <button @click="addMockTag()" class="new-tag-button">Add</button>
      </div>
      <template #content="{ close }">
        <div>
          <span>Add a new tag:</span>
          <div class="tag-results" @click="newTag = tag.name; addMockTag(); close()" v-for="tag in selectedTags.slice(0, 5)">
            <div class="tag-result">
              {{ tag.name }}
            </div>
          </div>
          <div class="tag-result" @click="addMockTag()" v-if="selectedTags.length === 0">{{ newTag }}</div>
        </div>
      </template>
    </Popper>
  </div>
</template>

<style scoped lang="scss">

.delete-tag-icon {
  margin-left: 0.5rem;
}

.task-title {
  margin-right: 0.5rem;
}
.new-tag-container {
  .new-tag-name {
    outline: none;
    border: none;
    border-radius: 4px;
    padding: 1px 2px;
    width: 6rem;
  }
  
  .new-tag-button {
    padding: 0 0.5rem;
    border-radius: 4px;
    border: none;
    margin-left: 0.5rem;

    &:hover, &:focus {
      cursor: pointer;
    }
  }
}

.tag-result {
  padding: 0.1rem 0.4rem;
  margin: 0.3rem 0;
  border-radius: 5px;
  background-color: rgba(233, 244, 233, 0.1);

  &:hover, &:focus {
    cursor: pointer;
  }
}

</style>