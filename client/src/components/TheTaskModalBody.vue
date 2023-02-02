<script setup lang="ts">
import Subchores from '@/components/Subchores.vue';
import PomoCountSetter from '@/components/PomoCountSetter.vue';
import type { TaskType } from '@/types';

defineProps<{
  task: TaskType;
  isNew?: boolean;
}>();

defineEmits(['descriptionInput', 'newPomoCount', 'saveTask']);
</script>

<template>
  <div>
    <!-- Description -->
    <div class="new-task-description">
      <textarea
        @input="event => $emit('descriptionInput', (event.target as HTMLInputElement).value)"
        @keyup.ctrl.enter="$emit('saveTask')"
        :value="task.description"
        placeholder="Description"
        class="new-task-textarea-description"
      >
      </textarea>
    </div>
    <!-- Subtasks -->
    <div class="new-task-subtasks-container">
      <h2 class="title">Subtasks</h2>
      <!-- Add subtask button -->
      <div>
        <!-- Subtasks list -->
        <Subchores
          :is-project="false"
          :chores="task.subtasks"
          :task="task"
          :isNew="isNew"
        />
      </div>
    </div>
    <!-- Bottom container -->
    <div class="bottom-container">
      <!-- Estimated Pomos -->
      <div class="estimated-pomos-container">
        <div>
          <span style="font-weight: 800">Estimated pomos</span>
        </div>
        <!-- Counter -->
        <PomoCountSetter
          :chore="task"
          @newPomoCount="$emit('newPomoCount', $event)"
        />
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
  flex-direction: column;

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

        &:hover,
        &:focus,
        &:active {
          cursor: pointer;
        }
      }
    }
  }
}

@media (max-width: 768px) {
  .new-task-description {
    margin-top: 0.5rem;
    margin-bottom: 0;
    .new-task-textarea-description {
      height: 80px;
    }
  }
  .new-task-subtasks-container {
    margin: 0 0 0.5rem 0;
  }
}
</style>
