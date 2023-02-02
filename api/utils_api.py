from django.test import Client
from json import loads

creds = {
  'username': 'test_user',
  'password': 'test_password'
}

class AuthUtils():
  def __init__(self):
    self.c = Client()
    self.access_token = {} 

  def register(self, creds=creds):
    return self.c.post('/api/auth/register/', {
      **creds,
      'passwordConfirmation': creds['password']
    })
    
  def login(self, creds=creds):
    response = self.c.post('/api/auth/login/', creds)
    self.access_token = self.c.cookies['access_token']
    return response

  def auth(self):
    self.register()
    self.login()
