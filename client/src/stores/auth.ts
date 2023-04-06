import { defineStore } from 'pinia';
import axios from 'axios';
import router from '@/router';
import { ref } from 'vue';
import { useAlertStore } from '@/stores/alerts';
import type { IUser } from '@/types';

axios.defaults.baseURL = 'http://127.0.0.1:8000/api/';
axios.defaults.headers.common['Content-Type'] = 'application/json';
axios.defaults.withCredentials = true;

type UserCredentials = {
  username: string;
  password: string;
  passwordConfirmation?: string;
};

export const useAuthStore = defineStore('auth', () => {
  const user = ref<IUser | null>(null);
  const isAuthed = ref(false);
  const error = ref();
  const alerts = useAlertStore();

  // First is login in, this will not have an error
  async function login(credentials: UserCredentials) {
    try {
      const response = await axios.post('auth/login/', credentials);
      if (response.status === 200) {
        // After the user logs in, we get its user
        await getUser();
        error.value = null;
        alerts.success('Successfully logged in!');
        // And we push the user to the main / page
        await router.push('/');
      }
    } catch (e: any) {
      error.value = e;
    }
  }

  // Runs at start
  async function getUser() {
    try {
      const response = await axios.get('me/');

      if (response.status === 200) {
        user.value = response.data;
        isAuthed.value = true;
      } else {
        isAuthed.value = false;
      }
    } catch (e) {
      // If refresh token is not longer valid, logout
      logout();
    }
  }

  async function register(credentials: UserCredentials) {
    error.value = null;
    try {
      const response = await axios.post('auth/register/', credentials);
      if (response.status === 201) {
        // If the user is created, log him in
        login({
          username: credentials.username,
          password: credentials.password,
        });
      }
    } catch (err: any) {
      error.value = err;
    }
    router.push('/register');
  }

  async function logout() {
    if (!isAuthed.value) return;

    const response = await axios.post('auth/logout/');

    if (response.status === 200) {
      // Reset user state
      user.value = null;
      isAuthed.value = false;

      alerts.info('Logged out!');
      localStorage.clear();

      await router.push('/');
    }
  }

  return { user, isAuthed, error, login, getUser, register, logout }
},
{ persist: true });
