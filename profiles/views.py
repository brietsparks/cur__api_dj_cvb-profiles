from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.

from profiles.models import Profile


def dummy_view(request):
    p = Profile.nodes.get_or_none(uuid='1582f053-4cf1-49b3-83dd-1a6b98e67cc7')

    return JsonResponse({'foo': p.uuid})