from django.conf.urls import url
from django.contrib import admin

from .views import ( comment_thread
	)

app_name = 'comments'

urlpatterns = [
    url(r'^(?P<id>[\w-]+)/$',comment_thread, name='comment_thread'),
]
