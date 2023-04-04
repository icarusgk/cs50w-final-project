from django.test import TestCase
from .models import Task, Project, Tag, Stats, Mode, User
import datetime


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


class TagTestCase(TestCase):
  def setUp(self):
    user = User.objects.create(**{
      'username': 'test_user',
      'password': 'test_pass'
    })

    user_1 = User.objects.create(**{
      'username': 'test_user_1',
      'password': 'test_pass_1'
    })

    Tag.objects.create(name='Vue 3', user=user)
    Tag.objects.create(name='Nuxt 3', user=user)
    Tag.objects.create(name='Django', user=user_1)
    Tag.objects.create(name='DRF', user=user_1)


  def test_user_tags_count(self):
    user = User.objects.get(username='test_user')
    user_1 = User.objects.get(username='test_user_1')

    self.assertEqual(user.tags.count(), 2)
    self.assertEqual(user_1.tags.count(), 2)
    

  # This test helped me find out that tags were unique
  # globally, not only for the user
  def test_tag_repeated_on_dif_user(self):
    user = User.objects.get(username='test_user')
    user_1 = User.objects.get(username='test_user_1')
    tag = Tag.objects.create(name='Vue 3', user=user_1)
    tag_2 = Tag.objects.create(name='Django', user=user)
    self.assertTrue(tag)
    self.assertTrue(tag_2)


class TaskTestCase(TestCase):
  def setUp(self):
    self.user = User.objects.create(**{
      'username': 'test_user',
      'password': 'test_pass'
    })

    self.task = Task.objects.create(**{
      'user': self.user,
      'title': 'Learn refs',
      'description': 'Study more about Vue 3 refs',
      'estimated': 2,
    })


  def test_task_gone_through(self):
    self.assertEqual(self.task.gone_through, 0)

  
  def test_task_empty_tags(self):
    self.assertQuerysetEqual(self.task.tags.all(), [])


  def test_task_tags_addition(self):
    vue = Tag.objects.create(**{
      'user': self.user,
      'name': 'Vue 3'
    })

    nuxt = Tag.objects.create(**{
      'user': self.user,
      'name': 'Nuxt 3'
    })

    self.task.tags.add(vue)
    self.task.tags.add(nuxt)

    self.assertEqual(self.task.tags.count(), 2)
    self.assertQuerysetEqual(self.task.tags.all(), [vue, nuxt], ordered=False)
    

  def test_task_not_done(self):
    self.assertFalse(self.task.done)


  def test_task_not_in_project(self):
    self.assertFalse(self.task.in_project)



class ProjectTestCase(TestCase):
  def setUp(self):
    self.user = User.objects.create(**{
      'username': 'test_user',
      'password': 'test_pass'
    })
    
    self.project = Project.objects.create(**{
      'name': 'Learn Nuxt v3',
      'user': self.user
    })
    
  
  def test_project_empty_tasks(self):
    self.assertQuerysetEqual(self.project.tasks.all(), [])


  def test_project_tasks(self):
    task_1 = Task.objects.create(**{
      'user': self.user,
      'title': 'Study refs',
      'description': 'Read more about refs',
      'in_project': True
    })

    task_2 = Task.objects.create(**{
      'user': self.user,
      'title': 'Read about Nuxt 3 routing',
      'description': 'Find out how the routing works',
      'in_project': True
    })


    self.project.tasks.add(task_1)
    self.project.tasks.add(task_2)

    self.assertTrue(task_1.in_project)
    self.assertTrue(task_2.in_project)
    self.assertQuerysetEqual(self.project.tasks.all(), [task_1, task_2], ordered=False)
    self.assertEqual(self.project.tasks.count(), 2)
    self.assertEqual(task_1.project_tasks.first(), self.project)


  def test_user_projects(self):
    self.assertEqual(self.user.projects.count(), 1)


class SubtaskTestCase(TestCase):
  def setUp(self):
    user = User.objects.create(**{
      'username': 'test_user',
      'password': 'test_pass'
    })

    self.task = Task.objects.create(**{
      'user': user,
      'title': 'Study refs',
      'description': 'Read more about refs',
      'in_project': True
    })

    self.subtask_1 = Task.objects.create(**{
      'user': user,
      'title': 'Pinia',
      'description': 'Find out more about Pinia',
      'parent_task': self.task
    })

    self.subtask_2 = Task.objects.create(**{
      'user': user,
      'title': 'Router',
      'description': 'Find out more about Vue Router',
      'parent_task': self.task
    })

  
  def test_subtask_done_status(self):
    self.assertFalse(self.subtask_1.done)
    self.assertFalse(self.subtask_2.done)

  
  def test_task_subtasks(self):
    self.assertQuerysetEqual(self.task.subtasks.all(), [self.subtask_1, self.subtask_2], ordered=False)
    self.assertEqual(self.task.subtasks.count(), 2)
