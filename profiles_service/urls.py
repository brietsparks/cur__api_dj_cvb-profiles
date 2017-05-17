from django.conf.urls import url
from django.contrib import admin

from profiles.views import dummy_view

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^foo/$', dummy_view)
]
