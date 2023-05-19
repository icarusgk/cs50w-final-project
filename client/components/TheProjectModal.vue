<script setup lang="ts">
import type { IProject } from '@/types';

const props = defineProps<{
  project: IProject;
  open: boolean;
}>();

const emit = defineEmits<{
  (e: 'exit:modal'): void;
  (e: 'update:name', name: string): void;
}>();

const chore = useChoreStore();
const page = usePageStore();

const { name: title } = toRefs(props.project);

const isTitlePristine = computed(() => title.value === props.project.name)

function deleteProject() {
  const shouldDelete = window.confirm('Are you sure?');

  if (!shouldDelete) {
    return;
  }

  chore.deleteProject(props.project.id as number);
  emit('exit:modal');

  const isLastProjectOnPage =
    page.projectPagination.page === page.totalProjectPages &&
    chore.projects.length === 1;

  if (isLastProjectOnPage) {
    page.decreaseProjectPagination();
  }
}

function saveAndExit() {
  chore.saveNewProjectTitle(props.project, title.value);
  emit('update:name', title.value);
  emit('exit:modal');
}

function checkAndSave() {
  isTitlePristine.value ? emit('exit:modal') : saveAndExit();
}
</script>

<template>
  <div>
    <!-- Modal -->
    <AppModal :open="open" @exit:modal="checkAndSave()">
      <!-- Title -->
      <template #title>
        <input
          type="text"
          name="title"
          class="w-[95%] border-none bg-transparent text-white font-bold text-[2rem] lg:w-full outline-none"
          maxlength="30"
          v-model="title"
          @keyup.ctrl.enter="checkAndSave()"
          v-focus
        />
      </template>
      <template #delete-icon>
        <div @click="deleteProject()" class="i-fluent:delete-20-filled scale-150 pointer mr-5" />
      </template>
      <!-- Modal Info -->
      <TheProjectModalBody :project="project" />
    </AppModal>
  </div>
</template>
