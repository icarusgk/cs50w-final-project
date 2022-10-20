<script setup>
import { ref, reactive } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { useTimerStore } from '@/stores/timer';
import { useAlertStore } from '@/stores/alerts';
import axios from 'axios';
import DeleteIcon from '@/components/icons/DeleteIcon.vue';
import Popper from 'vue3-popper';

const auth = useAuthStore();
const timer = useTimerStore();
const alert = useAlertStore();

const modes = ref(JSON.parse(localStorage.getItem('modes') || '[]'));
const currentMode = ref(JSON.parse(localStorage.getItem('timer') || '{}'));
const showForm = ref(false);

const newMode = reactive({
  name: '',
  pomo: 25,
  short_break: 5,
  long_break: 15,
});

// Live updates
function changeAutoStartPomos() {
  axios.patch(`users/${auth.user?.id}/`, {
    auto_start_pomos: auth.user?.auto_start_pomos,
  });
}

function changeAutoStartBreaks() {
  axios.patch(`users/${auth.user?.id}/`, {
    auto_start_breaks: auth.user?.auto_start_breaks,
  });
}

async function changeMode(id) {
  const { status, data } = await axios.post('currentMode/', {
    mode_id: id,
  });

  if (status === 200) {
    timer.setNewTimer(data);
    currentMode.value = data;
  }
}

async function deleteMode(id) {
  const { status } = await axios.delete(`modes/${id}/`);

  if (status === 204) {
    const deletedMode = modes.value.find((mode) => mode.id === id);
    modes.value = modes.value.filter((mode) => mode.id !== deletedMode.id);

    localStorage.setItem('modes', JSON.stringify(modes.value));

    const current = JSON.parse(localStorage.getItem('timer'));
    alert.success('Timer deleted!');

    // If the deleted mode was the current one
    if (current.id === deletedMode.id) {
      // Successfully sets to default
      timer.setToDefault();
      // Reactive current mode
      // This value gets assigned in chore.ts
      currentMode.value.name = 'Default';
    }
  }
}

async function createMode() {
  const { status, data } = await axios.post('modes/', newMode);

  if (status === 200) {
    modes.value.push(data);
    localStorage.setItem('modes', JSON.stringify(modes.value));

    changeMode(data.id);

    showForm.value = false;
  }
}

function backToDefault() {
  timer.setToDefault();
  currentMode.value.name = 'Default';
}
</script>

<template>
  <div>
    <div>
      <input
        type="checkbox"
        id="auto_start_pomos"
        @change="changeAutoStartPomos"
        v-model="auth.user.auto_start_pomos"
      />
      <label for="auto_start_pomos">Auto start pomos</label>
    </div>
    <div>
      <input
        type="checkbox"
        id="auto_start_breaks"
        @change="changeAutoStartBreaks()"
        v-model="auth.user.auto_start_breaks"
      />
      <label for="auto_start_breaks">Auto start breaks</label>
    </div>
    <div v-if="Object.keys(modes).length > 0">
      <button class="back-to-default-button" @click="backToDefault()">
        Back to default
      </button>
      <p>Change mode:</p>
      <div v-for="mode in modes" :key="mode.name">
        <Popper placement="right" hover>
          <div class="mode-radio-input">
            <input
              type="radio"
              id="two"
              :value="mode.name"
              @change="changeMode(mode.id)"
              v-model="currentMode.name"
            />
            <label :for="mode.name">{{ mode.name }}</label>
            <div @click="deleteMode(mode.id)" class="delete-icon">
              <DeleteIcon />
            </div>
          </div>
          <template #content>
            <div>
              <div class="mode-info">
                <span><strong>Pomo:</strong> {{ mode.pomo }} min</span>
                <span
                  ><strong>Short Rest:</strong> {{ mode.short_break }} min</span
                >
                <span
                  ><strong>Long Rest:</strong> {{ mode.long_break }} min</span
                >
              </div>
            </div>
          </template>
        </Popper>
      </div>
    </div>
    <button
      v-if="modes.length < 3"
      class="new-mode-button"
      @click="showForm = !showForm"
    >
      {{ showForm ? 'Close' : 'Create a new Mode' }}
    </button>
    <div v-if="showForm">
      <p style="font-weight: 600; font-size: 2rem">Create new mode</p>
      <form @submit.prevent="createMode()">
        <div class="">
          <span>Name:</span>
          <input
            class="name-input"
            v-model="newMode.name"
            type="text"
            placeholder="New mode name"
          />
        </div>
        <div class="modes">
          <div class="mode-container">
            <span>Pomo:</span>
            <input v-model="newMode.pomo" type="number" class="mode-input" />
          </div>
          <div class="mode-container">
            <span>Short rest:</span>
            <input
              v-model="newMode.short_break"
              type="number"
              class="mode-input"
            />
          </div>
          <div class="mode-container">
            <span>Long rest:</span>
            <input
              v-model="newMode.long_break"
              type="number"
              class="mode-input"
            />
          </div>
        </div>
        <input class="create-mode-button" type="submit" value="Create" />
      </form>
    </div>
  </div>
</template>

<style scoped lang="scss">
@mixin btn($color, $padding) {
  border: none;
  background: $color;
  border-radius: 10px;
  margin-top: 1rem;
  padding: $padding;
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

.back-to-default-button {
  @include btn(white, 0.5rem);
  margin-bottom: 1rem;
}

.mode-radio-input {
  display: flex;

  input[type='radio'] {
    margin-right: 1rem;
  }

  .delete-icon {
    margin-left: 1rem;

    &:hover,
    &:focus,
    &:active {
      cursor: pointer;
    }
  }
}
.mode-info {
  display: flex;
  flex-direction: column;
}
.new-mode-button {
  @include btn(white, 0.8rem);
}

.create-mode-button {
  @include btn(#ff4f5f, 0.8rem);
  color: white;
  width: 100%;
}

.name-input {
  margin-top: 2px;
  height: 1.5rem;
  outline: none;
  border: none;
  border-radius: 4px;
  padding: 1px 8px;
  width: 10rem;
  background: rgb(87, 87, 87);
  color: white;
  margin-left: 0.5rem;
}
.modes {
  display: flex;

  .mode-container {
    display: flex;
    flex-direction: column;
  }

  .mode-input {
    margin-top: 2px;
    height: 1.5rem;
    outline: none;
    border: none;
    border-radius: 4px;
    padding: 1px 8px;
    width: 6rem;
    margin-right: 1rem;
    background: rgb(87, 87, 87);
    color: white;
  }
}
</style>
