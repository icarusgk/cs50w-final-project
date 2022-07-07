<script setup lang="ts">
import { ref } from 'vue';
import MiniLabel from './MiniLabel.vue';
import TaskInfoIconVue from './icons/TaskInfoIcon.vue';
import type TypeTask from '@/types/TaskType'

defineProps<{
  task: TypeTask
}>()

// Mock Data
const mockSubtasks = ref(["Ref's", "Watchers", "SSR", "Emits"])
const mockTags = ref(["dev", "programming", "front-end", "software"])
const mockProjects = ref(["Vue", "Rails", "Super Important"])

const pomoLimits = ref({ min: 1, max: 9 })
const estimatedPomos = ref(1)

function decreasePomos() {
  if (estimatedPomos.value > pomoLimits.value.min) {
    estimatedPomos.value--;
  }
}

function increasePomos() {
  if (estimatedPomos.value < pomoLimits.value.max) {
    estimatedPomos.value++;
  }
}

</script>

<template>
  <!-- Title with tags -->
  <div class="task-heading-container">
    <!-- Tags -->
    <div class="tags-container">
      <MiniLabel v-for="tag in mockTags" :is-tag="true">
        <template #title>
          #{{ tag }}
        </template>
      </MiniLabel>
    </div>
    <div class="task-title">
      <h1>{{ task.title }}</h1>
    </div>    
  </div>
  <!-- Description -->
  <div class="description">
    <p>{{ task.description }}</p>
  </div>
  <!-- Subtasks -->
  <div class="subtasks-container">
    <h2>Subtasks</h2>
    <!-- List -->
    <div class="minitask-container">
      <MiniLabel v-for="title in mockSubtasks" :is-task="true">
        <template #title>
          {{ title }}
        </template>
        <template #icon>
          <TaskInfoIconVue class="icon" />
        </template>
      </MiniLabel>
    </div>
  </div>
  <div class="bottom-container">
    <!-- Estimated Pomos -->
    <div class="estimated-pomos-container">
      <div>
        <span>Estimated pomos</span>
      </div>
      <div class="counter-container">
          <input
            type="number"
            class="estimated-pomos-input"
            :min="pomoLimits.min"
            :max="pomoLimits.max"
            :value="estimatedPomos"
          />
          <button @click="decreasePomos()" class="counter-button">-</button>
        <button @click="increasePomos()" class="counter-button">+</button>
      </div>
    </div>
    <!-- Add to project -->
    <div class="add-to-project-dropdown">
      <div>
        <span>Add to project</span>
      </div>
      <div>
        <select class="project-select">
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
</template>

<style lang="scss" scoped>
.task-heading-container {
  display: flex;
  box-sizing: unset;
  flex-direction: column;
  .task-title {
    margin-top: 1rem;
  }
  .tags-container {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 0;
  }
}

.description {
  margin: 1rem 0;
}

.subtasks-container {
  margin: 1rem 0;
  .minitask-container {
    display: flex;
    flex-wrap: wrap;
    margin: 0.5rem 0;

    .icon {
      margin-left: 1rem;
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
      }
      .counter-button {
        padding: 0 0.3rem;
        border-radius: 4px;
        border: none;
        margin: 0 4px;
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
    }
  }
}
</style>