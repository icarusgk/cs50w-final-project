<script setup lang="ts">
import SideBar from '@/components/Sidebar.vue'
import UpperMenu from '@/components/UpperMenu.vue'
import { useChoreStore } from '@/stores/chore'

useChoreStore().fetchAll()
</script>

<template>
  <div class="body">
    <SideBar />
    <div class="menu-and-content">
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
