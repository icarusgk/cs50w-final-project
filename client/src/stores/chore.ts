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
    decreaseProjectPagination() {
      this.projectPagination.page -= 1;
      this.projectPagination.count -= 1;
      this.projectPagination.added -= 1;
    },
    decreaseTaskPagination() {
      this.taskPagination.page -= 1;
      this.taskPagination.count -= 1;
      this.taskPagination.added -= 1;
    },
    previousProjectPage() {
      if (this.projectPagination.page > 1) {
        this.projectPagination.page--;
      }
    },
    setProjectPage(page: number) {
      this.projectPagination.page = page;
    },
    setProjectAdded(added: number) {
      this.projectPagination.added = added;
    },
    nextProjectPage() {
      if (this.projectPagination.page < this.totalProjectPages) {
        this.projectPagination.page++;
      }
    },
    previousTaskPage() {
      if (this.taskPagination.page > 1) {
        this.taskPagination.page--;
      }
    },
    setTaskPage(page: number) {
      this.taskPagination.page = page;
    },
    setTaskAdded(added: number) {
      this.taskPagination.added = added;
    },
    nextTaskPage() {
      if (this.taskPagination.page < this.totalTaskPages) {
        this.taskPagination.page++;
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
      if (status === 200) {
        this.stats = data;
      }
    },
    async increaseTodayStats() {
      const date = new Date();
      date.setHours(date.getHours() - date.getTimezoneOffset() / 60);

      const { data, status } = await useFetch('stats', 'post', {
        day: date.toISOString().slice(0, 10)
      });
      if (status === 201) {
        let stat = this.stats.find((stat) => stat.id === data.id);

        if (stat)  {
          stat.chores_done = data.chores_done;
        }
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
      if (status === 201) {
        useAlertStore().success(`Task ${task.title} created!`);
        // Send user to the first page
        this.taskPagination.page = 1;
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

      if (status === 204) {
        // if it is the last
        if (this.tasks.length === 1 && this.taskPagination.count === 0) {
          this.tasks = this.tasks.filter((t: TaskType) => t.id !== task.id);
          this.taskPagination.page = 1;
        } else {
          this.fetchTasks();
        }

        const auth = useAuthStore();

        useAlertStore().info(`Task '${task.title}' deleted`);

        if (task.id === auth.user!.current_task_id) {
          auth.user!.current_task_id = 0;
        }        
      }
    },
    async addProject(project: ProjectType) {
      const { status } = await useFetch('projects', 'post', project);

      if (status === 201) {
        useAlertStore().success(`Project ${project.name} created!`);
        // Send user to the first page
        this.projectPagination.page = 1;
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

      if (status === 204) {
        if (this.projects.length === 1 && this.projectPagination.count === 0) {
          this.projects = this.projects.filter((p: ProjectType) => p.id !== id);
          this.projectPagination.page = 1;
        } else {
          this.fetchProjects();
        }
        useAlertStore().info('Project deleted!');
      }
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
