<template>
  <div class="sidebar">
    <RouterLink to="/" aria-label="Pomo">
      <div class="logo-container">
        <img src="../assets/tomato-logo.png" class="logo-img" alt="Pomo Logo" />
      </div>
    </RouterLink>
    <div class="menu-container">
      <RouterLink to="/" aria-label="Home">
        <SidebarItem>
          <template #icon>
            <HomeIcon />
          </template>
          <template #heading>Home</template>
        </SidebarItem>
      </RouterLink>
      <RouterLink to="/stats" aria-label="Stats">
        <SidebarItem>
          <template #icon>
            <StatsIcon />
          </template>
          <template #heading>Stats</template>
        </SidebarItem>
      </RouterLink>
      <RouterLink to="/about" aria-label="About">
        <SidebarItem>
          <template #icon>
            <AboutIcon />
          </template>
          <template #heading>About</template>
        </SidebarItem>
      </RouterLink>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.sidebar {
  background-color: #2f2f2f;
  width: 130px;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: fixed;

  .logo-container {
    margin-top: 2rem;

    .logo-img {
      width: 100%;
      height: 100%;
    }
  }

  .menu-container {
    display: flex;
    flex-direction: column;
    height: 60%;
    margin-top: 4rem;
    align-items: center;

    a {
      text-decoration: none;
    }

    .router-link-active {
      background-color: var(--vivid-red);
      border-radius: 8px;
    }
  }
}

@media (max-width: 768px) {
  .sidebar {
    width: 100%;
    height: 3rem;
    background-color: var(--light-gray);
    position: fixed;
    bottom: 0;
    z-index: 3;

    flex-direction: row;
    justify-content: center;

    .menu-container {
      flex-direction: row;
      margin-bottom: 4rem;

      a {
        transform: scale(70%);
        margin: 0 -2rem;
      }

      .item {
        color: rgb(119, 119, 119);
      }

      .router-link-active {
        background-color: var(--vivid-red);
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
