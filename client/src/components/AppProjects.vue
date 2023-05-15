<script setup lang="ts">
const chore = useChoreStore();
const page = usePageStore();

page.projectPagination.page = 1;
page.projectPagination.page_size = 2;
page.projectPagination.added = 1;

chore.fetchProjects();

const projects = computed(() => chore.projects.slice(0, 2));

function setPage(newPage: number) {
  page.setProjectPage(newPage);
}

function setAdded(newAdded: number) {
  page.setProjectAdded(newAdded);
}
</script>

<template>
  <div class="mt-2">
    <!-- Projects Title -->
    <Title class="pointer my-5 mx-3">
      <template #icon>
        <div class="i-mdi:lightbulb scale-350 mr-3"></div>
      </template>
      <template #type>
        <h1 @click="$router.push('/projects')">Projects</h1>
      </template>
      <template #count>
        <span v-if="page.totalProjectPages > 1">
          Page {{ page.projectPagination.page }} of
          {{ page.totalProjectPages }}
        </span>
      </template>
    </Title>
    <!-- Project List Container -->
    <div>
      <div class="flex items-center bg-light-gray w-full p-4 rounded-xl lg:w-4/5" v-if="projects.length === 0">
        <div class="i-fluent-info-12-regular scale-150 ml-3" />
        <span class="ml-4">There are no projects</span>
      </div>
      <!-- List of projects -->
      <div v-auto-animate>
        <Project
          v-for="project in projects"
          :project="project"
          :key="project.id"
        />
      </div>
    </div>
    <!-- Paginator -->
    <Paginate
      :pages="page.totalProjectPages"
      :page="page.projectPagination.page"
      :added="page.projectPagination.added"
      @prev="page.previousProjectPage()"
      @set:page="(page: number) => setPage(page)"
      @set:added="(added: number) => setAdded(added)"
      @next="page.nextProjectPage()"
    />
  </div>
</template>
