<script setup>
const creds = reactive({
  username: '',
  password: '',
});
const errors = reactive({
  username: '',
  password: '',
});

const auth = useAuthStore();

function login() {
  creds.username == ''
    ? (errors.username = 'Username is empty')
    : (errors.username = '');
  creds.password == ''
    ? (errors.password = 'Password is empty')
    : (errors.password = '');

  if (creds.username && creds.password) {
    // clear errors
    errors.username = '';
    errors.password = '';

    auth.login(creds).then(() => {
      if (auth.error) {
        useAlertStore().error('Your username or password is incorrect.');
      }
    });
  }
}
</script>

<template>
  <div class="text-center text-white">
    <div class="text-center">
      <h1>Login</h1>
      <form class="mt-4" @submit.prevent="login()">
        <div>
          <input
            v-model="creds.username"
            placeholder="Username"
            type="username"
            name="username"
            id="username"
            class="p-4 bg-[rgba(92,92,92,0.5)] outline-none border-none text-white mb-4 rounded-lg"
          />
          <Transition name="fade">
            <span v-if="errors.username" class="text-vivid-red block">
              {{ errors.username }}
            </span>
          </Transition>
        </div>
        <div>
          <input
            v-model="creds.password"
            placeholder="Password"
            type="password"
            name="password"
            id="password"
            autocomplete="true"
            class="p-4 bg-[rgba(92,92,92,0.5)] outline-none border-none text-white mb-4 rounded-lg"
          />
          <Transition name="fade">
            <span v-if="errors.password" class="text-vivid-red block">
              {{ errors.password }}
            </span>
          </Transition>
        </div>
        <div>
          <input type="submit" value="Submit" class="py-3 px-16 bg-vivid-red text-white border-none rounded-lg transition-all duration-200 ease-in-out pointer hover:bg-[#ff4b4b9f]" />
        </div>
      </form>
      <div class="mt-8">
        <span>Don't have an account yet? </span>
        <RouterLink class="text-vivid-red" to="/register">Register here!</RouterLink>
      </div>
    </div>
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.7s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
