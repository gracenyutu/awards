from django.test import TestCase
from .models import Post, Rating
from django.contrib.auth.models import User
# Create your tests here.
class TestProfile(TestCase):
    def setUp(self):
        self.user = User(id=1, username='grace', password='free5461')
        self.user.save()

    def test_instance(self):
        self.assertTrue(isinstance(self.user, User))

    def test_save_user(self):
        self.user.save()

    def test_delete_user(self):
        self.user.delete()


class PostTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(id=1, username='grace')
        self.post = Post.objects.create(id=1, title='test post', photo='https://commons.wikimedia.org/wiki/Commons:Quality_images', description='photos',
                                        user=self.user, url='http://free.com')

    def test_instance(self):
        self.assertTrue(isinstance(self.post, Post))

    def test_save_post(self):
        self.post.save_post()
        post = Post.objects.all()
        self.assertTrue(len(post) > 0)

    def test_get_posts(self):
        self.post.save()
        posts = Post.all_posts()
        self.assertTrue(len(posts) > 0)

    def test_search_post(self):
        self.post.save()
        post = Post.search_site('test')
        self.assertTrue(len(post) > 0)

    def test_delete_post(self):
        self.post.delete_post()
        post = Post.search_site('test')
        self.assertTrue(len(post) < 1)


class RatingTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(id=1, username='grace')
        self.post = Post.objects.create(id=1, title='test post', photo='https://commons.wikimedia.org/wiki/Commons:Quality_images', description='desc',
                                        user=self.user, url='http://free.com')
        self.rating = Rating.objects.create(id=1, design=6, usability=7, content=9, user=self.user, post=self.post)

    def test_instance(self):
        self.assertTrue(isinstance(self.rating, Rating))

    def test_save_rating(self):
        self.rating.save_rating()
        rating = Rating.objects.all()
        self.assertTrue(len(rating) > 0)
