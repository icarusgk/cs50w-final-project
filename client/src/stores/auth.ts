import { defineStore } from 'pinia';
import axios from 'axios';

type User = {
  id: number,
  username: string,
  email: string,
  streak: number
}

export const useAuthStore = defineStore({
  id: 'auth',
  state: () => ({
    user: null as User | null,
    isAuthenticated: localStorage.key(0) === 'jwt'
  }),
  getters: {

  },
  actions: {
    async getUser() {
      try {
        const response = await axios({
          method: 'get',
          url: '/api/me/',
          headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('jwt')
          }
        })
        if (response.status === 200) {
          this.user = response.data
          return response.data
        }
      } catch (err) {
        console.log('getUser err', err)
      }
    },
    async login(credentials: {username: string, password: string}) {
      try {
        // Login
        const response = await axios({
          method: 'post',
          url: '/api/token/',
          headers: {'Content-Type': 'application/json'},
          data: credentials
        })
        // Set the cookie to the jwt
        if (response.status === 200) {
          // console.log(response)
          localStorage.setItem('jwt', response.data?.access)
          this.isAuthenticated = true
          this.user = await this.getUser()
        }    
      } catch (err) {
        console.log(err)
      }
    },
    logout() {
      this.user = null
      this.isAuthenticated = false
      localStorage.removeItem('jwt')
    }
  }
})