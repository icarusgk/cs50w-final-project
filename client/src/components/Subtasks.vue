<script setup lang="ts">
import { ref } from 'vue';
import { useFetch } from '@/composables/useFetch';
import type { Task, SubtaskType } from '@/types'

import Subtask from '@/components/Subtask.vue';
import MiniLabel from '@/components/slots/MiniLabel.vue';
import AddTagIcon from '@/components/icons/AddTagIcon.vue';
import DoneIcon from './icons/DoneIcon.vue';
import MarkedDoneIcon from './icons/MarkedDoneIcon.vue';

const props = defineProps(['subtasks', 'isProject', 'task', 'project', 'isNew'])

const task = ref(props.task)
const project = ref(props.project)

const newSubtask = ref<SubtaskType>({
  title: '',
  description: ''
})

const newSubtaskOpened = ref(false)

const subtaskDetails = ref<{
  opened: boolean,
  subtask: SubtaskType | null
}>({
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
  }
}

async function addSubtask() {
  // Just a title is required
  if (newSubtask.value.title) {

    // Push subtasks to new project
    if (props.isProject && props.isNew) {
      project.value.tasks.push(newSubtask.value)
      close()
    }
    // Add subtasks to an existing project
    else if (props.isProject && !props.isNew) {
      // Make API call
      // Works !!
      const response = await useFetch(`/projects/${props.project.id}/`, {
        method: 'patch',
        data: {
          "obj": "project",
          "action": "add_new",
          "task": newSubtask.value
        }
      })
      if (response?.status === 200) {
        project.value.tasks.push(response.data)
        close()
      }
    }
    // Push subtasks to the new task
    else if (!props.isProject && props.isNew) {
      // !! Works
      task.value.subtasks.push(newSubtask.value)
    }
    // Add subtasks to an existing task
    else if (!props.isProject && !props.isNew) {
      // Make the API call
      const response = await useFetch(`/tasks/${props.task.id}/`, {
        method: 'patch',
        data: {
          "obj": "subtask",
          "action": "add",
          "subtask": newSubtask.value
        }
      })
      if (response?.status === 200) {
        task.value.subtasks.push(response.data)
      }
    }
  }

  // Modify existing subtask
  else if (subtaskDetails.value.subtask && !newSubtaskOpened.value) {
    if (props.isProject) {
      // Make the api call
      const response = await useFetch(`/projects/${props.project.id}/`, {
        method: 'patch',
        data: {
          "obj": "project",
          "action": "update_task",
          "subtask": subtaskDetails.value.subtask
        }
      })
      if (response?.status === 200) {
        close()
      }
      // console.log(subtaskDetails.value.subtask)
    } else {
      // Make the api call
      const response = await useFetch(`/tasks/${props.task.id}/`, {
        method: 'patch',
        data: {
          "obj": "subtask",
          "action": "update",
          "subtask": subtaskDetails.value.subtask
        }
      })
      if (response?.status === 200) {
        close()
      }
    }
  }  
  
}

function close() {
  subtaskDetails.value.opened = false
  resetSubtask()
}

async function deleteSubtask() {
  if (props.isProject) {
    // Works !!
    // Delete task
    const response = await useFetch(`/projects/${props.project.id}/`, {
      method: 'patch',
      data: {
        "obj": "project",
        "action": "delete_task",
        "task_id": subtaskDetails.value.subtask?.id
      }
    })
    if (response?.status === 200) {
      project.value.tasks = project.value.tasks.filter(
        (task: any) => task.id !== subtaskDetails.value.subtask?.id
      )
    }
  } else {
    // If is task
    task.value.subtasks = task.value.subtasks.filter(
      (sub: Task) => sub !== subtaskDetails.value.subtask)

    // Make the API call
    const response = await useFetch(`/tasks/${props.task.id}/`, {
      method: 'patch',
      data: {
        "obj": "subtask",
        "action": "remove",
        "subtask_id": subtaskDetails.value.subtask?.id
      }
    })
    console.log(response?.data)
  }
  
  subtaskDetails.value.opened = false
}

async function toggleDone(subtask: SubtaskType) {
  if (props.isProject) {
    const response = await useFetch(`/projects/${props.project.id}/`, {
      method: 'patch',
      data: {
        "obj": "project",
        "action": "task_done",
        "task_id": subtask.id
      }
    })
    if (response?.status === 200) {
      subtask.done = response.data.done
    }
  }
  else {
    const response = await useFetch(`/tasks/${props.task.id}/`, {
      method: 'patch',
      data: {
        "obj": "subtask",
        "action": "done",
        "subtask_id": subtask.id
      }
    })
    if (response?.status === 200) {
      subtask.done = response.data.done
    }
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
    <MiniLabel v-for="subtask in subtasks" :is-task="true">
      <template #icon>
        <DoneIcon @click="toggleDone(subtask)" v-if="!subtask.done" class="icon" />
        <MarkedDoneIcon @click="toggleDone(subtask)" v-else class="icon" />
      </template>
      <template #title>  
        <div @click="openDetails(subtask)">{{ subtask.title }}</div>
      </template>      
    </MiniLabel>
    <!-- Add new subtask -->
    <MiniLabel v-if="subtasks.length === 0" @click="openNewSubtask" :is-task="true">
      <template #title>
        <span class="add-subtask">{{ isProject ? 'Add task' : 'Add subtask' }}</span>
      </template>
      <template #icon>
        <AddTagIcon class="new-subtask" />
      </template>
    </MiniLabel>
    <div v-else>
      <MiniLabel @click="openNewSubtask" :is-task="true">
        <template #icon>
          <AddTagIcon class="new-subtask" />
        </template>
      </MiniLabel>
    </div>
  </div>
  <div v-if="newSubtaskOpened">
    <!-- Listen to the event emitter -->
    <Subtask @close="closeNewSubtask()" @save="addSubtask" :subtask="newSubtask" :newSub="true" />
  </div>
  <!-- Existing task -->
  <div v-if="subtaskDetails.opened">
    <Subtask  @close="closeDetails()" @save="addSubtask" @delete="deleteSubtask()" :subtask="subtaskDetails.subtask" />
  </div>
</template>

<style scoped lang="scss">
.new-task-minitask-container {
  display: flex;
  flex-wrap: wrap;
  margin: 0.5rem 0;
  height: 100%;
  gap: 10px;

  .add-subtask {
    margin-right: 1rem;
  }

  .icon {
    margin-left: 1rem;
    margin-top: 2px;
  }

  .new-subtask {
    width: 15px;
    height: 15px;
    margin-top: 2px;
  }
  .done {
    background-color: var(--vivid-red);
    opacity: 0.4;
  }
}
</style>