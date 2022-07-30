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
      this.tasks.push(task)
    },
    deleteTask(taskId: number) {
      this.tasks = this.tasks.filter((task: Task) => task.id !== taskId)
    },
    addProject(project: Project) {
      this.projects.push(project)
    },
    deleteProject(projectId: number) {
      this.projects = this.projects.filter((project: Project) => project.id !== projectId)
    }
  }
})