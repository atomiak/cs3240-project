"""
REFERENCES
Title: Django Documentation Testing Tools
Author: Django Software Foundation
Date: Copyright 2005-2020, accessed 10/15/2020
URL: https://docs.djangoproject.com/en/3.1/topics/testing/tools/

Title: Django Tutorial Part 10: Testing a Django web application
Author: Mozilla Web Docs
Date: Copyright 2005-2020, accessed 10/17/2020
URL: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing

Title: RequestFactory documentation
Author: Kite
Date: Accessed 11/2/2020
URL: https://www.kite.com/python/docs/django.test.RequestFactory

All packages used under the Django umbrella
"""

from django.test import TestCase

# Create your tests here.
from events.models import Post
from django.contrib.auth.models import User
from django.urls import reverse
from events.forms import EventForm
import datetime
from django.test import RequestFactory
from events.views import EditView
from events.views import CreateView
from events.views import DetailView
from django.shortcuts import render, redirect
import events.views

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

class EventEditView(TestCase):
    def setUp(self):
        user = User.objects.create(username = 'testuser02')
        
        self.new_event = Post.objects.create(
            name="Event 2",
            description = "test event 2",
            user = user,
            category = 'Party',
            longitude = "1",
            latitude = "-1"
        )

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('events:edit', kwargs={'pk':self.new_event.pk}))
        self.assertEqual(response.status_code, 302) #a valid redirect has code 302
    
    # def test_view_uses_correct_template(self):
    #     response = self.client.get(reverse('events:edit', kwargs={'pk':self.new_event.pk}))
    #     self.assertEqual(response.status_code, 302)
    #     self.assertTemplateUsed(response, 'events/edit.html')


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
                'address':'Charlottesville, VA',
                'event_date':date
                }
            )
        self.assertTrue(form.is_valid())

class RequestsInViewsTest(TestCase):
    def setUp(self):
        self.userA = User.objects.create(username='testusrA')
        self.userB = User.objects.create(username='testusrB')
        self.event1 = Post.objects.create(
            name="Fun Event",
            description = "test event 1",
            user = self.userA,
            category = 'Party',
            longitude = "1",
            latitude = "-1"
        )
        self.event2 = Post.objects.create(
            name="Fun Event 2",
            description = "test event 2",
            user = self.userB,
            category = 'Athletic Event',
            longitude = "1",
            latitude = "-1"
        )

    
    def test_valid_event_ownership(self):
        self.assertEqual(self.userA, self.event1.user)
        self.assertEqual(self.userB, self.event2.user)
    
    def test_invalid_event_ownership(self):
        self.assertFalse(self.userA == self.event2.user)
        self.assertFalse(self.userB == self.event1.user)

    def test_edit_post_equal(self):
        def setup_view(view, request, *args, **kwargs):
            view.request = request
            view.args = args
            view.kwargs = kwargs
            return view
        
        factory = RequestFactory()
        edit_post_request1 = factory.post('/')
        edit_post_request1.user = self.userA

        edit_post_request2 = factory.post('/')
        edit_post_request2.user = self.userB

        edit_view = EditView()
        edit_view = setup_view(edit_view, edit_post_request1)

        self.assertEqual(edit_view.post(edit_post_request1, self.event1.pk).url, redirect(reverse('events:detail', args=[self.event1.pk])).url)

    def test_edit_post_not_equal(self):
        def setup_view(view, request, *args, **kwargs):
            view.request = request
            view.args = args
            view.kwargs = kwargs
            return view
        
        factory = RequestFactory()
        edit_post_request1 = factory.post('/')
        edit_post_request1.user = self.userA

        edit_post_request2 = factory.post('/')
        edit_post_request2.user = self.userB

        edit_view = EditView()
        edit_view = setup_view(edit_view, edit_post_request1)

        self.assertNotEqual(edit_view.post(edit_post_request1, self.event1.pk).url, redirect(reverse('events:detail', args=[self.event2.pk])).url)
        self.assertNotEqual(edit_view.post(edit_post_request2, self.event2.pk).url, redirect(reverse('events:detail', args=[self.event1.pk])).url)

    def test_edit_get_equal(self):
        def setup_view(view, request, *args, **kwargs):
            view.request = request
            view.args = args
            view.kwargs = kwargs
            return view
        
        factory = RequestFactory()
        edit_get_request1 = factory.get('/')
        edit_get_request1.user = self.userA

        edit_view = EditView()
        edit_view = setup_view(edit_view, edit_get_request1)

        self.assertEqual(edit_view.get(edit_get_request1, self.event1.pk).status_code, render(edit_get_request1, 'events/edit.html', {'form': EventForm(instance=self.event1)}).status_code)

    def test_create_post_equal(self):
        def setup_view(view, request, *args, **kwargs):
            view.request = request
            view.args = args
            view.kwargs = kwargs
            return view
        
        factory = RequestFactory()
        create_post_request1 = factory.post('/')
        create_post_request1.user = self.userA

        create_view = CreateView()
        create_view = setup_view(create_view, create_post_request1)

        response = create_view.post(create_post_request1)

        self.assertEqual(redirect(reverse('events:events')), response)

    def test_detail_post_url_equal(self):
        def setup_view(view, request, *args, **kwargs):
            view.request = request
            view.args = args
            view.kwargs = kwargs
            return view
        
        factory = RequestFactory()
        detail_post_request1 = factory.post('/')
        detail_post_request1.user = self.userA

        detail_view = DetailView()
        detail_view = setup_view(detail_view, detail_post_request1)

        response = detail_view.post(detail_post_request1, self.event1.pk)

        self.assertEqual(redirect(reverse('events:events')).url, response.url)

    def test_detail_post_user_added(self):
        def setup_view(view, request, *args, **kwargs):
            view.request = request
            view.args = args
            view.kwargs = kwargs
            return view
        
        factory = RequestFactory()
        detail_post_request1 = factory.post('/')
        detail_post_request1.user = self.userB

        detail_view = DetailView()
        detail_view = setup_view(detail_view, detail_post_request1)

        response = detail_view.post(detail_post_request1, self.event1.pk)
        self.assertTrue(detail_post_request1.user in self.event1.attendees.all())

    def test_detail_post_user_left(self):
        def setup_view(view, request, *args, **kwargs):
            view.request = request
            view.args = args
            view.kwargs = kwargs
            return view
        
        factory = RequestFactory()
        detail_post_request1 = factory.post('/')
        detail_post_request1.user = self.userB

        detail_view = DetailView()
        detail_view = setup_view(detail_view, detail_post_request1)

        response = detail_view.post(detail_post_request1, self.event1.pk)
        response2 = detail_view.post(detail_post_request1, self.event1.pk)

        self.assertFalse(detail_post_request1.user in self.event1.attendees.all())

    def test_edit_post_user_not_owner(self):
        def setup_view(view, request, *args, **kwargs):
            view.request = request
            view.args = args
            view.kwargs = kwargs
            return view
        
        factory = RequestFactory()
        edit_post_request = factory.post('/')
        edit_post_request.user = self.userB

        edit_view = EditView()
        edit_view = setup_view(edit_view, edit_post_request)

        response = edit_view.post(edit_post_request, self.event1.pk)
        self.assertEqual(redirect('/accounts/google/login?process=login').url, response.url)

    def test_edit_get_user_not_owner(self):
        def setup_view(view, request, *args, **kwargs):
            view.request = request
            view.args = args
            view.kwargs = kwargs
            return view
        
        factory = RequestFactory()
        edit_get_request = factory.get('/')
        edit_get_request.user = self.userB

        edit_view = EditView()
        edit_view = setup_view(edit_view, edit_get_request)

        response = edit_view.get(edit_get_request, self.event1.pk)
        self.assertEqual(redirect('/accounts/google/login?process=login').url, response.url)

    def test_invalid_delete(self):
        factory = RequestFactory()
        delete_request = factory.delete('/')
        delete_request.user = self.userB

        response = events.views.delete(delete_request, self.event1.pk)
        self.assertEqual(redirect('/accounts/google/login?process=login').url, response.url)
    
    def test_valid_delete(self):
        factory = RequestFactory()
        delete_request = factory.delete('/')
        delete_request.user = self.userA
        response = events.views.delete(delete_request, self.event1.pk)
        self.assertEqual(redirect('events:events').url, response.url)
