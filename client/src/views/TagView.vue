<script setup lang="ts">
import type { ITask, ITag } from '@/types';

const route = useRoute();
const router = useRouter();
const chore = useChoreStore();

const tasks = ref<ITask[]>([]);
const fetchedTags = ref(false);

watchEffect(async () => {
  const urlTag = route.params.name;

  if (urlTag) {
    const { data } = await useFetch(`tagInfo/${urlTag}`, 'get');
    tasks.value = data as ITask[];
    fetchedTags.value = true;
  }
});

async function deleteTag() {
  const urlTag = route.params.name;

  const tagFound = chore.tags.find((t: ITag) => t.name === urlTag);

  if (window.confirm('Are you sure?')) {
    const { status } = await useFetch('tags', 'delete', null, tagFound?.id);
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
</script>

<template>
  <div class="<sm:p-4 py-8 px-16">
    <div class="flex items-center text-white gap-4">
      <BackIcon class="pointer" @click="$router.back()" />
    </div>
    <div class="flex items-center justify-between mb-4">
      <span class="text-white font-extrabold text-3xl">#{{ route.params.name }}</span>
      <div @click="deleteTag()" class="flex items-center bg-vivid-red text-white rounded-lg p-[0.7rem] delete-tag pointer">
        <span class="mr-4">Delete tag</span>
        <div><DeleteIcon /></div>
      </div>
    </div>
    <div class="flex flex-wrap gap-4">
      <BaseViewTask
        v-if="fetchedTags"
        v-for="task in tasks"
        :task="task"
        :key="task.id"
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
