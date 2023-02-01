import { defineStore } from 'pinia';
import axios from 'axios';
import router from '@/router';
import { useChoreStore } from './chore';

const firstCalledInstance = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/',
  headers: {
    'Content-Type': 'application/json',
  },
});

// An interceptor that refreshes the token credentials only on getUser()

firstCalledInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response.status === 401) {
      const jwt = localStorage.getItem('jwt');
      const refresh = jwt ? JSON.parse(jwt).refresh : null;
      // Change the tokens here
      const response = await firstCalledInstance.post('token/refresh/', {
        refresh,
      });

      if (response.status === 200) {
        localStorage.setItem('jwt', JSON.stringify(response.data));
        location.reload();
      }
      return axios(error.response);
    }

    // This has to be obligatory
    return Promise.reject(error);
  }
);

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
    isAuthed: Boolean(localStorage.getItem('jwt')),
    error: null,
  }),
  actions: {
    // First is login in, this will not have an error
    async login(credentials: UserCredentials) {
      try {
        // Grab the access and refresh token
        const response = await axios.post('token/', credentials);
        // Set the localStorage key to the jwt
        if (response.status === 200) {
          // { refresh: '', access: '' }
          localStorage.setItem('jwt', JSON.stringify(response.data));

          // After the user logs in, we get its user
          await this.getUser();
          this.error = null;
          // And we push the user to the main / page
          await router.push('/');

          location.reload();
        }
      } catch (e: any) {
        this.error = e;
      }
    },
    async getUser() {
      const jwt = localStorage.getItem('jwt');
      const accessToken = jwt ? JSON.parse(jwt).access : null;

      try {
        const response = await firstCalledInstance.get('me/', {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });

        if (response.status === 200) {
          this.user = response.data;
        }
      } catch (e) {
        // If refresh token is not longer valid, logout
        this.logout();
      }
    },
    async register(credentials: UserCredentials) {
      this.error = null;
      try {
        const response = await axios.post('register/', credentials);
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
      // Reset user state
      this.user = null;

      localStorage.removeItem('jwt');
      localStorage.removeItem('timer');
      localStorage.removeItem('modes');

      useChoreStore().$reset();

      await router.push('/');
      location.reload();
    },
  },
});
