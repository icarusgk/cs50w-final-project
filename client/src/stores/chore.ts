import type { ProjectType, TagType, TaskType, StatType } from '@/types';
import { defineStore } from 'pinia';
import axios from 'axios';
import { useFetch } from '@/composables/useFetch';
import { useAlertStore } from './alerts';
import { useAuthStore } from './auth';

export const useChoreStore = defineStore('chores', {
  state: () => ({
    tasks: [] as TaskType[],
    projects: [] as ProjectType[],
    tags: [] as TagType[],
    projectPagination: {
      count: 0,
      page: 1,
      added: 1,
      page_size: 2,
    },
    taskPagination: {
      count: 0,
      page: 1,
      added: 1,
      page_size: 4,
    },
    stats: [] as StatType[],
  }),
  getters: {
    totalProjectPages: (state) =>
      Math.ceil(
        state.projectPagination.count / state.projectPagination.page_size
      ),
    totalTaskPages: (state) =>
      Math.ceil(state.taskPagination.count / state.taskPagination.page_size),
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
      const date = new Date();
      date.setHours(date.getHours() - date.getTimezoneOffset() / 60);

      const { data, status } = await useFetch('stats', 'post', {
        day: date.toISOString().slice(0, 10)
      });
      if (status === 200) {
        let stat = this.stats.find((stat) => stat.id === data.id);

        if (stat) stat.chores_done = data.chores_done;
      }
    },
    async fetchTasks() {
      const { page, page_size } = this.taskPagination;
      const { data, status } = await axios.get('tasks/', {
        params: { page, page_size },
      });

      if (status === 200) {
        this.tasks = data.results;
        this.taskPagination.count = data.count;
      }
    },
    async fetchProjects() {
      const { page, page_size } = this.projectPagination;
      const { data, status } = await axios.get('projects/', {
        params: { page, page_size },
      });

      if (status === 200) {
        this.projects = data.results;
        this.projectPagination.count = data.count;
      }
    },
    async fetchTags() {
      const { data, status } = await useFetch('tags', 'get');

      if (status === 200) {
        return (this.tags = data);
      }
    },
    async changeCurrentTask(id: number | undefined) {
      const { data, status } = await useFetch('currentTask', 'put', { id });

      if (status === 200) {
        useAuthStore().user!.current_task_id = data.id;
      }
    },
    // Fetch all chores from user (request.user in django)
    fetchAll() {
      const auth = useAuthStore();
      if (auth.isAuthenticated) {
        this.fetchModes();
        this.fetchTags();
      }
    },
    // Adds tasks with tags and subtasks
    async addTask(task: TaskType) {
      const { status } = await useFetch('tasks', 'post', task);
      if (status === 200) {
        useAlertStore().success(`Task ${task.title} created!`);
        this.fetchTasks();
      }
    },
    async saveTask(task: TaskType) {
      const { status } = await axios.put(`tasks/${task.id}/`, task);
      if (status === 200) {
        useAlertStore().success(`'${task.title}' saved!`);
        this.fetchTasks();
      }
    },
    async deleteTask(task: TaskType) {
      const { status } = await useFetch('tasks', 'delete', null, task.id);

      if (status === 200) {
        const auth = useAuthStore();

        useAlertStore().info(`Task '${task.title}' deleted`);

        if (task.id === auth.user!.current_task_id) {
          auth.user!.current_task_id = 0;
        }

        this.fetchTasks();
      }
    },
    async addProject(project: ProjectType) {
      const { status } = await useFetch('projects', 'post', project);

      if (status == 201) {
        useAlertStore().success(`Project ${project.name} created!`);
        this.fetchProjects();
      }
    },
    async saveProject(project: ProjectType, newProjectName: string) {
      const { status } = await axios.patch(`/projects/${project.id}/modify_title/`, {
        name: newProjectName,
      });

      if (status === 200) {
        useAlertStore().success('Project saved!');
      }
    },
    async deleteProject(id: number) {
      const { status } = await useFetch('projects', 'delete', null, id);

      if (status === 200) {
        useAlertStore().info('Project deleted!');
        this.fetchProjects();
      }
    },
    async addTag(tag: string) {
      const { data, status } = await useFetch('tags', 'post', tag);

      if (status === 200) console.log(data);
    },
    incrementGoneThrough() {
      this.increaseTodayStats();
      const auth = useAuthStore();

      if (auth.user?.current_task_id) {
        useFetch(
          'tasks',
          'patch',
          {
            obj: 'task',
            action: 'increment_gone_through',
          },
          auth.user!.current_task_id
        );
      }
    },
  },
});
