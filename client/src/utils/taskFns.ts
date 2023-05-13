import axios from 'axios';
import type { ITask, ITag } from '@/types';
import { useChoreStore, useAuthStore, usePageStore } from '@/stores';

const chore = useChoreStore();
const auth = useAuthStore();
const page = usePageStore();

export function addTag(task: ITask, tag: ITag) {
  task.tags.push(tag);
}

export function removeTag(task: ITask, tagId?: number) {
  task.tags = task.tags.filter((tag: ITag) => tag.id !== tagId);
}

export function saveTask(oldTask: ITask, newTask: ITask) {
  chore.saveTask(newTask);
  oldTask = newTask;
}

export async function toggleDone(task: ITask) {
  const response = await axios.patch(`tasks/${task.id}/`, {
    obj: 'task',
    action: 'done',
  });
  if (response?.status === 200) {
    task.done = response.data?.done;
    chore.fetchProjects();
  }
}

export function deleteTask(task: ITask) {
  // TODO: Replace with Dialog
  if (window.confirm('Are you sure you want to delete this task?')) {
    chore.deleteTask(task);

    if (
      page.taskPagination.page === page.totalTaskPages &&
      chore.tasks.length === 1
    ) {
      page.decreaseTaskPagination();
    }
  }
}

export async function changeCurrentTask(id: number | undefined) {
  const { data, status } = await axios.put('currentTask', { id })
  if (status === 200) {
    auth.user!.current_task_id = data.id;
  }
}