<script setup lang="ts">
import { ref } from 'vue'
import MiniLabel from '../../slots/MiniLabel.vue';
import AddTagIcon from '../../icons/AddTagIcon.vue';
import Subtask from '@/components/Subtask.vue';
import TaskInfoIconVue from '@/components/icons/TaskInfoIcon.vue';

const props = defineProps(['task'])

const subtask = ref({
  title: '',
  description: '',
  estimated: 0
})

const selected = ref('')
const pomoLimits = ref({ min: 1, max: 99 })
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

// TODO: Replace any with type
function addSubtask() {
  props.task.subtasks.push(subtask.value)
  subtask.value = {
    title: '',
    description: '',
    estimated: 0
  }
}

function closeDetails() {
  subtaskDetails.value.opened = false
  subtaskDetails.value.subtask = null
}
</script>

<template>
  <div>
    <!-- Description -->
    <div class="new-task-description">
      <textarea v-model.lazy.trim="props.task.description" placeholder="Description"
        class="new-task-textarea-description">
      </textarea>
    </div>
    <!-- Subtasks -->
    <div class="new-task-subtasks-container">
      <h2>Subtasks</h2>
      <!-- Add subtask button -->
      <div class="new-task-minitask-container">
        <!-- Subtasks list -->
        <MiniLabel @click="openDetails(subtask)" v-for="subtask in props.task.subtasks" :is-task="true">
          <template #title>
            {{ subtask.title }}
          </template>
          <template #icon>
            <TaskInfoIconVue class="icon" />
          </template>
        </MiniLabel>
        <!-- Add subtask -->
        <MiniLabel @click="openNewSubtask" :is-task="true">
          <template #title>
            Add subtask
          </template>
          <template #icon>
            <AddTagIcon class="new-subtask" />
          </template>
        </MiniLabel>
      </div>
      <div v-if="newSubtaskOpened">
        <!-- Listen to the event emitter -->
        <Subtask @close="newSubtaskOpened = false" @save="addSubtask" :subtask="subtask" />
      </div>
      <div v-if="subtaskDetails.opened">
        <Subtask @close="closeDetails()" :subtask="subtaskDetails.subtask" />
      </div>
    </div>
    <!-- Bottom container -->
    <div class="bottom-container">
      <!-- Estimated Pomos -->
      <div class="estimated-pomos-container">
        <div>
          <span style="font-weight: 800;">Estimated pomos</span>
        </div>

        <!-- Counter -->
        <div class="counter-container">
          <input type="number" class="estimated-pomos-input" :min="pomoLimits.min" :max="pomoLimits.max"
            v-model="props.task.estimated" />
          <button @click="props.task.estimated--" class="counter-button">-</button>
          <button @click="props.task.estimated++" class="counter-button">+</button>
        </div>
      </div>

      <!-- Add to project -->
      <div class="add-to-project-dropdown">
        <div>
          <span style="font-weight: 800;">Project</span>
        </div>
        <div>
          <select class="project-select" v-model="selected">
            <option disabled value="">Select one</option>
            <option v-for="project in ['vue learning', 'pomo.do']" :value="project">
              {{ project }}
            </option>
          </select>
        </div>
      </div>

    </div>
  </div>
</template>

<style lang="scss" scoped>
.task-title-input {
  background: transparent;
  border: none;
  outline: none;
  border-bottom: 1px solid white;
  color: white;
  margin-left: 2rem;
}

.new-task-description {
  margin: 1rem 0;

  .new-task-textarea-description {
    width: 100%;
    height: 50px;
    outline: none;
    background-color: transparent;
    color: white;
    font-family: sans-serif;
    border: none;
    resize: none;
  }
}

.new-task-subtasks-container {
  margin: 1rem 0;

  .new-task-minitask-container {
    display: flex;
    flex-wrap: wrap;
    margin: 0.5rem 0;
    height: 33px;
    
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
}

.bottom-container {
  display: flex;

  .estimated-pomos-container {
    display: flex;

    .counter-container {
      margin: 0 1rem;

      .estimated-pomos-input {
        background: transparent;
        border: none;
        color: white;
        width: 25%;
        outline: none;
        font-weight: 700;
      }

      .counter-button {
        padding: 0 0.4rem;
        border-radius: 4px;
        border: none;
        margin: 0 4px;

        &:hover {
          cursor: pointer;
        }
      }
    }

  }

  .add-to-project-dropdown {
    display: flex;
    position: relative;

    .project-select {
      margin-left: 1rem;
      border: none;
      outline: none;
      padding: 2px;
      border-radius: 4px;
      cursor: pointer;
    }
  }
}
</style>