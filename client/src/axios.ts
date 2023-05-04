import axios from 'axios';

axios.defaults.baseURL = import.meta.env.VITE_SERVER_URL;
axios.defaults.headers.common['Content-Type'] = 'application/json';
axios.defaults.withCredentials = true;

axios.interceptors.request.use(config => {
  // Appends slash
  if (config.url && !config.url.endsWith('/')) {
    config.url += '/';
  }
  return config;
});