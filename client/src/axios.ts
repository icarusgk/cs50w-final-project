import axios from 'axios';

axios.defaults.baseURL = 'http://127.0.0.1:8000/api/';
axios.defaults.headers.common['Content-Type'] = 'application/json';

const jwt = localStorage.getItem('jwt');

if (jwt) {
  const accessToken = JSON.parse(jwt).access;
  axios.defaults.headers.common['Authorization'] = 'Bearer ' + accessToken;
}
