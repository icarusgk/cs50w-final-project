<script setup lang="ts">
import { ref } from 'vue';
import { useChoreStore } from '@/stores/chore';
import type { Tag, TaskType } from '@/types';

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

// not updating cuz of this
const chore = useChoreStore();

// Saves task with PUT method
function saveTask() { 
  chore.saveTask(props.task);
  emit('exit');
}

function deleteTask() {
  chore.deleteTask(props.task);
  emit('exit');
}

function removeTag(tag: Tag) {
  props.task.tags = props.task.tags.filter((t: Tag) => t.id !== tag.id);  
}
</script>

<template>
  <div class="task-container">
    <!-- Modal -->
    <Modal :open="open" @exit-modal="$emit('exit')">
      <!-- Tags -->
      <template #tags>
        <Tags :task="props.task" :id="props.task.id" @remove-tag="tag => removeTag(tag)" />
        <div class="buttons">
          <div class="done-buttons" v-auto-animate>
            <DoneIcon @click="$emit('toggleDone')" v-if="!props.task.done" />
            <MarkedDoneIcon @click="$emit('toggleDone')" v-else />
          </div>
          <DeleteIcon @click="deleteTask()" class="delete-icon" />
        </div>
      </template>
      <!-- Title -->
      <template #title>
        <input
          type="text"
          name="title"
          id="task-input-title"
          v-model.lazy="props.task.title"
        />
      </template>
      <!-- Modal -->
      <TaskModalInfo :task="props.task" />
      <template #save-button>
        <AddToProjectPopup :taskId="props.task.id" />
        <SaveButton @click="saveTask()" :disabled="false" />
      </template>
    </Modal>
  </div>
</template>

<style scoped lang="scss">
.delete-icon {
  margin: 0.1rem 0.5rem;
  &:hover,
  &:focus,
  &:active {
    cursor: pointer;
  }
}

.buttons {
  display: flex;
  align-items: baseline;
}

.done-buttons {
  &:hover,
  &:focus,
  &:active {
    cursor: pointer;
  }
}

#task-input-title {
  border: none;
  background: transparent;
  color: white;
  font-size: 2rem;
  font-weight: 700;
  width: 100%;

  &:focus {
    outline: none;
  }
}
</style>
