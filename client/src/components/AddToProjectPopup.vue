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
  <div class="add-to-project-dropdown">
    <Popper arrow placement="bottom">
      <div>
        <span class="text">Add to Project</span>
      </div>
      <template #content>
        <!-- Popper Content -->
        <div class="project-select">
          <div
            class="project"
            v-if="chore.projects.length > 0"
            :class="{ inside: taskProjects.includes(project) }"
            v-for="project in allProjects"
            :key="project.id"
            @click="addToProject(project)"
          >
            {{ project.name }}
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

<style scoped lang="scss">
.add-to-project-dropdown {
  padding: 0.5rem;
  margin-top: 1rem;
  border-radius: 8px;
  width: 60%;
  text-align: center;
  background-color: rgb(58, 58, 58);

  &:hover,
  &:focus,
  &:active {
    cursor: pointer;
  }

  .text {
    font-weight: 500;
  }

  .project-select {
    width: 10rem;

    .project {
      background-color: rgb(92, 92, 92);
      padding: 0.5rem;
      border-radius: 8px;
      margin-bottom: 0.4rem;
      transition: background-color 0.3s ease-in-out;

      &:last-child {
        margin: 0;
      }
    }

    .inside {
      background-color: rgb(251, 105, 105);
    }
  }
}

@media (max-width: 768px) {
  .add-to-project-dropdown {
    width: 100%;
  }
}
</style>
