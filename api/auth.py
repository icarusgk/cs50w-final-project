from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import CSRFCheck
from django.conf import settings

# Authenticates the user on each request
class CustomAuthentication(JWTAuthentication):
  def authenticate(self, request):
    header = self.get_header(request)

    if header is None:
      raw_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE']) or None
    else:
      raw_token = self.get_raw_token(header)
    
    if raw_token is None:
      return None
    
    validated_token = self.get_validated_token(raw_token)
    CSRFCheck(request)
    return self.get_user(validated_token), validated_token