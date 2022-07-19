<script setup lang="ts">
import EstimatedIcon from './icons/EstimatedIcon.vue';

const props = defineProps(['subtask'])
</script>

<template>
<!-- Blur -->
<div class="subtask">
  <!-- Flex row -->
  <div class="container">
    <!-- Title and description -->
    <div class="title-and-description-container">
      <!-- Title -->
      <input 
        v-model.lazy="props.subtask.title" 
        placeholder="Title" 
        type="text"
        class="new-subtask-title"
      />
      <!-- Description -->
      <textarea 
        v-model.lazy.trim="props.subtask.description" 
        class="new-subtask-description" 
        placeholder="Description">
      </textarea>
    </div>
    <!-- Estimated Timers and save button -->
    <div class="timers-and-buttons-container">
      <div class="timers">
        <!-- Icon -->
        <EstimatedIcon />
        <!-- Number -->
        <input type="number" class="estimated-timers" :value="subtask.estimated" />
      </div>
      <!-- Buttons -->
      <div class="buttons">
        <!-- Emit the close event -->
        <!-- Cancel -->
        <button @click="$emit('close')" class="cancel-button">Cancel</button>
        <!-- Save -->
        <button @click="$emit('save')" class="save-button">Save!</button>
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
  &:hover, &:focus {
    cursor: pointer;
  }
}
.subtask {
  padding: 1rem;
  background-color: rgba(58, 58, 58, 0.7);
  border-radius: 10px;
  height: 8rem;

  // Outer container
  .container {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    height: 100%;
    
    // Left inner container
    .title-and-description-container {
      display: flex;
      flex-direction: column;
      width: 80%;

      .new-subtask-title {
        border: none;
        background: transparent;
        color: white;
        font-size: 1.5rem;
        font-weight: 900;
        font-family: sans-serif;
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
        font-family: sans-serif;
        border: none;
        resize: none;
      }
    }

    // Right inner container
    .timers-and-buttons-container {
      display: flex;
      flex-direction: column;
      justify-content: space-between;

      .timers {
        display: flex;
        justify-content: flex-end;

        .estimated-timers {
          background: transparent;
          border: none;
          color: white;
          width: 10%;
          outline: none;
          font-weight: 700;
          margin-left: 1rem;
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
</style>