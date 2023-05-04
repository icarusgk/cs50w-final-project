import type { ITask } from './ITask';

interface IProject {
  id?: number;
  name: string;
  tasks?: ITask[];
  user?: number;
}

export type { IProject };
