import uuid
import pytest

from app.models.user import User


def test_create_user_with_defaults():
    user = User(
        name="  Miguel Nascimento  ",
        username="  Miguel_01  ",
        password_hash="  hashed_password_123  ",
    )

    assert uuid.UUID(user.id)
    assert user.name == "Miguel Nascimento"
    assert user.username == "miguel_01"
    assert user.password_hash == "hashed_password_123"
    assert user.is_active is True


def test_create_user_with_custom_id_and_inactive():
    custom_id = str(uuid.uuid4())
    user = User(
        name="Ana Silva",
        username="AnaSilva",
        password_hash="hash_abc",
        is_active=False,
        user_id=f"  {custom_id}  ",
    )

    assert user.id == custom_id
    assert user.name == "Ana Silva"
    assert user.username == "anasilva"
    assert user.is_active is False


@pytest.mark.parametrize("invalid_id", ["", "   ", 123, None])
def test_invalid_user_id_raises_value_error(invalid_id):
    if invalid_id is None:
        pytest.skip("None gera UUID automático no _validate_id.")

    with pytest.raises(ValueError):
        User(
            name="Miguel",
            username="miguel",
            password_hash="hash_123",
            user_id=invalid_id,
        )


@pytest.mark.parametrize(
    "invalid_name",
    [
        "",
        " ",
        "A",
        "a" * 33,
        "Miguel  Silva",
        "Miguel123",
        "Miguel!",
        123,
        None,
    ],
)
def test_invalid_name_raises_value_error(invalid_name):
    with pytest.raises(ValueError):
        User(
            name=invalid_name,
            username="miguel",
            password_hash="hash_123",
        )


@pytest.mark.parametrize(
    "invalid_username",
    [
        "",
        "   ",
        "abc",
        "a" * 17,
        "miguel silva",
        "miguel-01",
        "miguel@01",
        123,
        None,
    ],
)
def test_invalid_username_raises_value_error(invalid_username):
    with pytest.raises(ValueError):
        User(
            name="Miguel",
            username=invalid_username,
            password_hash="hash_123",
        )


@pytest.mark.parametrize("invalid_hash", ["", "   ", 123, None])
def test_invalid_password_hash_raises_value_error(invalid_hash):
    with pytest.raises(ValueError):
        User(
            name="Miguel",
            username="miguel",
            password_hash=invalid_hash,
        )


@pytest.mark.parametrize("invalid_active", ["true", "false", 1, 0, None])
def test_invalid_is_active_raises_value_error(invalid_active):
    with pytest.raises(ValueError):
        User(
            name="Miguel",
            username="miguel",
            password_hash="hash_123",
            is_active=invalid_active,
        )