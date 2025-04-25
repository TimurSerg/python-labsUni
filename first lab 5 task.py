import hashlib

def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

def authenticate_user(users, login, password):
    if login in users:
        stored_password = users[login]['password']
        if stored_password == hash_password(password):
            return True
    return False

users = {
    'John1': {'password': hash_password('password123'), 'full_name': 'John Doe'},
    'Vasya2': {'password': hash_password('mysecret'), 'full_name': 'Jane Smith'}
}

login = input('Enter your login: ')
password = input('Enter your password: ')

if authenticate_user(users, login, password):
    print("Authentication successful")
else:
    print("Authentication failed")