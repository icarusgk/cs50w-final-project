<script setup lang="ts">
import StreaksIcon from '@/components/icons/StreaksIcon.vue';
import ThemeIcon from '@/components/icons/ThemeIcon.vue';
import UserIcon from '@/components/icons/UserIcon.vue';
import SettingsIcon from '@/components/icons/SettingsIcon.vue';
</script>

<template>
  <div id="icons">
    <ul>
      <!-- Four icons -->
      <!-- Streaks -->
      <li>
        <div id="streaks-icon">
          <StreaksIcon />
          <p id="streaks-days-info">78 days</p>
        </div>
      </li>
      <!-- Dark Theme -->
      <li><ThemeIcon /></li>
      <!-- User -->
      <li><UserIcon /></li>
      <!-- Settings -->
      <li><SettingsIcon /></li>
    </ul>
  </div>
</template>


<style lang="scss" scoped>
#icons {
  ul {
    text-align: right;

    li {
      display: inline-block;
      margin-right: 0.1rem;

      &:hover {
        cursor: pointer;
      }

      #streaks-icon {
        display: flex;
        align-items: center;
        margin-right: 2rem;

        #streaks-days-info {
          margin-left: 1rem;
          font-weight: bold;
        }
      }
    }
  }
}
</style>