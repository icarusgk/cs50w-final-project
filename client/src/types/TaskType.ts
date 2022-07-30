import type Tag from './TagType'

type Task = {
  id: number,
  tags: Tag[],
  title: string,
  description: string,
  estimated: number,
  gone_through?: number,
  minutes?: number,
  done?: boolean,
  subtasks: Task[]
}

export default Task