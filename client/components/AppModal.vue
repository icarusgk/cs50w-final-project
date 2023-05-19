<script setup lang="ts">
const props = defineProps<{
  open: Boolean;
  isTask?: Boolean;
}>();

const emit = defineEmits<{
  (e: 'exit:modal'): void
}>();

function exit(event: any) {
  if (event.key === 'Escape' && props.open) emit('exit:modal');
}

onMounted(() => window.addEventListener('keyup', exit))
onUnmounted(() => window.removeEventListener('keyup', exit))
</script>

<template>
  <Teleport to="body">
    <div v-if="open" class="modal responsive-modal" @keyup="(event) => exit(event)">
      <div class="flex justify-between" :class="{ 'items-center': !isTask }">
        <div class="flex flex-col w-full">
          <div v-if="isTask" class="flex mb-4">
            <slot name="tags"></slot>
          </div>

          <div class="title-container">
            <slot name="title"></slot>
          </div>
        </div>

        <div>
          <slot name="delete-icon"></slot>
        </div>

        <div @click="$emit('exit:modal')" class="pointer">
          <div class="i-fluent-dismiss-circle-32-filled scale-220" />
        </div>
      </div>
      <slot></slot>
      <div class="<sm:flex-col flex gap-4">
        <slot name="save-button"></slot>
      </div>
    </div>
  </Teleport>
</template>
