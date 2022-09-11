import type Tag from './TagType';
import type Subtask from './SubtaskType';
import type Project from './ProjectType';

type Task = {
  id?: number;
  tags: Tag[];
  title: string;
  description: string;
  estimated: number;
  gone_through?: number;
  minutes?: number;
  done?: boolean;
  subtasks: Subtask[];
  project_tasks?: Project[];
};

export default Task;
