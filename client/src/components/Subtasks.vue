<script setup lang="ts">
import { ref, reactive } from 'vue';
import { useChoreStore } from '@/stores/chore';
import { useAlertStore } from '@/stores/alerts';
import axios from 'axios';
import type { TaskType, SubtaskType, TagType } from '@/types';

import Subtask from '@/components/Subtask.vue';
import MiniLabel from '@/components/slots/MiniLabel.vue';
import AddTagIcon from '@/components/icons/AddTagIcon.vue';
import DoneIcon from '@/components/icons/DoneIcon.vue';
import MarkedDoneIcon from '@/components/icons/MarkedDoneIcon.vue';

import TaskInfoIcon from '@/components/icons/TaskInfoIcon.vue';

const props = defineProps(['chores', 'isProject', 'task', 'project', 'isNew']);

const existingTask = ref(props.task);
const existingProject = ref(props.project);

// Initial mold for a task
const taskModel = ref({
  tags: [],
  title: '',
  description: '',
  estimated: 1,
});

// Initial mold for a subtask
const subtaskModel = ref({
  title: '',
  description: '',
});

// A chore can be either a task in a project
// or a subtask in a task
const newChoreOpened = ref(false);

const activeChore = reactive<{
  opened: boolean;
  chore: any;
}>({
  opened: false,
  chore: null,
});

const tmp = {
  title: '',
  desc: '',
  estimated: 0
};


const alert = useAlertStore();

const handleTitle = (title: string) => tmp.title = title;
const handleDesc = (desc: string) => tmp.desc = desc;
const handleEstimated = (n: number) => tmp.estimated = n;

// Open the an empty chore
function openNewChore() {
  // Toggle the state of the active chore
  if (activeChore.opened) {
    activeChore.opened = false;
  }
  // Open a new chore
  newChoreOpened.value = true;
}

// Open chore details
function openDetails(chore: TaskType | SubtaskType) {
  // Assign the current task details
  activeChore.chore = chore;

  // Close the "details" for a new chore
  if (newChoreOpened.value) {
    newChoreOpened.value = false;
  }

  // Mark the chore details as opened
  activeChore.opened = true;
}

// Resets the subtask model to its initial value
function resetSubtaskModel() {
  subtaskModel.value = {
    title: '',
    description: '',
  };
}

// Resets the task model to its initial value
function resetTaskModel() {
  taskModel.value = {
    tags: [],
    title: '',
    description: '',
    estimated: 1,
  };
}

// Add task to existing project
async function addTaskToProject() {
  // if a new task is being pushed to a new or
  // existing project
  if (taskModel.value.title) {
    // Push new task to new project
    if (props.isProject && props.isNew) {
      existingProject.value.tasks.push(taskModel.value);
      alert.info('Task added!');
      resetTaskModel();
    }

    // Add new task to an existing project
    // LIVE
    if (props.isProject && !props.isNew) {
      // Works !!
      try {
        const response = await axios.patch(`projects/${props.project.id}/`, {
          obj: 'project',
          action: 'add_new',
          task: taskModel.value,
        });
        if (response?.status === 201) {
          // Returns a task inside the project
          existingProject.value.tasks.push(response.data);
          alert.success(`Task ${taskModel.value.title} saved!`);
          // Reset and close
          closeNew();
        }
      } catch (err) {
        console.log('err adding task to project', err);
      }
    }
  }

  // If an existing task has to be updated
  if (activeChore.chore && !newChoreOpened.value) {
    activeChore.chore.title = tmp.title !== '' ? tmp.title : activeChore.chore.title;
    activeChore.chore.description = tmp.desc !== '' ? tmp.desc : activeChore.chore.description;
    activeChore.chore.estimated = tmp.estimated !== 0 ? tmp.estimated : activeChore.chore.estimated;

    // Make the api call
    const response = await axios.patch(`projects/${props.project.id}/`, {
      obj: 'project',
      action: 'update_task',
      subtask: activeChore.chore,
    });

    if (response?.status === 200) {
      alert.success(`Task ${activeChore.chore.title} saved!`);
      closeDetails();
    }

    // Reset tmp's
    tmp.title = '';
    tmp.desc = '';
    tmp.estimated = 0;
  }
}

// Add subtask to task or task to project
async function saveSubtaskToTask() {
  // Just a title is required
  if (subtaskModel.value.title) {
    // Push subtasks to the new task
    if (!props.isProject && props.isNew) {
      existingTask.value.subtasks.push(subtaskModel.value);
      alert.info(`${subtaskModel.value.title} added!`);
      resetSubtaskModel();
    }
    // Add subtasks to an existing task
    else if (!props.isProject && !props.isNew) {
      // Make the API call
      const response = await axios.patch(`tasks/${props.task.id}/`, {
        obj: 'subtask',
        action: 'add',
        subtask: subtaskModel.value,
      });
      if (response?.status === 200) {
        existingTask.value.subtasks.push(response.data);
        alert.success(`${subtaskModel.value.title} saved!`);
        resetSubtaskModel();
      }
    }
  }

  // Modify existing subtask
  else if (activeChore.chore && !newChoreOpened.value) {
    if (!props.isProject) {
      activeChore.chore.title = tmp.title !== '' ? tmp.title : activeChore.chore.title;
      activeChore.chore.description = tmp.desc !== '' ? tmp.desc : activeChore.chore.description;      
      
      // Make the api call
      const response = await axios.patch(`/tasks/${props.task.id}/`, {
        obj: 'subtask',
        action: 'update',
        subtask: activeChore.chore,
      });
      if (response?.status === 200) {
        alert.success(`Subtask ${activeChore.chore.title} saved!`);
        closeDetails();
      }
    }
  }
}

// Delete chore (db) from parent component
async function deleteChore() {
  if (props.isProject) {
    // Delete task
    if (window.confirm('Are you sure?')) {
      const response = await axios.patch(`/projects/${props.project.id}/`, {
        obj: 'project',
        action: 'delete_task',
        task_id: activeChore.chore?.id,
      });
      if (response?.status === 200) {
        alert.success(`Task ${activeChore.chore?.title} removed from project!`);
        console.log(response.data);        
        existingProject.value.tasks = existingProject.value.tasks.filter(
          (task: TaskType) => task.id !== activeChore.chore?.id
        );
      }
    }
  } else {
    // If subtask
    const response = await axios.patch(`/tasks/${props.task.id}/`, {
      obj: 'subtask',
      action: 'remove',
      subtask_id: activeChore.chore?.id,
    });

    if (response?.status === 200) {
      // If is task
      alert.success(`Subtask ${activeChore.chore?.title} deleted!`);
      existingTask.value.subtasks = existingTask.value.subtasks.filter(
        (sub: TaskType) => sub !== activeChore.chore
      );
    }
  }
  activeChore.opened = false;
}

// Remove (visually) chore from parent component
function removeChore() {
  if (props.isProject) {
    existingProject.value.tasks = existingProject.value.tasks.filter(
      (task: TaskType) => task.title !== activeChore.chore?.title
    );
  } else {
    existingTask.value.subtasks = existingTask.value.subtasks.filter(
      (subtask: SubtaskType) => subtask.title !== activeChore.chore?.title
    );
  }
  closeDetails();
}

// Toggle done on Chore
async function toggleChoreDone(chore: TaskType | SubtaskType) {
  if (props.isProject) {
    try {
      const response = await axios.patch(`projects/${props.project.id}/`, {
        obj: 'project',
        action: 'task_done',
        task_id: chore.id,
      });
      if (response?.status === 200) {
        chore.done = response.data.done;
        // Visual changes
        let project_task = useChoreStore().tasks.find(
          (task: TaskType) => task.id === chore.id
        );

        if (project_task) {
          project_task.done = response.data.done;
        }
      }
    } catch (err) {
      console.log('task done update err', err);
    }
  } else {
    try {
      const response = await axios.patch(`tasks/${props.task.id}/`, {
        obj: 'subtask',
        action: 'done',
        subtask_id: chore.id,
      });
      if (response?.status === 200) {
        chore.done = response.data.done;
      }
    } catch (err) {
      console.log('subtask done update err', err);
    }
  }
}

// Close chore details
function closeDetails() {
  activeChore.opened = false;
  activeChore.chore = null;
}

// Close new model details and reset it
function closeNew() {
  newChoreOpened.value = false;
  props.isProject ? resetTaskModel() : resetSubtaskModel();
}

function removeTag(tag: TagType) {
  if (props.isProject) {

    // When a existing chore is opened
    if (activeChore.opened) {
      activeChore.chore.tags = activeChore.chore.tags.filter((t: TagType) => t.name !== tag.name);
      return;
    }

    // When a fresh chore is opened, just remove it
    taskModel.value.tags = taskModel.value.tags.filter((t: TagType) => t.name !== tag.name);
  }  
}
</script>

<template>
  <div class="new-task-minitask-container" v-auto-animate>
    <!-- Display each subtask list -->
    <MiniLabel v-for="chore in chores" :is-task="true">
      <template #icon>
        <TaskInfoIcon @click="openDetails(chore)" v-if="isNew" class="icon" />
        <div v-auto-animate>
          <DoneIcon
            @click="toggleChoreDone(chore)"
            v-if="!chore.done && !isNew"
            class="icon"
          />
          <MarkedDoneIcon
            @click="toggleChoreDone(chore)"
            v-if="chore.done"
            class="icon"
          />
        </div>
      </template>
      <template #title>
        <div @click="openDetails(chore)">{{ chore.title }}</div>
      </template>
    </MiniLabel>
    <!-- Add new subtask or task -->
    <MiniLabel v-if="chores.length === 0" @click="openNewChore" :is-task="true">
      <template #title>
        <span class="add-subtask">{{
          isProject ? 'Add task' : 'Add subtask'
        }}</span>
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
    <!-- A new fresh chore -->
    <Subtask
      @close="closeNew()"
      @save="saveSubtaskToTask()"
      @saveTask="addTaskToProject()"
      @removeTag="removeTag($event)"
      @titleChange="isProject ? taskModel.title = $event : subtaskModel.title = $event"
      @descChange="isProject ? taskModel.description = $event : subtaskModel.description = $event"
      :chore="isProject ? taskModel : subtaskModel"
      :newChore="true"
      :key="isProject ? existingProject.tasks.length : task.subtasks.length"
      :isProject="isProject"
    />
  </div>
  <!-- If an existing chore is opened -->
  <div v-if="activeChore.opened">
    <Subtask
      @close="closeDetails()"
      @save="saveSubtaskToTask()"
      @saveTask="addTaskToProject()"
      @remove="removeChore()"
      @delete="deleteChore()"
      @removeTag="removeTag($event)"
      @titleChange="handleTitle"
      @descChange="handleDesc"
      @increasePomo="handleEstimated"
      @decreasePomo="handleEstimated"
      :chore="activeChore.chore"
      :parentNew="isNew"
      :newChore="isNew"
      :key="isNew ? activeChore.chore?.title : activeChore.chore?.id"
      :isProject="isProject"
    />
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
