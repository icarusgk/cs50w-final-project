import { ref, isRef, unref, watchEffect } from 'vue'
import axios from 'axios'

export function useFetch(url: string) {
  const data = ref()
  const error = ref()
  
  async function doFetch() {
    data.value = null
    error.value = null

    // Unwrapp potential refs
    const urlValue = unref(url)

    try {
      const response = await axios.get(`http://127.0.0.1:3001${url}`)
      data.value = await response.data
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