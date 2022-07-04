import { ref, isRef, unref, watchEffect } from 'vue'

export function useFetch(url: URL) {
  const data = ref()
  const error = ref()
  
  async function doFetch() {
    data.value = null
    data.value = null

    // Unwrapp potential refs
    const urlValue = unref(url)

    try {
      const response = await fetch(urlValue)
      data.value = await response.json()
    } catch (err) {
      error.value = err
    }
  }

  if (isRef(url)) {
    // setup reactive re-fetch if input URL is a ref
    watchEffect(doFetch)
  } else {
    // otherwise, just fetch once
    doFetch()
  }

  return { data, error, retry: doFetch }

}