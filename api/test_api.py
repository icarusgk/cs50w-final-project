from django.test import TestCase, Client
from .models import Task, Project, Subtask, Tag, Stats, Mode, User
from .serializers import *
from .utils_api import AuthUtils
from django.utils.timezone import now

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










