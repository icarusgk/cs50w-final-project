import axios from 'axios';

axios.defaults.baseURL = import.meta.env.VITE_SERVER_URL;
axios.defaults.headers.common['Content-Type'] = 'application/json';

const jwt = localStorage.getItem('jwt');

if (jwt) {
  const accessToken = JSON.parse(jwt).access;
  axios.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`;
}
