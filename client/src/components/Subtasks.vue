<script setup lang="ts">
import { ref, reactive } from 'vue';
import { useFetch } from '@/composables/useFetch';
import type { TaskType, SubtaskType } from '@/types'

import Subtask from '@/components/Subtask.vue';
import MiniLabel from '@/components/slots/MiniLabel.vue';
import AddTagIcon from '@/components/icons/AddTagIcon.vue';
import DoneIcon from './icons/DoneIcon.vue';
import MarkedDoneIcon from './icons/MarkedDoneIcon.vue';
import { useChoreStore } from '@/stores/chore'
import TaskInfoIcon from './icons/TaskInfoIcon.vue'

const props = defineProps(['chores', 'isProject', 'task', 'project', 'isNew'])

const existingTask = ref(props.task)
const existingProject = ref(props.project)

// Initial mold for a task
const taskModel = ref({
  tags: [],
  title: '',
  description: '',
  estimated: 1
})

// Initial mold for a subtask
const subtaskModel = ref({
  title: '',
  description: ''
})

// A chore can be either a task in a project
// or a subtask in a task
const newChoreOpened = ref(false)

const activeChore = reactive<{
  opened: boolean,
  chore: TaskType | SubtaskType | null
}>({
  opened: false,
  chore: null
})

// Open the an empty chore
function openNewChore() {
  // Toggle the state of the active chore
  if (activeChore.opened) { activeChore.opened = false }
  // Open a new chore
  newChoreOpened.value = true
}

// Open chore details
function openDetails(chore: TaskType | SubtaskType) {
  // Assign the current task details
  activeChore.chore = chore

  // Close the "details" for a new chore
  if (newChoreOpened.value) { newChoreOpened.value = false }

  // Mark the chore details as opened
  activeChore.opened = true
}

// Resets the subtask model to its initial value
function resetSubtaskModel() {
  subtaskModel.value = {
    title: '',
    description: '',
  }
}

// Resets the task model to its initial value
function resetTaskModel() {
  taskModel.value = {
    tags: [],
    title: '',
    description: '',
    estimated: 1
  }
}

// Add task to existing project
async function addTaskToProject() {
  // if a new task is being pushed to a new or 
  // existing project
  if (taskModel.value.title) {

    // Push new task to new project
    if (props.isProject && props.isNew) {
      existingProject.value.tasks.push(taskModel.value)
      resetTaskModel()
    }

    // Add new task to an existing project
    // LIVE
    if (props.isProject && !props.isNew) {
      // Works !!
      try {
        const response = await useFetch(`/projects/${props.project.id}/`, {
          method: 'patch',
          data: {
            "obj": "project",
            "action": "add_new",
            "task": taskModel.value
          }
        })
        if (response?.status === 201) {
          // Returns a task inside the project
          existingProject.value.tasks.push(response.data)
          // Reset and close
          closeNew()
        }
      } catch (err) {
        console.log('err adding task to project', err)
      }
    }
  }

  // If an existing task has to be updated
  if (activeChore.chore && !newChoreOpened.value) {
    // Make the api call
    const response = await useFetch(`/projects/${props.project.id}/`, {
      method: 'patch',
      data: {
        "obj": "project",
        "action": "update_task",
        "subtask": activeChore.chore
      }
    })
    if (response?.status === 200) {
      closeDetails()
    }
  }
    
}

// Add subtask to task or task to project
async function addSubtaskToTask() {
  // Just a title is required
  if (subtaskModel.value.title) {
    // Push subtasks to the new task
    if (!props.isProject && props.isNew) {
      existingTask.value.subtasks.push(subtaskModel.value)
      resetSubtaskModel()
    }
    // Add subtasks to an existing task
    else if (!props.isProject && !props.isNew) {
      // Make the API call
      const response = await useFetch(`/tasks/${props.task.id}/`, {
        method: 'patch',
        data: {
          "obj": "subtask",
          "action": "add",
          "subtask": subtaskModel.value
        }
      })
      if (response?.status === 200) {
        existingTask.value.subtasks.push(response.data)
        resetSubtaskModel()
      }
    }
  }

  // Modify existing subtask
  else if (activeChore.chore && !newChoreOpened.value) {
    if (!props.isProject) {
      // Make the api call
      const response = await useFetch(`/tasks/${props.task.id}/`, {
        method: 'patch',
        data: {
          "obj": "subtask",
          "action": "update",
          "subtask": activeChore.chore
        }
      })
      if (response?.status === 200) {
        closeDetails()
      }
    }
  }  
  
}

// Delete chore (db) from parent component
async function deleteChore() {
  if (props.isProject) {
    // Works !!
    // Delete task
    const response = await useFetch(`/projects/${props.project.id}/`, {
      method: 'patch',
      data: {
        "obj": "project",
        "action": "delete_task",
        "task_id": activeChore.chore?.id
      }
    })
    if (response?.status === 200) {
      existingProject.value.tasks = existingProject.value.tasks.filter(
        (task: TaskType) => task.id !== activeChore.chore?.id
      )
    }
  } else {
    // If is task
    existingTask.value.subtasks = existingTask.value.subtasks.filter(
      (sub: TaskType) => sub !== activeChore.chore)

    // Make the API call
    const response = await useFetch(`/tasks/${props.task.id}/`, {
      method: 'patch',
      data: {
        "obj": "subtask",
        "action": "remove",
        "subtask_id": activeChore.chore?.id
      }
    })
    console.log(response?.data)
  }
  activeChore.opened = false
}

// Remove (visually) chore from parent component
function removeChore() {  
  if (props.isProject) {
    existingProject.value.tasks = existingProject.value.tasks.filter(
      (task: TaskType) => task.title !== activeChore.chore?.title 
    )
  } else {
    existingTask.value.subtasks = existingTask.value.subtasks.filter(
      (subtask: SubtaskType) => subtask.title !== activeChore.chore?.title
    )
  }
  closeDetails()
}

// Toggle done on Chore
async function toggleChoreDone(chore: TaskType | SubtaskType) {
  if (props.isProject) {
    try {
      const response = await useFetch(`/projects/${props.project.id}/`, {
        method: 'patch',
        data: {
          "obj": "project",
          "action": "task_done",
          "task_id": chore.id
        }
      })
      if (response?.status === 200) {
        chore.done = response.data.done
        // Visual changes
        let project_task = useChoreStore().tasks.filter(
          (task: TaskType) => task.id === chore.id)[0]

        if (project_task) {
          project_task.done = response.data.done
        }
      }
    } catch (err) {
      console.log('task done update err', err)
    }
  }
  else {
    try {
      const response = await useFetch(`/tasks/${props.task.id}/`, {
        method: 'patch',
        data: {
          "obj": "subtask",
          "action": "done",
          "subtask_id": chore.id
        }
      })
      if (response?.status === 200) {
        chore.done = response.data.done
      }
    } catch (err) {
      console.log('subtask done update err', err)
    }
  }
}

// Close chore details
function closeDetails() {  
  activeChore.opened = false
  activeChore.chore = null
}

// Close new model details and reset it
function closeNew() {
  newChoreOpened.value = false
  props.isProject ? resetTaskModel() : resetSubtaskModel()  
}
</script>

<template>
  <div class="new-task-minitask-container">
    <!-- Display each subtask list -->
    <MiniLabel v-for="chore in chores" :is-task="true">
      <template #icon>
        <TaskInfoIcon @click="openDetails(chore)" v-if="isNew" class="icon" />
        <DoneIcon @click="toggleChoreDone(chore)" v-if="!chore.done && !isNew" class="icon" />
        <MarkedDoneIcon @click="toggleChoreDone(chore)" v-if="chore.done" class="icon" />
      </template>
      <template #title>  
        <div @click="openDetails(chore)">{{ chore.title }}</div>
      </template>
    </MiniLabel>
    <!-- Add new subtask or task -->
    <MiniLabel v-if="chores.length === 0" @click="openNewChore" :is-task="true">
      <template #title>
        <span class="add-subtask">{{ isProject ? 'Add task' : 'Add subtask' }}</span>
      </template>
      <template #icon>
        <AddTagIcon class="new-subtask" />
      </template>
    </MiniLabel>
    <!-- Add new subtask or task but just show the icon -->
    <div v-else>
      <MiniLabel @click="openNewChore" :is-task="true">
        <template #icon>
          <AddTagIcon class="new-subtask" />
        </template>
      </MiniLabel>
    </div>
  </div>
  <!-- If the a new chore is opened -->
  <div v-if="newChoreOpened">
    <!-- Listen to the event emitter -->
    <Subtask
      @close="closeNew()"
      @save="addSubtaskToTask()"
      @saveTask="addTaskToProject()"
      :chore="isProject ? taskModel : subtaskModel"
      :newChore="true"
      :key="isProject ? existingProject.tasks.length : task.subtasks.length"
      :isProject="isProject" />
  </div>
  <!-- If an existing chore is opened -->
  <div v-if="activeChore.opened">
    <Subtask
      @close="closeDetails()"
      @save="addSubtaskToTask()"
      @saveTask="addTaskToProject()"
      @remove="removeChore()"
      @delete="deleteChore()"
      :chore="activeChore.chore"
      :parentNew="isNew"
      :newChore="isNew"
      :key="isNew ? activeChore.chore?.title : activeChore.chore?.id"
      :isProject="isProject" />
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