<script setup lang="ts">
import { ref, watch } from 'vue';
import { useModalStore } from '@/stores/modal';
import { useAuthStore } from '@/stores/auth';

import UserIcon from '@/components/icons/UserIcon.vue';
import SettingsIcon from '@/components/icons/SettingsIcon.vue';
import Settings from '@/components/Settings.vue';
import Title from '@/components/Title.vue';
import Modal from '@/components/modals/Modal.vue';
import UserInfo from '@/components/UserInfo.vue';

const userOpen = ref(false);
const settingsOpen = ref(false);
const auth = useAuthStore();

watch([() => userOpen.value, () => settingsOpen.value], () => {
  useModalStore().toggle();
});
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
            @click="
              auth.isAuthenticated ? (userOpen = true) : (userOpen = false)
            "
          >
            <div class="user-info" v-if="auth.isAuthenticated">
              <UserIcon />
              <span>{{ auth.user?.username }}</span>
            </div>
          </div>
          <div v-if="!auth.isAuthenticated" class="user-actions-container">
            <div @click="$router.push('/login')">
              <span class="login-btn">Login</span>
            </div>
            <div @click="$router.push('/register')">
              <span class="register-btn">Register</span>
            </div>
          </div>
        </div>
      </li>
      <!-- Settings -->
      <li @click="settingsOpen = true" v-if="auth.isAuthenticated">
        <SettingsIcon />
      </li>
    </ul>
    <Modal :open="userOpen" @exit-modal="userOpen = false">
      <template #title>
        <h1>User</h1>
      </template>
      <UserInfo />
    </Modal>
    <Modal :open="settingsOpen" @exit-modal="settingsOpen = false">
      <template #title>
        <h1>Settings</h1>
      </template>
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
    list-style-type: none;
    margin-block: 0 0;
    margin-inline: 0 0;
    padding-inline-start: 0px;

    li {
      display: inline-block;
      margin-right: 0.1rem;

      &:hover,
      &:focus,
      &:active {
        cursor: pointer;
      }

      .login {
        display: flex;
        align-items: center;

        .user-info {
          display: flex;
          align-items: center;
          margin-right: 1rem;
        }

        .user-actions-container {
          display: flex;
          gap: 1rem;
          margin-top: 1.5rem;

          .login-btn {
            padding: 0.8rem 1rem;
            border-radius: 10px;
            transition: background-color 0.25s ease-in-out;

            &:hover {
              background-color: rgb(60, 60, 60);
            }
          }

          .register-btn {
            background-color: rgb(60, 60, 60);
            padding: 0.8rem 1rem;
            border-radius: 10px;
            transition: background-color 0.25s ease-in-out;

            &:hover {
              background-color: var(--vivid-red);
            }
          }
        }
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
        margin-left: -8px;
        margin-right: 10px;
        #streaks-icon {
          display: none;
        }
      }
    }
  }
}

@media (max-width: 480px) {
  #icons {
    ul {
      li {
        transform: scale(0.7);
        margin-right: -0.8rem;
        .login {
          .user-info {
            margin-right: 0;
            }
        }
      }
    }
  }
}
</style>
