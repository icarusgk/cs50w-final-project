<script setup lang="ts">
import SideBar from '@/components/Sidebar.vue'
import UpperMenu from '@/components/UpperMenu.vue'
import { useChoreStore } from '@/stores/chore'
import { useModalStore } from '@/stores/modal'
import { useAuthStore } from '@/stores/auth';

useModalStore().close()

const auth = useAuthStore()

if (auth.isAuthenticated) {
  auth.getUser()
  useChoreStore().fetchAll()
}
</script>

<template>
  <SideBar />
  <div class="body">
    <div class="menu-and-content" :class="{ blur: useModalStore().isOpened }">
      <UpperMenu class="upper-menu" />
      <router-view @vnodeUpdated="useModalStore().close()"></router-view>
    </div>
  </div>
</template>

<style lang="scss">
/* variables */
@import './assets/base.css';

/* Popper theme */
@import './assets/popper-theme.css';

/* Fonts */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800;900&display=swap');
* {
  font-family: 'Poppins';
}

/* Chrome, Safari, Edge, Opera */
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

/* Firefox */
input[type=number] {
  -moz-appearance: textfield;
}

/* Resets */
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
  transition: filter 0.15s ease-out;
}

html {
  background-color: #212121;
}

.blur {
  filter: blur(14px);
  pointer-events: none;
}


.body {
  display: flex;
  margin-left: 130px;

  .menu-and-content {
    width: 100%;
    display: flex;
    flex-direction: column;

    .upper-menu {
      padding: 2rem 3rem;
      color: white;
    }
  }
}


@media (max-width: 768px) {
.body {
  margin-left: 0;
  margin-bottom: 140px;

  .menu-and-content {
    padding: 0.5rem;
    .upper-menu {
      padding: 0;
    }
  }
}

.blur {
  filter: blur(60px);
}

  * {
    touch-action: manipulation;
  }
}
</style>
