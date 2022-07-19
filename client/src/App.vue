<script setup lang="ts">
import SideBar from '@/components/Sidebar.vue'
import UpperMenu from './components/UpperMenu.vue'
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
:root {
  --white: #fff;
  --black: #000;
  --gray: #636363;
  --lighter-gray: #4a4a4a;
  --vivid-red: #FF4B4C;
  --light-red: #FF4F5F;
  --dark-gray: #212121;
  --light-gray: #2F2F2F;
  --light-blue: #02B79F;
}

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
