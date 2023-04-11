<script setup lang="ts">
const chore = useChoreStore();

chore.projectPagination.page = 1;
chore.projectPagination.page_size = 10;
chore.projectPagination.added = 1;

chore.fetchProjects();

const projects = computed(() => chore.projects);
</script>

<template>
  <div class="p-2 lg:p-6">
    <div class="flex items-center gap-4 text-white ml-3">
      <div class="pointer i-bi-arrow-left-square-fill scale-250" @click="$router.back()" />
      <span class="text-white text-5xl font-extrabold">Projects</span>
    </div>
    <Paginate
      :pages="chore.totalProjectPages"
      :page="chore.projectPagination.page"
      :added="chore.projectPagination.added"
      @prev="chore.previousProjectPage"
      @set:page="(page: number) => chore.setProjectPage(page)"
      @set:added="(added: number) => chore.setProjectAdded(added)"
      @next="chore.nextProjectPage"
    />
    <div v-if="chore.projects.length > 0" class="flex flex-row flex-wrap text-white mt-4 gap-2">
      <BaseViewProject
        v-for="project in projects"
        :project="project"
        :key="project.id"
      />
    </div>
    <div class="m-4 flex items-center" v-else>
      <TaskInfoIcon />
      <span class="ml-4 font-semibold text-2xl">No Projects</span>
    </div>
    <Paginate
      :pages="chore.totalProjectPages"
      :page="chore.projectPagination.page"
      :added="chore.projectPagination.added"
      @prev="chore.previousProjectPage"
      @set:page="(page: number) => chore.setProjectPage(page)"
      @set:added="(added: number) => chore.setProjectAdded(added)"
      @next="chore.nextProjectPage"
    />
  </div>
</template>
