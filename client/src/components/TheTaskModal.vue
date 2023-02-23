<script setup lang="ts">
import type { ITag, ITask } from '@/types';

const props = defineProps<{
  task: ITask;
  open: boolean;
}>();

// const emit = defineEmits(['exit', 'toggleDone', 'deleteTask']);
const emit = defineEmits<{
  (e: 'exit:modal'): void
  (e: 'toggle:done'): void
  (e: 'delete:task'): void
}>();

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

  emit('exit:modal');
}

function deleteTask() {
  emit('delete:task');
  emit('exit:modal');
}

function removeTag(tag: ITag) {
  props.task.tags = props.task.tags.filter((t: ITag) => t.id !== tag.id);
}

function handleInput(event: any) {
  tmpNewTitle = event.target.value;
}

const handleDesc = (desc: any) => (tmpNewDesc = desc);

const handlePomos = (pomos: number) => (tmpEstimated = pomos);

const width = ref(window.innerWidth);

onMounted(() => {
  window.addEventListener('resize', () => (width.value = window.innerWidth));
});

onUnmounted(() => {
  window.removeEventListener('resize', () => (width.value = window.innerWidth));
});
</script>

<template>
  <div class="task-container">
    <!-- Modal -->
    <AppModal :open="open" @exit:modal="$emit('exit:modal')" :is-task="true">
      <!-- Tags -->
      <template #tags>
        <Tags
          :task="props.task"
          :id="props.task.id"
          @remove:tag="(tag: ITag) => removeTag(tag)"
          @close:modal="$emit('exit:modal')"
        />
        <div class="buttons">
          <div class="done-buttons" v-auto-animate>
            <DoneIcon @click="$emit('toggle:done')" v-if="!props.task.done" />
            <MarkedDoneIcon @click="$emit('toggle:done')" v-else />
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
        @input:description="handleDesc"
        @change:pomoCount="handlePomos($event)"
        @save:task="saveTask()"
      />
      <template #save-button>
        <AddToProjectPopup :taskId="props.task.id" />
        <div class="pomos-done" v-if="width < 480">
          <span>Pomos done: {{ task.gone_through }}</span>
        </div>
        <SaveButton @click="saveTask()" />
      </template>
    </AppModal>
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
      font-weight: 600;
    }
  }
}
</style>
