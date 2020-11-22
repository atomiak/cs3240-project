from django.test import TestCase

# Create your tests here.
from events.models import Post
from django.contrib.auth.models import User
from django.urls import reverse
from events.forms import EventForm
import datetime

class PostFieldsTest(TestCase):  
     def create_post(self, name="Test", description="A test event", category='Party', longitude="1", latitude="-1"):
         return Post.objects.create(name=name, description=description, user = User.objects.create(username='testusr'), category=category, longitude=longitude, latitude=latitude)
    
     def test_post_creation(self):
         p = self.create_post()
         self.assertTrue(isinstance(p, Post))
         self.assertEqual(p.name_to_text(), p.name)
         self.assertEqual(p.description_to_text(), p.description)
         self.assertEqual(p.category_to_text(), p.category)
         self.assertEqual(p.x_to_text(), p.longitude)
         self.assertEqual(p.y_to_text(), p.latitude)


class EventCreateView(TestCase):
    
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/events/create/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('events:create'))
        self.assertEqual(response.status_code, 200)


    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('events:create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/create.html')

class EventDetailView(TestCase):
    def setUp(self):
        user = User.objects.create(username='testusr01')

        self.new_event = Post.objects.create(
            name="Event 1",
            description = "test event 1",
            user = user,
            category = 'Party',
            longitude = "1",
            latitude = "-1"
            )
    
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/events/', kwargs={'pk':1})
        self.assertEqual(response.status_code, 200)
    
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('events:detail', kwargs={'pk':self.new_event.pk}))
        self.assertEqual(response.status_code, 200)
    
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('events:detail', kwargs={'pk':self.new_event.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/detail.html')


class EventFormTest(TestCase):
    def test_event_form_date_today(self):
        date = datetime.date.today()
        form = EventForm(
            data={
                'name':'testname',
                'description':'testdescription',
                'category':'Party',
                'longitude':0,
                'latitude':0,
                'event_date':date
                }
            )
        self.assertTrue(form.is_valid())

