import { defineStore } from 'pinia';
import axios from 'axios';
import router from '@/router';
import { useChoreStore } from './chore';

type User = {
  id: number;
  username: string;
  email: string;
  streak: number;
};

type UserCredentials = {
  username: string;
  password: string;
  passwordConfirmation?: string;
};

export const useAuthStore = defineStore({
  id: 'auth',
  state: () => ({
    user: null as User | null,
    isAuthenticated: Boolean(localStorage.getItem('jwt')),
  }),
  getters: {},
  actions: {
    async getUser() {
      try {
        const response = await axios({
          method: 'get',
          url: '/me/',
          headers: {
            Authorization: 'Bearer ' + localStorage.getItem('jwt'),
          },
        });
        if (response.status === 200 && response.data) {
          // console.log('setting user...');

          this.user = response.data;
          // console.log('user is', this.user);

          return response.data;
        }
      } catch (err) {
        console.log('getUser err', err);
      }
    },
    async register(credentials: UserCredentials) {
      try {
        const response = await axios.post('register/', credentials);
        if (response.status === 200) {
          // If the user is created, log him in
          this.login({
            username: credentials.username,
            password: credentials.password,
          });
        }
      } catch (err) {
        console.log('err in register()', err);
      }
      router.push('/register');
    },
    async login(credentials: UserCredentials) {
      try {
        // Login
        const response = await axios.post('token/', credentials);
        // Set the cookie to the jwt
        if (response.status === 200) {
          localStorage.setItem('jwt', response.data?.access);
          this.isAuthenticated = true;
          await this.getUser();

          await router.push('/');

          location.reload();
        }
      } catch (err) {
        console.log(err);
      }
    },
    logout() {
      console.log('logging out user:', this.user);
      // Reset user state
      [this.user, this.isAuthenticated] = [null, false];
      localStorage.removeItem('jwt');
      localStorage.removeItem('timer');
      console.log('now the user is:', this.user);
      console.log('and jwt is', localStorage.getItem('jwt'));

      useChoreStore().$reset();

      // console.log(useChoreStore().tasks)
      router.push('/');
      location.reload();
    },
  },
});
