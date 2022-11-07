# Final Project

This is the repository for the [**Harvard's CS50w Final Project**](https://cs50.harvard.edu/web/2020/projects/final/capstone/)

<h1 style="text-align: center">🍅 Pomo.do</h1>

## About this project

**Pomo.do** is a pomodoro timer which divides productivity into spans of 25 minutes and helps keep track of projects, tasks, and subtasks. It is built with Vue 3 and Django.

I often struggle to keep focused on one thing and getting it done. Some of the things that help me with this are To-Do lists and Pomodoro timers, so I decided to make this app that combines both of them.

# 🧐 Distinctiveness and Complexity

I separated my app into a server REST API (Django REST Framework) and a front-end client (Vue 3 + Vite). 

I wanted to use Django as an API instead of the MVC model, so I decided to challenge myself and created the REST API with [Django REST Framework](https://www.django-rest-framework.org/), with the goal of learning common practices and concepts such as: serializers, pagination, responses, auth via tokens. DRF's specifics too such as: viewsets, and APIViews.

Furthermore I wanted to make my project different from the others in this course mainly by using [Vue 3](https://vuejs.org) in order to practice using a front-end framework and learn the commonly used concepts like props, two-way data binding and separation of concerns in components, as well as composables. I found this experience to be a refreshing one and it allowed me to see and learn a new way of organizing parts of the app into a better and cleaner structure.

Inside the client, 

I also used [Vite](https://vitejs.dev/) which provides a dev server and a build tool for modern web projects.

In addition, I used JWT tokens for authentication, which I later explain in this file. 

 
# 👀 What's contained in each file I created

## 📂 `api/`
The directory for my main app. Contains all the boilerplate files generated by Django plus the extra file of `serializers.py` that belongs to Django Rest Framework.

> 📄 `admin.py`

The default file created by Django. I registered my models here in order to access them later on the Admin panel.

> 📄 `models.py`

I created the following models in here:

- **Tag**

  A tag for assigning a task, to quickly organize them. A task can have a max of 3 tags, this is controlled by the client.
  - `user` (foreign key)
  - `name`

- **User**

  Extends the `AbstractUser` model from `django.contrib.auth.models` with the following extra fields:
  - **`current_task_id`**
  The id of the task the logged in user is currently working in. The client sets this id clicking on a created task. If the id is not set, it defaults to 0.
  - **`current_mode_id`**
  The id of the mode the logged in user has currently active, if it has one. If the mode is empty, it defaults to 0.
  - **`auto_start_pomos`**
  Part of the pomodoro timer settings, when True it doesn't require the user to start the pomodoro timer manually when the break is over.
  - **`auto_start_breaks`**
  Part of the pomodoro timer settings, when True it doesn't require the user to start the break timer manually when the pomodoro timer is over

- **Task**

  A task is the basic block for keeping track of what has to be done. Tasks can have subtasks inside them which are used to keep track of specific things to be done inside the task.

  - `user` (foreign key)
  - `title`
  - `description`
  - **`estimated`**
  The pomodoro timer count estimated to finish the task.
  - **`gone_through`**
  The pomodoro timer count the task has gone through.
  - **`tags`**
  The tags the task has. This is a many-to-many field so we can access the tasks inside the tag when clicking on a tag on the client.
  - `done` (the state of the task)
  - **`in_project`**
  Controls if the task is created inside a project. This helps us list independent tasks that don't belong to projects in the client.

- **Subtask**

  A subtask are used primarily on tasks. They are a smaller unit used to keep track of fine grained things to do inside a task.

  - `task` (foreign key)
  - `title`
  - `description`
  - `done` (the state of the subtask)

- **Project**

  A project's purpose is to encapsulate and contain multiple tasks for an easier task tracking.

  - `name`
  - `user` (foreign key)
  - **`tasks`**
  This is a many-to-many field so that we can have multiple tasks on different projects. It can be blank so that we can a project without any tasks inside it.

- **Stats**

  The logged in user stats. When a user finishes a pomodoro timer with a current working task active, the `chores_done` for the current day and the `gone_through` field for the active working task increase.

  - **`day`**
  The current day, defaults to `timezone.now` and accepts the format of `yyyy-mm-dd`
  - **`chores_done`**
  The number of chores done in the current day

- **Mode**

  A customized mode that the user can create. Each user can create a max of 3 modes, this is controlled by the client in the settings.

  - `user` (foreign key)
  - **`name`**
  The name of the mode e.g. "School classes" or "Short pomo"
  - **`pomo`**
  The length of the Pomodoro timer defaults to 25 minutes.
  - **`short_break`**
  The length of the short break timer defaults to 5 minutes.
  - **`long_break`**
  The length of the long break timer defaults to 15 minutes.

> 📄 `serializers.py`

This file is required for the Django Rest Framework. Its purpose is to serialize the data in our models. They allow querysets to be converted to native Python datatypes that can be easily be rendered to JSON.

They also allow parsed data from a request to be converted back into a model object and be saved after being validated.

In the classes inside this file I inherited from `ModelSerializer` which makes it easier to make a serializer for each of our models, we just need to specify inside the serializer in the class `Meta`,  the model it will be working with and the fields we want to serialize.

Most of the serializers do the same, except from the following two:

- In `TaskSerializer` I included an extra option called `depth` with a value of 1, this allow us to access the data inside the subtasks.

- In `ProjectSerializer` I overrode the `get_fields` function to serialize the data inside the `tasks` field with the `TaskSerializer`. Inside the `Meta` class I included the extra option of `depth` with a value of 2 to access the tags and tasks info inside the project.

>  📄 `urls.py`

The urls of my api application. Here I imported the `DefaultRouter` from `rest_framework.routers` to register the ViewSets created on the `views.py` file which I will later explain.

**`api/` matching**
I prefixed all my routes inside the api app with the route of `api/` inside the `main/urls.py` file. So when the user visits the route of `api/<matching-route>` it routes them to the route inside the the api app.

Then in the `urlpatterns` list, inside `api/urls.py`, I included the urls registered inside the router variable with the `include()` function with the route of `''` so when the user makes a request to the url of `api/tasks/` the DefaultRouter of Django Rest Framework controls the route and calls the appropriate ViewSet, in this case, the `TaskViewSet`. If the makes a request to `api/tags/` the router will handle it and call the appropriate ViewSet, the `TagViewSet`, and so on. 

After this, I created paths for
- The Current task
- The Current mode
- The Information of a tag
- Registering an user
- Retrieving the current user info

I included the documentation for each of this routes inside the `views.py` file.

> **JWT Auth**

I'm using JWT based authentication using the [`djangorestframework-simplejwt`](https://github.com/jazzband/djangorestframework-simplejwt) pip package.

**Login Process**
To login the user has to make a request to the `token/` route with the user credentials, this route will return a JSON object with the `refresh` and `access` keys. This tokens will be stored in the `localStorage` of the client under the `jwt` key.

```json
// Request
{
	"username": "icarusgk",
	"password": "1234"
}

// Response
{
  "refresh": "eyJ0eXAiOiJ...",
  "access": "eyJ0eXAiOiJ..."
}
```

From now on, the `access` key is included in the `Authorization` header of each request we make in the client with the prefix of `Bearer `. 

When these tokens expire we need to hit the `token/refresh/` route with the `refresh` token (saved in `localStorage`) as the body of the request, this will return a response with a new set of tokens that will replace the ones stored in `localStorage`.

```json
// Request made to 'token/refresh/'
{
	"refresh": "eyJ0eXAiOiJ..."
}

// Response
{
  "refresh": "eyJ0eXAiOiJ...",
  "access": "eyJ0eXAiOiJ..."
}
```

The `access` token is valid for 1 week and the `refresh` token is valid for a month. After the `refresh` token expires the user is logged out from the client.

> 📄 `views.py`

The `views.py` is where all my server logic is. I've included documentation inside each function inside this file.

I'm using class-based views, inheriting from [`viewsets.ModelViewSet`](https://www.django-rest-framework.org/api-guide/viewsets/#modelviewset) to create the views that Django Rest Framework's Default Router will have. The `ModelViewSet` class will provide common actions for our models such as `list`, `retrieve`, `create`, `update`, `partial_update` and `destroy`. We just need to provide the queryset, serializer and optionally permission classes or pagination classes. For example:

```python
class TagViewSet(viewsets.ModelViewSet):
  queryset = Tag.objects.all() # <- Queryset 
  serializer_class = TagSerializer # <- Serializer
  permission_classes = [permissions.IsAuthenticated] # <- Permissions
```

In some cases I overrode the `ModelViewSet` functions to suit the needs of my app. The `get_queryset` function for instance, I overrode it in order to return the current logged in user's data instead of returning all the users data.

After these `ModelViewSet` inherited views, I created [`APIView`](https://www.django-rest-framework.org/api-guide/views/) inherited class-based views. I chose this class for its ease of use. I've included the documentation inside the functions for these classes too.

## 🗃️ `client/src/`

I'm using Vue 3 as the framework for my client with Vite as the bundler and dev server.

### 🖌 `assets/`

This folder contains the assets for my project such as the `base.css` for the color variables, the [Popper](https://valgeirb.github.io/vue3-popper/) theme variables, the logo and the sound for starting and finishing a timer.

### 📁 `components/`
This is the folder where all my components are. It includes four folders: buttons, icons, modals, and slots.

#### 📁 `buttons/`

##### 📂 `new-buttons/`
Contains the clickable buttons used to create a task or a project. As well as the info buttons for Tags, Task and Project.

| Filename               | Description                                                                                                                                                                            |
|------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `NewProjectButton.vue` | Displays a modal that shows a form to create a new project.                                                                                                                            |
| `NewTaskButton.vue`    | Displays a modal that shows a form to create a new task.                                                                                                                               |
| `ChoreButton.vue`      | Is a wrapper component for the mentioned New Project and New Task buttons.                                                                                                             |
| `Tags.vue`             | Displays, adds and removes tags from a Task component. It can display tags without directly interacting with them as is the case when looking at tasks from the `TaskView`             |
| `Task.vue`             | The main button that is showed in the home screen with the task name, a delete and an info icon. When the info icon is clicked it displays a task info in a modal that allows editing. |
| `Project.vue`          | Displays a project's name with an info icon, when the info icon is clicked it displays a modal with the tasks that are inside it.                                                      |

#### 📂 `icons/`

The various icons used throughout the app, I made them as a Vue component for its ease of use inside the app.

#### 📂 `modals/`
The modals used throughout the application.

> `Modal.vue`

> 💡 This is a blank slate that can be used to create a modal anywhere in the app.

This is the base modal, it accepts the `open` prop to handle whether the modal is open or closed and the `isTask` prop which when set to false it aligns the items in the top part of the modal where the tags usually go. (We only pass this prop when the Modal is a task modal.)

This component uses the `<Teleport>` Vue built-in component to go the body of the html, we set its z-index to a value of 10 and align it to the center of the screen.

When the app is visited from a phone or a tablet, the modal automatically adjusts itself to the proper size through media queries.

> `ProjectModalInfo.vue`

This file contains the info part of the Project Modal, the tasks list. It uses the `Subtasks` component to manage the tasks. 

❕ Because subtasks and tasks are similar visually, the `Subtasks` component can handle tasks and subtasks.

> `TaskModalInfo.vue`

Contains the info part of the Task Modal, (description, subtasks, and the estimated pomos counter). I decided to create this different file to unclutter the main `TaskModal.vue` file and practice separation of concerns in components.


#### 📂 `slots/`

These are wrapper components for buttons or labels used inside the app that need tweaking depending where they are used.

> `MenuIcon.vue`

A wrapper component for the icons in the sidebar, it includes a slot for the icon and a title of the icon.

> `MiniLabel.vue`

A wrapper component that displays differently depending on the props being passed.<br>`isTask`: For adding and displaying subtasks inside the task modal or tasks inside the project modal.<br>`isTag`: For displaying tags inside the task modal.<br>`isAdd`: For adding a tag.

> `TaskType.vue`

A wrapper component for the header displayed on top of the projects and tasks lists . It accepts an icon and a title. I created this file because I wanted to work with Vue slots.

Rest of the files inside the `components/` folder

| Filename                | Description                                                                                                                                                                                                                                                                                                                                   |
|-------------------------|--------------|
| `AddToProjectPopup.vue` | Adds the current opened task to a project, and if the task is already inside the project it highlights it.                                                                                                                                                                                                                                    |
| `Alerts.vue`            | The component for showing alerts globally when an action is done, it transitions at the top right of the page. It uses the alert store which I will later talk about. It has three styles: alert, error and info.                                                                                                                             |
| `Chart.vue`             | The main component for the displaying the stats in a chart. It uses the [`apexcharts`](https://apexcharts.com/) library. This chart resizes automatically based on the window height and width. It is included in the `StatsView`.                                                                                                              |
| `CurrentTask.vue`       | Displays the current task the user is working on below the timer, it includes a button for removing the task as being the one the user is currently working on.                                                                                                                                                                               |
| `Paginate.vue`          | The pagination component showed below each of the projects and tasks lists. It conditionally based on the number of pages displays a ... button that moves 3 pages when clicked.                                                                                                                                                              |
| `ProjectInfo.vue`       | Displays the project's name and when clicked it opens its modal. It is used in the `ProjectView`.                                                                                                                                                                                                                                               |
| `ProjectModal.vue`      | Controls whether the Project Modal is showed and displays its info.                                                                                                                                                                                                                                                                           |
| `Projects.vue`          | The component that shows the `TaskType`, the page count, iterates over the projects and shows the pagination component.                                                                                                                                                                                                                         |
| `SaveButton.vue`        | The save button used in the Task and Project Modal.                                                                                                                                                                                                                                                                                           |
| `Settings.vue`          | Displays the settings modal to control whether to auto start pomos or breaks and create,change and delete modes.                                                                                                                                                                                                                              |
| `Sidebar.vue`           | The sidebar displayed at the left of the page, it includes links to the stats and the info of the app.                                                                                                                                                                                                                                        |
| `Subtask.vue`           | Controls the subtask or task being showed, it is the info part of the subtask/task. It contains the tags if its a task inside a project, it handles the title and description input to clear if the task or subtask is not saved. Conditionally shows pomo counter if it's a task.                                                            |
| `Subtasks.vue`          | This is the most complex component in the project, this is because this component is used in two cases: the parent component is a project or task. If the parent component is a task it handles the creation and deletion of subtasks. If the parent component is a project it handles the creation and deletion of tasks inside the project. |
| `TaskInfo.vue`          | The component that is displayed when the user is on the `TaskView`. It shows the tags, the number of pomos done and the number of estimated pomos, as well as the title and description. When clicked it opens the task modal info.                                                                                                             |
| `TaskModal.vue`         | The whole task modal being displayed with the tags, done, delete and close icons. As well as the title, description and `TaskModalInfo` mentioned previously, as well as the add to project and save buttons.                                                                                                                                   |
| `Tasks.vue`             | The component that shows the `TaskType`, the page count, iterates over the tasks and shows the pagination component.                                                                                                                                                                                                                            |
| `Timer.vue`             | The main timer component, it starts, restarts and stops the timer. It sets the type of timer and displays the Current Task                                                                                                                                                                                                                    |
| `TimerSetter.vue`       | The pomo count setter inside the task modal.                                                                                                                                                                                                                                                                                                  |
| `Title.vue`             | The title "Pomodoro Timer" displayed at the top of the app. When clicked it returns to the '/' route.                                                                                                                                                                                                                                         |
| `UnauthedChart.vue`     | The blurred chart showed when the user is not registered/logged out.                                                                                                                                                                                                                                                                          |
| `UnauthedLogin.vue`     | The component displayed in the Home page and above the blurred chart to Sign up or Login.                                                                                                                                                                                                                                                     |
| `UpperMenu.vue`         | The menu showed at the top of the app, where the title, user info, settings, and log in / register buttons are displayed.                                                                                                                                                                                                                     |
| `UserInfo.vue`          | The modal where the user can log out.                                                                                                                                                                                                                                                                                                         |


### 📂 `composables/`

> `useFetch.ts`

An `axios` wrapper, I created this file because I wanted to try Vue [composables](https://vuejs.org/guide/reusability/composables.html).


### 📂 `router/`

> `index.ts`

The main router file, it lazily loads the view components. 

❕If the user visits the `/login` or `/register` routes when logged it redirects them to home.


### 📂 `stores/`

I'm using [Pinia](https://pinia.vuejs.org/) as my library of choice for state management.

> `alerts.ts`

> 💡 The store for creating alerts that are available throughout the app.

I wanted to practice types and interfaces in TypeScript, so in this store I created the `AlertStyle` type with the different types of alerts there can be. Later I created an interface for the options of an alert. 

After this, I created the `defaultOptions` for any alert, and made the `AlertOptions` interface `Required`.

Finally I declare the `Alert` interface extending the `AlertOptions` plus an id and the message the alert will contain.

I found using interfaces more useful because you can extend them to other interfaces.

Inside the state, this store has an `items[]` array of type `Alert` that has all the alerts currently being displayed. When a new alert is created the `notify()` action is called which creates a new alert item with an unique id and pushes it to the items array. When 2 seconds are passed it removes itself from the items array with the `remove()` action. The `success()`, `error()` and `info()` actions use the `notify()` action with a custom style.


> `auth.ts`

> 💡 The store for managing the JWT tokens (saving, removing and replacing them) and handle the log in, register and logout process. 

At the top it creates a custom `axios` instance for login in and uses this instance for creating an interceptor. This interceptor fires when the get request for the `me/` endpoint in the `getUser()` store action fails, it then intercepts the request and replaces the JWT tokens. 

The `getUser()` action is called on each page initial load. If the `refresh` token has expired, it calls the `logout()` action to log the user out.

**Registering**

When a user registers, it automatically logs them in calling the login store action.

**Logging out**

When a user logs out, the `localStorage` is removed and the chore store is reset.

> `chore.ts`

> 💡 The store responsible for fetching the tasks, projects, tags, modes and stats. As well as managing the project and task pagination initially based on the returned data from tasks and projects.

I used [`getters`](https://pinia.vuejs.org/core-concepts/getters.html) in this store for retrieving the total pages of tasks and projects based on the store's state.

I later then created store actions for moving between pages.

Finally I created actions for increasing the stats, changing the current task, incrementing `current_task` `gone_through` pomodoros and managing the saving, deleting and updating of tasks and projects too.


> `modal.ts`

Manages a global state of the modal so that only one modal opens a time.

> `timer.ts`

> 💡The store for managing a global timer that retains state even when the page is changed. It has a `timerId` as part of the state that is set to the returned value of `window.setInterval` in Timer.vue's `initTimer()` function and is used when clearing the Interval in the `stopTimer()` function.

I'm using the [`dayjs`](https://github.com/iamkun/dayjs/) library to easily manage time in the store.

I created a `defaultTimer` that is used when a timer mode is not found in `localStorage` or the user is not logged in.

Then as part of the state I have a `currentTimer` that is set to a string of whichever timer is currently on i.e. (`pomo, short_break, long_break`) and I have a dedicated object for each of them in the state too with the timer and seconds as keys. 

After this I have the `currentMode` which helps keeping track of the timer's name the user is currently in. This with the help of the `sessions` and `current` state helps keeping track of the timers and assigning the next timer.

The done state and the ongoing variables keep track of the timer to conditionally display a UI elements.

And the `auto_start_pomo` and `auto_start_breaks` use the `auth` store to retrieve the user settings if the user is authenticated, if not they default to false.

I created store `getters` for order to retrieve the minutes and seconds from the `currentTimer.timer` and the `formattedTime` for displaying the time in the pages tab title in the format of `mm:ss`

As the final part of the store I have the timer actions to set a timer to the data passed, setting a timer to a new mode, decrementing a second from the `currentTimer`, setting the next timer based on the `sessions` and `current` state variables, setting the timer to the default one declared at the top, and setting a timer based on the passed name. I use most of these methods in the `Timer.vue` component.


### 📂 `types/`

The directory where I keep the types for the data I receive and set from and to the server.

> `index.ts`

The file I import all the files in the directory and export them.

### 📂 `views/`****

> The pages that the Vue Router renders on each route.

| **Route** | **Component** | **Description** |
|-------|-----------| ----------- |
| `/` | `Home.vue` |Contains the main content of the app uses the `auth` store to conditionally render components based if the user is signed in or not.|
| `about/` | `AboutView.vue` | Explains what a pomodoro timer is, how to use the technique, and has info on this course as well.|
|`register/`| `RegisterView.vue` | Has the form for registering a new user to the app and a link to let an existing user log in. If the registration process is successful the user is automatically logged in as explained in the `auth` store section.
| `login/` | `LoginView.vue` | Has the form for an existing user to log in. And a link to register a new user at the bottom. | 
| `projects/` | `ProjectsView.vue` | Displays 10 projects per page. |
| `tasks/` | `TasksView.vue` | Displays 10 projects per page. |
| `stats/` | `StatsView.vue` | This is where the chart displaying the user stats is. It uses the built-in `<Suspense>` Vue component for fetching the stats. The second icon in the sidebar. |
| `tags/` | `TagsView.vue` | Displays all the user tags. |
| `tag/:name` | `TagView.vue` | A page that accepts the parameter of `:name` to display all the tasks that contain that tag. |



### Rest of the files inside the directory

> `App.vue`

In this file, I render the whole app. 

I have the `SideBar` component, the `UpperMenu` by the right side positioned at the top and the rest of the content is displayed as a view by the `router-view` component, being the `HomeView` the default one on the `/` route.

I added the `Alerts` component in here so that they were accessible throughout the app.

> `axios.ts`

The config file for my `axios` instance. It sets a `baseURL`, a `Content-Type` header and adds the `Authorization` header to each request being sent.

> `main.ts`

> 💡 This is the main file of the application, it imports the `createApp` function from the `vue` library and with the imported `App` from `App.vue` we can create the app.

Then we proceed to call the `use()` function for being able to use things as `Pinia store, router, autoAnimatePlugin` in our app. Then we call the `component()` function to register the `Popper` component globally in order to use it in any component of our app.
Finally we call the `mount()` function and we pass the id of the element when we want to mount the app, in this case `#app`.

In the last of the file we fetch all the modes, tags and the user's stats with the `fetchAll()` function from the `chore` store.

> `.prettierrc`

I specified the styling rules for the app in here. We can easily format all of the files with these rules in the `src/` directory with the command:

```
prettier --write .
```

> `index.html`

The mounting point for the Vue app. It has a `<div>` with an id of `#app` which is where the app will be mounted to.

> `package.json`

This file keeps tracks of the dependencies in the app, as well as managing the scripts, the name and the version of the app.

> `tsconfig.*.json`

TypeScript configuration files required by the app and Vite.

Vite configuration file. It uses the `vue()` plugin and an alias of `@` for importing from the `./src` directory. 

# 🤔 How to run my application

Setting up the server
- Create a virtual environment
- Activate the virtual environment
- Install the requirements

Setting up the client
- Change directory to the client folder
- Install the dependencies
- Run the project


# Any other additional information the staff should know about your project.

