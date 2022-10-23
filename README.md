# Final Project

This is the repository for the **Harvard's CS50w Final Project**

Link to final project page: https://cs50.harvard.edu/web/2020/projects/final/capstone/

**Getting Started**

- In a README.md in your project’s main directory, include a writeup describing your project, and specifically your file MUST include all of the following:

# Distinctiveness and Complexity
Why you believe your project satisfies the distinctiveness and complexity requirements, mentioned above.

# What's contained in each file I created

## api/
The directory for my app. I decided to use The Django Rest Framework for this app.

> admin.py

The default file created by Django. I registered my models here in order to access them later on the Admin panel

> models.py

I created the following models in here:

- Tag

  A tag for assigning a task, to quickly organize them. A task can have a max of 3 tags, this is controlled by the client.
  - user (foreign key)
  - name
- User

  Extend the `AbstractUser` model from `django.contrib.auth.models` in here with the following fields:
  - **current_task_id**
  The id of the task the logged in user is currently working in. The client set this id clicking on a created task. If the id is not set, it defaults to 0.
  - **current_mode_id**
  The id of the mode the logged in user has currently active, if it has one. If the mode is empty, it defaults to 0.
  - **auto_start_pomos**
  Part of the pomodoro timer settings, when True it doesn't require the user to start the pomodoro timer when the break is over.
  - **auto_start_breaks**
  Part of the pomodoro timer settings, when True it doesn't require the user to start the break timer when the pomodoro timer is over.  
- Task
  A task is the basic block for keeping track of what has to be done. Tasks can have subtasks inside them which 
  - user (foreign key)
  - title
  - description
  - **estimated**
  The pomodoro timer count estimated to finish the task.
  - **gone_through**
  The pomodoro timer count the task has gone_through
  - **tags**
  The tags the task has. Many to many field so we can access the tasks when clicking on a tag on the client.
  - done (the state of the task)
  - **in_project**
  If the task is created inside a project. This helps us list the tasks only outside the project in the client.

- Subtask

  A subtask are used primarily on tasks. They are a smaller unit used to keep track of fine grained things to do inside a task.
  - task (foreign key)
  - title
  - description
  - done (the state of the subtask)
- Project

  A project's purpose is to encapsulate multiple tasks for an easier task tracking.
  - name
  - user (foreign key)
  - **tasks**
  Many to many field so that we can have multiple tasks on different projects. It can be blank so that we can a project without any tasks inside it.
- Stats

  The user stats. When a user finishes a pomodoro timer with a current working task active, the chores_done for the current day and the gone_through field for the active working task increase.
  - **day**
  The current day, defaults to `timezone.now` and accept the format of `yyyy-mm-dd`
  - **chores_done**
  The number of chores done in the current day
- Mode

  A customized mode that the user can create. Each user can create a max of 3 modes, this is controlled by the client in the settings.
  - user (foreign key)
  - **name**
  The name of the mode e.g. "School classes" or "Short pomo"
  - **pomo**
  The length of the Pomodoro timer defaults to 25 minutes.
  - **short_break**
  The length of the short break timer defaults to 5 minutes.
  - **long_break**
  The length of the long break timer defaults to 15 minutes.

> serializers.py

This file is required for the Django Rest Framework. Its purpose is to serialize the data in our models. They allow querysets to be converted to native Python datatypes that can be easily be rendered to JSON.

They also allow parsed data from a request to be converted back into a model object and be saved after being validated.

I inherited from `ModelSerializer` which makes it easier to make a serializer for each of our models, we just need to specify the model the serializer is going to be working with and the fields we want to serialize inside the class `Meta`

In `TaskSerializer` I included an extra option called `depth` with a value of 1, this allow us to access the data inside the subtasks.

In `ProjectSerializer` I overrode an the `get_fields` function to serialize the data inside the `tasks` field with the TaskSerializer. In the `Meta` class I included the extra option of `depth` with a value of 2 to access the tags and tasks info.

>  urls.py

The urls of my api application. Here I imported the `DefaultRouter` from `rest_framework.routers` to register the ViewSets created on the views.py file which I will later explain.

I anteceded all my routes inside the api app with the route of `api/` inside the `main/urls.py` file. So when the user visits the route of `api/<matching-route>` it routes them to the route inside the the api app.

Then in the urlpatterns in `api/urls.py` I included the urls registered inside the router variable with the `include` function with the route of `''` so when the user makes a request to the url of `api/tasks/` the DefaultRouter of Django Rest Framework controls the route and calls the appropiate ViewSet, in this case, the TaskViewSet. If the makes a request to `api/tags/` the router will handle it and call the appropieate ViewSet, the TagViewSet in this case, and so on. 

After this, I created paths for
- The Current task
- The Current mode
- The Information of a tag
- Registering an user
- Retrieving the current user info
I included the documentation for each of this routes inside the `views.py` file.

I'm using JWT based authentication using the [`djangorestframework-simplejwt`](https://github.com/jazzband/djangorestframework-simplejwt) pip package. 

To login the user has to make a request to the `token/` route with the user cretendials, this route will return a JSON object with the `refresh` and `access` keys.
```json
{
  "refresh": "eyJ0eXAiOiJ...",
  "access": "eyJ0eXAiOiJ..."
}
```

The `access` key is included in the Authorization header of each request we make in the client with the prefix of `Bearer `. 

When these tokens expire we need to hit the `token/refresh/` route with the `refresh` token as the body of the request, this will return a response with a new set of tokens.

> views.py

The views.py is where all my server logic is. I've included documentation inside each function inside this file.
I'm using class-based views, inheriting from [viewsets.ModelViewSet](https://www.django-rest-framework.org/api-guide/viewsets/#modelviewset) to create the views that Django Rest Framework's Default Router will contain. This will provide common actions for our models such as list, retrieve, create, update, partial_update and destroy. We just need to provide the queryset, serializer and optionally permission classes or pagination classes. For example:
```python
class TagViewSet(viewsets.ModelViewSet):
  queryset = Tag.objects.all() # <- Queryset 
  serializer_class = TagSerializer # <- Serializer
  permission_classes = [permissions.IsAuthenticated] # <- Permissions
```

In some cases I overrode the ModelViewSet functions to suit the needs of my app. The `get_queryset` function for instance, to return the current logged in user's data.

After these ModelViewSet inherited views, I created [`APIView`](https://www.django-rest-framework.org/api-guide/views/) inherited class-based views for its ease of use. I've included the documentation inside of the functions for these classes too.

## client/src

### assets/
The assets for my project such as the `base.css` for the color variables, the popper theme variables, the logo and the sound for starting and finishing a timer.

### components/
This is where all my components are.


# How to run my application


# Any other additional information the staff should know about your project.