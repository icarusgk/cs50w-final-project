import axios from 'axios';

axios.defaults.baseURL = 'http://127.0.0.1:8000/api/';
axios.defaults.headers.common['Content-Type'] = 'application/json';

const jwt = localStorage.getItem('jwt');

const accessToken = jwt ? JSON.parse(jwt).access : null;
axios.defaults.headers.common['Authorization'] = 'Bearer ' + accessToken;

