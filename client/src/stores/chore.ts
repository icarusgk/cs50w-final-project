import type Project from "@/types/ProjectType";
import type Task from "@/types/TaskType";
import axios from "axios";
import { defineStore } from "pinia";


export const useChoreStore = defineStore({
  id: 'chores',
  state: () => ({
    tasks: [] as Task[],
    projects: [] as Project[]
  }),
  actions: {
    // fetchers
    async fetchTasks() {
      try {
        const response = await axios.get(`http://127.0.0.1:3001/tasks`)
        this.tasks = response.data
      } catch (err) {
        console.log(err)
      }
    },
    async fetchProjects() {
      try {
        const response = await axios.get(`http://127.0.0.1:3001/projects`)
        this.projects = response.data
      } catch (err) {
        console.log(err)
      }
    },
    addTask(task: Task) {
      axios.post(`http://127.0.0.1:3001/tasks/`, task)
      this.tasks.push(task)
    },
    async deleteTask(taskId: number) {
      const response = await axios.delete(`http://127.0.0.1:3001/tasks/${taskId}`)
      if (response.status === 200) {
        this.tasks = this.tasks.filter((task: Task) => task.id !== taskId)
      }
    },
    addProject(project: Project) {
      axios.post(`http://127.0.0.1:3001/projects/`, project)
      this.projects.push(project)
    },
    async deleteProject(projectId: number) {
      const response = await axios.delete(`http://127.0.0.1:3001/projects/${projectId}`) 
      if (response.status === 200) {
        this.projects = this.projects.filter((project: Project) => project.id !== projectId)
      }
    }
  }
})