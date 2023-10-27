import requests

if __name__ == '__main__':

    data = {
        'username': 'johndoe',
        'password': 'password123'
    }

    result = requests.post('http://127.0.0.1:8000/token', data)

    print(result.content, result.status_code, result.reason)
