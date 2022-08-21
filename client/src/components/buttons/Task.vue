<script setup lang="ts">
import axios from 'axios';
import { ref, watch } from 'vue';
import { useModalStore } from '@/stores/modal';
import { useChoreStore } from '@/stores/chore';
import type { Task, Project } from '@/types';


import DoneIcon from '../icons/DoneIcon.vue';
import MarkedDoneIcon from '../icons/MarkedDoneIcon.vue';
import TaskModal from '../TaskModal.vue';
import TaskInfoIcon from "@/components/icons/TaskInfoIcon.vue";
import { useFetch } from '@/composables/useFetch';


const props = defineProps<{
  task: Task
}>()

const task = ref(props.task)
const open = ref(false)

watch(() => open.value, () => {
  useModalStore().toggle()
})

async function toggleDone() {
  const response = await useFetch(`/tasks/${props.task.id}/`, {
    method: 'patch',
    data: {
      "obj": "task",
      "action": "done"
    }
  })
  if (response?.status === 200) {
    task.value.done = response.data?.done
    useChoreStore().fetchProjects()
  }
}

// function setCurrent() {
//   useChoreStore().changeCurrentTask(props.task.id)
// }
</script>

<template>
  <div class="task-container">
    <div @click="toggleDone()" class="task-checkbox">
      <DoneIcon v-if="!task.done" />
      <MarkedDoneIcon v-else />
    </div>
    <!-- Name -->
    <div class="task-title-container" :class="{ done: task.done }">
      <div class="title-container">
        <span class="title">{{ props.task.title }}</span>
      </div>
      <div class="task-info-icon" @click="open = true">
        <TaskInfoIcon />
      </div>
    </div>
    <TaskModal :task=task :open="open" @exit="open = false" @toggle-done="toggleDone()" />
  </div>
</template>

<style scoped lang="scss">
.task-container {
  display: flex;
  align-items: center;
  margin: 0 0.2rem 0.5rem 0.2rem;

  .task-checkbox {
    margin-right: 1rem;
  }
  
  .task-title-container {
    padding: 0.2rem 0.8rem;
    border-radius: 8px;
    background-color: var(--vivid-red);
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;

    
    .task-info-icon {
      margin-top: 0.2rem;
      &:hover, &:focus {
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