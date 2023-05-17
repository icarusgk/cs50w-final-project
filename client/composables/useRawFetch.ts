import type { UseFetchOptions } from 'nuxt/app';

export default function useRawFetch<T>(url: string, options?: UseFetchOptions<T>) {
  if (url && !url.endsWith('/')) url += '/';

  const customFetch = $fetch.create<T>({
    // TODO: Change to fly.io endpoint on prod
    baseURL: 'http://127.0.0.1:8000/api/',
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' }
  });
  
  // @ts-expect-error
  return customFetch.raw<T>(url, options);
}