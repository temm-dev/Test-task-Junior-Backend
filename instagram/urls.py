from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SyncPostsView, PostViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')

urlpatterns = [
    path('sync/', SyncPostsView.as_view(), name='sync'),
    path('', include(router.urls)),
]