import type Task from './ITask';

interface Project {
  id?: number;
  name: string;
  tasks?: Task[];
  user?: number;
};

export default Project;
