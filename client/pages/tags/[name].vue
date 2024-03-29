<script setup lang="ts">
import type { ITask, ITag } from '@/types';

const route = useRoute();
const router = useRouter();
const chore = useChoreStore();

const tasks = ref<ITask[]>([]);
const fetchedTags = ref(false);

const urlTag = route.params.name;

watchEffect(async () => {
  if (urlTag) {
    const { _data } = await useRawFetch<ITask[]>(`tagInfo/${urlTag}`);

    if (_data) tasks.value = _data;
    fetchedTags.value = true;
  }
});

function deleteTask(task: ITask) {
  tasks.value = tasks.value.filter((t: ITask) => t.id !== task.id);
  if (tasks.value.length === 0) router.back();
}

async function deleteTag() {
  const urlTag = route.params.name;
  const tagFound = chore.tags.find((t: ITag) => t.name === urlTag);

  if (window.confirm('Are you sure?')) {
    const { status } = await useRawFetch(`tags/${tagFound?.id}`, {
      method: 'delete'
    });
    if (status === 204) {
      router.back();
      // Refresh the current tasks, project and tags
      if (tasks.value.length > 0) {
        chore.fetchTasks();
        chore.fetchProjects();
      }
      chore.fetchTags();
    }
  }
}

function removeTaskFromTag(task: ITask, tag?: ITag) {
  if (tag?.name === urlTag) {
    deleteTask(task);
  }
}
</script>

<template>
  <div class="<sm:p-4 py-8 px-16">
    <div class="flex items-center text-white gap-4 ml-3 mb-6">
      <div class="pointer i-bi-arrow-left-square-fill scale-250" @click="router.back()" />
      <div class="flex items-center justify-between w-full">
        <span class="text-white font-extrabold text-3xl ml-4">#{{ route.params.name }}</span>
        <div @click="deleteTag()" class="flex items-center bg-vivid-red text-white rounded-lg p-[0.7rem] delete-tag pointer">
          <div class="i-fluent:delete-12-regular scale-130" />
          <span class="ml-2">Delete tag</span>
        </div>
      </div>
    </div>
    
    <div class="flex flex-wrap gap-4">
      <BaseViewTask
        v-if="fetchedTags"
        v-for="task in tasks"
        :task="task"
        :key="task.id"
        @delete:task="deleteTask"
        @remove:tag="removeTaskFromTag"
      />
      <div v-else>
        <span class="text-white text-xl">Loading...</span>
      </div>

      <div v-if="fetchedTags && tasks.length === 0">
        <span class="text-white text-xl">There are no tasks inside this tag.</span>
      </div>
    </div>
  </div>
</template>
