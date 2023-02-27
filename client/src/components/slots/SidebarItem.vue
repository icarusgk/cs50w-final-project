<template>
  <div class="item group flex items-center <sm:rounded-tl-[10px] <sm:rounded-tr-[10px] w-full <sm:hover:w-full text-white p-4 pl-[1.7rem] relative transition-all duration-200 ease-in-out hover:bg-vivid-red hover:w-[180%] hover:rounded-tr-[10px] hover:rounded-br-[10px]">
    <i>
      <slot name="icon"></slot>
    </i>
    <div class="title <sm:transition-none <sm:flex-row absolute <sm:opacity-100 <sm:static <sm:visible <sm:transition-none <sm:ml-2 left-16 opacity-0 invisible transition transition ease-in-out duration-500 group-hover:opacity-100 group-hover:visible group-hover:delay-0">
      <h3>
        <slot name="heading"></slot>
      </h3>
    </div>
  </div>
</template>
