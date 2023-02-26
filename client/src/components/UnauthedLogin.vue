<template>
  <div class="text-2xl mt-8 md:text-3xl block text-[2rem] font-semibold p-4 bg-vivid-red rounded-lg">
    <router-link class="no-underline text-white transition-all duration-200 ease-in hover:decoration-solid hover:text-[rgb(255,201,201)]" to="/login">Login</router-link>
    <span> or </span>
    <router-link class="no-underline text-white transition-all duration-200 ease-in hover:decoration-solid hover:text-[rgb(255,201,201)]" to="/register">Sign up</router-link>
  </div>
  <div class="py-4 px-0 font-medium text-xl">
    <slot></slot>
  </div>
</template>

