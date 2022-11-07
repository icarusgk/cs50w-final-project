<script setup lang="ts">
import axios from 'axios';
import { ref, watch } from 'vue';
import { useModalStore } from '@/stores/modal';
import { useChoreStore } from '@/stores/chore';
import type { TaskType } from '@/types';

import DoneIcon from '../icons/DoneIcon.vue';
import MarkedDoneIcon from '../icons/MarkedDoneIcon.vue';
import TaskModal from '../TaskModal.vue';
import TaskInfoIcon from '@/components/icons/TaskInfoIcon.vue';
import DeleteIcon from '../icons/DeleteIcon.vue';

const props = defineProps<{
  task: TaskType;
}>();

const emit = defineEmits(['setCurrent']);

const open = ref(false);
const chore = useChoreStore();

watch(open, () => {
  useModalStore().toggle();
});

async function toggleDone() {
  const response = await axios.patch(`tasks/${props.task.id}/`, {
    obj: 'task',
    action: 'done',
  });
  if (response?.status === 200) {
    props.task.done = response.data?.done;
    chore.fetchProjects();
  }
}

async function deleteTask() {
  if (window.confirm('Are you sure you want to delete this task?')) {
    chore.deleteTask(props.task);
  }
}
</script>

<template>
  <div class="task-container">
    <div @click="toggleDone()" class="task-checkbox" v-auto-animate>
      <DoneIcon v-if="!task.done" />
      <MarkedDoneIcon v-else />
    </div>
    <!-- Name -->
    <div class="task-title-container" :class="{ done: task.done }">
      <div @click="$emit('setCurrent', task.id)" class="title-container">
        <Popper hover arrow placement="bottom" openDelay="1000">
          <span class="title">{{ props.task.title }}</span>
          <template #content>
            Click to set it to current
          </template>
        </Popper>
      </div>
      <div class="icon-container">
        <div class="task-icon" @click="deleteTask()" style="margin-top: 0.3rem">
          <DeleteIcon />
        </div>
        <div class="task-icon" @click="open = true">
          <TaskInfoIcon />
        </div>
      </div>
    </div>
    <TaskModal
      :task="props.task"
      :open="open"
      @exit="open = false"
      @toggle-done="toggleDone()"
    />
  </div>
</template>

<style scoped lang="scss">
.task-container {
  display: flex;
  align-items: center;
  margin: 0 0.2rem 0.5rem 0.2rem;

  .task-checkbox {
    margin-right: 1rem;
    &:hover,
    &:focus,
    &:active {
      cursor: pointer;
    }
  }

  .task-title-container {
    padding: 0.2rem 0.8rem;
    border-radius: 8px;
    background-color: var(--vivid-red);
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    transition: all 0.2s ease;

    .icon-container {
      display: flex;
    }

    .title-container {
      &:hover,
      &:focus,
      &:active {
        cursor: pointer;
      }
    }

    .task-icon {
      margin-top: 0.2rem;
      margin-right: 0.2rem;
      &:hover,
      &:focus,
      &:active {
        cursor: pointer;
      }
    }
  }

  .done {
    background-color: var(--vivid-red);
    opacity: 0.4;
  }
}
</style>
