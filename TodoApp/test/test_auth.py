from .utils import *
from ..routers.auth import get_db, get_current_user, authenticate_user, create_access_token, SECRET_KEY, ALGORITHM
from jose import jwt
from datetime import timedelta
import pytest
from fastapi import HTTPException

app.dependency_overrides[get_db] = override_get_db

def test_authenticate_user(test_user): 
  db = TestingSessionLocal()

  authenticated_user = authenticate_user(test_user.username, 'testpassword', db)
  assert authenticated_user is not None
  assert authenticated_user.username == test_user.username

  non_exist_user = authenticate_user('Wrong_user_name', 'testpassword', db)
  assert non_exist_user is False

  wrong_password_user = authenticate_user("testing", 'wrongpassword', db)
  assert wrong_password_user is False


def test_create_access_token(): 
  username = 'testuser'
  user_id = 1
  role = 'user'
  expires_delta = timedelta(days=1)

  token = create_access_token(username, user_id, role, expires_delta)

# This part with argument "algorithm" works in lecture but not here
# decode_token = jwt.decode(token, SECRET_KEY, algorithm=[ALGORITHM]
                                # options={'verify_signature': False})
  decode_token = jwt.decode(token, SECRET_KEY, 
                                options={'verify_signature': False})

  assert decode_token['sub'] == username
  assert decode_token['id'] == user_id
  assert decode_token['role'] == role

@pytest.mark.asyncio
async def test_get_current_user_valid_token(): 
  encode = {'sub': 'testing', 'id': 1, 'role': 'admin'}
  token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

  user = await get_current_user(token=token)
  assert user == {'username': 'testing', 'id': 1, 'user_role': 'admin'}


@pytest.mark.asyncio
async def test_get_current_user_missing_payload(): 
  encode = {'role': 'user'}
  token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

  with pytest.raises(HTTPException) as exception_info: 
    await get_current_user(token=token)

  assert exception_info.value.status_code == 401
  assert exception_info.value.detail == 'Could not validate user.'



 