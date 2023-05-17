<script setup lang="ts">
const settingsOpen = ref(false);
const auth = useAuthStore();
const modal = useModalStore();

watch(settingsOpen, () => {
  modal.toggle();
});
</script>

<template>
  <div class="flex justify-between mb-4 mx-10 lg:mb-1 lg:mx-16 lg:mb-8 lg:mt-2 text-white">
    <AppTitle />
    <ul class="flex text-right list-none mt-2 items-center">
      <!-- Four icons -->
      <!-- User -->
      <li class="inline-block mr-0.5 pointer">
        <div class="flex items-center">
          <div class="flex items-center">
            <Popper arrow placement="bottom">
              <div class="flex items-center mr-4 <sm:mr-1" v-if="auth.isAuthed">
                <div class="i-fluent:person-12-filled scale-230 mr-6 <sm:scale-160 <sm:mr-3" />
                <span>{{ auth.user?.username }}</span>
              </div>
              <template #content>
                <div class="flex flex-col justify-center items-center">
                  <div @click="$router.push('/tags')" class="p-[0.7rem] m-2 rounded-lg bg-[rgb(92,92,92)] transition duration-150 hover:bg-dark-100 text-white">
                    Manage tags
                  </div>
                  <button @click="auth.logout()" class="py-2 px-4 mb-2 rounded-lg border-none bg-vivid-red text-white font-medium transition duration-100 ease-in pointer hover:bg-[#ff4b4b9f] focus:bg-[#ff4b4b9f] active:bg-[#ff4b4b9f]">
                    Logout
                  </button>
                </div>
              </template>
            </Popper>
          </div>
          <div v-if="!auth.isAuthed" class="flex gap-4">
            <div @click="$router.push('/login')">
              <span class="action-btn hover:bg-[rgb(60,60,60)]">Login</span>
            </div>
            <div @click="$router.push('/register')">
              <span class="action-btn bg-[rgb(60,60,60)] hover:bg-vivid-red">Register</span>
            </div>
          </div>
        </div>
      </li>
      <!-- Settings -->
      <li class="pointer" @click="settingsOpen = true" v-if="auth.isAuthed">
        <div class="i-solar:settings-linear scale-250 ml-3 <sm:scale-170" />
      </li>
    </ul>
    <AppModal :open="settingsOpen" @exit:modal="settingsOpen = false">
      <template #title>
        <span class="font-bold text-4xl">Settings</span>
      </template>
      <TheSettings />
    </AppModal>
  </div>
</template>