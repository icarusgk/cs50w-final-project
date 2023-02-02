<script setup lang="ts">
import type { TagType, TaskType } from '@/types';

import router from '@/router';

const props = defineProps<{
  id?: number;
  task: TaskType;
  info?: boolean;
  new?: boolean;
}>();

const emit = defineEmits(['addTag', 'removeTag', 'close']);

const chore = useChoreStore();
const alert = useAlertStore();

const newTagVisible = ref(true);
const newTag = ref('');

// Base all the tags out of the tags in the store
const allTags = ref(chore.tags);

function removeRepeatedTags(tags: TagType[]) {
  tags.forEach((taskTag: TagType) => {
  allTags.value = allTags.value.filter(
    (tag: TagType) => tag.name !== taskTag.name
  );});
}

// On opening of the task
removeRepeatedTags(props.task.tags);

// When the task changes

// Watch for changes in the props
watch(() => props.task.tags, (newTags) => removeRepeatedTags(newTags), { deep: true });


const selectedTags = computed(() => {
  return allTags.value.filter((tag: TagType) =>
    tag.name.includes(newTag.value.toLowerCase())
  );
});


const hasNotTag = () => !props.task.tags.some((tag: TagType) => tag.name === newTag.value)

async function addTag() {
  if (newTag.value) {
    // Push the tag but not upload it
    if (props.new && hasNotTag()) {
      // Check if newTag is not on props.task.tags
      props.task.tags.push({ name: newTag.value });
      // if not new
    } else {
      // filter if not in taskTags
      if (!(props.task.tags.filter((tag) => tag.name === newTag.value).length > 0)) {
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
            props.task.tags.push(response.data?.tag);
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

async function deleteTag(tag: TagType) {  
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
        emit('removeTag', tag);

        // Repopulate tags
        chore.fetchTags();
        allTags.value.push(tag);
      }
    }
  } else {
    // If is new, just remove it
    emit('removeTag', tag);
    allTags.value.push(tag);
  }
}

function addSelectedTag(tag: TagType) {
  newTag.value = tag.name;
  addTag();
}

function goToTag(tag: string) {
  router.push(`/tags/${tag}`);
  emit('close');
}
</script>

<template>
  <!-- Existing tags -->
  <div v-auto-animate class="tags-animate-container">
    <MiniLabel v-if="task.tags.length === 0 && info" :is-add="true">
      <template #title>
        <span>No tags</span>
      </template>
    </MiniLabel>
    <MiniLabel v-else v-for="tag in task.tags" :is-tag="true">
      <template #title>
        <span @click="goToTag(tag.name)">
          #{{ tag.name }}
        </span>
      </template>
      <template #icon>
        <DeleteTagIcon
          v-if="!info"
          @click="deleteTag(tag)"
          class="delete-tag-icon"
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
        <span class="task-title">Add tag</span>
      </template>
      <template #icon>
        <AddTagIcon />
      </template>
    </MiniLabel>

    <!-- Replace the button with input -->
    <MiniLabel
      v-if="!info && task.tags.length > 0 && task.tags.length < 3 && newTagVisible"
      @click="newTagVisible = false"
      :is-add="true"
    >
      <template #icon>
        <AddTagIcon />
      </template>
    </MiniLabel>
    <!-- Form -->
    <div class="form-container" v-if="!newTagVisible">
      <Popper placement="bottom" :arrow="true">
        <!-- Input -->
        <div class="new-tag-container">
          <input
            type="text"
            class="new-tag-name-input"
            v-model="newTag"
            @keydown.enter="addTag()"
          />
          <CloseIcon class="close-icon" @click="newTagVisible = true" />
          <button @click="addTag()" class="new-tag-button">Add</button>
        </div>
        <template #content="{ close }">
          <!-- Pre fetched tags -->
          <div>
            <span class="add-new-tag-text">Add a new tag:</span>
            <div 
              class="tag-results"
              @click="addSelectedTag(tag); close();"
              v-for="tag in selectedTags.slice(0, 5)"
            >
              <div class="tag-result">
                {{ tag.name }}
              </div>
            </div>
            <div
              class="tag-result"
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

<style scoped lang="scss">
.delete-tag-icon {
  margin-left: 0.5rem;
}

.task-title {
  margin-right: 0.5rem;
}

.tags-animate-container {
  display: flex;
  width: 100%;
}

.new-tag-container {
  display: flex;
  align-items: center;
  margin-left: 6px;

  .new-tag-name-input {
    margin-top: 2px;
    height: 1.5rem;
    outline: none;
    border: none;
    border-radius: 4px;
    padding: 1px 8px;
    width: 6rem;
    background: rgb(87, 87, 87);
    color: white;
  }

  .close-icon {
    transform: scale(40%);

    &:hover,
    &:focus,
    &:active {
      cursor: pointer;
    }
  }

  .new-tag-button {
    padding: 0 0.5rem;
    border-radius: 4px;
    border: none;

    &:hover,
    &:focus,
    &:active {
      cursor: pointer;
    }
  }
}

.add-new-tag-text {
  font-size: 0.75rem;
}

.tag-result {
  padding: 0.1rem 0.4rem;
  margin: 0.3rem 0;
  border-radius: 5px;
  background-color: rgba(233, 244, 233, 0.1);

  &:hover,
  &:focus,
  &:active {
    cursor: pointer;
  }
}
</style>
