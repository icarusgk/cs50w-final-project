<template>
  <div class="w-full h-12 bg-light-gray z-3 bottom-0 bg-[#2f2f2f] lg:w-20 lg:h-full flex lg:flex-col justify-center items-center fixed">
    <div class="hidden mt-8 flex justify-center ml-4 lg:block">
      <img src="../assets/tomato-logo.png" class="w-[70%]" alt="Pomo Logo" />
    </div>
    <div class="flex justify-center items-center w-full lg:flex-col h-full lg:mt-16 lg:justify-between">
      <div class="flex gap-20 w-1/2 justify-center lg:gap-0 lg:flex-col lg:w-20">
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
      <div class="w-[30%] ml-6 lg:w-20 lg:m-0">
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

<style scoped>
.router-link-active {
  background-color: var(--vivid-red);
  border-radius: 0 10px 10px 0;
}

@media (max-width: 768px) {
  .router-link-active {
    background-color: var(--vivid-red);
    padding: 0;
    border-radius: 8px;
  }
}
</style>
