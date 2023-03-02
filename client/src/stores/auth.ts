import { defineStore } from 'pinia';
import axios from 'axios';
import router from '@/router';
import { useChoreStore } from './chore';
import { ref } from 'vue';
import type { IUser } from '@/types';

axios.defaults.baseURL = import.meta.env.VITE_SERVER_URL;
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

  // First is login in, this will not have an error
  async function login(credentials: UserCredentials) {
    try {
      const response = await axios.post('auth/login/', credentials);
      if (response.status === 200) {
        // After the user logs in, we get its user
        await getUser();
        error.value = null;
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
    const response = await axios.post('auth/logout/');
    console.log(response);
    if (response.status === 200) {
      // Reset user state
      user.value = null;
      isAuthed.value = false;

      localStorage.removeItem('timer');
      localStorage.removeItem('modes');

      useChoreStore().$reset();

      await router.push('/');
    }
  }

  return { user, isAuthed, error, login, getUser, register, logout }
},
{ persist: true });
