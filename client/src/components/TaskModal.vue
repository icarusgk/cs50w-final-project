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

const task = ref(props.task);
const pristine = ref(true);
const chores = useChoreStore();

// Saves task with PUT method
function saveTask() {
  chores.saveTask(props.task);
  emit('exit');
}

function deleteTask() {
  chores.deleteTask(task.value);
  emit('exit');
}

function checkPristine(description: string) {
  pristine.value = description === props.task.description;
}

function removeTag(tag: Tag) {
  task.value.tags = task.value.tags.filter((t: Tag) => t.id !== tag.id);  
}
</script>

<template>
  <div class="task-container">
    <!-- Modal -->
    <Modal :open="open" @exit-modal="$emit('exit')">
      <!-- Tags -->
      <template #tags>
        <Tags :task="task" :id="task.id" @remove-tag="tag => removeTag(tag)" />
        <div class="done-buttons" v-auto-animate>
          <DoneIcon @click="$emit('toggleDone')" v-if="!props.task.done" />
          <MarkedDoneIcon @click="$emit('toggleDone')" v-else />
        </div>
        <DeleteIcon @click="deleteTask()" class="delete-icon" />
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
      <TaskModalInfo :task="task" @description-change="checkPristine" />
      <template #save-button>
        <AddToProjectPopup :taskId="task.id" />
        <SaveButton @click="saveTask()" :disabled="false" />
      </template>
    </Modal>
  </div>
</template>

<style scoped lang="scss">
.delete-icon {
  margin: 0.1rem 0.5rem;
  &:hover,
  &:focus {
    cursor: pointer;
  }
}

.done-buttons {
  &:hover, &:focus {
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
