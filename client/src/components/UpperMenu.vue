<script setup lang="ts">
import { ref, watch } from 'vue';
import { useModalStore } from '@/stores/modal';
import { useAuthStore } from '@/stores/auth';

import UserIcon from '@/components/icons/UserIcon.vue';
import SettingsIcon from '@/components/icons/SettingsIcon.vue';
import Settings from './Settings.vue';
import Title from './Title.vue';
import Modal from './modals/Modal.vue';
import UserInfo from './UserInfo.vue';

const userOpen = ref(false);
const settingsOpen = ref(false);
const auth = useAuthStore();

watch([
  () => userOpen.value,
  () => settingsOpen.value,
  ],
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
      <!-- User -->
      <li>
        <div class="login">
          <div
            class="login"
            @click="auth.isAuthenticated ? (userOpen = true) : (userOpen = false)"
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
      <li @click="settingsOpen = true" v-if="auth.isAuthenticated">
        <SettingsIcon />
      </li>
    </ul>
    <Modal :open="userOpen" @exit-modal="userOpen = false">
      <UserInfo />
    </Modal>
    <Modal :open="settingsOpen" @exit-modal="settingsOpen = false">
      <Settings />
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
