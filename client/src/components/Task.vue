<script setup lang="ts">
import axios from 'axios'
import { ref, watch } from "vue";
import Tags from "./buttons/Tags.vue";
import TaskInfoIcon from "./icons/TaskInfoIcon.vue";
import Modal from "./modals/Modal.vue";
import TaskModal from "./modals/TaskModal.vue";
import type TypeTask from "@/types/TaskType"
import { useModalStore } from "@/stores/modal";
import SaveButton from "./SaveButton.vue";
import DeleteIcon from "./icons/DeleteIcon.vue";
import DoneIcon from "./icons/DoneIcon.vue";
import MarkedDoneIcon from "./icons/MarkedDoneIcon.vue";
import { useChoreStore } from '@/stores/chore';

const props = defineProps<{
  task: TypeTask
}>()

const emit = defineEmits(['deleteTask'])

const task = ref(props.task)
const open = ref(false)

// When open.value changes, toggle
watch(() => open.value, () => {
  useModalStore().toggle()
})


async function saveTask() {
  const response = await axios.put(
    `http://127.0.0.1:3001/tasks/${props.task.id}`,
    props.task
  )
  if (response.status === 200) {
    console.log("Saved!")
  }
  open.value = false;
}

async function deleteTask() {
  const response = await axios.delete(`http://127.0.0.1:3001/tasks/${props.task.id}`)
  console.log(response)
  open.value = false;
  useChoreStore().deleteTask(props.task.id)
}

async function toggleDone() {
  task.value.done = !task.value.done
  const response = await axios.put(`http://127.0.0.1:3001/tasks/${props.task.id}`, task.value)
  console.log(response)
}

</script>

<template>
  <div class="task-container">
    <!-- Checkbox -->
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
    <!-- Modal -->
    <Modal :open="open" @exit-modal="open = false">
      <!-- Tags -->
      <template #tags>
        <Tags :tags="task.tags" />
        <DeleteIcon @click="deleteTask()" class="delete-icon" />
      </template>
      <!-- Title -->
      <template #title>
        <input type="text" name="title" id="task-input-title" v-model="props.task.title" />
      </template>
      <!-- Modal -->
      <TaskModal :task="task" />
      <SaveButton @click="saveTask()" />
    </Modal>
  </div>
</template>

<style lang="scss" scoped>
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

.delete-icon {
  margin: 0.1rem 0.5rem;
  &:hover, &:focus {
    cursor: pointer;
  }
}

#task-input-title {
  border: none;
  background: transparent;
  color: white;
  font-size: 2rem;
  font-weight: 900;
  font-family: sans-serif;
  width: 100%;

  &:focus {
    outline: none;
  }

}



</style>
