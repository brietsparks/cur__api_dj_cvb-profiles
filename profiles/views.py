from django.shortcuts import render
from django.http import JsonResponse
from graphene_django.views import GraphQLView
from django.utils.decorators import decorator_from_middleware

from .models import Profile
from .middleware import ProfilesTokenMiddleware


def dummy_view(request):
    p = Profile.nodes.get_or_none(uuid='1582f053-4cf1-49b3-83dd-1a6b98e67cc7')
    return JsonResponse({'foo': p.uuid})


@decorator_from_middleware(ProfilesTokenMiddleware)
class ProfilesGraphQLView(GraphQLView):
    pass

