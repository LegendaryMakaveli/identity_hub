from models.user import User
from utils.encryptor import Encryptor
from utils.token_generator import TokenGenerator
from service.email_service import EmailService
from service.storage_service import StorageService


class AuthService:
    def __init__(self):
        self.storage = StorageService()
        self.encryptor = Encryptor()
        self.emailer = EmailService()

    def register(self):
        print("\nREGISTER USER")
        username = input("Username: ").strip()

        if username in self.storage.users:
            print("Username already exists.")
            return

        email = input("Email: ").strip()
        pw = input("Password: ")
        conf = input("Confirm Password: ")

        if pw != conf:
            print("Passwords do not match.")
            return

        encrypted = self.encryptor.encrypt(pw)

        user = User(username, encrypted, "user", email)
        self.storage.users[username] = user
        self.storage.save()

        code = TokenGenerator.generate()[:6]
        user.verification_code = code
        self.storage.save()   # ← FIXED

        self.emailer.send(email, "Verify Account", f"Your code is {code}")
        print("Verification email sent.")

        return

    def verify_email(self):
        username = input("Username: ").strip()

        if username not in self.storage.users:
            print("User not found.")
            return

        code = input("Enter verification code: ").strip()
        user = self.storage.users[username]

        if hasattr(user, "verification_code") and user.verification_code == code:
            user.verified = True
            del user.verification_code
            self.storage.save()
            print("Email verified.")
        else:
            print("Invalid code.")

    def login(self):
        username = input("Username: ").strip()
        pw = input("Password: ")

        if username not in self.storage.users:
            print("Invalid username.")
            return

        user = self.storage.users[username]

        if user.failed_attempts >= 3:
            print("Account locked.")
            return

        if not self.encryptor.verify(user.encrypted_password, pw):
            user.failed_attempts += 1
            self.storage.save()
            print("Wrong password.")
            return

        user.failed_attempts = 0
        user.session_token = TokenGenerator.generate()
        self.storage.save()

        print("Login successful. Token =", user.session_token)

    def reset_password(self):
        username = input("Username: ").strip()

        if username not in self.storage.users:
            print("User not found.")
            return

        user = self.storage.users[username]
        reset_code = TokenGenerator.generate()[:6]
        user.reset_code = reset_code
        self.storage.save()

        self.emailer.send(user.email, "Reset Password", f"Your code: {reset_code}")
        print("Reset code sent.")

        entered = input("Enter reset code: ")

        if entered != reset_code:
            print("Invalid code.")
            return

        new_pw = input("New password: ")
        user.encrypted_password = self.encryptor.encrypt(new_pw)
        del user.reset_code
        self.storage.save()

        print("Password reset successfully.")

    def admin_panel(self):
        username = input("Admin username: ")
        token = input("Session token: ")

        if username not in self.storage.users:
            print("Invalid user.")
            return

        user = self.storage.users[username]

        if user.role != "admin":
            print("Not an admin.")
            return

        if user.session_token != token:
            print("Invalid token.")
            return

        print("\nADMIN PANEL")
        print("1. View all users")
        print("2. Delete user")
        choice = input("Choose: ")

        if choice == "1":
            for u in self.storage.users:
                print("-", u)

        elif choice == "2":
            target = input("User to delete: ")
            if target in self.storage.users:
                del self.storage.users[target]
                self.storage.save()
                print("User deleted.")

    def run(self):
        while True:
            print("\n=== AUTH SYSTEM ===")
            print("1. Register")
            print("2. Verify Email")
            print("3. Login")
            print("4. Reset Password")
            print("5. Admin Panel")
            print("6. Exit")

            ch = input("Choose: ")

            if ch == "1":
                self.register()
            elif ch == "2":
                self.verify_email()
            elif ch == "3":
                self.login()
            elif ch == "4":
                self.reset_password()
            elif ch == "5":
                self.admin_panel()
            elif ch == "6":
                break
            else:
                print("Invalid option.")
