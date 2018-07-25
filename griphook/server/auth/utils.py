from griphook.server import bcrypt


def check_user_password_hash(user, password):
    return user and bcrypt.check_password_hash(user.password, password)
