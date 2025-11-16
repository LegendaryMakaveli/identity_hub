class User:
    def __init__(self, username, encrypted_password, role="user", email=None, verified=False, failed_attempts=0, session_token=None):
        self.username = username
        self.encrypted_password = encrypted_password
        self.role = role
        self.email = email
        self.verified = verified
        self.failed_attempts = failed_attempts
        self.session_token = session_token

    @staticmethod
    def from_dict(data: dict):
        return User(
            username=data.get("username"),
            encrypted_password=data.get("encrypted_password"),
            role=data.get("role", "user"),
            email=data.get("email"),
            verified=data.get("verified", False),
            failed_attempts=data.get("failed_attempts", 0),
            session_token=data.get("session_token")
        )
