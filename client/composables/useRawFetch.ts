import type { UseFetchOptions } from 'nuxt/app';

export default function useRawFetch<T>(url: string, options?: UseFetchOptions<T>) {
  if (url && !url.endsWith('/')) url += '/';

  const config = useRuntimeConfig();
  const customFetch = $fetch.create<T>({
    baseURL: config.public.apiBase,
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' }
  });
  
  // @ts-expect-error
  return customFetch.raw<T>(url, options);
}