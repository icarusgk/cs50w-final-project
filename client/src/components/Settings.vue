<script setup>
import { ref, reactive } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { useTimerStore } from '@/stores/timer';
import axios from 'axios';

const auth = useAuthStore();
const timer = useTimerStore();

const modes = ref(JSON.parse(localStorage.getItem('modes') || '[]'));
const currentMode = ref(JSON.parse(localStorage.getItem('timer') || '{}'));
const showForm = ref(false);

const newMode = reactive({
  name: 'New mode name',
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
    <h1>Settings</h1>
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
      <button @click="backToDefault()">Back to default</button>
      <p>Change mode:</p>
      <div v-for="mode in modes" :key="mode.name">
        <input
          type="radio"
          id="two"
          :value="mode.name"
          @change="changeMode(mode.id)"
          v-model="currentMode.name"
        />
        <label :for="mode.name">{{ mode.name }}</label>
        <div
          v-if="currentMode.name === mode.name"
          class="details"
        >
          <span>Pomo: {{ mode.pomo }}</span>
          <span>Pomo: {{ mode.short_break }}</span>
          <span>Pomo: {{ mode.long_break }}</span>
        </div>
        <button 
          v-if="mode.name !== 'Default'"
          @click="deleteMode(mode.id)"
        >
          delete
        </button>
      </div>
    </div>
    <button @click="showForm = true">Create a new Mode</button>
    <div v-if="showForm">
      <p style="font-weight: 600; font-size: 2rem">Create new mode</p>
      <form @submit.prevent="createMode()">
        <div>
          <span>Name:</span>
          <input v-model="newMode.name" type="text" />
        </div>
        <div>
          <span>Pomo:</span>
          <input v-model="newMode.pomo" type="number" />
        </div>
        <div>
          <span>Short rest:</span>
          <input v-model="newMode.short_break" type="number" />
        </div>
        <div>
          <span>Long rest:</span>
          <input v-model="newMode.long_break" type="number" />
        </div>
        <input type="submit" value="Create" />
      </form>
    </div>
  </div>
</template>

<style></style>
