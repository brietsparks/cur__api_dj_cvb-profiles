from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Client
from django_jwt_wrapper.token import JWT


@api_view(['POST'])
def get_access_token(request):
    response_data = {
        'valid_credentials': None,
        'access_token': None,
    }

    # todo: validate:
    client_id = request.dat['client_id']                        # string
    client_secret = request.data['client_secret']               # string
    permission_names = request.data['requested_permissions']    # array of strings

    client = Client.objects.authenticate(client_id, client_secret)
    if client:
        response_data['valid_credentials'] = True
    else:
        response_data['valid_credentials'] = False
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    permissions = list(client.get_granted_permissions(permission_names).values('name', 'description'))

    response_data['access_token'] = JWT.create_token(600, permissions=permissions, aud=client.id, aud_alias=client.name)

    return Response(response_data)

