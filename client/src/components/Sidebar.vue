<script setup lang="ts">
import HomeIcon from './icons/HomeIcon.vue'
import StatsIcon from './icons/StatsIcon.vue'
import AboutIcon from './icons/AboutIcon.vue'
import MenuIcon from './MenuIcon.vue'
</script>

<template>
  <div class="container">
    <div class="logo-container">
      <img src="../assets/tomato-logo.png" class="logo-img" />
    </div>
    <div class="menu-container">
      <MenuIcon>
        <template #icon>
          <HomeIcon />
        </template>
        <template #heading>Home</template>
      </MenuIcon>
      <MenuIcon>
        <template #icon>
          <StatsIcon />
        </template>
        <template #heading>Stats</template>
      </MenuIcon>
      <MenuIcon>
        <template #icon>
          <AboutIcon />
        </template>
        <template #heading>About</template>
      </MenuIcon>
    </div>
  </div>
</template>

<style>
.container {
  background-color: #2f2f2f;
  width: 130px;
  height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.menu-container {
  display: flex;
  flex-direction: column;
  height: 60%;
  justify-content: space-evenly;
  margin-top: 4rem;
  align-items: center;
}

.logo-container {
  margin-top: 2rem;
}
</style>

