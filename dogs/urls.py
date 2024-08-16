from django.urls import path
from rest_framework.routers import SimpleRouter

from dogs.apps import DogsConfig
from dogs.views import (
    DogViewSet,
    BreedCreateAPIView,
    BreedUpdateAPIView,
    BreedDestroyAPIView,
    BreedListAPIView,
    BreedRetrieveAPIView,
)

app_name = DogsConfig.name

router = SimpleRouter()
router.register("", DogViewSet)

urlpatterns = [
    path("breeds/", BreedListAPIView.as_view(), name="breeds_list"),
    path("breeds/<int:pk>/", BreedRetrieveAPIView.as_view(), name="breeds_retrieve"),
    path("breeds/create/", BreedCreateAPIView.as_view(), name="breeds_create"),
    path(
        "breeds/<int:pk>/delete/", BreedDestroyAPIView.as_view(), name="breeds_delete"
    ),
    path("breeds/<int:pk>/update/", BreedUpdateAPIView.as_view(), name="breeds_update"),
]

urlpatterns += router.urls
