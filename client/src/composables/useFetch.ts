import axios from 'axios';

export async function useFetch(
  url: string,
  method: string,
  data?: any,
  id?: any
): Promise<any> {
  url += '/';

  if (id) {
    url += `${id}/`;
  }

  try {
    return await axios({ method, url, data });
  } catch (err) {
    console.log('useFetch error', err);
  }
}
