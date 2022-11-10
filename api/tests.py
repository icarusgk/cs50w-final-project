from django.test import TestCase, Client
from .models import Task, Project, Subtask, Tag, Stats, Mode, User
import json

# Create your tests here.

class UserTestCase(TestCase):
  def setUp(self) -> None:
    User.objects.create(**{
      'username': 'test_user',
      'password': 'test_password',
    })
    self.c = Client()

  def get_user(self, username):
    try:
      return User.objects.get(username=username)
    except User.DoesNotExist:
      return False

  def test_user_creation(self):
    user = self.get_user('test_user')
    self.assertTrue(user)

  def test_user_credentials(self):
    user = self.get_user('test_user')
    self.assertEqual(user.username, 'test_user')

  def test_user_settings(self):
    user = self.get_user('test_user')
    self.assertEqual(user.current_task_id, 0)
    self.assertEqual(user.current_mode_id, 0)
    self.assertFalse(user.auto_start_pomos)
    self.assertFalse(user.auto_start_breaks)

  def test_user_register(self, username='test_user_r', password='test_password_r'):
    response = self.c.post('/api/register/', {
      'username': username,
      'password': password,
      'passwordConfirmation': password
    })

    expected_response = {"message": f"User Created {username}"}

    self.assertEqual(response.status_code, 200)
    self.assertEqual(json.loads(response.content), expected_response)

  def test_user_login(self, username='test_user_l', password='test_password_l'):
    self.test_user_register(username, password)

    response = self.c.post('/api/token/', {
      'username': username,
      'password': password
    })

    tokens = json.loads(response.content)

    self.assertEqual(response.status_code, 200)
    self.assertTrue(tokens['access'])
    self.assertTrue(tokens['refresh'])
    return tokens

  def test_user_refresh_token(self):
    tokens = self.test_user_login('test_user_ref', 'test_password_ref')
    
    response = self.c.post('/api/token/refresh/', {
      'refresh': tokens['refresh']
    })

    new_tokens = json.loads(response.content)

    self.assertEqual(response.status_code, 200)
    self.assertTrue(new_tokens['access'])
    self.assertTrue(new_tokens['refresh'])

  def test_user_self_info(self):
    tokens = self.test_user_login('test_user_self', 'test_password_self')
    auth_headers = {
      'HTTP_AUTHORIZATION': 'Bearer ' + tokens['access']
    }
    response = self.c.get('/api/me/', **auth_headers)

    self.assertEqual(response.status_code, 200)
    self.assertEqual(json.loads(response.content)['username'], 'test_user_self')

  def tearDown(self):
    user = self.get_user('test_user')
    user.delete()

    
    

