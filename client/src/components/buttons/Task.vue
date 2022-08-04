<script setup lang="ts">
import axios from 'axios';
import { ref, watch } from 'vue';
import { useModalStore } from '@/stores/modal.js';
import type { Task } from '@/types';


import DoneIcon from '../icons/DoneIcon.vue';
import MarkedDoneIcon from '../icons/MarkedDoneIcon.vue';
import TaskModal from '../TaskModal.vue';
import TaskInfoIcon from "@/components/icons/TaskInfoIcon.vue";

const props = defineProps<{
  task: Task
}>()

const task = ref(props.task)
const open = ref(false)

watch(() => open.value, () => {
  useModalStore().toggle()
})

async function toggleDone() {
  task.value.done = !task.value.done
  const response = await axios.put(`http://127.0.0.1:3001/tasks/${props.task.id}`, task.value)
  console.log(response)
}

</script>

<template>
  <div class="task-container" @click="open = true">
    <div @click="toggleDone()" class="task-checkbox">
      <DoneIcon v-if="!task.done" />
      <MarkedDoneIcon v-else />
    </div>
    <!-- Name -->
    <div @click="open = true" class="task-title-container" :class="{ done: task.done }">
      <div class="title-container">
        <p>{{ props.task.title }}</p>
      </div>
      <div class="task-info-icon">
        <TaskInfoIcon />
      </div>
    </div>
    <TaskModal :task=task :open="open" @exit="open = false" />
  </div>
</template>

<style scoped lang="scss">
.task-container {
  display: flex;
  align-items: center;
  margin: 0 0.2rem 0.5rem 0.2rem;

  &:hover, &:focus {
    cursor: pointer;
  } 

  .task-checkbox {
    margin-right: 1rem;
  }
  
  .task-title-container {
    padding: 0.2rem 1rem;
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