import os
import json
from models.user import User


class StorageService:
    DATA_FILE = "users.json"

    def __init__(self):
        self.users = {}
        self.load()

    def save(self):
        data = {
            username: user.__dict__
            for username, user in self.users.items()
        }
        with open(self.DATA_FILE, "w") as file:
            json.dump(data, file, indent=4)

    def load(self):
        if not os.path.exists(self.DATA_FILE):
            return

        with open(self.DATA_FILE, "r") as f:
            data = json.load(f)

        for username, user_data in data.items():
            user = User.from_dict(user_data)
            self.users[username] = user
