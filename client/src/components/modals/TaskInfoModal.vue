<script setup lang="ts">
import { ref } from 'vue';
import type TypeTask from '@/types/TaskType'

import MiniLabel from '@/components/slots/MiniLabel.vue';
import TaskInfoIconVue from '@/components/icons/TaskInfoIcon.vue';
import AddTagIcon from '@/components/icons/AddTagIcon.vue'

const props = defineProps<{
  task: TypeTask
}>()

// Mock Data
const mockProjects = ref(["Vue", "Rails", "Super Important"])
const selected = ref('')
const pomoLimits = ref({ min: 1, max: 99 })


function saveTask() {
  console.log(props.task)
}

</script>

<template>
  <!-- Description -->
  <div class="description">
    <textarea v-model.lazy.trim="props.task.description" id="task-textarea-description"></textarea>
  </div>
  <!-- Subtasks -->
  <div class="subtasks-container">
    <h2>Subtasks</h2>
    <!-- List -->
    <div class="minitask-container">
      <MiniLabel v-for="subtask in task.subtasks" :is-task="true">
        <template #title>
          {{ subtask.title }}
        </template>
        <template #icon>
          <TaskInfoIconVue class="icon" />
        </template>
      </MiniLabel>
      <!-- Redirect to new task -->
      <MiniLabel :is-task="true">
        <template #title>
          Add subtask
        </template>
        <template #icon>
          <AddTagIcon class="new-subtask" />
        </template>
      </MiniLabel>
    </div>
  </div>
  <div class="bottom-container">
    <!-- Estimated Pomos -->
    <div class="estimated-pomos-container">
      <div>
        <span style="font-weight: 800;">Estimated pomos</span>
      </div>

      <!-- Counter -->
      <div class="counter-container">
        <input
          type="number"
          class="estimated-pomos-input"
          :min="pomoLimits.min"
          :max="pomoLimits.max"
          v-model="task.estimated"
        />
        <button class="counter-button">-</button>
        <button class="counter-button">+</button>
      </div>
    </div>
    
    <!-- Add to project -->
    <div class="add-to-project-dropdown">
      <div>
        <span style="font-weight: 800;">Add to project</span>
      </div>
      <div>
        <select class="project-select" v-model="selected">
          <option disabled value="">Select one</option>
          <option
            v-for="project in mockProjects"
            :value="project"
          >
            {{ project }}
          </option>
        </select>
      </div>
    </div>

 </div>
 <button
    @click="saveTask()" 
    class="close-modal-button"
  >Save!
  </button>
</template>

<style lang="scss" scoped>
.task-heading-container {
  display: flex;
  box-sizing: unset;
  flex-direction: column;
  .task-title {
    margin-top: 1rem;
  }
}

.description {
  margin: 1rem 0;

  #task-textarea-description {
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

.subtasks-container {
  margin: 1rem 0;
  .minitask-container {
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
