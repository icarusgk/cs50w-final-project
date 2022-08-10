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
    <div class="title">
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

  &:hover, &:focus {
    cursor: pointer;
  }

  .icon {
    margin-top: 2px;
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
  background-color: var(--lighter-gray);
  color: var(--white);
  height: 100%;
}

.add {
  padding: 0.1rem 0.3rem;
  border-radius: 5px;
  margin: 0.2rem 0.2rem;
  font: {
    size: 0.7rem;
    weight: 500;
  }
  background-color: #444;
  color: var(--white);
}

@media (max-width: 768px) {
  .tag {
    font-size: 0.55rem;
  }
}

</style>