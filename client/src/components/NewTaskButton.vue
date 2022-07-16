<script setup lang="ts">
import TaskButton from './TaskButton.vue';
import NewTaskModal from './NewTaskModal.vue';
import MiniLabel from './MiniLabel.vue';
import { ref } from 'vue';
import AddTagIcon from './icons/AddTagIcon.vue';

const initialTask = ref<{
  tags: string[]
  title: string,
  description: string
  estimated: number,
  subtasks: {
    title: string,
    description: string,
    estimated: number
  }[]
}>({
  tags: [],
  title: '',
  description: '',
  estimated: 0,
  subtasks: []
})

const tagVisible = ref(true)
const newTag = ref('')

const toggleTag = () => tagVisible.value = !tagVisible.value

function addTag() {
  toggleTag()

  if (newTag.value) {
    initialTask.value.tags.push(newTag.value)
    console.log(initialTask.value.tags)
  }
  newTag.value = ""
}

function saveTask() {

}
</script>

<template>
  <TaskButton>
    <template #type>
      Add new task
    </template>
    <template #tags>
      <!-- Tags that have been added previously -->
      <MiniLabel v-for="tag in initialTask.tags" :is-tag="true">
        <template #title>
          #{{ tag }}
        </template>
      </MiniLabel>
      <!-- Add tag -->
      <MiniLabel v-if="tagVisible" :is-add="true" @click="toggleTag()">
        <template #title>
          Add tag
        </template>
        <template #icon>
          <AddTagIcon />
        </template>
      </MiniLabel>
      <!-- Form for adding the tag -->
      <div v-else-if="!tagVisible">
        <input v-model="newTag" type="text" @keyup.enter="addTag()" class="new-tag-name" />
      </div>
    </template>
    <!-- New task title -->
    <template #title>
      <input 
        type="text" 
        name="title" 
        id="new-task-input-title" 
        placeholder="New task title" 
        v-model="initialTask.title" 
      />
    </template>
    <NewTaskModal :task="initialTask" />
    <template #save-button>
      <button
        @click="saveTask()" 
        class="close-modal-button"
      >Save!
      </button>
    </template>
  </TaskButton>
</template>

<style scoped lang="scss">
#new-task-input-title {
  border: none;
  background: transparent;
  color: white;
  font-size: 2rem;
  font-weight: 900;
  font-family: sans-serif;
  width: 100%;

  &:focus {
    outline: none;
  }
}

.close-modal-button {
  background-color: var(--vivid-red);
  color: var(--white);

  font: {
    weight: 900;
    family: sans-serif;
  }

  width: 100%;
  border: none;
  border-radius: 10px;
  margin-top: 1rem;
  padding: 0.8rem 0.8rem;

  &:hover {
    cursor: pointer;
  }
}
</style>