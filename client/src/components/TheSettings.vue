<script setup lang="ts">
import type { ITimer } from '@/types';
import { local } from '@/utils';

const auth = useAuthStore();
const timer = useTimerStore();
const alert = useAlertStore();

const showForm = ref(false);

const newMode = ref<ITimer>({
  name: '',
  pomo: 25,
  short_break: 5,
  long_break: 15,
});

// Live updates
async function toggleAutoStartPomos() {
  const { data, status } = await axios.patch(`users/${auth.user?.id}/`, {
    auto_start_pomos: !auth.user?.auto_start_pomos
  });

  if (status === 200 && auth.user) { 
    auth.user.auto_start_pomos = data.auto_start_pomos;
    alert.info(`Auto start pomos set to ${data.auto_start_pomos}`);  }
}

async function toggleAutoStartBreaks() {
  const { data, status } = await axios.patch(`users/${auth.user?.id}/`, {
    auto_start_breaks: !auth.user?.auto_start_breaks
  });  

  if (status === 200 && auth.user) {
    auth.user.auto_start_breaks = data.auto_start_breaks;
    alert.info(`Auto start breaks set to ${data.auto_start_breaks}`);
  }
}

function resetMode() {
  newMode.value = {
    name: '',
    pomo: 25,
    short_break: 5,
    long_break: 15,
  };
}

async function changeMode(mode: ITimer) {
  const { data, status } = await axios.post('currentMode', {
    mode_id: mode.id,
  });
  if (status === 200) timer.setNewTimer(data);
}

async function deleteMode(id?: number) {
  const { status } = await axios.delete(`modes/${id}/`);

  if (status === 204) {
    const deletedMode = timer.modes.find((mode: ITimer) => mode.id === id);

    if (deletedMode) {
      timer.modes = timer.modes.filter((mode: ITimer) => mode.id !== deletedMode.id);
      local.set('modes', timer.modes);

      const current = local.get('timer')
      alert.success('Timer deleted!');

      // If the deleted mode was the current one
      if (current.id === deletedMode.id) {
        // Successfully sets to default
        timer.setToDefault();
      }
    }    
  }
}

async function createMode() {
  const { status, data } = await axios.post('modes/', newMode.value);

  if (status === 201) {
    timer.modes.push(data);
    local.set('modes', timer.modes)

    if (!timer.isRunning) changeMode(data);
    
    resetMode();
    showForm.value = false;
  }
}

function backToDefault() {
  timer.setToDefault();
}
</script>

<template>
  <div>
    <div>
      <input
        type="checkbox"
        id="auto-start-pomos"
        class="mr-4"
        @change="toggleAutoStartPomos()"
        :checked="auth.user?.auto_start_pomos"
      />
      <label for="auto-start-pomos">Auto start pomos</label>
    </div>
    <div>
      <input
        type="checkbox"
        id="auto-start-breaks"
        class="mr-4"
        @change="toggleAutoStartBreaks()"
        :checked="auth.user?.auto_start_breaks"
      />
      <label for="auto-start-breaks">Auto start breaks</label>
    </div>
    <div v-if="Object.keys(timer.modes).length > 0">
      <button class="mb-4 back-to-default-btn settings-btn text-gray-700" @click="backToDefault()">
        Back to default
      </button>
      <p>Change mode:</p>
      <div v-for="mode in timer.modes" :key="mode.id">
        <Popper placement="right" hover>
          <div class="flex">
            <input
              type="radio"
              id="two"
              class="mr-4"
              :value="mode"
              @change="changeMode(mode)"
              v-model="timer.currentMode"
            />
            <label :for="mode.name">{{ mode.name }}</label>
            <div @click="deleteMode(mode.id)" class="ml-4 pointer i-fluent-delete-48-filled scale-125 self-center" />
          </div>
          <template #content>
            <div>
              <div class="flex flex-col">
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
      v-if="timer.modes.length < 3"
      class="new-mode-btn settings-btn text-gray-700"
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
            class="mt-[2px] h-6 outline-none border-none rounded-md py-[1px] px-[8px] w-40 bg-[rgb(87,87,87)] text-white ml-2"
            v-model="newMode.name"
            type="text"
            placeholder="New mode name"
          />
        </div>
        <div class="flex">
          <div class="flex flex-col">
            <span>Pomo:</span>
            <input v-model="newMode.pomo" type="number" class="<sm:w-4/5 <sm:mr-2 mt-[2px] h-6 outline-none border-none rounded-md py-[1px] px-[8px] bg-[rgb(87,87,87)] text-white mr-4 w-24" />
          </div>
          <div class="flex flex-col">
            <span>Short rest:</span>
            <input
              v-model="newMode.short_break"
              type="number"
              class="<sm:w-4/5 <sm:mr-2 mt-[2px] h-6 outline-none border-none rounded-md py-[1px] px-[8px] bg-[rgb(87,87,87)] text-white mr-4 w-24"
            />
          </div>
          <div class="flex flex-col">
            <span>Long rest:</span>
            <input
              v-model="newMode.long_break"
              type="number"
              class="<sm:w-4/5 <sm:mr-2 mt-[2px] h-6 outline-none border-none rounded-md py-[1px] px-[8px] bg-[rgb(87,87,87)] text-white mr-4 w-24"
            />
          </div>
        </div>
        <input class="create-mode-btn settings-btn text-white w-full" type="submit" value="Create" />
      </form>
    </div>
  </div>
</template>
