import { ref } from 'vue'
import axios, { type AxiosResponse } from 'axios'
import type { Project, Task, Tag } from '@/types'

type Options = {
  method?: string,
  data?: any // TODO: Change to datatypes
}

const fetch = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + localStorage.getItem('jwt')
  }
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
    console.log('err in path', path, err)
  }
  return data.value
}
