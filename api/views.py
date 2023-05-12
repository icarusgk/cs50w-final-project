from .serializers import *
from .models import *
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import permissions, status
from rest_framework.pagination import PageNumberPagination
from django.http import Http404
from rest_framework_simplejwt.views import TokenObtainPairView
from django.conf import settings


class ProjectResultsSetPagination(PageNumberPagination):
    """Sets the page size and max size for Project Pagination"""
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 10


class TaskResultsSetPagination(PageNumberPagination):
    """Sets the page size and max size for Task Pagination"""
    page_size = 4
    page_size_query_param = 'page_size'
    max_page_size = 10


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer


class StatsViewSet(viewsets.ModelViewSet):
    queryset = Stats.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = StatsSerializer

    def get_queryset(self):
        """
        Returns current user's stats
        """
        return self.request.user.stats.all().order_by('day')

    def create(self, request):
        """
        Creates a new stat for the current day
        """
        # See if there is a stat with the same date
        stat, created = Stats.objects.get_or_create(
            user=request.user, day=request.data['day'])

        stat.chores_done = 1 if created else stat.chores_done + 1
        stat.save()

        return Response(
            StatsSerializer(stat).data,
            status=status.HTTP_201_CREATED)


class ModeViewSet(viewsets.ModelViewSet):
    queryset = Mode.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ModesSerializer

    def get_queryset(self):
        """
        Returns current user's modes
        """
        return self.request.user.modes.all()

    def create(self, request):
        """
        Checks for time validation (pomo, short_break, long_break)
        and creates a new timer mode
        """
        pomo = request.data['pomo']
        short_break = request.data['short_break']
        long_break = request.data['long_break']

        if int(pomo) >= 60 or int(short_break) >= 60 or int(long_break) >= 60:
            return Response(
                {'message': 'Not valid, timers can only be less than an hour long.'},
                status=status.HTTP_400_BAD_REQUEST)

        if request.data['name'] == 'Default':
            return Response({'message': 'There can only be one default mode.'},
                            status=status.HTTP_400_BAD_REQUEST)


        serializer = ModesSerializer(data=request.data)

        if serializer.is_valid():
            mode = Mode.objects.create(**serializer.data, user=request.user)
            return Response(
                ModesSerializer(mode).data,
                status=status.HTTP_201_CREATED)

        return Response('not valid', status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """
        Deletes a mode from the current user
        """
        # Reset to default if the current timer is the one
        # being deleted
        if request.user.current_mode_id == int(pk):
            user = User.objects.get(id=request.user.id)
            user.current_mode_id = 0
            user.save()

            mode_to_delete = Mode.objects.get(id=int(pk))
            mode_to_delete.delete()

            return Response(
                'Back to default',
                status=status.HTTP_204_NO_CONTENT)
        return super().destroy(request)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TaskSerializer
    pagination_class = TaskResultsSetPagination

    def get_queryset(self):
        """
        Returns the current user's parent tasks
        in descending order
        """
        return self.request.user.tasks.all().filter(in_project=False, parent_task=None).order_by('-id')

    def retrieve(self, request, pk=None):
        """
        Return a certain task info based on the
        authenticated user
        """
        task = Task.objects.filter(id=pk).first()
        if task.user != request.user:
            return Response({"data": "error"},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(TaskSerializer(task).data, status=status.HTTP_200_OK)

    def create(self, request):
        """
        Create a new task with tags and subtasks
        for the current user
        """
        serializer = TaskSerializer(data=request.data)

        subtasks = request.data.get('subtasks')
        tags = request.data.get('tags')

        print(request.data)

        if serializer.is_valid():
            task = Task(user=request.user, **serializer.data)
            task.save()

            # Add tags
            if tags:
                for tag in tags:
                    tag_obj, _ = Tag.objects.get_or_create(name=tag['name'], user=request.user)
                    task.tags.add(tag_obj)

            # Add subtasks
            if subtasks:
                for subtask in subtasks:
                    task_serializer = TaskSerializer(data=subtask)
                    if task_serializer.is_valid():
                        sub = Task(user=request.user, **serializer.data, parent_task=task)
                        sub.save()

            # Return the newly created task
            return Response(
                TaskSerializer(task).data,
                status=status.HTTP_201_CREATED)
        return Response({'message': 'error'},
                        status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        """
        Updates in real time
        these elements (obj) inside the tasks:
        - Tags
        - Subtasks

        And updates the task itself
        """
        # Assign the request to a data variable
        # for ease of use
        data = request.data
        if "obj" in data:
            obj = data['obj']
            # Live update tags
            if obj == 'tag':
                task = Task.objects.filter(id=pk).first()

                if data['action'] == 'remove':
                    tag_id = data['tag_id']
                    tag_obj = Tag.objects.get(id=tag_id)

                    task.tags.remove(tag_obj)
                    task.save()

                    return Response({'message': f'tag removed'},
                                    status=status.HTTP_200_OK)

                if data['action'] == 'add':
                    # Get or create the tag
                    (tag_obj, is_new) = Tag.objects.get_or_create(
                        user=request.user, name=data['tag_name'])

                    # If tag already exists, check if tag is in obj already
                    if not is_new and tag_obj in task.tags.all():
                        return Response(
                            {'message': 'tag already exists in task'}, status=status.HTTP_400_BAD_REQUEST)

                    # Add tag
                    task.tags.add(tag_obj)
                    task.save()

                    serialized_tag = TagSerializer(tag_obj).data

                    if is_new:
                        return Response({
                            'message': 'new',
                            'tag': serialized_tag,
                        }, status=status.HTTP_201_CREATED)
                    return Response({'tag': serialized_tag},
                                    status=status.HTTP_200_OK)
            # Live update subtasks
            elif obj == 'subtask':
                task = Task.objects.get(id=pk)

                # Create subtask
                if data['action'] == 'add':
                    subtask = data['subtask']
                    # Replace subtask to Task object
                    subtask = Task.objects.create(user=request.user, **subtask, parent_task=task)

                    return Response(
                        TaskSerializer(subtask).data,
                        status=status.HTTP_201_CREATED)
                # Remove subtask
                elif data['action'] == 'remove':
                    subtask_obj = Task.objects.get(id=data['subtask_id'])
                    subtask_obj.delete()

                    return Response({"message": "subtask removed"},
                                    status=status.HTTP_204_NO_CONTENT)
                # Update subtask
                elif data['action'] == 'update':
                    subtask = data['subtask']
                    subtask_obj = Task.objects.get(id=subtask['id'])
                    serializer = TaskSerializer(subtask_obj, data=subtask)

                    if serializer.is_valid():
                        serializer.save()

                    return Response({"message": "updated"},
                                    status=status.HTTP_200_OK)
                elif data['action'] == 'done':
                    subtask_obj = Task.objects.get(id=data['subtask_id'])

                    subtask_obj.done = not subtask_obj.done
                    subtask_obj.save()

                    return Response({"done": subtask_obj.done},
                                    status=status.HTTP_200_OK)
            elif obj == 'task':
                if data['action'] == 'done':
                    task = Task.objects.get(id=pk)

                    task.done = not task.done
                    task.save()

                    return Response({"done": task.done},
                                    status=status.HTTP_200_OK)
                if data['action'] == 'increment_gone_through':
                    task = Task.objects.get(id=pk)

                    task.gone_through += 1
                    task.save()

                    return Response(
                        task.gone_through,
                        status=status.HTTP_200_OK)

            return Response({'message': 'error'})

    def destroy(self, request, pk=None):
        """
        Deletes a task from the current user
        """
        user = User.objects.get(id=request.user.id)
        task = Task.objects.get(id=int(pk))

        # If the task being deleted is the same
        # as the current one
        # set it to 0
        if int(pk) == user.current_task_id:
            user.current_task_id = 0
            user.save()

        task.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TagSerializer

    def get_queryset(self):
        """
        Returns the current user's tags
        """
        return self.request.user.tags.all()


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProjectSerializer
    pagination_class = ProjectResultsSetPagination

    def get_queryset(self):
        """
        Returns the current user's projects
        """
        return self.request.user.projects.all().order_by('-id')

    def get_project(self, pk):
        """
        Tries to get the project object with the id of pk
        it if fails it raises a HTTP404 error

        Keyword arguments:
        pk -- the id of the to be retrieved object
        """
        try:
            return Project.objects.get(id=pk)
        except Project.DoesNotExist:
            raise Http404

    def create(self, request):
        """
        Create a new Project with tasks
        """
        project = Project.objects.create(
            user=request.user, name=request.data['name'])

        tasks = request.data.get('tasks')

        if tasks:
            for task in tasks:
                task_serializer = TaskSerializer(data=task)

                if task_serializer.is_valid():
                    task_obj = Task.objects.create(
                        user=request.user, in_project=True, **task_serializer.data)

                    tags = task.get('tags')

                    if tags:
                        for tag in task['tags']:
                            tag_obj = Tag.objects.filter(
                                name=tag['name']).first()

                            if not tag_obj:
                                # Create tag
                                tag_obj = Tag.objects.create(name=tag['name'], user=request.user)

                            task_obj.tags.add(tag_obj)

                    # Add task to the project
                    project.tasks.add(task_obj)
                    project.save()

        return Response(
            ProjectSerializer(project).data,
            status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['patch'])
    def modify_title(self, request, pk=None):
        """Modifies the project's title"""
        project = self.get_project(pk)
        project.name = request.data['name']
        project.save()

        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'])
    def add_new_task(self, request, pk=None):
        """Adds a new task inside the project"""
        project = self.get_project(pk)

        task_serializer = TaskSerializer(data=request.data['task'])

        if task_serializer.is_valid():
            task = Task.objects.create(
                user=request.user, in_project=True, **task_serializer.data)

            tags = request.data['task']['tags']
            for tag in tags:
                (the_tag, created) = Tag.objects.get_or_create(
                    name=tag['name'], user=request.user)
                task.tags.add(the_tag)

            task.save()

            project.tasks.add(task)
            project.save()
        return Response(
            TaskSerializer(task).data,
            status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['patch'])
    def update_task(self, request, pk=None):
        """Updates the task inside the project"""
        task = Task.objects.get(id=request.data['subtask']['id'])
        serializer = TaskSerializer(task, data=request.data['subtask'])

        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'])
    def delete_task(self, request, pk=None):
        """
        Deletes a task inside a project
        or removes it from outside the project
        """
        task = Task.objects.get(id=request.data['task_id'])

        # Remove task from project
        if not task.in_project:
            project = self.get_project(pk)
            project.tasks.remove(task)

            return Response("task removed", status=status.HTTP_204_NO_CONTENT)
        # delete task totally
        task.delete()

        return Response("task deleted", status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['patch'])
    def add_to_project(self, request, pk=None):
        """Adds a task to a project from outside"""
        project = self.get_project(pk)
        task = Task.objects.get(id=request.data['task_id'])

        project.tasks.add(task)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'])
    def task_done(self, request, pk=None):
        """Toggles a task done status"""
        project = self.get_project(pk)
        task = project.tasks.get(id=request.data['task_id'])

        task.done = not task.done
        task.save()

        return Response({"done": task.done}, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        """
        Deletes the project with an id of pk
        """
        project = self.get_project(pk)

        for task in project.tasks.all():
            if task.in_project:
                task.delete()

        project.delete()

        return Response({'data': 'project deleted'},
                        status=status.HTTP_204_NO_CONTENT)


class RegisterJWTView(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        confirmation = request.data['passwordConfirmation']

        if User.objects.filter(username=username):
            return Response({'message': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)

        if password == confirmation:
            user = User.objects.create_user(username=username, password=password)
            user.save()

            return Response({'message': f'User Created {username}'}, status=status.HTTP_201_CREATED)

        return Response({'message': 'error creating user'}, status=status.HTTP_400_BAD_REQUEST)

# The user's login, it inherits from TokenObtainPairView
class LoginJWTView(TokenObtainPairView):
  def finalize_response(self, request, response, *args, **kwargs):
    """
    Customize the response of the JWT tokens

    So that instead of returning the tokens in the response
    the access token is set as a cookie and the refresh token
    is stored in the user session.
    """
    # Check for the 'refresh' key from the response
    if response.data.get('refresh'):
      # Set the cookie
      response.set_cookie('access_token', response.data['access'], max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'], httponly=True, samesite='None', secure=True)

      # Set the session token
      request.session['refresh'] = response.data['refresh']

      # Add a message to the response
      response.data['message'] = 'Successfully logged in!'

      # Remove the tokens from the JSON response
      del response.data['access']
      del response.data['refresh']
      # Call the super method
    return super().finalize_response(request, response, *args, **kwargs)


class LogoutJWTView(APIView):
    def post(self, request):
        """
        Logs out the user and deletes the cookies
        from the client
        """
        response = Response()

        # Check if the user is logged in
        if request.COOKIES.get('sessionid'):
            # Delete the token and the session
            response.set_cookie(
                'access_token',
                '',
                samesite='None',
                secure=True
            )

            response.set_cookie(
                'sessionid',
                '',
                samesite='None',
                secure=True
            )

            # Delete the refresh token from the session
            # and the cookies from the request
            request.session = {}
            request.COOKIES = {}

            response.data = { 'message': 'You are logged out' }
            response.status_code = 200
        else:
            # If user is not logged in
            response.data = { 'message': 'You are not logged in' }
            response.status_code = 200
        return response


class CurrentUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Returns the current user's info
        """
        return Response(
            UserSerializer(
                request.user).data,
            status=status.HTTP_200_OK)


class CurrentTaskView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Returns the current user's current task id
        """
        return Response({'id': request.user.current_task_id},
                        status=status.HTTP_200_OK)

    def put(self, request):
        """
        Changes the current task id received in the request
        """
        user = User.objects.get(id=request.user.id)
        user.current_task_id = request.data['id']
        user.save()

        return Response({'id': user.current_task_id},
                        status=status.HTTP_200_OK)


class CurrentModeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_mode(self, id):
        """
        Tries to get the mode object with the id of id
        it if fails it raises a HTTP404 error

        Keyword arguments:
        id -- the id of the to be retrieved object
        """
        try:
            mode = Mode.objects.get(id=id)
            return Response(
                ModesSerializer(mode).data,
                status=status.HTTP_200_OK)
        except Mode.DoesNotExist:
            raise Http404

    def get(self, request):
        return self.get_mode(request.user.current_mode_id)

    # Change the current mode
    def post(self, request):
        mode_id = request.data['mode_id']
        user = User.objects.get(id=request.user.id)

        user.current_mode_id = mode_id

        user.save()

        return self.get_mode(mode_id)


class TagInfo(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, name=None):
        """
        Tries to get the tag with the name of name
        if it succeeds it returns the tasks inside the tag
        if it fails it raise a HTTP 404 error

        Keyword arguments:
        name -- the name of the tag
        """
        try:
            tag = Tag.objects.get(name=name, user=self.request.user)
            return Response(
                TaskSerializer(
                    tag.tasks,
                    many=True).data,
                status=status.HTTP_200_OK)
        except Tag.DoesNotExist:
            raise Http404
