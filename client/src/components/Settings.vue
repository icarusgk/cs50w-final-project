<script setup>
import { useAuthStore } from '@/stores/auth';
import axios from 'axios';

const auth = useAuthStore();

// Live updates
function changeAutoStartPomos() {
  axios.patch(`users/${auth.user?.id}/`, {
    auto_start_pomos: auth.user.auto_start_pomos,
  });
}

function changeAutoStartBreaks() {
  axios.patch(`users/${auth.user?.id}/`, {
    auto_start_breaks: auth.user.auto_start_breaks,
  });
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
  </div>
</template>

<style></style>
