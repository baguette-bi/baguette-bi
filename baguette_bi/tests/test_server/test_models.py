from baguette_bi.server import crypto
from baguette_bi.server.models import User


def test_user_set_password():
    user = User(username="test")
    user.set_password("testpass")
    assert user.password_hash is not None
    assert user.password_hash != "testpass"
    assert crypto.pwd_context.verify("testpass", user.password_hash)


def test_user_check_password():
    user = User(username="test")
    user.set_password("testpass")
    assert not user.check_password("incorrect")
    assert not user.check_password("")
    assert user.check_password("testpass")
