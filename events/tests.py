from django.test import TestCase

# Create your tests here.
from events.models import Post
from django.contrib.auth.models import User

class PostFieldsTest(TestCase):
    # def create_post(self, name="Test", description="A test event", category='Party', xcoordinate="1", ycoordinate="-1"):
    #     return Post.objects.create(name=name, description=description, user = User.objects.create(username='testusr'), category=category, xcoordinate=xcoordinate, ycoordinate=ycoordinate)
    
    # def test_post_creation(self):
    #     p = self.create_post()
    #     self.assertTrue(isinstance(p, Post))
    #     self.assertEqual(p.name_to_text(), p.name)
    #     self.assertEqual(p.description_to_text(), p.description)
    #     self.assertEqual(p.category_to_text(), p.category)
    #     self.assertEqual(p.x_to_text(), p.xcoordinate)
    #     self.assertEqual(p.y_to_text(), p.ycoordinate)
    def test(self):
        self.assertFalse(1 == 2)