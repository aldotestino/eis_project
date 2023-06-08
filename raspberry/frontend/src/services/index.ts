import axios from 'axios';
import { QueryClient } from 'react-query';

const client = (() => {
  return axios.create({
    baseURL: 'http://192.168.1.64:8080/api'
  });
})();

const queryClient = new QueryClient();

export { client, queryClient };