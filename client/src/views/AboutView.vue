<template>
  <div class="m-4 text-white my-8 mx-16">
    <div class="flex items-center -ml-2 mb-4">
      <div class="i-solar-info-square-bold scale-250" />
      <h1 class="ml-4">About</h1>
    </div>
  </div>
  <div class="2xl:mx-0 2xl:my-8 2xl:gap-8 flex-col flex gap-48 text-white justify-center items-center my-0 mx-16">
    <div class="w-full lg:w-[85%] 3xl:w-[80%] 3xl:justify-center">
      <div class="flex flex-col">
        <div>
          <div class="text-center">
            <img src="@/assets/tomato.png" alt="Tomato Logo" class="pb-4" />
            <p><b>Pomodoro</b></p>
            <span>is the italian word for tomato</span>
          </div>
        </div>
        <div class="mt-12 p-0 w-full text-center w-[600px] pl-12">
          <h2>The Pomodoro Technique</h2>
          <p class="mt-4">
            Pomodoro is a time management method where we divide the tasks we
            need to do into small sections of time with regular, brief breaks to
            encourage sustained focus and prevent mental weariness.
          </p>
        </div>
      </div>
      <div class="lg:m-0 text-center pt-8 mb-4">
        <div class="mb-12">
          <span class="block text-xl font-bold">How to use this technique?</span>
          <p>
            This technique was developed in the late 1980 by Francesco Cirillio,
            he described its bigges strength is its simplicity:
          </p>
        </div>
        <div class="lg:flex-col lg:w-full lg:mt-8 w-[950px] flex mt-4 text-center">
          <div class="flex flex-col mr-8">
            <span class="lg:block lg:font-semibold lg:m-0 block font-semibold ml-0.5 mb-4">Step 1</span>
            <span class="step-body">Pick a task to be done</span>
          </div>

          <div class="flex flex-col mr-8">
            <span class="lg:block lg:font-semibold lg:m-0 block font-semibold ml-0.5 mb-4">Step 2</span>
            <span class="step-body"
              >Start the Pomodoro Timer and focus on a single task until the
              timer rings</span
            >
          </div>

          <div class="flex flex-col mr-8">
            <span class="lg:block lg:font-semibold lg:m-0 block font-semibold ml-0.5 mb-4">Step 3</span>
            <span class="step-body"
              >When the timer is up, reflect on what you have completed</span
            >
          </div>

          <div class="flex flex-col mr-8">
            <span class="lg:block lg:font-semibold lg:m-0 block font-semibold ml-0.5 mb-4">Step 4</span>
            <span class="step-body">Take a 5 minute break</span>
          </div>

          <div class="flex flex-col mr-8">
            <span class="lg:block lg:font-semibold lg:m-0 block font-semibold ml-0.5 mb-4">Step 5</span>
            <span class="step-body"
              >Every 4 pomodoros, take a longer 15 minute break</span
            >
          </div>
        </div>
      </div>
    </div>
    <div class="2xl:w-4/5 3xl:mx-16 3xl:my-0 3xl:w-[70%] lg:mt-0 lg:mb-8 w-full w-1/5">
      <span class="block text-xl font-semibold">Try this technique if you:</span>
      <ul class="list-none">
        <li class="flex mt-4">
          <span class="pr-3">👀</span>
          <p>Find little distractions that often derail the whole workday.</p>
        </li>
        <li class="flex mt-4">
          <span class="pr-3">😮‍💨</span>
          <p>Consistently work past the point of optimal productivity.</p>
        </li>
        <li class="flex mt-4">
          <span class="pr-3">🎯</span>
          <p>Enjoy gamified goal-setting.</p>
        </li>
        <li class="flex mt-4">
          <span class="pr-3">📚</span>
          <p>
            Have lots of open-ended work that could take unlimited amounts of
            time (e.g., studying for an exam, research for a blog post, etc.).
          </p>
        </li>
        <li class="flex mt-4">
          <span class="pr-3">😅</span>
          <p>
            Are overly optimistic when it comes to how much you can get done in
            a day
          </p>
        </li>
      </ul>
    </div>
  </div>
</template>

