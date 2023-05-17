import type { IProject, ITag, ITask, IStat, IPage, IMode } from '@/types';

export const useChoreStore = defineStore('chores', () => {
  const alert = useAlertStore();
  const auth = useAuthStore();
  const page = usePageStore();

  const tasks = ref<ITask[]>([]);
  const projects = ref<IProject[]>([]);
  const tags = ref<ITag[]>([]);
  const stats = ref<IStat[]>([]);
  
  async function fetchModes() {
    const { status, _data } = await useRawFetch<IMode[]>('modes');
    if (status === 200) useLocal.set('modes', _data);
  }
  async function fetchStats() {
    const { _data, status } = await useRawFetch<IStat[]>('stats');
    if (status === 200 && _data) stats.value = _data;
  }
  async function increaseTodayStats() {
    const date = new Date();
    date.setHours(date.getHours() - date.getTimezoneOffset() / 60);

    const { _data, status } = await useRawFetch<IStat>('stats', {
      method: 'post',
      body: { day: date.toISOString().slice(0, 10), }
    });
    
    if (status === 201 && _data) {
      let stat = stats.value.find((stat) => stat.id === _data.id);

      if (stat) stat.chores_done = _data.chores_done;
    }
  }
  async function fetchTasks() {
    const { _data, status } = await useRawFetch<IPage<ITask>>('tasks', {
      params: {
        page: page.taskPagination.page,
        page_size: page.taskPagination.page_size
      }
    });

    if (status === 200 && _data) {
      tasks.value = _data.results;
      page.taskPagination.count = _data.count;
    }
  }
  async function fetchProjects() {
    const { _data, status } = await useRawFetch<IPage<IProject>>('projects', {
      params: {
        page: page.projectPagination.page,
        page_size: page.projectPagination.page_size
      }
    });

    if (status === 200 && _data) {
      projects.value = _data.results;
      page.projectPagination.count = _data.count;
    }
  }
  async function fetchTags() {
    
    const { _data, status } = await useRawFetch<ITag[]>('tags');
    if (status === 200 && _data) {
      return (tags.value = _data);
    }
  }
  async function addTask(task: ITask) {
    const { status } = await useRawFetch('tasks', { method: 'post', body: task });
    if (status === 201) {
      alert.success(`Task ${task.title} created!`);
      // Send user to the first page
      page.taskPagination.page = 1;
      fetchTasks();
    }
  }
  async function saveTheTask(task: ITask) {
    const { status } = await useRawFetch(`tasks/${task.id}`, { method: 'put', body: task });
    if (status === 200) {
      alert.success(`'${task.title}' saved!`);
      fetchTasks();
    }
  }
  async function deleteTheTask(task: ITask) {
    const { status } = await useRawFetch(`tasks/${task.id}`, { method: 'delete' })

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
    const { status } = await useRawFetch('projects', { method: 'post', body: project});

    if (status === 201) {
      alert.success(`Project ${project.name} created!`);
      // Send user to the first page
      page.projectPagination.page = 1;
      fetchProjects();
    }
  }
  async function saveProject(project: IProject, newProjectName: string) {
    const { status } = await useRawFetch( `/projects/${project.id}/modify_title`,
      { method: 'PATCH', body: { name: newProjectName } }
    );

    if (status === 200) alert.success('Project saved!');
  }
  async function deleteProject(id: number) {
    const { status } = await useRawFetch(`projects/${id}`, { method: 'delete' });

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
      const { status } = await useRawFetch(`tasks/${auth.user.current_task_id}`, {
        method: 'PATCH', body: { obj: 'task', action: 'increment_gone_through', }
      });

      if (status === 200) fetchTasks();
    }
  }
  function deleteTask(task: ITask) {
    // TODO: Replace with Dialog
    if (window.confirm('Are you sure you want to delete this task?')) {
      deleteTheTask(task);
  
      if (
        page.taskPagination.page === page.totalTaskPages &&
        tasks.value.length === 1
      ) {
        page.decreaseTaskPagination();
      }
    }
  }
  async function changeCurrentTask(id: number | undefined) {
    const { _data, status } = await useRawFetch<ITask>('currentTask', { method: 'PUT', body: { id } })
    if (status === 200 && auth.user) {
      auth.user.current_task_id = _data?.id;
    }
  }
  async function toggleDone(task: ITask) {
    const { _data, status } = await useRawFetch<ITask>(`tasks/${task.id}/`, {
      method: 'PATCH', body: { obj: 'task', action: 'done' }
    })

    if (status === 200 && _data) {
      task.done = _data?.done;
      fetchProjects();
    }
  }
  function saveTask(oldTask: ITask, newTask: ITask) {
    saveTheTask(newTask);
    oldTask = newTask;
  }
  
  return {
    tasks, projects, tags, stats, fetchModes, fetchStats, increaseTodayStats, fetchTasks, fetchProjects, fetchTags,
    addTask, saveTask, deleteTask, addProject, saveProject, deleteProject, incrementGoneThrough,
    changeCurrentTask, toggleDone
  }
}, { persist: true });
