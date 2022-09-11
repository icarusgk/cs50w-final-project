<script setup lang="ts">
import { ref, watch, computed } from 'vue';
import { useModalStore } from '@/stores/modal';
import { useAuthStore } from '@/stores/auth';

import StreaksIcon from '@/components/icons/StreaksIcon.vue';
import UserIcon from '@/components/icons/UserIcon.vue';
import SettingsIcon from '@/components/icons/SettingsIcon.vue';
import Title from './Title.vue';
import Modal from './modals/Modal.vue';
const open = ref(false);
const auth = useAuthStore();

watch(
  () => open.value,
  () => {
    useModalStore().toggle();
  }
);
</script>

<template>
  <div id="icons">
    <Title />
    <ul>
      <!-- Four icons -->
      <!-- Streaks -->
      <li>
        <div v-if="auth.isAuthenticated" id="streaks-icon">
          <StreaksIcon />
          <p id="streaks-days-info">{{ auth.user?.streak }} days</p>
        </div>
      </li>
      <!-- User -->
      <li>
        <div class="login">
          <div
            class="login"
            @click="auth.isAuthenticated ? (open = true) : (open = false)"
          >
            <UserIcon />
            <span v-if="auth.user">{{ auth.user?.username }}</span>
          </div>
          <span v-if="!auth.isAuthenticated" @click="$router.push('/login')"
            >Login</span
          >
        </div>
      </li>
      <!-- Settings -->
      <li v-if="auth.isAuthenticated"><SettingsIcon /></li>
    </ul>
    <Modal :open="open" @exit-modal="open = false">
      <div>
        <h1>Logout</h1>
        <h2>Hello there {{ auth.user?.username }}</h2>
        <h2>Your current streak is of {{ auth.user?.streak }} days</h2>
        <button
          id="logout-btn"
          @click="
            auth.logout();
            open = false;
          "
        >
          Logout
        </button>
      </div>
    </Modal>
  </div>
</template>

<style lang="scss" scoped>
#icons {
  display: flex;
  justify-content: space-between;

  ul {
    text-align: right;

    li {
      display: inline-block;
      margin-right: 0.1rem;

      &:hover,
      &:focus {
        cursor: pointer;
      }

      .login {
        display: flex;
        align-items: center;
      }

      #streaks-icon {
        display: flex;
        align-items: center;
        margin-right: 2rem;

        #streaks-days-info {
          margin-left: 1rem;
          font-weight: bold;
        }
      }
    }
  }
}

#logout-btn {
  padding: 0.5rem 1rem;
  border-radius: 8px;
  border: none;
  background-color: var(--vivid-red);
  color: white;
  font-weight: 500;
  transition: background-color 0.15s ease-in;

  &:hover {
    cursor: pointer;
    background-color: #ff4b4b9f;
  }
}

@media (max-width: 1160px) {
  #icons {
    ul {
      text-align: left;

      li {
        transform: scale(0.7);
        margin-left: -8px;

        #streaks-icon {
          display: none;
        }
      }
    }
  }
}
</style>
