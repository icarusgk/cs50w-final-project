<script setup lang="ts">
import type { ITag, ITask } from '@/types';

import router from '@/router';

const props = defineProps<{
  id?: number;
  task: ITask;
  info?: boolean;
  new?: boolean;
}>();

const { task } = toRefs(props);

const emit = defineEmits<{
  (e: 'add:tag', tag: ITag): void
  (e: 'remove:tag', tag: ITag): void
  (e: 'close:modal'): void
}>(); 

const chore = useChoreStore();
const alert = useAlertStore();

const newTagVisible = ref(true);
const newTag = ref('');

// Base all the tags out of the tags in the store
const allTags = ref(chore.tags);

function removeRepeatedTags(tags: ITag[]) {
  tags.forEach((taskTag: ITag) => {
    allTags.value = allTags.value.filter(
      (tag: ITag) => tag.name !== taskTag.name
    );
  });
}

// On opening of the task
removeRepeatedTags(task.value.tags);

// When the task changes

// Watch for changes in the props
watch(() => task.value.tags, (newTags) => {
  removeRepeatedTags(newTags)
}, { deep: true });

const selectedTags = computed(() => {
  return allTags.value.filter((tag: ITag) =>
    tag.name.includes(newTag.value.toLowerCase())
  );
});

const hasNotTag = () =>
  !task.value.tags.some((tag: ITag) => tag.name === newTag.value);

async function addTag() {
  if (newTag.value) {
    // Push the tag but not upload it
    if (props.new && hasNotTag()) {
      // Check if newTag is not on task.value.tags
      emit('add:tag', { name: newTag.value })
      // task.value.tags.push({ name: newTag.value });
      // if not new
    } else {
      // filter if not in taskTags
      if (
        !(task.value.tags.filter((tag) => tag.name === newTag.value).length > 0)
      ) {
        // Make the request
        try {
          // Add the new tag to the existing task
          const response = await axios.patch(`tasks/${props.id}/`, {
            obj: 'tag',
            action: 'add',
            tag_name: newTag.value,
          });

          if (response?.status === 201 || response.status === 200) {
            if (response.data?.message === 'new') {
              alert.success('Tag created');
              chore.tags.push(response.data?.tag);
            } else {
              alert.info('Tag added');
            }
            // response.data will be the tag obj {id, name}
            emit('add:tag', response.data?.tag);
          }
        } catch (err) {
          console.log('addTag err', err);
        }
      }
    }
  }
  newTag.value = '';
  newTagVisible.value = true;
}

async function deleteTag(tag: ITag) {
  // In the opened subtask / task is not new
  if (!props.new) {
    // Ask for confirmation
    if (window.confirm('Are you sure?')) {
      const response = await axios.patch(`tasks/${props.id}/`, {
        obj: 'tag',
        action: 'remove',
        tag_id: tag.id,
      });
      if (response?.status === 200) {
        // emit the deletion of the tag
        alert.info('Tag removed');
        emit('remove:tag', tag);

        // Repopulate tags
        chore.fetchTags();
        allTags.value.push(tag);
      }
    }
  } else {
    // If is new, just remove it
    emit('remove:tag', tag);
    allTags.value.push(tag);
  }
}

function addSelectedTag(tag: ITag) {
  newTag.value = tag.name;
  addTag();
}

function goToTag(tag: string) {
  router.push(`/tags/${tag}`);
  emit('close:modal');
}
</script>

<template>
  <!-- Existing tags -->
  <div v-auto-animate class="flex w-full">
    <MiniLabel v-if="task.tags.length === 0 && info" :is-add="true">
      <template #title>
        <span>No tags</span>
      </template>
    </MiniLabel>
    <MiniLabel v-else v-for="tag in task.tags" :is-tag="true">
      <template #title>
        <span @click="goToTag(tag.name)"> #{{ tag.name }} </span>
      </template>
      <template #icon>
        <DeleteTagIcon
          v-if="!info"
          @click="deleteTag(tag)"
          class="ml-2"
        />
      </template>
    </MiniLabel>

    <!-- Add tags -->
    <MiniLabel
      v-if="!info && task.tags.length === 0 && newTagVisible"
      @click="newTagVisible = false"
      :is-add="true"
    >
      <template #title>
        <span class="mr-2">Add tag</span>
      </template>
      <template #icon>
        <AddTagIcon />
      </template>
    </MiniLabel>

    <!-- Replace the button with input -->
    <MiniLabel
      v-if="
        !info && task.tags.length > 0 && task.tags.length < 3 && newTagVisible
      "
      @click="newTagVisible = false"
      :is-add="true"
    >
      <template #icon>
        <AddTagIcon />
      </template>
    </MiniLabel>
    <!-- Form -->
    <div v-if="!newTagVisible">
      <Popper placement="bottom" :arrow="true">
        <!-- Input -->
        <div class="flex items-center ml-1.5">
          <input
            type="text"
            class="mt-[2px] h-6 outline-none border-none rounded-[4px] py-[1px] px-[8px] w-24 bg-[rgb(87,87,87)] text-white"
            v-model="newTag"
            v-focus
            @keydown.enter="addTag()"
          />
          <CloseIcon class="transform scale-40 pointer" @click="newTagVisible = true" />
          <button @click="addTag()" class="px-0 py-2 border-none pointer">Add</button>
        </div>
        <template #content="{ close }">
          <!-- Pre fetched tags -->
          <div>
            <span class="text-xs">Add a new tag:</span>
            <div
              class="tag-results"
              @click="
                addSelectedTag(tag);
                close();
              "
              v-for="tag in selectedTags.slice(0, 5)"
            >
              <div class="py-[0.1rem] px-[0.4rem] my-[0.3rem] mx-0 rounded-md pointer">
                {{ tag.name }}
              </div>
            </div>
            <div
              class="py-[0.1rem] px-[0.4rem] my-[0.3rem] mx-0 rounded-md pointer"
              @click="addTag()"
              v-if="selectedTags.length === 0"
            >
              {{ newTag }}
            </div>
          </div>
        </template>
      </Popper>
    </div>
  </div>
</template>
