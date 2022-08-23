import type { Project, Tag, TaskType } from '@/types'
import { defineStore } from "pinia";
import { useFetch } from '@/composables/useFetch';


export const useChoreStore = defineStore({
  id: 'chores',
  state: () => ({
    tasks: [] as TaskType[],
    projects: [] as Project[],
    tags: [] as Tag[],
    // currentTask: null as { id: number } | null
  }),
  actions: {
    // fetchers
    async fetchTasks() {
      try {
        const response = await useFetch('/tasks/')
        if (response?.status === 200) {
          this.tasks = response?.data
        }
      } catch (err) {
        console.log("tasks error", err)
      }
    },
    async fetchProjects() {
      const response = await useFetch('/projects/')
      this.projects = response?.data
    },
    async fetchTags() {
      const response = await useFetch('/tags/')
      this.tags = response?.data
    },
    // async fetchCurrentTask() {
    //   const response = await useFetch('/currentTask/')
    //   this.currentTask = response?.data
    // },
    fetchAll() {
      this.fetchProjects()
      this.fetchTags()
      this.fetchTasks()
      // this.fetchCurrentTask()
    },
    // Adds tasks with tags and subtasks
    async addTask(task: TaskType) {
      try {
        const response = await useFetch('/tasks/', { method: 'post', data: task })
        if (response?.status === 200) {
          this.tasks.push(response.data)
        }
      } catch (err) {
        console.log('add task err', err)
      }
    },
    async deleteTask(id: number | undefined) {
      const response = await useFetch(`/tasks/${id}/`, { method: 'delete' })
      console.log(response)
      if (response?.status === 204) {
        this.tasks = this.tasks.filter((task: TaskType) => task.id !== id)
      }
    },
    async addProject(project: Project) {
      const response = await useFetch('/projects/', { method: 'post', data: project })
      if (response?.status == 201) {
        this.projects.push(response.data)
      }
    },
    async deleteProject(id: number) {
      const response = await useFetch(`/projects/${id}/`, { method: 'delete' })
      console.log(response)
      if (response?.status === 200) {
        this.projects = this.projects.filter((project: Project) => project.id !== id)
      }
    },
    async addTag(tag: string) {
      try {
        const response = await useFetch('/tags/', { method: 'post', data: tag })
      
        if (response?.status === 200) {
          console.log(response.data)
        }  
      } catch (err) {
        console.log('addTag err', err)
      }
    },
    // changeCurrentTask(id: number) {
    //   useFetch('/currentTask/', { method: 'put', data: { id: id } })
    //   this.currentTask = { id: id }
    // }
  }
})