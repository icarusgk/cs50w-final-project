<script setup lang="ts">
import { ref } from 'vue';
import MiniLabel from './slots/MiniLabel.vue';
import AddTagIcon from './icons/AddTagIcon.vue';
import Subtask from '@/components/Subtask.vue';
import TaskInfoIconVue from '@/components/icons/TaskInfoIcon.vue';
import axios from 'axios';

const props = defineProps(['subtasks', 'isProject', 'task', 'project'])

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

    if (props.isProject) {
      project.value.tasks.push(newSubtask.value)
      modify('projects', props.project.id, props.project)
    } else {
        task.value.subtasks.push(newSubtask.value)
        modify('tasks', props.task.id, props.task)
    }
  }

  else if (subtaskDetails.value.subtask && !newSubtaskOpened.value) {
    if (props.isProject) {
      modify('projects', props.project.id, props.project)
    } else {
        modify('tasks', props.task.id, props.task)
    }
    
  }
  subtaskDetails.value.opened = false
  resetSubtask()
}

// TODO: Replace with subtask type
async function modify(type: string, id: number, data: any) {
  const response = await axios.put(`http://127.0.0.1:3001/${type}/${id}`, data)
  console.log(response)
}


function deleteTask() {
  if (props.isProject) {
    project.value.tasks = project.value.tasks.filter((task: any) => task !== subtaskDetails.value.subtask)
    axios.put(`http://127.0.0.1:3001/projects/${props.project.id}`, project.value)
  } else {
    task.value.subtasks = task.value.subtasks.filter((sub: any) => sub !== subtaskDetails.value.subtask)
    axios.put(`http://127.0.0.1:3001/tasks/${props.task.id}`, task.value)
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
    <Subtask @save="addSubtask"  @close="closeDetails()" @delete="deleteTask()" :subtask="subtaskDetails.subtask" />
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