<script setup lang="ts">
import { ref, watch } from "vue";
import { useModalStore } from "@/stores/modal";
import { useChoreStore } from '@/stores/chore';
import type TypeTask from "@/types/TaskType"

import axios from 'axios'

import Tags from "@/components/buttons/Tags.vue";
import Modal from "@/components/modals/Modal.vue";
import TaskModalInfo from "@/components/modals/TaskModalInfo.vue";
import SaveButton from "@/components/SaveButton.vue";
import DeleteIcon from "@/components/icons/DeleteIcon.vue";
import AddToProjectPopup from "./AddToProjectPopup.vue";

import tags from "@/mocks/tags";

const props = defineProps<{
  task: TypeTask
  open: boolean
}>()

const emit = defineEmits(['exit'])

const task = ref(props.task)
const pristine = ref(true)


async function saveTask() {
  const response = await axios.put(
    `http://127.0.0.1:3001/tasks/${props.task.id}`,
    props.task
  )
  if (response.status === 200) {
    console.log("Saved!")
  }
  emit('exit')
}

async function deleteTask() {
  useChoreStore().deleteTask(props.task.id)
  emit('exit')
}

function checkPristine(description: string) {
  pristine.value = description === props.task.description
}
</script>

<template>
  <div class="task-container">
    <!-- Modal -->
    <Modal :open="open" @exit-modal="$emit('exit')">
      <!-- Tags -->
      <template #tags>
        <Tags :taskTags="task.tags" :allTags="tags" />
        <DeleteIcon @click="deleteTask()" class="delete-icon" />
      </template>
      <!-- Title -->
      <template #title>
        <input type="text" name="title" id="task-input-title" v-model="props.task.title" />
      </template>
      <!-- Modal -->
      <TaskModalInfo :task="task" @description-change="checkPristine" />
      <template #save-button>
        <AddToProjectPopup />
        <SaveButton @click="saveTask()" :disabled="false" />
      </template>
    </Modal>
  </div>
</template>

<style lang="scss" scoped>

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
