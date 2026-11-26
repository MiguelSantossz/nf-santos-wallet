import pytest
from app.models.user import User
from app.services.user_manager import UserManager


@pytest.fixture
def manager() -> UserManager:
    return UserManager()


def test_add_user_stores_and_retrieves_user(manager: UserManager) -> None:
    user = User(
        name="  Miguel Nascimento  ",
        username="  Miguel_01  ",
        password_hash="  hashed_password_123  ",
    )

    manager.add_user(user)

    assert manager.get_by_id(user.id) == user
    assert manager.get_by_username("Miguel_01") == user


@pytest.mark.parametrize(
    "raw_id",
    [
        "migs123456",
        "migs123456 ",
        " migs123456",
        "    migs123456   ",
    ],
)
def test_get_by_id_normalizes_whitespace(manager: UserManager, raw_id: str) -> None:
    user = User(
        name="Nycollas",
        username="Nycksw",
        password_hash="hashed_pass_word",
        user_id="migs123456",
    )
    manager.add_user(user)

    assert manager.get_by_id(raw_id) == user


@pytest.mark.parametrize(
    "raw_username",
    [
        "Nick40",
        "Nick40 ",
        "   NICK40   ",
        " nick40  ",
    ],
)
def test_get_by_username_normalizes_case_and_whitespace(
    manager: UserManager, raw_username: str
) -> None:
    user = User(
        name="Nicole",
        username="Nick40",
        password_hash="Nick2801",
    )
    manager.add_user(user)

    assert manager.get_by_username(raw_username) == user


def test_create_user_assigns_id_and_registers_user(manager: UserManager) -> None:
    user = manager.create_user(
        name="Nicole",
        username="nick4012",
        password_hash="nick28101",
        user_id="custom_id_01",
    )

    assert user.id == "custom_id_01"
    assert manager.get_by_id("custom_id_01") == user
    assert manager.get_by_username("nick4012") == user


def test_get_nonexistent_user_returns_none(manager: UserManager) -> None:
    assert manager.get_by_id("id_inexistente") is None
    assert manager.get_by_username("usuario_inexistente") is None