from django.conf.urls import url
from django.contrib import admin

from profiles.views import dummy_view

from graphene_django.views import GraphQLView

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^graphql', GraphQLView.as_view()),
    url(r'^graphiql', GraphQLView.as_view(graphiql=True)),

    url(r'^foo/$', dummy_view)
]
