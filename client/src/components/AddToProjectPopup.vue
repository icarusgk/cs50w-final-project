<script setup lang="ts">
import type { IProject } from '@/types';

const props = defineProps<{
  taskId?: number;
}>();

const chore = useChoreStore();

const allProjects = chore.projects;

const taskProjects = ref<IProject[]>([]);

// Detect if is in project
allProjects.forEach((project: IProject) => {
  project.tasks?.forEach((task) => {
    if (task.id === props?.taskId) {
      taskProjects.value.push(project);
    }
  });
});

async function addToProject(project: IProject) {
  if (!taskProjects.value.includes(project)) {
    // Make API call to add the current task to project
    const response = await axios.patch(
      `projects/${project.id}/add_to_project/`,
      {
        task_id: props.taskId,
      }
    );

    if (response?.status === 200) {
      // Refetch
      chore.fetchProjects();
      // Visual changes
      taskProjects.value.push(project);
    }
  } else {
    const response = await axios.patch(`projects/${project.id}/delete_task/`, {
      task_id: props.taskId,
    });
    console.log(response);
    if (response?.status === 200) {
      console.log('removed', response.data);
      // Refetch
      chore.fetchProjects();
      // Visual changes
      taskProjects.value = taskProjects.value.filter((p) => p !== project);
    }
  }
}
</script>

<template>
  <!-- Add to project -->
  <div
    class="p-2 mt-4 rounded-lg w-full bg-[rgb(58,58,58)]] lg:w-[60%] pointer text-center"
  >
    <Popper arrow placement="bottom">
      <div>
        <span class="font-medium">Add to Project</span>
      </div>
      <template #content>
        <!-- Popper Content -->
        <div class="w-[10rem]">
          <div v-if="chore.projects.length > 0">
            <div
              :class="[{ 'bg-[rgb(251,105,105)]': taskProjects.includes(project) }, 'bg-lighter-gray p-2 rounded-lg mb-2 transition duration-300 ease-in-out last:m-0']"
              v-for="project in allProjects"
              :key="project.id"
              @click="addToProject(project)"
            >
              {{ project.name }}
            </div>
          </div>
          <div v-else>
            <span>No projects</span>
          </div>
        </div>
        <!-- Popper Content -->
      </template>
    </Popper>
  </div>
</template>

