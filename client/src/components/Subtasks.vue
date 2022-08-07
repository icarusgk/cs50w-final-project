<script setup lang="ts">
import { ref } from 'vue';
import { useFetch } from '@/composables/useFetch';
import type { Task } from '@/types'

import Subtask from '@/components/Subtask.vue';
import TaskInfoIconVue from '@/components/icons/TaskInfoIcon.vue';
import MiniLabel from '@/components/slots/MiniLabel.vue';
import AddTagIcon from '@/components/icons/AddTagIcon.vue';



const props = defineProps(['subtasks', 'isProject', 'task', 'project', 'isNew'])

const task = ref(props.task)
const project = ref(props.project)

const newSubtask = ref({
  title: '',
  description: '',
  estimated: 1
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
  newSubtask.value = {
    title: '',
    description: '',
    estimated: 1
  }
}

async function addSubtask() {
  if (newSubtask.value.title) {

    // Push subtasks to new project
    if (props.isProject && props.isNew) {
      project.value.tasks.push(newSubtask.value)
    }
    // Add subtasks to an existing project
    else if (props.isProject && !props.isNew) {
      project.value.tasks.push(newSubtask.value)
      modify('projects', props.project.id, props.project)
    }
    // Push subtasks to the new task
    else if (!props.isProject && props.isNew) {
      task.value.subtasks.push(newSubtask.value)
    }
    // Add subtasks to an existing task
    else if (!props.isProject && !props.isNew) {
      task.value.subtasks.push(newSubtask.value)
      modify('tasks', props.task.id, props.task)
    }
  }

  // Modify existing subtask
  else if (subtaskDetails.value.subtask && !newSubtaskOpened.value) {
    props.isProject ?
      modify('projects', props.project.id, props.project)
    : modify('tasks', props.task.id, props.task)
  }
  
  subtaskDetails.value.opened = false
  resetSubtask()
}

// TODO: Replace with subtask type
async function modify(type: string, id: number, data: any) {
  const response = await useFetch(`/${type}/${id}`, { method: 'put', data: data })
  console.log(response)
}


function deleteSubtask() {
  if (props.isProject) {    
    project.value.tasks = project.value.tasks.filter(
      (task: Task) => task !== subtaskDetails.value.subtask)
    useFetch(`/projects/${props.project.id}`, { method: 'put', data: project.value })
  } else {
    task.value.subtasks = task.value.subtasks.filter(
      (sub: Task) => sub !== subtaskDetails.value.subtask)
    useFetch(`/tasks/${props.task.id}`, { method: 'put', data: task.value })
  }
  
  subtaskDetails.value.opened = false
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
    <Subtask @close="closeNewSubtask()" @save="addSubtask" :subtask="newSubtask" :newSub="true" />
  </div>
  <!-- Existing task -->
  <div v-if="subtaskDetails.opened">
    <Subtask @save="addSubtask"  @close="closeDetails()" @delete="deleteSubtask()" :subtask="subtaskDetails.subtask" />
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