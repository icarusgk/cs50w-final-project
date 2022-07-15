import type Tag from './TagType'

type Task = {
  id: Number,
  tags: Tag[],
  title: string,
  description: string,
  estimated: Number,
  gone_through: Number,
  minutes: Number,
  subtasks: Task[]
}

export default Task