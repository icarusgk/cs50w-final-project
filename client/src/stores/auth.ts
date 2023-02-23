import { defineStore } from 'pinia';
import axios from 'axios';
import router from '@/router';
import { useChoreStore } from './chore';

axios.defaults.baseURL = 'http://127.0.0.1:8000/api/';
axios.defaults.headers.common['Content-Type'] = 'application/json';
axios.defaults.withCredentials = true;

type User = {
  id: number;
  username: string;
  email: string;
  streak: number;
  auto_start_pomos: boolean;
  auto_start_breaks: boolean;
  current_task_id: number | null;
};

type UserCredentials = {
  username: string;
  password: string;
  passwordConfirmation?: string;
};

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null as User | null,
    isAuthed: null as Boolean | null,
    error: null,
  }),
  actions: {
    // First is login in, this will not have an error
    async login(credentials: UserCredentials) {
      try {
        const response = await axios.post('auth/login/', credentials);
        if (response.status === 200) {
          // After the user logs in, we get its user
          await this.getUser();

          this.error = null;
          // And we push the user to the main / page
          await router.push('/');
        }
      } catch (e: any) {
        this.error = e;
      }
    },
    // Runs at start
    async getUser() {
      try {
        const response = await axios.get('me/');

        if (response.status === 200) {
          this.user = response.data;
          this.isAuthed = true;
        }
      } catch (e) {
        // If refresh token is not longer valid, logout
        this.logout();
      }
    },
    async register(credentials: UserCredentials) {
      this.error = null;
      try {
        const response = await axios.post('auth/register/', credentials);
        if (response.status === 201) {
          // If the user is created, log him in
          this.login({
            username: credentials.username,
            password: credentials.password,
          });
        }
      } catch (err: any) {
        this.error = err;
      }
      router.push('/register');
    },
    async logout() {
      const response = await axios.post('auth/logout/');
      console.log(response);
      if (response.status === 200) {
        // Reset user state
        this.user = null;
        this.isAuthed = false;

        localStorage.removeItem('timer');
        localStorage.removeItem('modes');

        useChoreStore().$reset();

        await router.push('/');
      }
    },
  },
  persist: true
});
