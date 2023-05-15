<script setup lang="ts">
const auth = useAuthStore();
</script>

<template>
  <div class="flex flex-col justify-center items-center p-4 text-white lg:flex-row lg:px-16 lg:w-full lg:p-0 lg:items-start">
    <!-- Timer -->
    <TheTimer class="w-full mt-4 flex-wrap sm:w-[550px] lg:mt-12" />
    <!-- Tasks and Projects -->
    <div class="w-full mt-8 mx-4 sm:w-lg md:w-xl lg:w-120 lg:mt-0">
      <!-- Buttons -->
      <div :class="['flex', { 'opacity-10': !auth.isAuthed }]">
        <!-- New Task -->
        <NewTaskButton />
        <!-- New Project -->
        <NewProjectButton />
      </div>
      <div class="w-4/5 mt-32" v-if="!auth.isAuthed">
        <UnauthedLogin> To add tasks and projects </UnauthedLogin>
      </div>
      <!-- Projects and Tasks if user is authed -->
      <div v-if="auth.isAuthed">
        <AppProjects />
        <AppTasks />
      </div>
    </div>
  </div>
</template>