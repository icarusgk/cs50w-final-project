import type Task from './TaskType'

type Project = {
  id: number,
  title: string,
  tasks: Task[]
}

export default Project