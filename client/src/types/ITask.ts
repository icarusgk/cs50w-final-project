import type { ITag } from './ITag';
import type { IProject } from './IProject';

export interface ITask {
  id?: number;
  tags: ITag[];
  title: string;
  description: string;
  estimated: number;
  gone_through?: number;
  minutes?: number;
  done?: boolean;
  subtasks?: ITask[];
  project_tasks?: IProject[];
}

