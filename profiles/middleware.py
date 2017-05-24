# Checks request for api token and authenticates user if a value one is found
# Checks request for a jwt access token and authenticates user if a valid one is found
class ProfilesTokenMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    """
    If dev mode, then allow anonymous user (for graphiql), if not then don't
    If header authorization is
        bearer (jwt), then authenticate a user
        token (api token), then authenticate an admin
    """
    def __call__(self, request):
        response = self.get_response(request)

        print('\n')
        print(request)
        print(request.user)
        print('\n')

        return response

    # Checks request for api token
    def auth_header_has_jwt(self, request):
        pass

    # Checks request for a jwt access token
    def auth_header_has_api_token(self, request):
        pass
