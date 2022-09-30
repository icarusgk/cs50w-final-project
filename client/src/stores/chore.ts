import type { Project, Tag, TaskType, StatType } from '@/types';
import { defineStore } from 'pinia';
import axios from 'axios';
import { useFetch } from '@/composables/useFetch';

const PROJECT_PAGE_SIZE = 2;
const TASK_PAGE_SIZE = 4;

export const useChoreStore = defineStore({
  id: 'chores',
  state: () => ({
    tasks: [] as TaskType[],
    projects: [] as Project[],
    tags: [] as Tag[],
    projectPagination: {
      count: 0,
      page: 1,
      added: 1,
    },
    taskPagination: {
      count: 0,
      page: 1,
      added: 1
    },
    stats: [] as StatType[],
    currentTaskId: null as number | null,
  }),
  getters: {
    totalProjectPages: (state) =>
      Math.ceil(state.projectPagination.count / PROJECT_PAGE_SIZE),
    totalTaskPages: (state) =>
      Math.ceil(state.taskPagination.count / TASK_PAGE_SIZE),
  },
  actions: {
    previousProjectPage() {
      if (this.projectPagination.page > 1) {
        this.projectPagination.page--;
        this.fetchProjects();
      }
    },
    setProjectPage(page: number) {
      this.projectPagination.page = page;
      this.fetchProjects();
    },
    nextProjectPage() {
      if (this.projectPagination.page < this.totalProjectPages) {
        this.projectPagination.page++;
        this.fetchProjects();
      }
    },
    previousTaskPage() {
      if (this.taskPagination.page > 1) {
        this.taskPagination.page--;
        this.fetchTasks();
      }
    },
    setTaskPage(page: number) {
      this.taskPagination.page = page;
      this.fetchTasks();
    },
    nextTaskPage() {
      if (this.taskPagination.page < this.totalTaskPages) {
        this.taskPagination.page++;
        this.fetchTasks();
      }
    },
    // fetchers
    async fetchModes() {
      const { status, data } = await useFetch('modes', 'get');
      if (status === 200) {
        const modes = JSON.stringify(data);
        localStorage.setItem('modes', modes);
      }
    },
    async fetchStats() {
      const { data, status } = await useFetch('stats', 'get');
      if (status === 200) this.stats = data;
    },
    async increaseTodayStats() {
      const { data, status } = await useFetch('stats', 'post', {
        day: new Date().toISOString().slice(0, 10),
      });
      if (status === 200) {
        let stat = this.stats.find(stat => stat.id === data.id);

        if (stat) {
          stat.chores_done = data.chores_done;          
        }
      }
    },
    async fetchTasks() {
      const { data, status } = await axios.get(
        `tasks/?page=${this.taskPagination.page}`
      );

      if (status === 200) {
        this.tasks = data.results;
        this.taskPagination.count = data.count;
      }
    },
    async fetchProjects() {
      const { data, status } = await axios.get(
        `projects/?page=${this.projectPagination.page}`
      );

      if (status === 200) {
        this.projects = data.results;
        this.projectPagination.count = data.count;
      }
    },
    async fetchTags() {
      const { data, status } = await useFetch('tags', 'get');

      if (status === 200) this.tags = data;
    },
    async fetchCurrentTask() {
      const { data, status } = await useFetch('currentTask', 'get');

      if (status === 200) this.currentTaskId = data.id;
    },
    async changeCurrentTask(id: number | undefined) {
      const { data, status } = await useFetch('currentTask', 'put', { id });

      if (status === 200) this.currentTaskId = data.id;
    },
    // Fetch all chores from user (request.user in django)
    fetchAll() {
      this.fetchStats();
      this.fetchModes();
      this.fetchTags();
      this.fetchTasks();
      this.fetchProjects();      
      this.fetchCurrentTask();
    },
    // Adds tasks with tags and subtasks
    async addTask(task: TaskType) {
      const { data, status } = await useFetch('tasks', 'post', task);
      console.log(data);

      if (status === 200) this.tasks.unshift(data);
    },
    async deleteTask(id: number | undefined) {
      const { status } = await useFetch('tasks', 'delete', null, id);

      if (status === 204) {
        this.tasks = this.tasks.filter((task: TaskType) => task.id !== id);
      }
    },
    async addProject(project: Project) {
      const { data, status } = await useFetch('projects', 'post', project);

      if (status == 201) this.projects.push(data);
    },
    async deleteProject(id: number) {
      const { status } = await useFetch('projects', 'delete', null, id);

      if (status === 200) {
        this.projects = this.projects.filter(
          (project: Project) => project.id !== id
        );
      }
    },
    async addTag(tag: string) {
      const { data, status } = await useFetch('tags', 'post', tag);

      if (status === 200) console.log(data);
    },
    async incrementGoneThrough() {
      const { status } = await useFetch(
        'tasks',
        'patch',
        {
          obj: 'task',
          action: 'increment_gone_through',
        },
        this.currentTaskId
      );

      if (status === 200) {
        this.increaseTodayStats();
      }
    },
  },
});
