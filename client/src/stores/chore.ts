import type { Project, Tag, TaskType } from '@/types';
import { defineStore } from 'pinia';
import axios from 'axios';

function tryCatcher() {}

export const useChoreStore = defineStore({
  id: 'chores',
  state: () => ({
    tasks: [] as TaskType[],
    projects: [] as Project[],
    tags: [] as Tag[],
    currentTaskId: null as number | null,
  }),
  actions: {
    // fetchers
    async fetchTasks() {
      const response = await axios
        .get('tasks/')
        .catch((err) => console.log('tasks error', err));

      if (response?.status === 200) {
        this.tasks = response?.data;
      }
    },
    async fetchProjects() {
      const response = await axios
        .get('projects/')
        .catch((err) => console.log('projects error', err));
      if (response?.status === 200) {
        this.projects = response?.data;
      }
    },
    async fetchTags() {
      const response = await axios
        .get('tags/')
        .catch((err) => console.log('tags error', err));
      if (response?.status === 200) {
        this.tags = response?.data;
      }
    },
    async fetchCurrentTask() {
      const response = await axios
        .get('currentTask/')
        .catch((err) => console.log('current Task err', err));

      if (response?.status === 200) {
        this.currentTaskId = response?.data.id;
      }
    },
    async changeCurrentTask(id: number | undefined) {
      const response = await axios
        .put('currentTask/', {
          id: id
        })
        .catch((err) => console.log('change current task err', err));

      if (response?.status === 200) {
        this.currentTaskId = response?.data.id;
      }
    },
    // Fetch all chores from user (request.user in django)
    fetchAll() {
      this.fetchTasks();
      this.fetchProjects();
      this.fetchTags();
      this.fetchCurrentTask()
    },
    // Adds tasks with tags and subtasks
    async addTask(task: TaskType) {
      const response = await axios
        .post('tasks/', task)
        .catch((err) => console.log('add task err', err));

      if (response?.status === 200) {
        this.tasks.push(response.data);
      }
    },
    async deleteTask(id: number | undefined) {
      const response = await axios
        .delete(`tasks/${id}/`)
        .catch((err) => console.log('delete task err', err));

      if (response?.status === 204) {
        this.tasks = this.tasks.filter((task: TaskType) => task.id !== id);
      }
    },
    async addProject(project: Project) {
      const response = await axios
        .post('projects/', project)
        .catch((err) => console.log('add project err', err));

      if (response?.status == 201) {
        this.projects.push(response.data);
      }
    },
    async deleteProject(id: number) {
      const response = await axios
        .delete(`projects/${id}/`)
        .catch((err) => console.log('delete project err', err));

      if (response?.status === 200) {
        this.projects = this.projects.filter(
          (project: Project) => project.id !== id
        );
      }
    },
    async addTag(tag: string) {
      const response = await axios
        .post('tags/', tag)
        .catch((err) => console.log('add tag err', err));

      if (response?.status === 200) {
        console.log(response.data);
      }
    },
    async incrementGoneThrough() {
      const response = await axios
      .patch(`tasks/${this.currentTaskId}/`, {
        obj: "task",
        action: "increment_gone_through"
      })
      .catch(err => console.log('incrementGoneThrough err', err))

      if (response?.status === 200) {
        let task = this.tasks.filter((task: TaskType) => task.id === this.currentTaskId)[0];
        task.gone_through = response.data;
      }
    }
  },
});
