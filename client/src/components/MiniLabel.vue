<script setup lang="ts">
defineProps<{
  isTask?: Boolean
  isTag?: Boolean
  isAdd?: Boolean
}>()

</script>

<template>
  <div class="minilabel" :class="{ task: isTask, tag: isTag, add: isAdd }" >
    <!-- Title -->
    <div>
      <slot name="title"></slot>
    </div>
    <!-- Icon -->
    <div class="icon">
      <slot name="icon"></slot>
    </div>
    
  </div>
</template>

<style lang="scss" scoped>
.minilabel {
  display: flex;
  align-items: center;

  &:hover {
    cursor: pointer;
  }

  .icon {
    margin-top: 2px;
    margin-left: 0.3rem;
  }
}

.tag {
  padding: 0.15rem 0.3rem;
  border-radius: 5px;
  margin: 0.2rem 0.2rem;
  font: {
    size: 0.7rem;
    weight: 500;
  }
  background-color: var(--white);
  color: var(--black);
}

.task {
  padding: 0.01rem 0.7rem;
  border-radius: 8px;
  margin-right: 0.5rem;
  background-color: var(--lighter-gray);
  color: var(--white);
}

.add {
  padding: 0.6rem 0.5rem;
  border-radius: 5px;
  margin: 0.2rem 0.2rem;
  font: {
    size: 0.7rem;
    weight: 500;
  }
  background-color: #444;
  color: var(--white);
}

</style>