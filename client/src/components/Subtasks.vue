<script setup lang="ts">
import { ref } from 'vue';
import MiniLabel from './slots/MiniLabel.vue';
import AddTagIcon from './icons/AddTagIcon.vue';
import Subtask from '@/components/Subtask.vue';
import TaskInfoIconVue from '@/components/icons/TaskInfoIcon.vue';

const props = defineProps(['subtasks', 'isProject'])

const subtask = ref({
  title: '',
  description: '',
  estimated: 0
})

const newSubtaskOpened = ref(false)

const subtaskDetails = ref({
  opened: false,
  subtask: null
})

function openNewSubtask() {
  if (subtaskDetails.value.opened) {
    subtaskDetails.value.opened = false
  }
  newSubtaskOpened.value = true
}

function openDetails(subtask: any) {
  subtaskDetails.value.subtask = subtask
  if (newSubtaskOpened.value) {
    newSubtaskOpened.value = false
  }
  subtaskDetails.value.opened = true
}

function resetSubtask() {
  subtask.value = {
    title: '',
    description: '',
    estimated: 0
  }
}

// TODO: Replace any with type
function addSubtask() {
  if (subtask.value.title) {
    props.subtasks.push(subtask.value)
    resetSubtask()
  }
}

function closeDetails() {
  subtaskDetails.value.opened = false
  subtaskDetails.value.subtask = null
}

function closeNewSubtask() {
  newSubtaskOpened.value = false
  resetSubtask()
}
</script>

<template>
  <div class="new-task-minitask-container">
    <!-- Subtasks list -->
    <MiniLabel @click="openDetails(subtask)" v-for="subtask in subtasks" :is-task="true">
      <template #title>
        {{ subtask.title }}
      </template>
      <template #icon>
        <TaskInfoIconVue class="icon" />
      </template>
    </MiniLabel>
    <!-- Add new subtask -->
    <MiniLabel @click="openNewSubtask" :is-task="true">
      <template #title>
        {{ isProject ? 'Add task' : 'Add subtask' }}
      </template>
      <template #icon>
        <AddTagIcon class="new-subtask" />
      </template>
    </MiniLabel>
  </div>
  <div v-if="newSubtaskOpened">
    <!-- Listen to the event emitter -->
    <Subtask @close="closeNewSubtask()" @save="addSubtask" :subtask="subtask" />
  </div>
  <div v-if="subtaskDetails.opened">
    <Subtask @close="closeDetails()" :subtask="subtaskDetails.subtask" />
  </div>
</template>

<style scoped lang="scss">
.new-task-minitask-container {
  display: flex;
  flex-wrap: wrap;
  margin: 0.5rem 0;
  height: 100%;
  gap: 10px;

  .icon {
    margin-left: 1rem;
    margin-top: 2px;
  }

  .new-subtask {
    width: 15px;
    height: 15px;
    margin-top: 2px;
    margin-left: 0.5rem;
  }
}
</style>