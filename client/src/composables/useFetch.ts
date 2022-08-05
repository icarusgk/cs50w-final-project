import { ref } from 'vue'
import axios, { type AxiosResponse } from 'axios'
import type { Project, Task, Tag } from '@/types'

type Options = {
  method?: string,
  data?: Project | Task | Tag | { id: number }
}

const fetch = axios.create({
  baseURL: 'http://127.0.0.1:3001',
  headers: { 'Content-Type': 'application/json' }
})

export async function useFetch(path: string, options?: Options) {
  const data = ref<AxiosResponse>()

  try {
    const response = await fetch({
      url: path,
      method: options?.method,
      data: options?.data
    })
    data.value = response
  } catch (err) {
    console.log(err)
  }

  return data.value
}
