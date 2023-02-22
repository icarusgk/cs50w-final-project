<template>
  <div class="sidebar">
    <RouterLink to="/" aria-label="Pomo">
      <div class="logo-container">
        <img src="../assets/tomato-logo.png" class="logo-img" alt="Pomo Logo" />
      </div>
    </RouterLink>
    <div class="menu-container">
      <div class="main-icons">
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
      </div>
      <div class="info-container">
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
  </div>
</template>

<style lang="scss" scoped>
.sidebar {
  background-color: #2f2f2f;
  width: 80px;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: fixed;

  // The div that surrounds the logo
  .logo-container {
    margin-top: 2rem;
    display: flex;
    justify-content: center;

    // Pomo image at the top
    .logo-img {
      width: 70%;
      height: 100%;
    }
  }

  // All the icons on the sidebar
  .menu-container {
    display: flex;
    flex-direction: column;
    height: 100%;
    margin-top: 4rem;
    align-items: center;
    justify-content: space-between;

    .main-icons {
      display: flex;
      flex-direction: column;
      justify-content: center;
      width: 80px;
    }

    .info-container {
      width: 80px;
    }

    a {
      text-decoration: none;
    }

    .router-link-active {
      background-color: var(--vivid-red);
      border-radius: 0 10px 10px 0;
    }
  }
}

// TODO: Fix mobile view
@media (max-width: 768px) {
  .sidebar {
    width: 100%;
    height: 3rem;
    background-color: var(--light-gray);
    position: fixed;
    bottom: 0;
    z-index: 3;

    .logo-container {
      display: none;
    }

    flex-direction: row;
    justify-content: center;

    .menu-container {
      flex-direction: row;
      justify-content: center;
      margin-bottom: 4rem;
      width: 100%;

      .main-icons {
        flex-direction: row;
        gap: 5rem;
        width: 50%;
      }

      .info-container {
        width: 30%;
        margin-left: 1.5rem;
      }

      a {
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
}
</style>
