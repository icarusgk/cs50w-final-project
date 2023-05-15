import axios from "axios";

axios.defaults.baseURL = 'http://127.0.0.1:8000/api/';
axios.defaults.headers.common['Content-Type'] = 'application/json';
axios.defaults.withCredentials = true;

axios.interceptors.request.use(config => {
  // Appends slash
  if (config.url && !config.url.endsWith('/')) {
    config.url += '/';
  }
  return config;
});