from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

import main
from main import views
from main.views import PostViewSet, CommentViewSet


router = DefaultRouter()
router.register('posts', PostViewSet)
router.register('comment', CommentViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main.views.post_list, name='post_list'),
    path('api-auth/', include('rest_framework.urls')),
    path('v1/api/account/', include('account.urls')),
    path('account/', include('account.urls')),
    path('v1/api/', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

