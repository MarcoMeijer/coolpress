from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from press.models import CoolUser, Category, Post


class PostModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.u = User.objects.create(first_name='test')
        cls.cu = CoolUser.objects.create(user=cls.u)
        cls.cat = Category.objects.create(slug='random', label='Some random news')
        cls.p = Post.objects.create(category=cls.cat, author=cls.cu)
        pass

    def test_sample_post(self):
        self.assertEqual(self.p.id, 1)

        cnt_of_post = Post.objects.count()
        self.assertEqual(cnt_of_post, 1)

    def test_post_detail(self):
        client = Client()
        url = reverse('post-detail', kwargs={'post_id': self.p.id})
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
