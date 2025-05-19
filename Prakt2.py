import hashlib
from datetime import datetime

class User:

    def __init__(self, username, password_hash, is_active=True):
        self.username = username
        self.password_hash = password_hash
        self.is_active = is_active

    def verify_password(self, password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest() == self.password_hash

class Administrator(User):

    def __init__(self, username, password, is_active=True):
        super().__init__(username, hashlib.sha256(password.encode('utf-8')).hexdigest(), is_active)
        self.admin_specific_setting = True

class RegularUser(User):

    def __init__(self, username, password, is_active=True):
        super().__init__(username, hashlib.sha256(password.encode('utf-8')).hexdigest(), is_active)
        self.last_login_date = None

class AccessControl:

    def __init__(self):
        self.users = {}

    def add_user(self, user):
        self.users[user.username] = user

    def authenticate_user(self, username, password):
        user = self.users.get(username)

        if user and user.verify_password(password):
            if isinstance(user, RegularUser):
                user.last_login_date = datetime.now()
            return user
        else:
            return None

if __name__ == "__main__":
    acl = AccessControl()

    admin_user = Administrator("Admin_Timur", "Admin1")
    regular_user = RegularUser("User_Vasya", "User13")

    acl.add_user(admin_user)
    acl.add_user(regular_user)

    print("Ласкаво просимо до системи!")

    while True:
        username_input = input("Введіть ім'я користувача: ")
        password_input = input("Введіть пароль: ")

        authenticated_user = acl.authenticate_user(username_input, password_input)

        if authenticated_user:
            print(f"\n Аутентифікація успішна! Ви увійшли як {authenticated_user.username}.")
            if isinstance(authenticated_user, Administrator):
                print(f"  Рівень доступу: Адміністратор.")
            elif isinstance(authenticated_user, RegularUser):
                print(f"  Рівень доступу: Звичайний користувач. Останній вхід: {authenticated_user.last_login_date}")
        else:
            print("\n Помилка аутентифікації: Неправильне ім'я користувача або пароль.")