from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render  # Import render for lambda functions
from raktkan.views import home_view, register  # Import your views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),  # Home page URL pattern
    path('login/', include('django.contrib.auth.urls')),  # Built-in auth URLs
    path('register/', register, name='register'),  # Direct registration view
    path('dashboard/', include('admins.urls')),
    path('find_blood_bank/', include('bloodbanks.urls')),
    path('donor/', include('donors.urls')),
    path('recipient/', include('recipients.urls')),
    path('blogs/', include('blogs.urls')),
    path('donationdrive/', include('donationdrive.urls')),
    path('feedback/', lambda request: render(request, 'feedback.html'), name='feedback'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

