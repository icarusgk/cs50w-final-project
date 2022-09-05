<script setup>
import HomeIcon from '@/components/icons/HomeIcon.vue'
import StatsIcon from '@/components/icons/StatsIcon.vue'
import AboutIcon from '@/components/icons/AboutIcon.vue'
import MenuIcon from '@/components/slots/MenuIcon.vue'
</script>

<template>
  <div class="container">
    <div class="logo-container">
      <img src="../assets/tomato-logo.png" class="logo-img" />
    </div>
    <div class="menu-container">
      <router-link to="/">
        <MenuIcon>
          <template #icon>
            <HomeIcon />
          </template>
          <template #heading>Home</template>
        </MenuIcon>
      </router-link>
      <router-link to="/stats">
        <MenuIcon>
          <template #icon>
            <StatsIcon />
          </template>
          <template #heading>Stats</template>
        </MenuIcon>
      </router-link>
      <router-link to="/about">
        <MenuIcon>
          <template #icon>
            <AboutIcon />
          </template>
          <template #heading>About</template>
        </MenuIcon>
      </router-link>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.container {
  background-color: #2f2f2f;
  width: 130px;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: fixed;

  .logo-container {
    margin-top: 2rem;
  }

  .menu-container {
    display: flex;
    flex-direction: column;
    height: 60%;
    justify-content: space-evenly;
    margin-top: 4rem;
    align-items: center;

    a {
      text-decoration: none;
    }

    .router-link-active {
      background-color: var(--vivid-red);
      padding: 0 1rem;
      border-radius: 8px;
    }

  }
}


@media (max-width: 768px) {
  .container {
    width: 100%;
    height: 3rem;
    background-color: var(--light-gray);
    position: fixed;
    bottom: 0;
    z-index: 3;

    flex-direction: row;
    justify-content: space-around;
    

    .menu-container {
      
      flex-direction: row;
      margin-bottom: 4rem;

      a {
        transform: scale(0.8);
        margin: 0 -2rem;
      }

      .item {
        color: rgb(119, 119, 119);
      }

      .router-link-active {
        background-color: transparent;
        padding: 0;
        border-radius: 8px;
        
        .item {
          color: white;
        }
      }
    }
  }  
  
  .logo-container {
    display: none;
  }
  

  
}
</style>

