import { client } from '.';

async function getHome() {
  const { data } = await client.get('/home');
  return data;
}

export {
  getHome
};