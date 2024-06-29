from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StoryRequestViewSet, user_signup

router = DefaultRouter()
router.register(r'story_requests', StoryRequestViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('storyrequest/generate_story/', StoryRequestViewSet.as_view({'post': 'generate_story'}), name='generate_story'),
    path('user/join', user_signup, name='user_signup')
]
