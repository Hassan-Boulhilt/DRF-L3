# from django.test import TestCase
import json
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
from profiles.models import Profile, ProfileStatus
from profiles.api.serializers import ProfileSerializer, ProfileStatusSerializer



class RegistrationTestCase(APITestCase):
    def test_registration(self):
        data  = {"username": "Ahmed", "email": "ahmed@localhost.api", "password1": "some_strong_psw", "password2": "some_strong_psw"}
        response = self.client.post("/api/dj-rest-auth/registration/", data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
class ProfileViewsetTestCase(APITestCase):
    
    list_url = reverse('profile-list')
    
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="camel", email="camel@localhost.api")
        
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()
    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
    def test_profile_list_authenticated(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_profile_list_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_profile_detail_retrieve(self):
        profile = Profile.objects.first()
        url = reverse('profile-detail', kwargs={"pk": profile.id})
        response = self.client.get(url)
        serializer_data = ProfileSerializer(profile).data
        self.assertEqual(response.data, serializer_data)        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_profile_update_by_owner(self):
        profile = Profile.objects.first()
        url = reverse('profile-detail', kwargs={"pk": profile.id})
        data = {"city": "New York", "bio": "I love New York"}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertEqual(json.loads(response.content), {"id": 1, "user": "camel", "avatar": None,"city": "New York", "bio": "I love New York"})
    def test_profile_update_by_random_user(self):
        random_user = User.objects.create_user(username="random", password="some_strong_psw")
        self.client.force_authenticate(user=random_user)
        url = reverse('profile-detail', kwargs={"pk": 1})
        data = {"bio": "I love Tan-Tan"}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
class ProfileStatusViewsetTestCase(APITestCase):
    
    url = reverse('status-list')
    
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="camel", password="some_strong_psw")
        self.status = ProfileStatus.objects.create(user_profile=self.user.profile, status_content="status test")        
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()
        
    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
    def test_status_list_authenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_status_list_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_status_create(self):
        data = {"status_content": "a new status"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["user_profile"], "camel")
        self.assertEqual(response.data["status_content"], "a new status")
    
    def test_single_status_retrieve(self):
        serializer_data = ProfileStatusSerializer(instance=self.status).data
        url = reverse('status-detail', kwargs={"pk": 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), serializer_data)
        
    def test_single_status_update_owner(self):
        data = {"status_content": "content updated"}
        url = reverse('status-detail', kwargs={"pk": 1})
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status_content"], "content updated")
    
    def test_single_status_update_by_random_user(self):
        random_user = User.objects.create_user(username="random", password="some_strong_psw")
        self.client.force_authenticate(user=random_user)
        data = {"status_content": "content updated"}
        url = reverse('status-detail', kwargs={"pk": 1})
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)