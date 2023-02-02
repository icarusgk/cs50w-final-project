from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.conf import settings

class TokenRefreshMiddleware:
  def __init__(self, get_response):
    self.get_response = get_response

  def __call__(self, request):
    response = self.get_response(request)
    refresh_token = request.session.get('refresh')

    excluded_routes = ['/api/auth/login/', '/api/auth/register/', '/api/auth/logout/']
    
    # Use this middleware everywhere except the login route
    if request.path not in excluded_routes:
      # Check if the refresh token is still valid
      try:
        # Set the new set of tokens based on the refresh token
        # stored in the user's session
        new_tokens = RefreshToken(refresh_token)
        # If the refresh token is still valid, try to refresh the access token
        try:
          access_token = request.COOKIES.get('access_token')
          if access_token:
            AccessToken(access_token)
          else:
            # In case the access token is deleted, set a new one
            request.COOKIES['access_token'] = str(new_tokens.access_token)

            response = self.get_response(request)

            # Sessionid means the user is logged in
            if request.COOKIES.get('sessionid'):
              response.set_cookie(
                'access_token',
                new_tokens.access_token,
                max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE']
              ) 
            # except the AccessToken() call
        except:
          # Set the new cookie on the server
          request.COOKIES['access_token'] = str(new_tokens.access_token)

          response = self.get_response(request)

          # Set the new cookie on the client
          response.set_cookie(
            'access_token',
            new_tokens.access_token,
            max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE']
          )
        # except the RefreshToken() call
      except:
        # If the refresh token is no longer valid, logout the user
        request.session = {}
        response = self.get_response(request)
        response.delete_cookie('access_token')
        response.delete_cookie('sessionid')
    
    return response