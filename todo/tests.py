from django.test import TestCase
from django.urls import reverse
from datetime import date, timedelta

from .models import Todo


class TodoModelTests(TestCase):
	def test_create_todo_minimal(self):
		t = Todo.objects.create(title='Test 1')
		self.assertEqual(str(t), 'Test 1')
		self.assertFalse(t.completed)
		self.assertIsNone(t.due_date)

	def test_toggle_completed(self):
		t = Todo.objects.create(title='Toggle me')
		t.completed = True
		t.save()
		t.refresh_from_db()
		self.assertTrue(t.completed)


class TodoViewTests(TestCase):
	def setUp(self):
		# Create some todos
		self.t1 = Todo.objects.create(title='check1', description='dental appointment', due_date=date.today() + timedelta(days=1))
		self.t2 = Todo.objects.create(title='check2', description="John's wedding", due_date=date.today() - timedelta(days=1), completed=True)
		self.t3 = Todo.objects.create(title='check3', description='homework due', due_date=date.today() + timedelta(days=5))

	def test_homepage_shows_todos(self):
		resp = self.client.get(reverse('todo:index'))
		self.assertEqual(resp.status_code, 200)
		content = resp.content.decode('utf-8')
		self.assertIn('check1', content)
		self.assertIn('check2', content)
		self.assertIn('check3', content)

	def test_add_todo_valid(self):
		due = (date.today() + timedelta(days=3)).isoformat()
		resp = self.client.post(reverse('todo:add'), {'title': 'New Task', 'description': 'abc', 'due_date': due})
		self.assertEqual(resp.status_code, 302)
		self.assertTrue(Todo.objects.filter(title='New Task').exists())

	def test_add_todo_invalid_empty_title(self):
		resp = self.client.post(reverse('todo:add'), {'title': '', 'description': 'no title'})
		# Should render form with errors (status 200)
		self.assertEqual(resp.status_code, 200)
		self.assertIn('This field is required', resp.content.decode('utf-8'))

	def test_edit_todo(self):
		url = reverse('todo:edit', kwargs={'pk': self.t1.pk})
		new_title = 'Updated check1'
		resp = self.client.post(url, {'title': new_title, 'description': self.t1.description, 'due_date': self.t1.due_date})
		self.assertEqual(resp.status_code, 302)
		self.t1.refresh_from_db()
		self.assertEqual(self.t1.title, new_title)

	def test_delete_todo(self):
		url = reverse('todo:delete', kwargs={'pk': self.t3.pk})
		# GET shows the confirm page
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 200)
		# POST deletes
		resp = self.client.post(url)
		self.assertEqual(resp.status_code, 302)
		self.assertFalse(Todo.objects.filter(pk=self.t3.pk).exists())

	def test_toggle_todo(self):
		# toggle t1
		url = reverse('todo:toggle', kwargs={'pk': self.t1.pk})
		before = self.t1.completed
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 302)
		self.t1.refresh_from_db()
		self.assertNotEqual(self.t1.completed, before)

	def test_nonexistent_operations_raise_404(self):
		bad_pk = 9999
		for name in ['edit', 'delete', 'toggle']:
			url = reverse(f'todo:{name}', kwargs={'pk': bad_pk})
			resp = self.client.get(url)
			self.assertEqual(resp.status_code, 404)

	def test_long_title_rejected(self):
		long_title = 'x' * 201
		resp = self.client.post(reverse('todo:add'), {'title': long_title, 'description': 'too long'})
		self.assertEqual(resp.status_code, 200)
		self.assertIn('Ensure this value has at most 200 characters', resp.content.decode('utf-8'))

	def test_due_date_optional(self):
		resp = self.client.post(reverse('todo:add'), {'title': 'No due', 'description': 'N/A', 'due_date': ''})
		self.assertEqual(resp.status_code, 302)
		self.assertTrue(Todo.objects.filter(title='No due').exists())

