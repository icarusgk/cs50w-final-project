<script setup lang="ts">
import type { ITask } from '@/types';

defineProps<{
  task: ITask;
  isNew?: boolean;
}>();

defineEmits<{
  (e: 'input:description', description: string): void
  (e: 'change:pomoCount', count: number): void
  (e: 'save:task'): void
}>();
</script>

<template>
  <div>
    <!-- Description -->
    <div class="mt-2 mb-0 lg:my-4 lg:mx-0">
      <textarea
        @input="event => $emit('input:description', (event.target as HTMLInputElement).value)"
        @keyup.ctrl.enter="$emit('save:task')"
        :value="task.description"
        placeholder="Description"
        class="h-[80px] placeholder-gray-300 w-full outline-none border-b-gray-400 border-b-[1px] bg-transparent lg:h-[50px]"
      >
      </textarea>
    </div>
    <!-- Subtasks -->
    <div class="my-4 mx-0">
      <h2>Subtasks</h2>
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
    <div class="flex flex-col">
      <!-- Estimated Pomos -->
      <div class="flex">
        <div>
          <span class="font-extrabold">Estimated pomos</span>
        </div>
        <!-- Counter -->
        <PomoCountSetter
          :chore="task"
          @change:pomoCount="(count: number) => $emit('change:pomoCount', count)"
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

    $placeholderColor: rgb(190, 190, 190);

    &::-webkit-input-placeholder {
      color: $placeholderColor;
    }
    &::-moz-input-placeholder {
      color: $placeholderColor;
    }
    &::-ms-input-placeholder {
      color: $placeholderColor;
    }
    &::placeholder {
      color: $placeholderColor;
    }
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
