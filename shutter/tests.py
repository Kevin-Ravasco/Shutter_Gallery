import unittest

from allauth.account.models import EmailAddress
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.test import SimpleTestCase
from django.test.client import MULTIPART_CONTENT
from django.urls import reverse, resolve
from django.contrib import messages

from .views import *
from .forms import AddAlbumForm, AddPhotoForm, CreateProfileForm

from allauth.utils import get_user_model


# Create your tests here.


class HomeViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create(username='user', password='password', is_active=True)
        EmailAddress.objects.create(user=self.user, email="example@example.com", primary=True, verified=True)
        self.response = self.client.force_login(self.user)

        self.user2 = get_user_model().objects.create(username='user2', password='password2', is_active=True)
        EmailAddress.objects.create(user=self.user2, email="user2@example.com", primary=True, verified=True)

        self.album = Album.objects.create(name='TestAlbum', created_by=self.user)
        self.photo = Photo.objects.create(image='image.jpg', album=self.album)
        self.photo2 = Photo.objects.create(image='image2.jpg', album=self.album)

        self.album2 = Album.objects.create(name='TestAlbum2', created_by=self.user2)
        self.photo3 = Photo.objects.create(image='image3.jpg', album=self.album2)
        self.photo4 = Photo.objects.create(image='image4.jpg', album=self.album2)

    def test_home_url_resolves_home_view(self):
        url = reverse('home')
        resolved = resolve(url)
        self.assertEquals(resolved.func, home)

    def test_home_view_uses_index_template(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'shutter/index.html')

    def test_home_view_redirects_to_login_when_unauthenticated(self):
        client = Client()
        url = reverse('home')
        response = client.get(url)
        expected_url = '/accounts/login/?next=/'
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, expected_url, 302)

    def test_home_view_resolves_when_authenticated(self):
        response = self.client.get(reverse('home'))
        self.assertEquals(response.status_code, 200)

    def test_home_view_displays_album(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, self.album)

    def test_home_view_does_not_display_album2(self):
        response = self.client.get(reverse('home'))
        self.assertNotContains(response, self.album2)

    def test_home_view_displays_albums_photo_as_cover_photo(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, self.photo.image)

    def test_home_view_does_not_display_2photos_from_the_same_album(self):
        response = self.client.get(reverse('home'))
        self.assertNotContains(response, self.photo2.image)

    def test_post_request(self):
        response = self.client.post(reverse('home'), data={'album': 'Album3'})
        album3 = Album.objects.get(id=3)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(album3.name, 'Album3')
        self.assertRedirects(response, reverse('photos', args=[album3.id]), 302)

    def test_has_form(self):
        response = self.client.get(reverse('home'))
        form = response.context['form']
        self.assertIsInstance(form, AddAlbumForm)

    def test_csrf(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'csrfmiddlewaretoken')


class PhotoViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        user = get_user_model().objects.create(username='user', password='password', is_active=True)
        EmailAddress.objects.create(user=user, email="user@example.com", primary=True, verified=True)
        self.response = self.client.force_login(user)

        user2 = get_user_model().objects.create(username='user2', password='password2', is_active=True)
        EmailAddress.objects.create(user=user2, email="user2@example.com", primary=True, verified=True)

        self.album = Album.objects.create(name='TestAlbum', created_by=user)
        self.photo = Photo.objects.create(image='image.jpg', album=self.album)
        self.photo2 = Photo.objects.create(image='image2.jpg', album=self.album)

        self.album2 = Album.objects.create(name='TestAlbum2', created_by=user2)
        self.photo3 = Photo.objects.create(image='image3.jpg', album=self.album2)
        self.photo4 = Photo.objects.create(image='image4.jpg', album=self.album2)

    def test_resolves_delete_album_page_view(self):
        url = reverse('photos', args=[self.album.id])
        resolved = resolve(url)
        self.assertEquals(resolved.func, photos)

    def test_photo_view_status_code_when_authenticated(self):
        url = reverse('photos', args=[self.album.id])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response.status_code, 302)

    def test_uses_single_template(self):
        url = reverse('photos', args=[self.album.id])
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'shutter/single.html')

    def test_photo_view_redirects_when_uanuthenticated(self):
        url = reverse('photos', args=[self.album.id])
        client = Client()
        response = client.get(url)
        expected_url = '/accounts/login/?next=/photos/1/'
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, expected_url, 302)

    def test_photo_view_has_photos_from_album(self):
        url = reverse('photos', args=[self.album.id])
        response = self.client.get(url)
        self.assertContains(response, self.album.name)
        self.assertContains(response, self.photo.image)
        self.assertContains(response, self.photo2.image)

    def test_photo_view_has_no_photos_from_album2(self):
        url = reverse('photos', args=[self.album.id])
        response = self.client.get(url)
        self.assertNotContains(response, self.album2.name)
        self.assertNotContains(response, self.photo3.image)
        self.assertNotContains(response, self.photo4.image)

    def test_contains_link_to_delete_album_view(self):
        response = self.client.get(reverse('photos', args=[self.album.id]))
        delete_album_url = reverse('delete_album_page', args=[self.album.id])
        self.assertContains(response, delete_album_url)

    def test_has_album_form(self):
        response = self.client.get(reverse('photos', args=[self.album.id]))
        form = response.context['album_form']
        self.assertIsInstance(form, AddAlbumForm)

    def test_csrf(self):
        response = self.client.get(reverse('photos', args=[self.album.id]))
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_html(self):
        response = self.client.get(reverse('photos', args=[self.album.id]))
        self.assertContains(response, '<form')
        self.assertContains(response, 'class="modal fade" id="modal-progress" data-backdrop="static" '
                                      'data-keyboard="false"')
        self.assertContains(response, 'js-upload-photos')
        self.assertContains(response, 'id="fileupload" type="file" name="image" multiple')


class ProfileViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create(username='user', password='password', is_active=True)
        EmailAddress.objects.create(user=self.user, email="user@example.com", primary=True, verified=True)
        self.client.force_login(self.user)
        self.response = self.client.get(reverse('profile'))

        self.user2 = get_user_model().objects.create(username='user2', password='password2', is_active=True)
        EmailAddress.objects.create(user=self.user2, email="user2@example.com", primary=True, verified=True)

        self.album = Album.objects.create(name='TestAlbum', created_by=self.user)
        self.photo = Photo.objects.create(image='image.jpg', album=self.album)
        self.photo2 = Photo.objects.create(image='image2.jpg', album=self.album)

        self.album2 = Album.objects.create(name='TestAlbum2', created_by=self.user2)
        self.photo3 = Photo.objects.create(image='image3.jpg', album=self.album2)
        self.photo4 = Photo.objects.create(image='image4.jpg', album=self.album2)

    def test_uses_profile_template(self):
        response = self.response
        self.assertTemplateUsed(response, 'shutter/profile.html')

    def test_resolves_profile_view(self):
        url = reverse('profile')
        resolved = resolve(url)
        self.assertEquals(resolved.func, profile)

    def test_profile_view_when_authenticated(self):
        response = self.response
        self.assertEquals(response.status_code, 200)

    def test_profile_view_when_unauthenticated(self):
        client = Client()
        url = reverse('profile')
        response = client.get(url)
        expected_url = '/accounts/login/?next=/profile/'
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, expected_url, 302)

    def test_post_method_create_profile(self):
        # Check image upload test
        # profilepic = SimpleUploadedFile("profilepic.jpg", b"file_content", content_type="image/jpeg")
        self.client.post(reverse('profile'),
                         data={'first_name': 'firstName', 'last_name': 'lastName', 'phone': 123, 'image': 'profic.jpg'})
        user_profile = Profile.objects.get(user=self.user)
        self.assertEquals(user_profile.first_name, 'firstName')
        self.assertEquals(user_profile.last_name, 'lastName')
        self.assertEquals(user_profile.phone, 123)
        # self.assertEquals(user_profile.image, 'profic.jpg')

    def test_post_method_update_profile(self):
        # Check image upload test
        # profilepic = SimpleUploadedFile("profilepic.jpg", b"file_content", content_type="image/jpeg")
        response = self.client.post(reverse('profile'),
                                    data={'first_name': 'firstNameUpdated', 'last_name': 'lastNameUpdated',
                                          'phone': 123456, 'image': 'profic2.jpg'}, content_type='image/jpeg')
        user_profile = Profile.objects.get(user=self.user)
        self.assertEquals(user_profile.first_name, 'firstNameUpdated')
        self.assertEquals(user_profile.last_name, 'lastNameUpdated')
        self.assertEquals(user_profile.phone, 123456)
        self.assertEquals(user_profile.image, 'profic2.jpg')
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('profile'), 302)

    def test_has_create_profile_form(self):
        response = self.response
        form = response.context['form']
        self.assertIsInstance(form, CreateProfileForm)

    def test_csrf(self):
        response = self.response
        self.assertContains(response, 'csrfmiddlewaretoken')


class DeleteAlbumPage(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create(username='user', password='password', is_active=True)
        EmailAddress.objects.create(user=self.user, email="user@example.com", primary=True, verified=True)
        self.client.force_login(self.user)
        self.album = Album.objects.create(name='TestAlbum', created_by=self.user)
        self.response = self.client.get(reverse('delete_album_page', args=[self.album.id]))

    def test_resolves_delete_album_page_view(self):
        url = reverse('delete_album_page', args=[self.album.id])
        resolved = resolve(url)
        self.assertEquals(resolved.func, delete_album_page)

    def test_uses_delete_album_template(self):
        response = self.response
        self.assertTemplateUsed(response, 'shutter/delete_album.html')

    def test_status_code(self):
        response = self.response
        self.assertEquals(response.status_code, 200)

    def test_contains_link_back_to_photos(self):
        response = self.response
        photos_url = reverse('photos', args=[self.album.id])
        self.assertContains(response, photos_url)

    def test_contains_link_to_delete_album_view(self):
        response = self.response
        delete_album_url = reverse('delete_album', args=[self.album.id])
        self.assertContains(response, delete_album_url)


class AlbumDeleteTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create(username='user', password='password', is_active=True)
        EmailAddress.objects.create(user=self.user, email="user@example.com", primary=True, verified=True)
        self.client.force_login(self.user)
        self.album = Album.objects.create(name='TestAlbum', created_by=self.user)

    def test_resolves_delete_album_view(self):
        url = reverse('delete_album', args=[self.album.id])
        resolved = resolve(url)
        self.assertEquals(resolved.func, delete_album)

    def test_it_deletes_album(self):
        self.client.post(reverse('delete_album', args=[self.album.id]))
        album = Album.objects.first()
        self.assertEquals(album, None)

    def test_redirects_to_home_after_successful_delete(self):
        response = self.client.post(reverse('delete_album', args=[self.album.id]))
        expected_url = reverse('home')
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, expected_url, 302)


class UpdateAlbumViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create(username='user', password='password', is_active=True)
        EmailAddress.objects.create(user=self.user, email="user@example.com", primary=True, verified=True)
        self.client.force_login(self.user)
        self.album = Album.objects.create(name='TestAlbum', created_by=self.user)
        self.response = self.client.post(reverse('update_album', args=[self.album.id]),
                                         data={'album': 'TestAlbumUpdate'})

    def test_album_post_method_updates_album_name(self):
        response = self.response
        album = Album.objects.get(id=1)
        self.assertEquals(album.name, 'TestAlbumUpdate')

    def test_resolves_delete_album_view(self):
        url = reverse('update_album', args=[self.album.id])
        resolved = resolve(url)
        self.assertEquals(resolved.func, update_album)

    def test_album_redirects_to_photos(self):
        response = self.response
        expected_url = reverse('photos', args=[self.album.id])
        self.assertRedirects(response, expected_url, 302)


class ContactViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create(username='user', password='password', is_active=True)
        EmailAddress.objects.create(user=self.user, email="user@example.com", primary=True, verified=True)
        self.client.force_login(self.user)
        self.response = self.client.get(reverse('contact'))

    def test_uses_contact_template(self):
        response = self.response
        self.assertTemplateUsed(response, 'shutter/contact.html')

    def test_response_status_code(self):
        response = self.response
        self.assertEquals(response.status_code, 200)

    def test_resolves_contact_view(self):
        url = reverse('contact')
        resolved = resolve(url)
        self.assertEquals(resolved.func, contact)

    def test_post_method(self):
        response = self.client.post(reverse('contact'), data={'first_name': 'firstName', 'last_name': 'lastName',
                                                              'email': 'test@example.com', 'subject': 'test subject',
                                                              'message': 'test message'})
        self.assertRedirects(response, reverse('contact'), 302)


class TestAddAlbumForm(TestCase):
    def test_add_album_form_with_valid_data(self):
        form = AddAlbumForm(data={'album': 'TestAlbum'})
        self.assertTrue(form.is_valid())

    def test_add_album_form_with_invalid_data(self):
        form = AddAlbumForm(data={'album': ''})
        self.assertEquals(form.is_valid(), False)


class TestCreateProfileForm(TestCase):
    def test_create_profile_form_with_valid_data(self):
        test_image = SimpleUploadedFile("testimage.jpg", b"file_content", content_type="image/jpeg")
        form = CreateProfileForm(data={'first_name': 'firstNameUpdated', 'last_name': 'lastNameUpdated',
                                       'phone': 123456, 'image': test_image})
        self.assertTrue(form.is_valid())


class TestAddPhotoForm(TestCase):
    def test_add_photo_form_with_valid_data(self):
        test_image2 = SimpleUploadedFile("testimage2.jpg", b"file_content", content_type="image/jpeg")
        form = AddPhotoForm(data={'image': test_image2})
        self.assertTrue(form.is_valid())

    def test_add_photo_form_with_invalid_data(self):
        form = AddAlbumForm(data={'image': 'testvideo.mp4'})
        self.assertEquals(form.is_valid(), False)
