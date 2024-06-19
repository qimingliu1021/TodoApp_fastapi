from .utils import *
from ..routers.users import get_db, get_current_user
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_return_user(test_user): 
  response = client.get("/users")
  assert response.status_code == status.HTTP_200_OK
  assert response.json()['username'] == 'qiming_test'
  assert response.json()['email'] == 'test@gmail.com'
  assert response.json()['first_name'] == 'Qiming'
  assert response.json()['last_name'] == 'Liu'
  assert response.json()['role'] == 'admin'
  assert response.json()['phone_number'] == '111-111-1111'


def test_change_password_success(test_user): 
  response = client.put("/users/password", json={"old_password": "testpassword", 
                                                  'new_password': 'newpassword'})
  assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_unauthorized(test_user): 
  response = client.put("/users/password",  json={"old_password": "wrong_password", 
                                                  'new_password': 'newpassword'})
  assert response.status_code == status.HTTP_401_UNAUTHORIZED
  assert response.json() == {'detail': 'Error changing password'}

def test_change_phone_number_success(test_user): 
  response = client.put("/users/phone_number/{phone_number}", json={'phone_number': '123-456-7899'})
  assert response.status_code == status.HTTP_204_NO_CONTENT



