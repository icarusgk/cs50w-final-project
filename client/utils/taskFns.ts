import type { ITask, ITag } from '@/types';

export function addTag(task: ITask, tag: ITag) {
  task.tags.push(tag);
}

export function removeTag(task: ITask, tagId?: number) {
  task.tags = task.tags.filter((tag: ITag) => tag.id !== tagId);
}
