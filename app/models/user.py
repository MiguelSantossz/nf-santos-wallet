import re
import uuid

class User:
    def __init__(self,
                 name: str,
                 username: str,
                 password_hash: str,
                 is_active: bool = True,
                 user_id: str | None = None):
        self.id = self._validate_id(user_id)
        self.name = self._validate_name(name)
        self.username = self._validate_username(username)
        self.password_hash = self._validate_password_hash(password_hash)

        if not isinstance(is_active, bool):
            raise ValueError("is_active must be a boolean.")
        self.is_active = is_active

    def _validate_id(self, user_id: str | None) -> str:
        if user_id is None:
            return str(uuid.uuid4())
        if not isinstance(user_id, str) or not user_id.strip():
            raise ValueError("User id must be a non-empty string.")
        return user_id.strip()
    
    def _validate_name(self,name:str) -> str:
        if not isinstance(name,str):
            raise ValueError("Name must be a string.")

        cleaned_name = name.strip()
        if not (2 <= len(cleaned_name) <= 32):
            raise ValueError("Name must be between 2 and 32 characters.")

        if not re.fullmatch(r"[^\W\d_]+(?: [^\W\d_]+)*", cleaned_name, flags=re.UNICODE): 
            raise ValueError("Name must contain only letters and single spaces.")

        return cleaned_name

    def _validate_username(self, username: str) -> str:
        if not isinstance(username, str):
            raise ValueError("Username must be a string.")

        cleaned_username = username.strip()
        if not (4 <= len(cleaned_username) <= 16):
            raise ValueError("Username must be between 4 and 16 characters.")

        # Aceita apenas letras (com acentos), números e underline (_)
        if not re.fullmatch(r"\w+", cleaned_username, flags=re.UNICODE):
            raise ValueError("Username must contain only letters, numbers, and underscores.")

        return cleaned_username.lower()

    def _validate_password_hash(self, password_hash: str) -> str:
        if not isinstance(password_hash, str) or not password_hash.strip():
            raise ValueError("Password hash must be a non-empty string.")
        return password_hash.strip()
    
 

   