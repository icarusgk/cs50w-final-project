<script setup lang="ts">
import { ref } from 'vue';
import { useChoreStore } from '@/stores/chore';
import type { Tag, TaskType } from '@/types';
import axios from 'axios';

import Tags from '@/components/buttons/Tags.vue';
import Modal from '@/components/modals/Modal.vue';
import TaskModalInfo from '@/components/modals/TaskModalInfo.vue';
import SaveButton from '@/components/SaveButton.vue';
import DeleteIcon from '@/components/icons/DeleteIcon.vue';
import AddToProjectPopup from './AddToProjectPopup.vue';
import DoneIcon from './icons/DoneIcon.vue';
import MarkedDoneIcon from './icons/MarkedDoneIcon.vue';

const props = defineProps<{
  task: TaskType;
  open: boolean;
}>();

const emit = defineEmits(['exit', 'toggleDone']);

const task = ref(props.task);
const pristine = ref(true);

// Saves task with PUT method
async function saveTask() {
  try {
    const response = await axios.put(`tasks/${props.task.id}/`, task.value);
    if (response?.status === 200) {
      console.log(response);
    }
  } catch (err) {
    console.log('saveTask() err', err);
  }
  emit('exit');
}

async function deleteTask() {
  useChoreStore().deleteTask(task.value?.id);
  emit('exit');
}

function checkPristine(description: string) {
  pristine.value = description === props.task.description;
}

function removeTag(tag: Tag) {
  task.value.tags = task.value.tags.filter((t: Tag) => t.name !== tag.name);
}
</script>

<template>
  <div class="task-container">
    <!-- Modal -->
    <Modal :open="open" @exit-modal="$emit('exit')">
      <!-- Tags -->
      <template #tags>
        <Tags :taskTags="task.tags" :id="task.id" />
        <DoneIcon @click="$emit('toggleDone')" v-if="!props.task.done" />
        <MarkedDoneIcon @click="$emit('toggleDone')" v-else />
        <DeleteIcon @click="deleteTask()" class="delete-icon" />
      </template>
      <!-- Title -->
      <template #title>
        <input
          type="text"
          name="title"
          id="task-input-title"
          v-model="props.task.title"
        />
      </template>
      <!-- Modal -->
      <TaskModalInfo :task="task" @description-change="checkPristine" />
      <template #save-button>
        <AddToProjectPopup :taskId="task.id" />
        <SaveButton @click="saveTask()" :disabled="false" />
      </template>
    </Modal>
  </div>
</template>

<style lang="scss" scoped>
.delete-icon {
  margin: 0.1rem 0.5rem;
  &:hover,
  &:focus {
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
