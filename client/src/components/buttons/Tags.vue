<script setup lang="ts">
import { ref, computed } from 'vue';
import { useChoreStore } from '@/stores/chore';
import type { Tag } from '@/types';

import MiniLabel from '@/components/slots/MiniLabel.vue';
import AddTagIcon from "@/components/icons/AddTagIcon.vue";
import DeleteTagIcon from "../icons/DeleteTagIcon.vue";
import { useFetch } from '@/composables/useFetch';

const props = defineProps<{
  id?: number,
  taskTags: Tag[],
  info?: boolean,
  new?: boolean
}>()

// A local manipulable copy of the tags
// For filtering and pushing
const taskTags = ref(props.taskTags)

const newTagVisible = ref(true)
const newTag = ref("")
// const taskTags = ref(props.taskTags)

const allTags = ref(useChoreStore().tags)

// Filter existing tags
props.taskTags.forEach((taskTag: Tag) => {
  allTags.value = allTags.value.filter((tag: Tag) => tag.name !== taskTag.name)
})

const selectedTags = computed(() => {
  return allTags.value.filter((tag: Tag) => tag.name.includes(newTag.value.toLowerCase()))
})

async function addTag() {
  if (newTag.value) {
    // Push the tag but not upload it
    if (props.new) {
      props.taskTags.push({
        name: newTag.value
      })
      console.log(newTag.value)
      // if not new
    } else {
      // filter if not in taskTags
      if (!(props.taskTags.filter(tag => tag.name === newTag.value).length > 0)) {
        // Make the request
        try {
          // Add the new tag to the existing task
          const response = await useFetch(`/tasks/${props.id}/`, {
            method: 'patch',
            data: {
              "obj": "tag",
              "action": "add",
              "tag_name": newTag.value
            }
          })

          if (response?.status === 200) {
            if (response.data?.message === "new") {
              useChoreStore().tags.push(response.data?.tag)
            }
            // response.data will be the tag obj {id, name}
            taskTags.value.push(response.data?.tag)
          }
        } catch (err) {
          console.log('addTag err', err);
        }
      }
    }
  }
  newTag.value = ""
  newTagVisible.value = true
}

async function deleteTag(tag: Tag) {
  // TODO: Ask for confirmation  
  const response = await useFetch(`/tasks/${props.id}/`,
    {
      method: 'patch',
      data: {
        "obj": "tag",
        "action": "remove",
        "tag_id": tag.id
      }
    }
  )
  if (response?.status === 200) {
    // emit the deletion of the tag
    removeTag(tag)
  }
}

function removeTag(tag: Tag) {
  taskTags.value = taskTags.value.filter((t: Tag) => t.name !== tag.name)
}

</script>

<template>
  <!-- Existing tags -->
  <MiniLabel v-for="tag in taskTags" :is-tag="true">
    <template #title>
      #{{ tag.name }}
    </template>
    <template #icon>
      <DeleteTagIcon v-if="!info" @click="deleteTag(tag)" class="delete-tag-icon" />
    </template>
  </MiniLabel>
  <!-- Add tags -->
  <MiniLabel v-if="!info && taskTags.length === 0 && newTagVisible" @click="newTagVisible = false" :is-add="true">
    <template #title>
      <span class="task-title">Add tag</span>
    </template>
    <template #icon>
      <AddTagIcon />
    </template>
  </MiniLabel>
  <!-- Replace the button with input -->
  <MiniLabel v-if="(!info && taskTags.length > 0 && taskTags.length < 3) && newTagVisible"
    @click="newTagVisible = false" :is-add="true">
    <template #icon>
      <AddTagIcon />
    </template>
  </MiniLabel>
  <!-- Form -->
  <div v-if="!newTagVisible">
    <Popper>
      <div class="new-tag-container">
        <input type="text" class="new-tag-name" v-model="newTag" @keydown.enter="addTag()" />
        <button @click="addTag()" class="new-tag-button">Add</button>
      </div>
      <template #content="{ close }">
        <div>
          <span>Add a new tag:</span>
          <div class="tag-results" @click="newTag = tag.name; addTag(); close()"
            v-for="tag in selectedTags.slice(0, 5)">
            <div class="tag-result">
              {{ tag.name }}
            </div>
          </div>
          <div class="tag-result" @click="addTag()" v-if="selectedTags.length === 0">{{ newTag }}</div>
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

    &:hover,
    &:focus {
      cursor: pointer;
    }
  }
}

.tag-result {
  padding: 0.1rem 0.4rem;
  margin: 0.3rem 0;
  border-radius: 5px;
  background-color: rgba(233, 244, 233, 0.1);

  &:hover,
  &:focus {
    cursor: pointer;
  }
}
</style>