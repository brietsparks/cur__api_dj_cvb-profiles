from django.conf.urls import url
from django.contrib import admin

from profiles.views import dummy_view

from profiles.views import ProfilesGraphQLView

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^graphql', ProfilesGraphQLView.as_view()),
    url(r'^graphiql', ProfilesGraphQLView.as_view(graphiql=True)),

    url(r'^foo/$', dummy_view)
]
