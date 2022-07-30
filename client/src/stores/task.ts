import type Task from "@/types/TaskType";
import axios from "axios";
import { defineStore } from "pinia";


export const useTaskStore = defineStore({
  id: 'tasks',
  state: () => ({
    tasks: [] as Task[]
  }),
  actions: {
    async fetchTasks() {
      try {
        const response = await axios.get(`http://127.0.0.1:3001/tasks`)
        this.tasks = response.data
      } catch (err) {
        console.log(err)
      }
    },
    add(task: Task) {
      this.tasks.push(task)
    },
    delete(taskId: number) {
      this.tasks = this.tasks.filter((task: any) => task.id !== taskId)
    }
  }
})