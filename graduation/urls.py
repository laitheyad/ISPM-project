from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.conf.urls.static import static

from GP import settings
from .views import *
app_name = 'graduation'
urlpatterns = [
    # url(r'^$', landing_view, name='home'),
    url(r'^$', login_View, name='login'),
    url(r'^apply_for_supervisor$', apply_for_supervisor, name='apply_for_supervisor'),
    path('logout/', logoutUser, name="logout"),
    path('accept_project/<int:pk>/', acceptProject, name="accept"),
    path('reject_project/<int:pk>/', rejectProject, name="reject"),
    path('accept_meeting/<int:pk>/', acceptMeeting, name="accept-meeting"),
    path('reject_meeting/<int:pk>/', rejectMeeting, name="reject-meeting"),
    path('request_meeting/', requestMeeting, name="request-meeting"),
    path('ReplayToProgressReport/', ReplayToProgressReport, name="ReplayToProgressReport"),
    path('ApplayForProgressReport/', ApplayForProgressReport, name="ApplayForProgressReport"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)