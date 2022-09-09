import axios from 'axios'

axios.defaults.baseURL = 'http://127.0.0.1:8000/api/'
axios.defaults.headers.common['Content-Type'] = 'application/json'

if (localStorage.getItem('jwt')) {
  axios.defaults.headers.common['Authorization'] = 'Bearer ' + localStorage.getItem('jwt')
}