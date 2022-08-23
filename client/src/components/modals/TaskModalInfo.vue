<script setup lang="ts">
import Subtasks from '@/components/Subtasks.vue';
import TimerSetter from '@/components/TimerSetter.vue';


const props = defineProps<{
  task: any,
  isNew?: boolean
}>()

const emit = defineEmits(['descriptionChange'])

function check(event: any) {
  emit('descriptionChange', event.target.value)
}
</script>

<template>
  <div>
    <!-- Description -->
    <div class="new-task-description">
      <textarea @input="check" v-model.lazy.trim="props.task.description" placeholder="Description"
        class="new-task-textarea-description">
      </textarea>
    </div>
    <!-- Subtasks -->
    <div class="new-task-subtasks-container">
      <h2 class="title">Subtasks</h2>
      <!-- Add subtask button -->
      <div>
        <!-- Subtasks list -->
        <Subtasks :is-project="false" :chores="task.subtasks" :task="task" :isNew="isNew" />
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
        <TimerSetter :chore="task" />
      </div>
      <div>
        
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
    height: 35px;
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

        &:hover, &:focus {
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
  }
  .new-task-subtasks-container {
    margin: 0 0 0.5rem 0;
  }
}
</style>