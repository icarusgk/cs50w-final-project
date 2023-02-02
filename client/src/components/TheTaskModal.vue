<script setup lang="ts">
import type { TagType, TaskType } from '@/types';

import Tags from '@/components/buttons/Tags.vue';
import Modal from '@/components/AppModal.vue';
import TheTaskModalBody from '@/components/TheTaskModalBody.vue';
import SaveButton from '@/components/buttons/SaveButton.vue';
import DeleteIcon from '@/components/icons/DeleteIcon.vue';
import AddToProjectPopup from '@/components/AddToProjectPopup.vue';
import DoneIcon from '@/components/icons/DoneIcon.vue';
import MarkedDoneIcon from '@/components/icons/MarkedDoneIcon.vue';

const props = defineProps<{
  task: TaskType;
  open: boolean;
}>();

const emit = defineEmits(['exit', 'toggleDone', 'deleteTask']);
let tmpNewTitle = '';
let tmpNewDesc = '';
let tmpEstimated: number;

const chore = useChoreStore();

// Saves task with PUT method
function saveTask() {
  props.task.title = tmpNewTitle !== '' ? tmpNewTitle : props.task.title;
  props.task.description =
    tmpNewDesc !== '' ? tmpNewDesc : props.task.description;
  props.task.estimated =
    tmpEstimated !== null ? tmpEstimated : props.task.estimated;

  chore.saveTask(props.task);

  emit('exit');
}

function deleteTask() {
  emit('deleteTask');
  emit('exit');
}

function removeTag(tag: TagType) {
  props.task.tags = props.task.tags.filter((t: TagType) => t.id !== tag.id);
}

function handleInput(event: any) {
  tmpNewTitle = event.target.value;
}

const handleDesc = (desc: any) => (tmpNewDesc = desc);

const handlePomos = (pomos: number) => (tmpEstimated = pomos);

const width = ref(window.innerWidth);

onMounted(() => {
  window.addEventListener('resize', () => width.value = window.innerWidth);
});

onUnmounted(() => {
  window.removeEventListener('resize', () => width.value = window.innerWidth)
});
</script>

<template>
  <div class="task-container">
    <!-- Modal -->
    <Modal :open="open" @exit-modal="$emit('exit')" :is-task="true">
      <!-- Tags -->
      <template #tags>
        <Tags
          :task="props.task"
          :id="props.task.id"
          @remove-tag="(tag) => removeTag(tag)"
          @close="$emit('exit')"
        />
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
          @input="(event) => handleInput(event)"
          :value="props.task.title"
          @keyup.ctrl.enter="saveTask()"
        />
      </template>
      <!-- Body -->
      <TheTaskModalBody
        :task="props.task"
        @description-input="handleDesc"
        @newPomoCount="handlePomos($event)"
        @saveTask="saveTask()"
      />
      <template #save-button>
        <AddToProjectPopup :taskId="props.task.id" />
        <div class="pomos-done" v-if="width < 480">
          <span>Pomos done: {{ task.gone_through }}</span>
        </div>
        <SaveButton @click="saveTask()" />
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

@media (max-width: 480px) {
  .pomos-done {
    text-align: center;
    span {
      font-size: 1.2rem;
      font-weight: 600;;
    }
  }
}
</style>
