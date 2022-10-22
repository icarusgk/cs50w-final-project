from .serializers import *
from .models import *
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.pagination import PageNumberPagination
from django.http import Http404


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

        return Response(StatsSerializer(stat).data)


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
        if request.data['pomo'] >= 60 or request.data['short_break'] >= 60 or request.data['long_break'] >= 60:
            return Response(
                {'message': 'Not valid, timers can only be less than an hour long.'})

        if request.data['name'] == 'Default':
            return Response({'message': 'There can only be one default mode.'})

        serializer = ModesSerializer(data=request.data)

        if serializer.is_valid():
            mode = Mode.objects.create(**serializer.data, user=request.user)
            return Response(ModesSerializer(mode).data)

        return Response('not valid')

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
        Returns the current user's tasks
        ordered descendingly
        """
        return self.request.user.tasks.all().filter(in_project=False).order_by('-id')

    def retrieve(self, request, pk=None):
        """
        Return a certain task info based on the
        authenticated user
        """
        task = Task.objects.filter(id=pk).first()
        if task.user != request.user:
            return Response({"data": "error"})
        return Response(TaskSerializer(task).data)

    def create(self, request):
        """
        Create a new task with tags and subtasks
        for the current user
        """
        serializer = TaskSerializer(data=request.data)
        subtasks = request.data['subtasks']
        tags = request.data['tags']

        if serializer.is_valid():
            task = Task(user=request.user, **serializer.data)
            task.save()

            # Add tags
            for tag in tags:
                tag_obj = Tag.objects.filter(name=tag['name']).first()
                if not tag_obj:
                    # Create tag
                    tag_obj = Tag.objects.create(
                        user=request.user, name=tag['name'])
                task.tags.add(tag_obj)

            # Add subtasks
            for subtask in subtasks:
                Subtask.objects.create(task=task, **subtask)

            # Return the newly created task
            return Response(TaskSerializer(task).data)
        return Response({'message': 'error'})

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

                    return Response({'message': f'tag removed'})

                if data['action'] == 'add':
                    # Get or create the tag
                    (tag_obj, is_new) = Tag.objects.get_or_create(
                        user=request.user, name=data['tag_name'])

                    # If tag already exists, check if tag is in obj already
                    if not is_new and tag_obj in task.tags.all():
                        return Response(
                            {'message': 'tag already exists in task'})

                    # Add tag
                    task.tags.add(tag_obj)
                    task.save()

                    serialized_tag = TagSerializer(tag_obj).data

                    if is_new:
                        return Response({
                            'message': 'new',
                            'tag': serialized_tag
                        })
                    return Response({'tag': serialized_tag})
            # Live update subtasks
            elif obj == 'subtask':
                task = Task.objects.get(id=pk)

                # Create subtask
                if data['action'] == 'add':
                    subtask = data['subtask']
                    subtask = Subtask.objects.create(task=task, **subtask)
                    task.save()

                    return Response(SubtaskSerializer(subtask).data)
                # Remove subtask
                elif data['action'] == 'remove':
                    subtask_obj = Subtask.objects.get(id=data['subtask_id'])
                    subtask_obj.delete()

                    return Response({"message": "subtask removed"})
                # Update subtask
                elif data['action'] == 'update':
                    subtask = data['subtask']
                    subtask_obj = Subtask.objects.get(id=subtask['id'])
                    serializer = SubtaskSerializer(subtask_obj, data=subtask)

                    if serializer.is_valid():
                        serializer.save()

                    return Response({"message": "updated"},
                                    status=status.HTTP_200_OK)
                elif data['action'] == 'done':
                    subtask_obj = Subtask.objects.get(id=data['subtask_id'])

                    subtask_obj.done = not subtask_obj.done
                    subtask_obj.save()

                    return Response({"done": subtask_obj.done})
            elif obj == 'task':
                if data['action'] == 'done':
                    task = Task.objects.get(id=pk)

                    task.done = not task.done
                    task.save()

                    return Response({"done": task.done})
                if data['action'] == 'increment_gone_through':
                    task = Task.objects.get(id=pk)

                    task.gone_through += 1
                    task.save()

                    return Response(task.gone_through)

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

        return Response(status=status.HTTP_200_OK)


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

    def get_object(self, pk):
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

        for task in request.data['tasks']:
            task_serializer = TaskSerializer(data=task)

            if task_serializer.is_valid():
                task_obj = Task.objects.create(
                    user=request.user, in_project=True, **task_serializer.data)

                for tag in task['tags']:
                    tag_obj = Tag.objects.filter(name=tag['name']).first()

                    if not tag_obj:
                        # Create tag
                        tag_obj = Tag.objects.create(name=tag['name'])

                    task_obj.tags.add(tag_obj)

                # Add task to the project
                project.tasks.add(task_obj)
                project.save()

        return Response(
            ProjectSerializer(project).data,
            status=status.HTTP_201_CREATED)

    def partial_update(self, request, pk=None):
        """
        Updates in real time the project with id of pk

        Keyword arguments:
        pk -- the id of the project
        """
        data = request.data

        if 'obj' in data:
            if data['obj'] == 'project':

                if data['action'] == 'modify_title':
                    project = self.get_object(pk)
                    project.name = data['name']

                    project.save()

                    return Response("name changed", status=status.HTTP_200_OK)

                if data['action'] == 'add_new':
                    project = self.get_object(pk)

                    task_serializer = TaskSerializer(data=data['task'])

                    if task_serializer.is_valid():
                        task = Task.objects.create(
                            user=request.user, in_project=True, **task_serializer.data)
                        
                        tags = data['task']['tags']
                        for tag in tags:
                            (the_tag, created) = Tag.objects.get_or_create(name=tag['name'])
                            task.tags.add(the_tag)

                        task.save()

                        project.tasks.add(task)
                        project.save()
                    return Response(
                        TaskSerializer(task).data,
                        status=status.HTTP_201_CREATED)

                if data['action'] == 'add_to_project':
                    project = self.get_object(pk)
                    task = Task.objects.get(id=data['task_id'])

                    project.tasks.add(task)

                if data['action'] == 'update_task':
                    task = Task.objects.get(id=data['subtask']['id'])
                    serializer = TaskSerializer(task, data=data['subtask'])

                    if serializer.is_valid():
                        serializer.save()

                        return Response(serializer.data)

                if data['action'] == 'delete_task':
                    task = Task.objects.get(id=data['task_id'])

                    # Remove task from project
                    if not task.in_project:
                        project = self.get_object(pk)
                        project.tasks.remove(task)

                        return Response("task removed")
                    # delete task totally
                    task.delete()

                    return Response("task deleted")

                if data['action'] == 'task_done':
                    project = self.get_object(pk)
                    task = project.tasks.get(id=data['task_id'])

                    task.done = not task.done
                    task.save()

                    return Response({"done": task.done})

                return Response(status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        """
        Deletes the project with an id of pk
        """
        project = self.get_object(pk)

        for task in project.tasks.all():
            if task.in_project:
                task.delete()

        project.delete()

        return Response({'data': 'project deleted'})


class RegisterView(APIView):
    """
    Register an user with an username and password
    """
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        confirmation = request.data['passwordConfirmation']

        if User.objects.filter(username=username):
            return Response({'message': 'User already exists'},
                            status=status.HTTP_400_BAD_REQUEST)

        if password == confirmation:
            user = User.objects.create_user(
                username=username, password=password)
            user.save()

            return Response({'message': f'User Created {username}'})

        return Response({'message': 'error creating user'})


class CurrentUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Returns the current user's info
        """
        return Response(UserSerializer(request.user).data)


class CurrentTaskView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Returns the current user's current task id
        """
        return Response({'id': request.user.current_task_id})

    def put(self, request):
        user = User.objects.get(id=request.user.id)
        user.current_task_id = request.data['id']
        user.save()

        return Response({'id': user.current_task_id})


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
            return Response(ModesSerializer(mode).data)
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
        if it succedes it returns the tasks inside the tag
        if it fails it raise a HTTP 404 error

        Keyword arguments:
        name -- the name of the tag
        """
        try:
            tag = Tag.objects.get(name=name)
            return Response(TaskSerializer(tag.tasks, many=True).data)
        except Tag.DoesNotExist:
            raise Http404
