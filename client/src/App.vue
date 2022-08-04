<script setup lang="ts">
import SideBar from '@/components/Sidebar.vue'
import UpperMenu from '@/components/UpperMenu.vue'
import { useChoreStore } from '@/stores/chore'
import { useModalStore } from '@/stores/modal'

useChoreStore().fetchAll()
useModalStore().close()
</script>

<template>
  <div class="body">
    <SideBar />
    <div class="menu-and-content" :class="{ blur: useModalStore().isOpened }">
      <UpperMenu class="upper-menu" />
      <router-view></router-view>
    </div>
  </div>
</template>

<style lang="scss">
/* variables */
@import './assets/base.css';

/* Popper theme */
@import './assets/popper-theme.css';

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
  transition: filter 0.1s ease-out;
}

.blur {
  filter: blur(14px);
  pointer-events: none;
}


.body {
  background-color: #212121;
  display: flex;

  .menu-and-content {
    width: 100%;
    display: flex;
    flex-direction: column;

    .upper-menu {
      padding: 2rem 4em 0 0;
      color: white;
    }
  }
}
</style>
