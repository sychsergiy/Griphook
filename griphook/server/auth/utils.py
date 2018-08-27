from griphook.server import db
from griphook.server.models import Admin

from .exceptions import AdminExists


def create_admin(password: str):
    if Admin.query.count() == 0:
        db.session.add(Admin(password))
        db.session.commit()
    else:
        raise AdminExists("Admin already exists")


def get_admin():
    return Admin.query.first()
