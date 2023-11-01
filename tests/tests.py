import json

import requests

if __name__ == '__main__':

    data = {
      "username": "testuser",
      "email": "",
      "first_name": "None",
      "last_name": "None",
      "is_active": True,
      "is_admin": False,
      "hashed_password": "stringpass"
    }

    result = requests.post('http://127.0.0.1/signup', json.dumps(data))

    print(result.content, result.status_code, result.reason)
