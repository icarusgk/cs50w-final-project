from django.test import TestCase, Client
from .models import Task, Project, Subtask, Tag, Stats, Mode, User
import datetime

# Create your tests here.

class UserTestCase(TestCase):
  def setUp(self) -> None:
    self.user = User.objects.create(**{
      'username': 'test_user',
      'password': 'test_password',
    })

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

  def tearDown(self):
    all_users = User.objects.all()
    all_users.delete()


class ModeTestCase(TestCase):
  def setUp(self) -> None:
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


class StatsTestCase(TestCase):
  def setDay(self, days: int):
    return datetime.datetime.now() + datetime.timedelta(days=days)


  def setUp(self):
    user = User.objects.create(**{
      'username': 'test_user',
      'password': 'test_pass'
    })
    
    user_1 = User.objects.create(**{
      'username': 'test_user_1',
      'password': 'test_pass_1'
    })

    Stats.objects.create(chores_done=3, user=user)
    Stats.objects.create(day=self.setDay(1), chores_done=9, user=user)
    Stats.objects.create(day=self.setDay(2), chores_done=12, user=user)
    Stats.objects.create(day=self.setDay(3), chores_done=6, user=user_1)


  def test_user_stats_count(self):
    user = User.objects.get(username='test_user')
    user_1 = User.objects.get(username='test_user_1')

    self.assertEqual(user.stats.count(), 3)
    self.assertEqual(user_1.stats.count(), 1)


  