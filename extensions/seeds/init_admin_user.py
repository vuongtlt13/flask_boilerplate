from werkzeug.security import generate_password_hash


def run(db):
    from api.user.model import User
    from api.user.user_type import UserType
    data = dict(
        email='admin@gmail.com',
        password=generate_password_hash('12345678'),
        is_active=1,
        user_type=UserType.ADMIN,
        name="ADMIN"
    )
    admin_user = User(**data)
    db.session.add(admin_user)
    db.session.commit()
