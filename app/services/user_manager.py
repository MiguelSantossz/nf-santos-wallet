from app.models.user import User

class UserManager:
    def __init__(self) -> None:
        self._users_by_id: dict[str,User] = {}

    def add_user(self,user: User) -> None:
        if not isinstance(user,User):
            raise ValueError("Expected a User instance.")
        
        if user.id in self._users_by_id:
            raise ValueError(f"User with id '{user.id}' already exists.")

        if self.get_by_username(user.username) is not None:
            raise ValueError("Username is already taken.")

        self._users_by_id[user.id] = user

    def get_by_id(self,user_id: str) -> User | None:
        if not isinstance(user_id,str) or not user_id.strip():
            return None
        return self._users_by_id.get(user_id.strip())

    def get_by_username(self,username: str) -> User | None:
        if not isinstance(username,str) or not username.strip():
            return None
        normalized = username.strip().lower()
        for user in self._users_by_id.values():
            if user.username == normalized:
                return user
        return None

    def list_users(self) -> list[User]:
        return list(self._users_by_id.values())

    def create_user(self,
                    name: str,
                    username: str,
                    password_hash: str,
                    user_id: str | None = None,
                    is_active: bool = True) -> User:
        
        if isinstance(username, str) and username.strip():
            if self.get_by_username(username.strip().lower()) is not None:
                raise ValueError(f"Username '{username.strip().lower()}' is already taken.")

        if isinstance(user_id, str) and user_id.strip():
            if self.get_by_id(user_id.strip()) is not None:
                raise ValueError(f"User with id '{user_id.strip()}' already exists.")

        user = User(
            name=name,
            username=username,
            password_hash=password_hash,
            user_id=user_id,
            is_active=is_active,
        )
        self.add_user(user)
        return user