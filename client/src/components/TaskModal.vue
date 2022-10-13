<script setup lang="ts">
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
let tmpNewTitle = '';
let tmpNewDesc = '';
let tmpEstimated: number;


const chore = useChoreStore();

// Saves task with PUT method
function saveTask() {
  props.task.title = tmpNewTitle !== '' ? tmpNewTitle : props.task.title ;
  props.task.description = tmpNewDesc !== '' ? tmpNewDesc : props.task.description;
  props.task.estimated = tmpEstimated !== null ? tmpEstimated : props.task.estimated;
  chore.saveTask(props.task);
  
  emit('exit');
}

function deleteTask() {
  if (window.confirm('Are you sure?')) {
    chore.deleteTask(props.task);
    emit('exit');
  }
}

function removeTag(tag: Tag) {
  props.task.tags = props.task.tags.filter((t: Tag) => t.id !== tag.id);  
}

function handleInput(event: any) {
  tmpNewTitle = event.target.value;
}

function handleDescription(event: any) {
  tmpNewDesc = event.target.value;
}

const handlePomos = (pomos: number) => tmpEstimated = pomos;
</script>

<template>
  <div class="task-container">
    <!-- Modal -->
    <Modal :open="open" @exit-modal="$emit('exit')" :is-task="true">
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
          @input="event => handleInput(event)"
          :value="props.task.title"
          @keyup.ctrl.enter="saveTask()"
        />
      </template>
      <!-- Modal -->
      <TaskModalInfo 
        :task="props.task"
        @description-input="handleDescription($event)" 
        @decrease-pomos="handlePomos($event)"
        @increase-pomos="handlePomos($event)"
        @saveTask="saveTask()"
      />
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
