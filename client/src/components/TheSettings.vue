<script setup>
const auth = useAuthStore();
const timer = useTimerStore();
const alert = useAlertStore();

const modes = ref(JSON.parse(localStorage.getItem('modes') || '[]'));
const currentMode = ref(JSON.parse(localStorage.getItem('timer') || '{}'));
const showForm = ref(false);

const newMode = ref({
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

function resetMode() {
  newMode.value = {
    name: '',
    pomo: 25,
    short_break: 5,
    long_break: 15,
  };
}

async function changeMode(id) {
  const { status, data } = await axios.post('currentMode/', {
    mode_id: id,
  });

  if (status === 200) {
    timer.setNewTimer(data);
    currentMode.value = data;
    timer.current = 'pomo';
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
  const { status, data } = await axios.post('modes/', newMode.value);

  if (status === 201) {
    modes.value.push(data);
    localStorage.setItem('modes', JSON.stringify(modes.value));

    if (!timer.ongoing) {
      changeMode(data.id);
    }
    resetMode();
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
        id="auto-start-pomos"
        class="mr-4"
        @change="changeAutoStartPomos"
        v-model="auth.user.auto_start_pomos"
      />
      <label for="auto-start-pomos">Auto start pomos</label>
    </div>
    <div>
      <input
        type="checkbox"
        id="auto-start-breaks"
        class="mr-4"
        @change="changeAutoStartBreaks()"
        v-model="auth.user.auto_start_breaks"
      />
      <label for="auto-start-breaks">Auto start breaks</label>
    </div>
    <div v-if="Object.keys(modes).length > 0">
      <button class="mb-4 back-to-default-btn settings-btn text-gray-700" @click="backToDefault()">
        Back to default
      </button>
      <p>Change mode:</p>
      <div v-for="mode in modes" :key="mode.name">
        <Popper placement="right" hover>
          <div class="flex">
            <input
              type="radio"
              id="two"
              class="mr-4"
              :value="mode.name"
              @change="changeMode(mode.id)"
              v-model="currentMode.name"
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
      v-if="modes.length < 3"
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
