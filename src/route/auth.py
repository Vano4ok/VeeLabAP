from src.app import auth
from src.model.user import User


@auth.verify_password
def verify_password(username, password):
    user = User.get_by_username_or_id(username)

    if user and User.verify_hash(password, user.password):
        return username


@auth.get_user_roles
def get_user_roles(user):
    user_entity = User.get_by_username(user)
    return [role.name for role in user_entity.roles]
