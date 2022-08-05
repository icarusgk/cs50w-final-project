<script setup lang="ts">
import { ref, watch } from 'vue'
import Subtasks from '@/components/Subtasks.vue';
import TimerSetter from '@/components/TimerSetter.vue';
import { useChoreStore } from '@/stores/chore';
import type Project from '@/types/ProjectType';

const props = defineProps<{
  task: any,
  isNew?: boolean
}>()

const projects = useChoreStore().projects
const selectedProjects = ref<Project[]>([])

// TODO: Connect to back-end
function addToProject(project: Project) {
  console.log('added', project.title);
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
      <div>
        <!-- Subtasks list -->
        <Subtasks :is-project="false" :subtasks="task.subtasks" :task="task" :isNew="isNew" />
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
        <TimerSetter :subtask="task" />
      </div>

      <!-- Add to project -->
      <div class="add-to-project-dropdown">
        <Popper arrow placement="bottom">
        <div>
          <span class="text"> Add to Project</span>
        </div>
        <template #content="{ close }">
          <div class="project-select">
            <div class="project" v-for="project in projects" @click="addToProject(project)">
              {{ project.title }}
            </div>
          </div>
        </template>
        </Popper>
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

        &:hover, &:focus {
          cursor: pointer;
        }
      }
    }

  }

  .add-to-project-dropdown {
    display: flex;
    position: relative;
    margin-left: 1rem;

    &:hover, &:focus {
      cursor: pointer;
    }

    .text {
      font-weight: 800;
    }

    .project-select { 
      width: 10rem;

      .project {
        background-color: rgb(92, 92, 92);
        padding: 0.5rem;
        border-radius: 8px;
        margin-bottom: 0.4rem;
        &:last-child {
          margin: 0;
        }
      }
    }
  }
}
</style>