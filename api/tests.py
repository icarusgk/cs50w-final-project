from django.test import TestCase, Client
from .models import Task, Project, Subtask, Tag, Stats, Mode, User
import json

# Create your tests here.

class UserTestCase(TestCase):
  def setUp(self) -> None:
    self.user = User.objects.create(**{
      'username': 'test_user',
      'password': 'test_password',
    })
    self.c = Client()

  def test_user_existence(self):
    self.assertTrue(self.user)
    self.assertEqual(User.objects.count(), 1)

  def test_user_credentials(self):
    self.assertEqual(self.user.username, 'test_user')
    self.assertEqual(self.user.password, 'test_password')

  def test_user_settings(self):
    self.assertEqual(self.user.current_task_id, 0)
    self.assertEqual(self.user.current_mode_id, 0)
    self.assertFalse(self.user.auto_start_pomos)
    self.assertFalse(self.user.auto_start_breaks)

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

  def test_user_retrieve_all(self):
    tokens = self.test_user_login('test_users', 'test_passwords')
    auth_headers = {
      'HTTP_AUTHORIZATION': 'Bearer ' + tokens['access']
    }
    response = self.c.get('/api/users/', **auth_headers)

    self.assertEqual(response.status_code, 200)
    self.assertEqual(type(json.loads(response.content)), list)

  def tearDown(self):
    all_users = User.objects.all()
    all_users.delete()


class ModeTestCase(TestCase):
  def setUp(self):
    user = User.objects.create(**{
      'username': 'test_user',
      'password': 'test_password'
    })
    self.mode = Mode.objects.create(**{
      'user': user,
      'name': 'Classes mode',
      'pomo': 50,
      'short_break': 10,
      'long_break': 30
    })
    self.c = Client()

  def test_mode_existence(self):
    self.assertTrue(self.mode)
    self.assertEqual(Mode.objects.count(), 1)

  def test_mode_correct_values(self):
    user = User.objects.get(username='test_user')
    
    self.assertEqual(self.mode.user, user)
    self.assertEqual(self.mode.name, 'Classes mode')
    self.assertEqual(self.mode.pomo, 50)
    self.assertEqual(self.mode.short_break, 10)
    self.assertEqual(self.mode.long_break, 30)


  def test_mode_creation(self):
    def auth():
      credentials = {
      'username': 'test_user_mode',
      'password': 'test_password_mode'
      }

      self.c.post('/api/register/', {
        **credentials,
        'passwordConfirmation': 'test_password_mode'
      })

      login_response = self.c.post('/api/token/', credentials)

      return json.loads(login_response.content)

    auth_headers = {
      'HTTP_AUTHORIZATION': 'Bearer ' + auth()['access']
    }

    new_mode = {
      'name': 'Short mode',
      'pomo': 15,
      'short_break': 2,
      'long_break': 5
    }
    response = self.c.post('/api/modes/', new_mode, **auth_headers)

    self.assertEqual(response.status_code, 200)
    self.assertEqual(json.loads(response.content), {
      'id': 2,
      **new_mode
    })
    
