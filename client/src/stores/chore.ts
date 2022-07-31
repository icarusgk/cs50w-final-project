import type { Project, Task } from '@/types'
import { defineStore } from "pinia";
import { useFetch } from '@/composables/useFetch';


export const useChoreStore = defineStore({
  id: 'chores',
  state: () => ({
    tasks: [] as Task[],
    projects: [] as Project[]
  }),
  actions: {
    // fetchers
    async fetchTasks() {
      const response = await useFetch('/tasks')
      this.tasks = response?.data
    },
    async fetchProjects() {
      const response = await useFetch('/projects')
      this.projects = response?.data
    },
    addTask(task: Task) {
      useFetch('/tasks', { method: 'post', data: task })
      this.tasks.push(task)
    },
    async deleteTask(id: number) {
      const response = await useFetch(`/tasks/${id}`, { method: 'delete'})
      if (response?.status === 200) {
        this.tasks = this.tasks.filter((task: Task) => task.id !== id)
      }
    },
    addProject(project: Project) {
      useFetch('/projects', { method: 'post', data: project })
      this.projects.push(project)
    },
    async deleteProject(id: number) {
      const response = await useFetch(`/projects/${id}`, { method: 'delete'})
      if (response?.status === 200) {
        this.projects = this.projects.filter((project: Project) => project.id !== id)
      }
    }
  }
})