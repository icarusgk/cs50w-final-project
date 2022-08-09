<script setup lang="ts">
import EstimatedIcon from '@/components/icons/EstimatedIcon.vue';
import DeleteIcon from '@/components/icons/DeleteIcon.vue';
import TimerSetter from '@/components/TimerSetter.vue';

const props = defineProps(['subtask', 'newSub'])
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
    <div class="options-and-buttons">
      <div class="delete-container">
        <DeleteIcon class="delete-button" v-if="!newSub" @click="$emit('delete')" />
      </div>
      <!-- Estimated Timers and save button -->
      <div class="timers-and-buttons-container">
        <div class="estimated">
          <EstimatedIcon class="icon" />
          <span class="text">Pomos</span>
          <TimerSetter :subtask="subtask" />
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

  // Outer container
  .container {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 100%;
    
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

    // Bottom container
    // Pomos and buttons
    .options-and-buttons {
      display: flex;
      align-items: flex-end;
      justify-content: flex-end;
      
      .delete-container {
          margin-right: 1rem;
          
          .delete-button {
            &:hover, &:focus {
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