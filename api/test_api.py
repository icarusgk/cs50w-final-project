from django.test import TestCase, Client
from .models import Task, Project, Subtask, Tag, Stats, Mode, User
from .serializers import *
from .utils_api import AuthUtils



class UserCreationTestCase(TestCase):
  def setUp(self):
    self.auth = AuthUtils()

  def test_user_register(self):
    response = self.auth.register()

    expected_response = {"message": f"User Created test_user"}

    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json(), expected_response)


  def test_user_login(self) -> dict:
    self.auth.register()
    login_response = self.auth.login()

    tokens = login_response.json()

    self.assertEqual(login_response.status_code, 200)
    self.assertTrue(tokens['access'])
    self.assertTrue(tokens['refresh'])



class UserOperationsTestCase(TestCase):
  def setUp(self):
    self.auth = AuthUtils()
    self.auth.auth()
    self.c = Client(**{
      'HTTP_AUTHORIZATION': 'Bearer ' + self.auth.tokens['access']
    })

  def test_user_refresh_token(self):    
    response = self.c.post('/api/token/refresh/', {
      'refresh': self.auth.tokens['refresh']
    })

    new_tokens = response.json()

    self.assertEqual(response.status_code, 200)
    self.assertTrue(new_tokens['access'])
    self.assertTrue(new_tokens['refresh'])


  def test_user_self_info(self):
    response = self.c.get('/api/me/')

    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json()['username'], 'test_user')


  def test_user_retrieve_all(self):
    response = self.c.get('/api/users/')

    self.assertEqual(response.status_code, 200)
    self.assertEqual(type(response.json()), list)



class ModeOperationsTestCase(TestCase):
  def setUp(self):
    self.auth = AuthUtils()
    self.auth.auth()
    self.c = Client(**{
      'HTTP_AUTHORIZATION': 'Bearer ' + self.auth.tokens['access']
    })

  def test_mode_creation(self):    
    new_mode = {
      'name': 'Short mode',
      'pomo': 15,
      'short_break': 2,
      'long_break': 5
    }
    response = self.c.post('/api/modes/', new_mode)

    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json(), {
      # look back
      'id': 1,
      **new_mode
    })


  def test_mode_deletion(self):
    self.test_mode_creation()

    response = self.c.delete('/api/modes/1/')
    self.assertEqual(response.status_code, 204)



class StatsOperationsTestCase(TestCase):
  def setUp(self):
    self.auth = AuthUtils()
    self.auth.auth()
    self.c = Client(**{
      'HTTP_AUTHORIZATION': 'Bearer ' + self.auth.tokens['access']
    })

  def test_stats_creation(self):
    today = {
      'day': '2022-11-11',
    }

    tomorrow = {
      'day': '2022-11-12'
    }

    response_1 = self.c.post('/api/stats/', today)
    response_2 = self.c.post('/api/stats/', tomorrow)
    
    self.assertEqual(response_1.status_code, 200)
    self.assertEqual(response_2.status_code, 200)

    self.assertEqual(response_1.json(), {
      'id': 1,
      'chores_done': 1,
      **today
    })

    self.assertEqual(response_2.json(), {
      'id': 2,
      'chores_done': 1,
      **tomorrow
    })
    

  def test_stats_increase(self):
    today = {
      'day': '2022-11-11'
    }

    # Create the stat
    self.c.post('/api/stats/', today)

    # Increment the stat
    response = self.c.post('/api/stats/', today)

    self.assertEqual(response.status_code, 200)

    self.assertEqual(response.json(), {
      'id': 1,
      'chores_done': 2,
      **today
    })

  def test_stat_retrieval(self):
    self.test_stats_creation()

    response = self.c.get('/api/stats/')

    stats = Stats.objects.all()

    self.assertEqual(response.status_code, 200)
    self.assertListEqual(response.json(), StatsSerializer(stats, many=True).data)

  
  # This test helped me find out that stats were
  # shared
  def test_stats_for_diff_users(self):
    self.test_stat_retrieval()

    c = Client()

    # Create new user
    new_user = {
      'username': 'test_user_1',
      'password': 'test_pass_1'
    }

    c.post('/api/register/', {
      **new_user,
      'passwordConfirmation': 'test_pass_1' 
    })

    login_response = c.post('/api/token/', new_user)

    tokens = login_response.json()

    auth_headers = {
      'HTTP_AUTHORIZATION': 'Bearer ' + tokens['access']
    }

    today = {
      'day': '2022-11-11'
    }

    tomorrow = {
      'day': '2022-11-12'
    }

    # Create same stats but for this user
    response_1 = c.post('/api/stats/', today, **auth_headers)
    response_2 = c.post('/api/stats/', tomorrow, **auth_headers)
    
    self.assertEqual(response_1.status_code, 200)
    self.assertEqual(response_2.status_code, 200)

    self.assertEqual(response_1.json(), {
      'id': 3,
      'chores_done': 1,
      **today
    })

    self.assertEqual(response_2.json(), {
      'id': 4,
      'chores_done': 1,
      **tomorrow
    })



class TagsTestCase(TestCase):
  def setUp(self):
    self.auth = AuthUtils()
    self.auth.auth()
    self.c = Client(**{
      'HTTP_AUTHORIZATION': 'Bearer ' + self.auth.tokens['access'],
    })

    user = User.objects.get(username='test_user')

    self.task = Task.objects.create(**{
      'user': user,
      'title': 'Learn DRF',
      'description': 'Study more about Django Rest Framework',
      'estimated': 3
    })

  
  def test_tag_creation(self):
    vue_tag = { 'tag_name': 'Vue' }
    nuxt_tag = { 'tag_name': 'Nuxt' }
    django_tag = { 'tag_name': 'Django' }

    options = { 'obj': 'tag', 'action': 'add' }

    # Add the tags to the tags
    response_1 = self.c.patch(f'/api/tasks/{self.task.id}/', {
      **options,
      **vue_tag
    }, content_type="application/json")

    response_2 = self.c.patch(f'/api/tasks/{self.task.id}/', {
      **options,
      **nuxt_tag
    }, content_type="application/json")

    response_3 = self.c.patch(f'/api/tasks/{self.task.id}/', {
      **options,
      **django_tag
    }, content_type="application/json")

    # Test Status codes
    self.assertEqual(response_1.status_code, 200)
    self.assertEqual(response_2.status_code, 200)
    self.assertEqual(response_3.status_code, 200)

    # Retrieve the models
    model_vue_tag = Tag.objects.get(name=vue_tag['tag_name'])
    model_nuxt_tag = Tag.objects.get(name=nuxt_tag['tag_name'])
    model_django_tag = Tag.objects.get(name=django_tag['tag_name'])

    # Test Serializers
    self.assertEqual(TagSerializer(model_vue_tag).data, {
      'id': model_vue_tag.id,
      'name': vue_tag['tag_name']
    })

    self.assertEqual(TagSerializer(model_nuxt_tag).data, {
      'id': model_nuxt_tag.id,
      'name': nuxt_tag['tag_name']
    })

    self.assertEqual(TagSerializer(model_django_tag).data, {
      'id': model_django_tag.id,
      'name': django_tag['tag_name']
    })


  def test_task_tags(self):
    self.test_tag_creation()

    vue_tag = self.c.get('/api/tags/1/').json()
    nuxt_tag = self.c.get('/api/tags/2/').json()
    django_tag = self.c.get('/api/tags/3/').json()

    self.assertEqual(TagSerializer(self.task.tags.all(), many=True).data, [
      vue_tag, nuxt_tag, django_tag
    ])

  
  def test_repeated_tag_on_task(self):
    self.test_tag_creation()

    repeated_tag = self.c.patch(f'/api/tasks/{self.task.id}/', {
      'obj': 'tag', 'action': 'add', 'tag_name': 'Django'
    }, content_type='application/json')

    self.assertEqual(repeated_tag.json()['message'], 'tag already exists in task')
    
  
  def test_tag_removal(self):
    self.test_tag_creation()

    vue_tag = self.c.get('/api/tags/1/').json()
    nuxt_tag = self.c.get('/api/tags/2/').json()
    django_tag = self.c.get('/api/tags/3/').json()

    response_1 = self.c.delete(f'/api/tags/{vue_tag["id"]}/')
    response_2 = self.c.delete(f'/api/tags/{nuxt_tag["id"]}/')
    response_3 = self.c.delete(f'/api/tags/{django_tag["id"]}/')

    self.assertEqual(response_1.status_code, 204)
    self.assertEqual(response_2.status_code, 204)
    self.assertEqual(response_3.status_code, 204)

    self.assertEqual(self.task.tags.count(), 0)



class TaskTestCase(TestCase):
  def setUp(self):
    self.auth = AuthUtils()
    self.auth.auth()
    
    self.c = Client(**{
      'HTTP_AUTHORIZATION': 'Bearer ' + self.auth.tokens['access']
    })

    self.task_1 = {
      'tags': [],
      'title': 'Learn Vue',
      'description': 'Read about refs',
      'estimated': 2,
      'subtasks': []
    }

    self.task_2 = {
      'tags': [],
      'title': 'Study Django Rest Framework',
      'description': 'Read more about it',
      'estimated': 4,
      'subtasks': []
    }

    self.task_1_res = self.c.post('/api/tasks/', self.task_1)
    self.task_2_res = self.c.post('/api/tasks/', self.task_2)

    self.task_1_model = Task.objects.get(title=self.task_1.get('title'))
    self.task_2_model = Task.objects.get(title=self.task_2.get('title'))



  def options(self, obj, action):
    return { 'obj': obj, 'action': action }


 
  def test_tasks_creation(self):
    self.assertEqual(self.task_1_res.status_code, 200)
    self.assertEqual(self.task_2_res.status_code, 200)    

    self.assertTrue(self.task_1_model)
    self.assertTrue(self.task_2_model)



  def test_task_serializer(self):
    self.assertEqual(self.task_1_res.json(), {
      **TaskSerializer(self.task_1).data,
      'id': self.task_1_model.id,
      'done': False,
      'gone_through': 0,
      'project_tasks': []
    })

    self.assertEqual(self.task_2_res.json(), {
      **TaskSerializer(self.task_2).data,
      'id': self.task_2_model.id,
      'done': False,
      'gone_through': 0,
      'project_tasks': []
    })


  
  def test_task_retrieval(self):
    response = self.c.get('/api/tasks/')
    self.assertEqual(response.status_code, 200)

  

  def test_task_retrieval_order(self):
    response = self.c.get('/api/tasks/')

    # Get results from paginated response
    tasks = response.json().get('results')
    
    # Use QuerySet instead of just Equal, for ordered values
    self.assertQuerysetEqual(
      TaskSerializer(Task.objects.all().order_by('-id'), many=True).data,
      tasks
    )

    return tasks

  
  def test_task_are_outside_projects(self):
    tasks = self.test_task_retrieval_order()

    for task in tasks:
      self.assertFalse(task.get('in_project'))

  

  def test_task_single_retrieval(self):
    res_1 = self.c.get(f'/api/tasks/{self.task_1_model.id}/')
    res_2 = self.c.get(f'/api/tasks/{self.task_2_model.id}/')

    self.assertEqual(res_1.status_code, 200)
    self.assertEqual(res_2.status_code, 200)
    
    self.assertEqual(TaskSerializer(self.task_1_model).data, res_1.json())
    self.assertEqual(TaskSerializer(self.task_2_model).data, res_2.json())



  def test_task_update(self):
    old_task_details = {
      'title': 'Learn Vue',
      'description': 'Read about refs',
    }
    
    self.assertEqual(self.task_1.get('title'), old_task_details.get('title'))
    self.assertEqual(self.task_1.get('description'), old_task_details.get('description'))

    new_task_details = {
      'title': 'Learn Vue 3 API',
      'description': 'Read even more about refs'
    }

    response = self.c.put(f'/api/tasks/{self.task_1_model.id}/', {
      **new_task_details
    }, content_type='application/json')

    self.assertEqual(response.status_code, 200)

    new_task = Task.objects.get(id=self.task_1_model.id)

    self.assertEqual(new_task.title, new_task_details.get('title'))
    self.assertEqual(new_task.description, new_task_details.get('description'))



  def test_task_tag_removal(self):
    tag = Tag.objects.create(name='Vue', user=User.objects.first())

    self.task_1_model.tags.add(tag)

    self.assertEqual(self.task_1_model.tags.count(), 1)

    response = self.c.patch(f'/api/tasks/{self.task_1_model.id}/', {
      **self.options('tag', 'remove'),
      'tag_id': tag.id
    }, content_type='application/json')

    self.assertEqual(self.task_1_model.tags.count(), 0)

    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json().get('message'), 'tag removed')


  
  def test_task_tag_addition(self):
    self.assertEqual(self.task_1_model.tags.count(), 0)

    tag_name = 'Astro'

    response = self.c.patch(f'/api/tasks/{self.task_1_model.id}/', {
      **self.options('tag', 'add'),
      'tag_name': tag_name
    }, content_type='application/json')

    self.assertEqual(self.task_1_model.tags.count(), 1)

    self.assertEqual(response.status_code, 200)

    self.assertEqual(response.json(), {'message': 'new', 'tag': {
      'id': 1,
      'name': tag_name
    }})


  
  def test_task_invalid_tag(self):
    self.test_task_tag_addition()

    self.assertEqual(self.task_1_model.tags.count(), 1)

    tag_name = 'Astro'

    response = self.c.patch(f'/api/tasks/{self.task_1_model.id}/', {
      **self.options('tag', 'add'),
      'tag_name': tag_name
    }, content_type='application/json')

    self.assertEqual(self.task_1_model.tags.count(), 1)
    self.assertEqual(response.json().get('message'), 'tag already exists in task')



  def test_task_tag_prev_created(self):
    tag_name = 'Nuxt v3'
    Tag.objects.create(name=tag_name, user=User.objects.first())

    self.assertEqual(self.task_1_model.tags.count(), 0)
    self.assertEqual(Tag.objects.count(), 1)

    response = self.c.patch(f'/api/tasks/{self.task_1_model.id}/', {
      **self.options('tag', 'add'),
      'tag_name': tag_name
    }, content_type='application/json')

    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json(), { 'tag': {
      'id': 1,
      'name': tag_name
    }})

    self.assertEqual(self.task_1_model.tags.count(), 1)
    self.assertEqual(Tag.objects.count(), 1)

  

  def test_task_subtask_addition(self):
    self.assertEqual(self.task_1_model.subtasks.count(), 0)

    subtask = {
      'title': 'Reactive alternative',
      'description': 'Read more about the alternative of refs',
    }

    response = self.c.patch(f'/api/tasks/{self.task_1_model.id}/', {
      **self.options('subtask', 'add'),
      'subtask': subtask
    }, content_type='application/json')

    self.assertEqual(response.status_code, 200)

    self.assertEqual(self.task_1_model.subtasks.count(), 1)

    self.assertEqual(response.json(), {
      'id': 1,
      **SubtaskSerializer(subtask).data,
      'done': False
    })



  def test_task_subtask_removal(self):
    subtask = {
      'title': 'Reactive alternative',
      'description': 'Read more about the alternative of refs',
    }

    sub = Subtask.objects.create(task=self.task_1_model, **subtask)

    self.assertEqual(self.task_1_model.subtasks.count(), 1)

    response = self.c.patch(f'/api/tasks/{self.task_1_model.id}/', {
      **self.options('subtask', 'remove'),
      'subtask_id': sub.id
    }, content_type='application/json')

    self.assertEqual(response.status_code, 200)

    self.assertEqual(self.task_1_model.subtasks.count(), 0)

    self.assertEqual(response.json(), {
      'message': 'subtask removed'
    })



  def test_task_subtask_update(self):
    self.test_task_subtask_addition()

    subtask = self.task_1_model.subtasks.first()

    self.assertEqual(self.task_1_model.subtasks.count(), 1)

    old_subtask_details = {
      'title': 'Reactive alternative',
      'description': 'Read more about the alternative of refs',
    }

    self.assertEqual(old_subtask_details.get('title'), subtask.title)
    self.assertEqual(old_subtask_details.get('description'), subtask.description)

    new_subtask_details = {
      'title': 'Reactive Docs',
      'description': 'Read more about the alternative of refs, \
        and the better use cases'
    }

    response = self.c.patch(f'/api/tasks/{self.task_1_model.id}/', {
      **self.options('subtask', 'update'),
      'subtask': {
        'id': subtask.id,
        **new_subtask_details
      }
    }, content_type='application/json')

    new_subtask = self.task_1_model.subtasks.first()

    self.assertEqual(response.status_code, 200)

    self.assertEqual(self.task_1_model.subtasks.count(), 1)

    self.assertEqual(new_subtask_details.get('title'), new_subtask.title)
    self.assertEqual(new_subtask_details.get('description'), new_subtask.description)

    self.assertEqual(response.json(), {'message': 'updated'})


  
  def test_task_subtask_done(self):
    self.test_task_subtask_addition()

    def change_done_status():
      return self.c.patch(f'/api/tasks/{self.task_1_model.id}/', {
        **self.options('subtask', 'done'),
        'subtask_id': self.task_1_model.subtasks.first().id,
      }, content_type='application/json')

    
    self.assertEqual(self.task_1_model.subtasks.first().done, False)

    response = change_done_status()

    self.assertEqual(self.task_1_model.subtasks.first().done, True)
    self.assertEqual(response.json(), {'done': True})

    response = change_done_status()

    self.assertEqual(self.task_1_model.subtasks.first().done, False)
    self.assertEqual(response.json(), {'done': False})



  def test_task_done(self):
    self.assertEqual(self.task_1_model.done, False)

    response = self.c.patch(f'/api/tasks/{self.task_1_model.id}/', {
      **self.options('task', 'done'),
    }, content_type='application/json')

    self.assertEqual(response.status_code, 200)

    self.assertEqual(Task.objects.first().done, True)
    self.assertEqual(response.json(), {'done': True})

    response = self.c.patch(f'/api/tasks/{self.task_1_model.id}/', {
      **self.options('task', 'done'),
    }, content_type='application/json')

    self.assertEqual(response.status_code, 200)

    self.assertEqual(Task.objects.first().done, False)
    self.assertEqual(response.json(), {'done': False})


  
  def test_task_gone_through(self):
    def increment():
      response = self.c.patch(f'/api/tasks/{self.task_1_model.id}/', {
        **self.options('task', 'increment_gone_through'),
      }, content_type='application/json')

      self.assertEqual(response.status_code, 200)
      return response

    self.assertEqual(self.task_1_model.gone_through, 0)

    response = increment()
    self.assertEqual(Task.objects.first().gone_through, 1)
    self.assertEqual(response.json(), 1)

    response = increment()
    self.assertEqual(Task.objects.first().gone_through, 2)
    self.assertEqual(response.json(), 2)

    response = increment()
    self.assertEqual(Task.objects.first().gone_through, 3)
    self.assertEqual(response.json(), 3)


  
  def test_task_invalid_request(self):
    response = self.c.patch(f'/api/tasks/{self.task_1_model.id}/', {
        # 'projects' is not a valid obj
        **self.options('projects', 'increment_gone_through'),
      }, content_type='application/json')
    
    self.assertEqual(response.json(), {'message': 'error'})



  def test_task_deletion(self):
    response = self.c.delete(f'/api/tasks/{self.task_1_model.id}/')

    self.assertEqual(response.status_code, 200)

    try:
      task = Task.objects.get(id=self.task_1_model.id)
    except Task.DoesNotExist:
      task = None

    self.assertEqual(task, None)



class ProjectTestCase(TestCase):
  def setUp(self):
    auth = AuthUtils()
    auth.auth()
    self.c = Client(**{
      'HTTP_AUTHORIZATION': 'Bearer ' + auth.tokens.get('access')
    })

    self.ex_project_1 = {
      'name': 'Nuxt Project',
      'user': User.objects.first(),
      'tasks': []
    }

    self.ex_project_2 = {
      'name': 'Astro Project',
      'user': User.objects.first(),
      'tasks': []
    }

    self.project_1 = self.c.post('/api/projects/', self.ex_project_1)
    self.project_2 = self.c.post('/api/projects/', self.ex_project_2)

    self.project_1_model = Project.objects.get(name=self.ex_project_1['name'])
    self.project_2_model = Project.objects.get(name=self.ex_project_2['name'])
    



  def test_project_creation(self):
    self.assertEqual(self.project_1.status_code, 201)    
    self.assertEqual(self.project_1.json(), ProjectSerializer(self.project_1_model).data)

    self.assertEqual(self.project_2.status_code, 201)
    self.assertEqual(self.project_2.json(), ProjectSerializer(self.project_2_model).data)
    

  
  def test_project_retrieval(self):
    response = self.c.get('/api/projects/')
    
    self.assertEqual(response.status_code, 200)
    self.assertEqual(Project.objects.count(), 2)

    projects = response.json().get('results')

    self.assertEqual(
      ProjectSerializer(Project.objects.all().order_by('-id'), many=True).data,
      projects
    )


  
  def test_project_retrieval_order(self):
    response = self.c.get('/api/projects/')
    
    self.assertEqual(response.status_code, 200)

    projects = response.json().get('results')

    self.assertQuerysetEqual(
      ProjectSerializer(Project.objects.all().order_by('-id'), many=True).data,
      projects,
      ordered=True
    )


  def test_project_single_retrieval(self):
    response_1 = self.c.get(f'/api/projects/{self.project_1_model.id}/')
    response_2 = self.c.get(f'/api/projects/{self.project_2_model.id}/')
    
    self.assertTrue(response_1.status_code, 200)
    self.assertTrue(response_2.status_code, 200)

    self.assertEqual(response_1.json(), ProjectSerializer(self.project_1_model).data)
    self.assertEqual(response_2.json(), ProjectSerializer(self.project_2_model).data)
    


  def test_project_modify_title(self):
    new_title = 'Nuxt v3 Project'

    self.assertNotEqual(self.project_1_model.name, new_title)

    pk = self.project_1_model.id

    response = self.c.patch(f'/api/projects/{pk}/modify_title/', {
      'name': new_title
    }, content_type='application/json')

    self.assertEqual(response.status_code, 200)
    self.assertEqual(Project.objects.get(id=pk).name, new_title)

    

  def test_project_add_new_task(self):
    task_1 = {
      'tags': [{'name': 'vue', 'name': 'nuxt'}],
      'title': 'Search more about Nuxt 3',
      'description': 'Find out when the framework releases',
      'subtasks': []
    }
    
    task_2 = {
      'tags': [{'name': 'files', 'name': 'framework'}],
      'title': 'File structure',
      'description': 'Find more about the file structure',
      'subtasks': []
    }

    pk = self.project_1_model.id

    project_1_model = Project.objects.get(id=pk)

    response_1 = self.c.patch(f'/api/projects/{pk}/add_new_task/', {
      'task': task_1
    }, content_type='application/json')

    self.assertEqual(response_1.status_code, 201)
    self.assertEqual(project_1_model.tasks.count(), 1)

    task_1_model = Task.objects.get(title=task_1.get('title'))

    self.assertEqual(response_1.json(), TaskSerializer(task_1_model).data)
    
    response_2 = self.c.patch(f'/api/projects/{pk}/add_new_task/', {
      'task': task_2
    }, content_type='application/json')

    
    self.assertEqual(response_2.status_code, 201)
    self.assertEqual(project_1_model.tasks.count(), 2)

    task_2_model = Task.objects.get(title=task_2.get('title'))

    self.assertEqual(response_2.json(), TaskSerializer(task_2_model).data)

    return task_1_model



  def test_project_update_task(self):
    task_1_model = self.test_project_add_new_task()

    task_1 = {
      'tags': [{'name': 'vue', 'name': 'nuxt'}],
      'title': 'Search more about Nuxt 3',
      'description': 'Find out when the framework releases',
      'subtasks': []
    }

    pk = self.project_1_model.id

    self.assertEqual(task_1_model.title, task_1['title'])

    new_details = {
      'title': 'Read more about Nuxt 3',
      'description': 'Find out the release date'
    }

    self.assertNotEqual(task_1_model.title, new_details['title'])
    self.assertNotEqual(task_1_model.description, new_details['description'])
    self.assertNotEqual(self.project_1_model.tasks.first().title, new_details['title'])
    self.assertNotEqual(self.project_1_model.tasks.first().description, new_details['description'])

    task_1_model.title = new_details['title']
    task_1_model.description = new_details['description']

    response = self.c.patch(f'/api/projects/{pk}/update_task/', {
      'subtask': TaskSerializer(task_1_model).data
    }, content_type='application/json')

    self.assertEqual(response.status_code, 200)

    self.assertEqual(response.json().get('title'), new_details['title'])
    self.assertEqual(response.json().get('description'), new_details['description'])
    self.assertEqual(self.project_1_model.tasks.first().title, new_details['title'])
    self.assertEqual(self.project_1_model.tasks.first().description, new_details['description'])


  
  def test_project_add_task_to_project(self):
    # Create a blank project with in_project False
    task = Task.objects.create(**{
      'user': User.objects.first(),
      'title': 'Tailwind docs',
      'description': 'How to style with Tailwind',
      'estimated': 2,
      'in_project': False
    })

    pk = self.project_1_model.id

    self.assertEqual(self.project_1_model.tasks.count(), 0)

    # Add it to project with patch
    response = self.c.patch(f'/api/projects/{pk}/add_to_project/', {
      'task_id': task.id
    }, content_type='application/json')

    self.assertEqual(response.status_code, 200)

    self.assertEqual(self.project_1_model.tasks.count(), 1)

    return task



  def test_project_delete_task(self):
    pk = self.project_1_model.id

    task = self.test_project_add_task_to_project()

    self.assertEqual(self.project_1_model.tasks.count(), 1)

    response = self.c.patch(f'/api/projects/{pk}/delete_task/', {
      'task_id': task.id
    }, content_type='application/json')

    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.content, b'"task removed"')

    self.assertEqual(self.project_1_model.tasks.count(), 0)

    task_1_model = self.test_project_add_new_task()

    self.assertEqual(self.project_1_model.tasks.count(), 2)

    response = self.c.patch(f'/api/projects/{pk}/delete_task/', {
      'task_id': task_1_model.id
    }, content_type='application/json')

    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.content, b'"task deleted"')
    
    self.assertEqual(self.project_1_model.tasks.count(), 1)



  def test_project_task_done(self):
    pk = self.project_1_model.id

    task_1_model = self.test_project_add_new_task()
    self.assertFalse(task_1_model.done)

    response = self.c.patch(f'/api/projects/{pk}/task_done/', {
      'task_id': task_1_model.id
    }, content_type='application/json')

    self.assertEqual(response.status_code, 200)

    task_after_update = Task.objects.first()
    self.assertEqual(response.json(), {'done': task_after_update.done})

    self.assertTrue(task_after_update.done)

    response = self.c.patch(f'/api/projects/{pk}/task_done/', {
      'task_id': task_1_model.id
    }, content_type='application/json')

    self.assertEqual(response.status_code, 200)

    task_after_update = Task.objects.first()
    self.assertEqual(response.json(), {'done': task_after_update.done})

    self.assertFalse(task_after_update.done)
  

  
  def test_project_removal(self):
    pk = self.project_1_model.id
    self.test_project_add_new_task()

    project_1 = Project.objects.get(id=pk)

    self.assertEqual(project_1.tasks.count(), 2)
    

    response = self.c.delete(f'/api/projects/{pk}/')

    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json(), {'data': 'project deleted'})

    self.assertQuerysetEqual(Project.objects.filter(id=pk), [])
    self.assertQuerysetEqual(Task.objects.filter(id=project_1.tasks.first()), [])
    self.assertQuerysetEqual(Task.objects.filter(id=project_1.tasks.last()), [])



class RegisterTestCase(TestCase):
  def setUp(self):
    self.user = {
      'username': 'test_user',
      'password': 'test_pass'
    }

  def test_register(self):
    c = Client()
    response = c.post('/api/register/', {
      **self.user,
      'passwordConfirmation': self.user['password']
    })

    expected_response = {'message': f'User Created {self.user["username"]}'}

    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json(), expected_response)

  
  def test_registering_invalid_user(self):
    self.test_register()

    c = Client()
    response = c.post('/api/register/', {
      **self.user,
      'passwordConfirmation': self.user['password']
    })

    expected_response = {'message': 'User already exists'}

    self.assertEqual(response.status_code, 400)
    self.assertEqual(response.json(), expected_response)



class CurrentTaskTestCase(TestCase):
  def setUp(self):
    auth = AuthUtils()
    auth.auth()
    self.c = Client(**{
      'HTTP_AUTHORIZATION': 'Bearer ' + auth.tokens.get('access')
    })

    self.task = Task.objects.create(**{
      'user': User.objects.first(),
      'title': 'Astro docs',
      'description': 'How to style Astro with Tailwind',
      'estimated': 1,
      'in_project': False
    })

    
  def test_current_task_put(self):
    response = self.c.put('/api/currentTask/', {
      'id': self.task.id
    }, content_type='application/json')

    self.assertEqual(response.status_code, 200)
    user = User.objects.first()
    self.assertEqual(response.json(), {'id': user.current_task_id})



  def test_current_task_get(self):
    self.test_current_task_put()
    response = self.c.get('/api/currentTask/')

    self.assertEqual(response.status_code, 200)
    user = User.objects.first()
    self.assertEqual(response.json(), {'id': user.current_task_id})



class CurrentModeTestCase(TestCase):
  def setUp(self):
    auth = AuthUtils()
    auth.auth()
    self.c = Client(**{
      'HTTP_AUTHORIZATION': 'Bearer ' + auth.tokens.get('access')
    })

  
  def test_no_mode(self):
    response = self.c.get('/api/currentMode/')

    self.assertEqual(response.status_code, 404)

  
  def test_mode_post(self):
    mode_details = {
      'user': User.objects.first(),
      'name': 'Classes mode',
      'pomo': 50,
      'short_break': 10,
      'long_break': 30
    }

    mode = Mode.objects.create(**mode_details)

    response = self.c.post('/api/currentMode/', {
      'mode_id': mode.id
    })

    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json(), ModesSerializer(mode).data)

    return mode


  def test_mode_get(self):
    mode = self.test_mode_post()

    response = self.c.get('/api/currentMode/')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json(), ModesSerializer(mode).data)



class TagInfoTestCase(TestCase):
  def setUp(self):
    auth = AuthUtils()
    auth.auth()
    self.c = Client(**{
      'HTTP_AUTHORIZATION': 'Bearer ' + auth.tokens.get('access')
    })

    user = User.objects.first()

    self.task_1 = {
      'tags': [{'name': 'django'}, {'name': 'rest'}, {'name': 'docs'}],
      'title': 'Read DRF\'s Docs',
      'description': 'Read Django Rest Framework Docs',
      'estimated': 3,
    }

    self.task_2 = {
      'tags': [{'name': 'django'}, {'name': 'auth'}, {'name': 'docs'}],
      'title': 'Read Django Auth Docs',
      'description': 'Read more about auth',
      'estimated': 1,
    }

    self.response_task_1 = self.c.post('/api/tasks/', {
      **self.task_1
    }, content_type='application/json')
    self.response_task_2 = self.c.post('/api/tasks/', {
      **self.task_2
    }, content_type='application/json')



  def test_tasks_creation(self):
    self.assertEqual(self.response_task_1.status_code, 200)
    self.assertEqual(self.response_task_2.status_code, 200)

    task_1 = Task.objects.get(title=self.task_1['title'])
    task_2 = Task.objects.get(title=self.task_2['title'])

    self.assertEqual(self.response_task_1.json(), TaskSerializer(task_1).data)
    self.assertEqual(self.response_task_2.json(), TaskSerializer(task_2).data)



  def test_tasks_inside_tag(self):
    django = self.c.get('/api/tagInfo/django/')
    rest = self.c.get('/api/tagInfo/rest/')
    docs = self.c.get('/api/tagInfo/docs/')
    auth = self.c.get('/api/tagInfo/auth/')


    django_tag = Tag.objects.get(name='django')
    self.assertEqual(django.json(), TaskSerializer(django_tag.tasks, many=True).data)
    self.assertEqual(django_tag.tasks.count(), 2)
    # docs 2
    docs_tag = Tag.objects.get(name='docs')
    self.assertEqual(docs.json(), TaskSerializer(docs_tag.tasks, many=True).data)
    self.assertEqual(docs_tag.tasks.count(), 2)

    # auth 1
    auth_tag = Tag.objects.get(name='auth')
    self.assertEqual(auth.json(), TaskSerializer(auth_tag.tasks, many=True).data)
    self.assertEqual(auth_tag.tasks.count(), 1)
    # rest 1
    rest_tag = Tag.objects.get(name='rest')
    self.assertEqual(rest.json(), TaskSerializer(rest_tag.tasks, many=True).data)
    self.assertEqual(rest_tag.tasks.count(), 1)
    
  
  def test_invalid_tag(self):
    invalid_tag = self.c.get('/api/tagInfo/angular/')

    self.assertEqual(invalid_tag.status_code, 404)



