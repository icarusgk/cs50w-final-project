<script setup lang="ts">
const chore = useChoreStore();
const page = usePageStore();

page.projectPagination.page = 1;
page.projectPagination.page_size = 10;
page.projectPagination.added = 1;

chore.fetchProjects();

const projects = computed(() => chore.projects);
</script>

<template>
  <div class="p-2 lg:p-6 text-white">
    <div class="flex items-center gap-4 text-white ml-3">
      <div class="pointer i-bi-arrow-left-square-fill scale-250" @click="$router.back()" />
      <span class="text-white text-5xl font-extrabold">Projects</span>
    </div>
    <Paginate
      :pages="page.totalProjectPages"
      :page="page.projectPagination.page"
      :added="page.projectPagination.added"
      @prev="page.previousProjectPage"
      @set:page="(p: number) => page.setProjectPage(p)"
      @set:added="(added: number) => page.setProjectAdded(added)"
      @next="page.nextProjectPage"
    />
    <div v-if="chore.projects.length > 0" class="flex flex-row flex-wrap text-white mt-4 gap-2">
      <BaseViewProject
        v-for="project in projects"
        :project="project"
        :key="project.id"
      />
    </div>
    <div class="m-4 flex items-center" v-else>
      <div class="i-fluent-info-12-regular scale-150 ml-3" />
      <span class="ml-4 font-semibold text-2xl">No Projects</span>
    </div>
    <Paginate
      :pages="page.totalProjectPages"
      :page="page.projectPagination.page"
      :added="page.projectPagination.added"
      @prev="page.previousProjectPage"
      @set:page="(p: number) => page.setProjectPage(p)"
      @set:added="(added: number) => page.setProjectAdded(added)"
      @next="page.nextProjectPage"
    />
  </div>
</template>
