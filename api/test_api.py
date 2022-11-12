from django.test import TestCase, Client
from .models import Task, Project, Subtask, Tag, Stats, Mode, User
from .serializers import *
from .utils_api import AuthUtils

import json

class UserCreationTestCase(TestCase):
  def setUp(self):
    self.auth = AuthUtils()

  def test_user_register(self):
    response = self.auth.register()

    expected_response = {"message": f"User Created test_user"}

    self.assertEqual(response.status_code, 200)
    self.assertEqual(json.loads(response.content), expected_response)


  def test_user_login(self) -> dict:
    self.auth.register()
    login_response = self.auth.login()

    tokens = json.loads(login_response.content)

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

    new_tokens = json.loads(response.content)

    self.assertEqual(response.status_code, 200)
    self.assertTrue(new_tokens['access'])
    self.assertTrue(new_tokens['refresh'])


  def test_user_self_info(self):
    response = self.c.get('/api/me/')

    self.assertEqual(response.status_code, 200)
    self.assertEqual(json.loads(response.content)['username'], 'test_user')


  def test_user_retrieve_all(self):
    response = self.c.get('/api/users/')

    self.assertEqual(response.status_code, 200)
    self.assertEqual(type(json.loads(response.content)), list)


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
    self.assertEqual(json.loads(response.content), {
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

    self.assertEqual(json.loads(response_1.content), {
      'id': 1,
      'chores_done': 1,
      **today
    })

    self.assertEqual(json.loads(response_2.content), {
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

    self.assertEqual(json.loads(response.content), {
      'id': 1,
      'chores_done': 2,
      **today
    })

  def test_stat_retrieval(self):
    self.test_stats_creation()

    response = self.c.get('/api/stats/')

    stats = Stats.objects.all()

    self.assertEqual(response.status_code, 200)
    self.assertListEqual(json.loads(response.content), StatsSerializer(stats, many=True).data)

  
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

    tokens = json.loads(login_response.content)

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

    self.assertEqual(json.loads(response_1.content), {
      'id': 3,
      'chores_done': 1,
      **today
    })

    self.assertEqual(json.loads(response_2.content), {
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



