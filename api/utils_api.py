from django.test import Client
from json import loads

creds = {
  'username': 'test_user',
  'password': 'test_password'
}

class AuthUtils():
  def __init__(self):
    self.c = Client()
    self.tokens = {} 

  def register(self, creds=creds):
    return self.c.post('/api/register/', {
      **creds,
      'passwordConfirmation': creds['password']
    })
    

  def login(self, creds=creds):
    response = self.c.post('/api/token/', creds)
    self.tokens = loads(response.content)
    return response

  def auth(self):
    self.register()
    self.login()
