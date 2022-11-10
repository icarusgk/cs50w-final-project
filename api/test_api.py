from django.test import TestCase, Client
from .models import Task, Project, Subtask, Tag, Stats, Mode, User
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


class APIModeTestCase(TestCase):
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
