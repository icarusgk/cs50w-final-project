import type { IProject, ITag, ITask, IStat } from '@/types';
import { defineStore } from 'pinia';
import axios from 'axios';
import { useAlertStore, useAuthStore, usePageStore } from '@/stores';
import { ref } from 'vue';
import { useLocal } from '@/utils'

export const useChoreStore = defineStore('chores', () => {
  const alert = useAlertStore();
  const auth = useAuthStore();
  const page = usePageStore();

  const tasks = ref<ITask[]>([]);
  const projects = ref<IProject[]>([]);
  const tags = ref<ITag[]>([]);
  const stats = ref<IStat[]>([]);
  
  async function fetchModes() {
    const { status, data } = await axios.get('modes')
    if (status === 200) useLocal.set('modes', data);
  }
  async function fetchStats() {
    const { data, status } = await axios.get('stats')
    if (status === 200) stats.value = data;
  }
  async function increaseTodayStats() {
    const date = new Date();
    date.setHours(date.getHours() - date.getTimezoneOffset() / 60);

    const { data, status } = await axios.post('stats', {
      day: date.toISOString().slice(0, 10),
    });
    
    if (status === 201) {
      let stat = stats.value.find((stat) => stat.id === data.id);

      if (stat) stat.chores_done = data.chores_done;
    }
  }
  async function fetchTasks() {
    const { data, status } = await axios.get('tasks', {
      params: { 
        page: page.taskPagination.page,
        page_size: page.taskPagination.page_size
      }
    });

    if (status === 200) {
      tasks.value = data.results;
      page.taskPagination.count = data.count;
    }
  }
  async function fetchProjects() {
    const { data, status } = await axios.get('projects', {
      params: {
        page: page.projectPagination.page,
        page_size: page.projectPagination.page_size
      }
    });

    if (status === 200) {
      projects.value = data.results;
      page.projectPagination.count = data.count;
    }
  }
  async function fetchTags() {
    const { data, status } = await axios.get('tags');
    if (status === 200) {
      return (tags.value = data);
    }
  }
  async function addTask(task: ITask) {
    const { status } = await axios.post('tasks', task);
    if (status === 201) {
      alert.success(`Task ${task.title} created!`);
      // Send user to the first page
      page.taskPagination.page = 1;
      fetchTasks();
    }
  }
  async function saveTask(task: ITask) {
    const { status } = await axios.put(`tasks/${task.id}`, task);
    if (status === 200) {
      alert.success(`'${task.title}' saved!`);
      fetchTasks();
    }
  }
  async function deleteTask(task: ITask) {
    const { status } = await axios.delete(`tasks/${task.id}`)

    if (status === 204) {
      // if it is the last
      if (tasks.value.length === 1 && page.taskPagination.count === 0) {
        tasks.value = tasks.value.filter((t: ITask) => t.id !== task.id);
        page.taskPagination.page = 1;
      } else {
        fetchTasks();
      }

      alert.info(`Task '${task.title}' deleted`);

      if (auth.user && task.id) {
        auth.user.current_task_id = 0;
      }
    }
  }
  async function addProject(project: IProject) {
    const { status } = await axios.post('projects', project);

    if (status === 201) {
      alert.success(`Project ${project.name} created!`);
      // Send user to the first page
      page.projectPagination.page = 1;
      fetchProjects();
    }
  }
  async function saveProject(project: IProject, newProjectName: string) {
    const { status } = await axios.patch( `/projects/${project.id}/modify_title`,
      { name: newProjectName }
    );

    if (status === 200) alert.success('Project saved!');
  }
  async function deleteProject(id: number) {
    const { status } = await axios.delete(`projects/${id}`)

    if (status === 204) {
      if (projects.value.length === 1 && page.projectPagination.count === 0) {
        projects.value = projects.value.filter((p: IProject) => p.id !== id);
        page.projectPagination.page = 1;
      } else {
        fetchProjects();
      }
      alert.info('Project deleted!');
    }
  }
  async function incrementGoneThrough() {
    increaseTodayStats();
    
    if (auth.user) {
      const { status } = await axios.patch(`tasks/${auth.user.current_task_id}`, {
        obj: 'task',
        action: 'increment_gone_through',
      });

      if (status === 200) fetchTasks();
    }
  }
  
  return {
    tasks, projects, tags, stats, fetchModes, fetchStats, increaseTodayStats, fetchTasks, fetchProjects, fetchTags,
    addTask, saveTask, deleteTask, addProject, saveProject, deleteProject, incrementGoneThrough
  }
}, { persist: true });
