<script setup lang="ts">
import DeleteIcon from '@/components/icons/DeleteIcon.vue';
import TimerSetter from '@/components/TimerSetter.vue';
import Tags from './buttons/Tags.vue';

const props = defineProps(['chore', 'newChore', 'isProject', 'parentNew']);
defineEmits(['save', 'saveTask', 'close', 'delete', 'remove']);
// const chore = ref(props.chore)
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
        />
      </div>
      <!-- Title and description -->
      <div
        class="title-and-description-container"
        @keyup.ctrl.enter="$emit('save')"
      >
        <!-- Title -->
        <input
          v-model.lazy="props.chore.title"
          placeholder="Title"
          type="text"
          class="new-subtask-title"
        />
        <!-- Description -->
        <textarea
          v-model.trim="props.chore.description"
          class="new-subtask-description"
          placeholder="Description"
        >
        </textarea>
      </div>
      <div class="options-and-buttons">
        <div class="delete-container">
          <DeleteIcon
            class="delete-button"
            v-if="!newChore"
            @click="$emit('delete')"
          />
          <DeleteIcon v-if="newChore && parentNew" @click="$emit('remove')" />
        </div>
        <div v-if="props.isProject">
          <TimerSetter :chore="chore" />
        </div>
        <!-- Estimated Timers and save button -->
        <div class="timers-and-buttons-container">
          <!-- Buttons -->
          <div class="buttons">
            <!-- Emit the close event -->
            <!-- Cancel -->
            <button @click="$emit('close')" class="cancel-button">
              Cancel
            </button>
            <!-- Save -->
            <button
              v-if="!isProject"
              @click="$emit('save')"
              class="save-button"
            >
              Save!
            </button>
            <button v-else class="save-button" @click="$emit('saveTask')">
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
  background-color: var($color);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  border: none;
  &:hover,
  &:focus,
  &:active {
    cursor: pointer;
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

      .timers-and-buttons-container {
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
            @include btn(--gray);
            margin-right: 0.5rem;
          }
          .save-button {
            @include btn(--vivid-red);
          }
        }
      }
    }
  }
}
</style>
