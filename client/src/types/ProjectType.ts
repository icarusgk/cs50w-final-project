import type Task from './TaskType';

type Project = {
  id?: number;
  name: string;
  tasks?: Task[];
  user?: number;
};

export default Project;
