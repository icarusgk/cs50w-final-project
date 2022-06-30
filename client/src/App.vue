<script setup lang="ts">
import SideBar from '@/components/Sidebar.vue'
</script>

<template>
  <div class="body">
    <SideBar />
    <router-view></router-view>
  </div>
</template>

<style>
/* variables */
:root {
  --white: #fff;
  --black: #000;
  --lighter-gray: #4a4a4a;
  --vivid-red: #FF4B4C;
  --light-red: #FF4F5F;
  --dark-gray: #212121;
  --light-gray: #2F2F2F;
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
}
</style>
