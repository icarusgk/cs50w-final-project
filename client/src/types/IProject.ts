import type { ITask } from './ITask';

export interface IProject {
  id?: number;
  name: string;
  tasks?: ITask[];
  user?: number;
}
