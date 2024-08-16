from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from dogs.models import Breed, Dog
from users.models import User


class DogTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@sky.pro")
        self.breed = Breed.objects.create(
            name="Лабродор", description="Очень красивая собака"
        )
        self.dog = Dog.objects.create(name="Гром", breed=self.breed, owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_dog_retrieve(self):
        url = reverse("dogs:dog-detail", args=(self.dog.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.dog.name)

    def test_dog_create(self):
        url = reverse("dogs:dog-list")
        data = {"name": "Форест"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Dog.objects.all().count(), 2)

    def test_dog_update(self):
        url = reverse("dogs:dog-detail", args=(self.dog.pk,))
        data = {"name": "Форест"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "Форест")

    def test_dog_delete(self):
        url = reverse("dogs:dog-detail", args=(self.dog.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Dog.objects.all().count(), 0)

    def test_dog_list(self):
        url = reverse("dogs:dog-list")
        response = self.client.get(url)
        data = response.json()
        # print(response.json())
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.dog.pk,
                    "breed": {
                        "id": self.breed.pk,
                        "dogs": [self.dog.name],
                        "name": self.breed.name,
                        "description": self.breed.description,
                        "owner": None,
                    },
                    "name": self.dog.name,
                    "photo": None,
                    "date_born": None,
                    "owner": self.user.pk,
                }
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)


class BreedTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@sky.pro")
        self.breed = Breed.objects.create(
            name="Лабродор", description="Очень красивая собака", owner=self.user
        )
        self.dog = Dog.objects.create(name="Гром", breed=self.breed, owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_breed_retrieve(self):
        url = reverse("dogs:breeds_retrieve", args=(self.breed.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.breed.name)

    def test_breed_create(self):
        url = reverse("dogs:breeds_create")
        data = {"name": "Овчарка"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Breed.objects.all().count(), 2)

    def test_breed_update(self):
        url = reverse("dogs:breeds_update", args=(self.breed.pk,))
        data = {"name": "Колли"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "Колли")

    def test_breed_delete(self):
        url = reverse("dogs:breeds_delete", args=(self.breed.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Breed.objects.all().count(), 0)
