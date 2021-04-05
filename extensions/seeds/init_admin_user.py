from werkzeug.security import generate_password_hash


def run(db):
    from api.user.model import User
    data = dict(
        username='admin',
        password=generate_password_hash('12345678'),
    )
    admin_user = User(**data)
    db.session.add(admin_user)
    db.session.commit()
