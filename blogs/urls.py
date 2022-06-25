from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from blogs.views import home


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home, name='home'),
    
    path('', include('account.urls', namespace='account')),
    path('api/', include('account.api.urls', namespace='account_api')),

    path('', include('accountProfile.urls', namespace='accountProfile')),

    path('', include('blog.urls', namespace='blog')),
]

handler404 = 'blogs.views.page_not_found_view'

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
