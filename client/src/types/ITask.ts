import type Tag from './ITag';
import type Subtask from './ISubtask';
import type Project from './IProject';

interface Task extends Subtask {
  id?: number;
  tags?: Tag[];
  title: string;
  description: string;
  estimated?: number;
  gone_through?: number;
  minutes?: number;
  done?: boolean;
  subtasks?: Task[];
  project_tasks?: Project[];
}

export default Task;
