<script setup lang="ts">
import type { TaskType, TagType } from '@/types';

const route = useRoute();
const router = useRouter();
const chore = useChoreStore();

const tasks = ref<TaskType[]>([]);
const fetchedTags = ref(false);

watchEffect(async () => {
  const urlTag = route.params.name;

  if (urlTag) {
    const { data } = await useFetch(`tagInfo/${urlTag}`, 'get');
    tasks.value = data as TaskType[];
    fetchedTags.value = true;
  }
});

async function deleteTag() {
  const urlTag = route.params.name;

  const tagFound = chore.tags.find((t: TagType) => t.name === urlTag);
  
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
  <div class="tag-info-container">
    <div class="go-back">
      <BackIcon class="button" @click="$router.back()" />
    </div>
    <div class="tag-name">
      <span class="title">#{{ route.params.name }}</span>
      <div @click="deleteTag()" class="delete-tag">
        <span class="text">Delete tag</span>
        <div><DeleteIcon /></div>
      </div>
    </div>
    <div class="all-tasks-container">
      <BaseViewTask v-if="fetchedTags" 
        v-for="task in tasks" :task="task" :key="task.id" 
      />
      <div v-else>
        <span class="info">Loading...</span>
      </div>

      <div v-if="fetchedTags && tasks.length === 0">
        <span class="info">There are no tasks inside this tag.</span>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.tag-info-container {
  padding: 2rem 4rem;
  .go-back {
    display: flex;
    align-items: center;
    color: white;
    gap: 1rem;

    .button {
      &:hover,
      &:focus,
      &:active {
        cursor: pointer;
      }
    }
    .title {
      color: white;
      font-size: 3rem;
      font-weight: 800;
    }
  }

  .tag-name {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1rem;

    .title {
      color: white;
      font-size: 2rem;
      font-weight: 800;
      margin-top: 0.5rem;
    }
    .delete-tag {
      display: flex;
      align-items: center;
      background-color: var(--vivid-red);
      color: white;
      border-radius: 8px;
      padding: 0.7rem;
      box-shadow: 0 3px 0 1px lighten(#ed4747, 10%);
      transition: box-shadow 0.2s cubic-bezier(0.075, 0.82, 0.165, 1);

      &:hover,
      &:focus,
      &:active {
        cursor: pointer;
      }

      &:active {
        box-shadow: 0 0 var(--vivid-red);
      }

      .text {
        margin-right: 1rem;
      }
    }
  }

  .all-tasks-container {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    gap: 1rem;
    .info {
      color: white;
      font-size: 1.1rem;
    }
  }
}

@media (max-width: 480px) {
  .tag-info-container {
    padding: 1rem;
  }
}
</style>
