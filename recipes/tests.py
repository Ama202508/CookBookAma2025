from datetime import timedelta
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from .models import Recipe


class RecipeTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='ana', password='parola123')
        self.user2 = User.objects.create_user(username='bob', password='parola123')

    # 1) Pagina de login se incarca si login-ul functioneaza
    def test_login_page_and_auth(self):
        resp = self.client.get(reverse('login'))
        self.assertEqual(resp.status_code, 200)
        ok = self.client.login(username='ana', password='parola123')
        self.assertTrue(ok)

    # 2) Crearea retetei necesita autentificare
    def test_create_requires_login(self):
        resp = self.client.get(reverse('recipe_add'))
        self.assertEqual(resp.status_code, 302)
        self.assertIn(reverse('login'), resp.url)

    # helper pentru a crea retete valabile
    def _mk_recipe(self, owner, title, created_at=None):
        r = Recipe.objects.create(
            owner=owner,
            title=title,
            description='desc',
            cook_time='10 min',
            date_added_str='2025-01-01 12:00:00',
        )
        if created_at:
            Recipe.objects.filter(pk=r.pk).update(created_at=created_at)
            r.refresh_from_db()
        return r

    # 3) Crearea retetei cand esti logat
    def test_create_recipe_success(self):
        self.client.login(username='ana', password='parola123')
        data = {
            'title': 'Salata de pui cu avocado & sos',
            'description': 'Pui, avocado, sos iaurt.',
            'cook_time': '30 min',
            'date_added_str': '2025-01-01 12:00:00',
        }
        resp = self.client.post(reverse('recipe_add'), data, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(Recipe.objects.filter(title='Salata de pui cu avocado & sos').exists())
        r = Recipe.objects.get(title='Salata de pui cu avocado & sos')
        self.assertEqual(r.owner, self.user1)
        self.assertEqual(r.cook_time, '30 min')
        self.assertIsNotNone(r.created_at)

    # 4) Sortare alfabetica pe pagina principala
    def test_sorting_alphabetical(self):
        self._mk_recipe(self.user1, 'Banana')
        self._mk_recipe(self.user1, 'Apple')
        self._mk_recipe(self.user1, 'Carrot')
        resp = self.client.get(reverse('recipe_list'))
        self.assertEqual(resp.status_code, 200)
        titles = [r.title for r in resp.context['recipes']]
        self.assertEqual(titles, ['Apple', 'Banana', 'Carrot'])

    # 5) Sortare după data (descrescator)
    def test_sorting_by_creation_date(self):
        now = timezone.now()
        self._mk_recipe(self.user1, 'r1', created_at=now - timedelta(days=2))
        self._mk_recipe(self.user1, 'r2', created_at=now - timedelta(days=1))
        self._mk_recipe(self.user1, 'r3', created_at=now)
        resp = self.client.get(reverse('recipe_list_by_date'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual([r.title for r in resp.context['recipes']], ['r3', 'r2', 'r1'])

    # 6) Doar autorul poate edita
    def test_only_owner_can_edit(self):
        r = self._mk_recipe(self.user1, 'Privat')
        self.client.login(username='bob', password='parola123')
        resp = self.client.get(reverse('recipe_edit', args=[r.id]))
        self.assertEqual(resp.status_code, 403)

    # 7) Validarea campului date_added_str
    def test_date_added_str_required(self):
        self.client.login(username='ana', password='parola123')
        data = {
            'title': 'Gresit',
            'description': 'X',
            'cook_time': '10',
            'date_added_str': '',
        }
        resp = self.client.post(reverse('recipe_add'), data)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Acest câmp este obligatoriu.')
