<script setup lang="ts">
import type { ITag, ITask } from '@/types';
const props = defineProps<{
  chore: ITask;
  newChore: boolean;
  isProject: boolean;
  parentNew: boolean;
}>();

defineEmits<{
  (e: 'save:project'): void;
  (e: 'save:task'): void;
  (e: 'close:details'): void;
  (e: 'delete:chore'): void;
  (e: 'remove:chore'): void;
  (e: 'remove:tag', tag: ITag): void;
  (e: 'change:title', newTitle: string): void;
  (e: 'change:description', newDescription: string): void;
  (e: 'change:pomoCount', pomoCount: number): void;
}>();
</script>

<template>
  <!-- Blur -->
  <div class="subtask">
    <!-- Flex row -->
    <div class="container">
      <div v-if="props.isProject" class="subtask-tags">
        <Tags
          :id="props.chore.id"
          :task="props.chore"
          :new="newChore"
          @remove:tag="$emit('remove:tag', $event)"
        />
      </div>
      <!-- Title and description -->
      <div class="title-and-description-container">
        <!-- Title -->
        <input
          :value="props.chore.title"
          @input="event => $emit('change:title', (event.target as HTMLInputElement).value)"
          placeholder="Title"
          type="text"
          autofocus
          class="new-subtask-title"
          @keyup.ctrl.enter="
            isProject ? $emit('save:task') : $emit('save:project')
          "
        />
        <!-- Description -->
        <textarea
          :value="props.chore.description"
          @input="event => $emit('change:description', (event.target as HTMLInputElement).value)"
          class="new-subtask-description"
          placeholder="Description"
          @keyup.ctrl.enter="
            isProject ? $emit('save:task') : $emit('save:project')
          "
        >
        </textarea>
      </div>
      <div class="options-and-buttons">
        <div class="delete-container">
          <DeleteIcon
            class="delete-button"
            v-if="!newChore"
            @click="$emit('delete:chore')"
          />
          <DeleteIcon v-if="newChore && parentNew" @click="$emit('remove:chore')" />
        </div>
        <div v-if="props.isProject">
          <PomoCountSetter
            :chore="chore"
            @change:pomoCount="(count: number) => $emit('change:pomoCount', count)"
          />
        </div>
        <!-- Estimated Timers and save button -->
        <div class="buttons-container">
          <!-- Buttons -->
          <div class="buttons">
            <!-- Emit the close event -->
            <!-- Cancel -->
            <button @click="$emit('close:details')" class="cancel-button">Close</button>
            <!-- Save -->
            <button
              v-if="!isProject"
              @click="$emit('save:project')"
              class="save-button"
            >
              Save!
            </button>
            <button v-else class="save-button" @click="$emit('save:task')">
              Save!
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
@mixin btn($color) {
  background-color: $color;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  border: none;
  box-shadow: 0 3px 0 1px darken($color, 20%);
  transition: box-shadow 0.2s cubic-bezier(0.075, 0.82, 0.165, 1);

  &:hover,
  &:focus,
  &:active {
    cursor: pointer;
  }

  &:active {
    box-shadow: 0 0 $color;
  }
}
.subtask {
  padding: 1rem;
  background-color: rgba(58, 58, 58, 0.7);
  border-radius: 10px;

  // Outer container
  .container {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 100%;

    .subtask-tags {
      display: flex;
    }

    // First container
    // Title and desc
    .title-and-description-container {
      display: flex;
      flex-direction: column;

      .new-subtask-title {
        border: none;
        background: transparent;
        color: white;
        font-size: 1.5rem;
        font-weight: 700;
        width: 100%;

        &:focus {
          outline: none;
        }
      }
      .new-subtask-description {
        width: 100%;
        height: 50px;
        outline: none;
        background-color: transparent;
        color: white;
        border: none;
        resize: none;
      }
    }

    // Bottom container
    // Pomos and buttons
    .options-and-buttons {
      display: flex;
      align-items: center;
      justify-content: flex-end;

      .delete-container {
        margin-right: 1rem;

        .delete-button {
          &:hover,
          &:focus,
          &:active {
            cursor: pointer;
          }
        }
      }

      .buttons-container {
        display: flex;
        flex-direction: column;
        align-self: flex-end;

        width: 150px;

        .estimated {
          display: flex;
          flex-direction: row;
          align-items: center;
          margin-bottom: 0.5rem;

          .icon {
            padding-top: 3px;
            width: 25px;
          }

          .text {
            font-size: 0.75rem;
          }
        }

        .buttons {
          display: flex;
          justify-content: flex-end;
          .cancel-button {
            @include btn(#636363);
            margin-right: 0.5rem;
          }
          .save-button {
            @include btn(#ed4747);
          }
        }
      }
    }
  }
}
</style>
