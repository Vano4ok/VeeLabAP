from src.app import app, auth
from src.model.user import User
from src.model.role import Role
from flask_restful import reqparse

from src.utils.exception_wrapper import handle_error_format, handle_server_exception


@app.route('/user/register', methods=['POST'])
def create_user():
    parser = reqparse.RequestParser()

    parser.add_argument('username', help='username cannot be blank', required=True)
    parser.add_argument('firstName', help='firstName cannot be blank', required=True)
    parser.add_argument('lastName', help='lastName cannot be blank', required=True)
    parser.add_argument('email', help='email cannot be blank', required=True)
    parser.add_argument('password', help='password cannot be blank', required=True)

    data = parser.parse_args()
    username = data['username']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']
    password = data['password']

    if '@' not in email:
        return handle_error_format('Please, enter valid email address.', 'Field \'email\' in the request body.'), 400

    if len(password) < 8:
        return handle_error_format('Password should consist of at least 8 symbols.',
                                   'Field \'password\' in the request body.'), 400

    if User.get_by_username(username):
        return handle_error_format('User with such username already exists.',
                                   'Field \'username\' in the request body.'), 400

    user = User(
        username=username,
        firstName=first_name,
        lastName=last_name,
        email=email,
        password=User.generate_hash(data['password'])
    )

    role = Role.get_by_name('user')
    user.roles.append(role)

    try:
        user.save_to_db()

        return {'message': 'User was successfully created'}, 200
    except:
        return {'message': 'Something went wrong'}, 500


@app.route('/user/<userId>', methods=['GET'])
def get_user_by_id(user_id: int):
    user = User.get_by_id(user_id)
    if not user:
        return handle_error_format('User with such id does not exist.',
                                   'Field \'userId\' in path parameters.'), 404
    return user.to_json()


@app.route('/user/<userId>', methods=['PUT'])
@auth.login_required
#@handle_server_exception
def update_user(user_id: int):
    parser = reqparse.RequestParser()

    parser.add_argument('username', help='username cannot be blank')
    parser.add_argument('first_name', help='fullname cannot be blank')
    parser.add_argument('last_name', help='fullname cannot be blank')

    data = parser.parse_args()
    username = data['username']
    first_name = data['first_name']
    last_name = data['last_name']

    if User.get_by_username(username):
        return handle_error_format('User with such username already exists.',
                                   'Field \'username\' in the request body.'), 400

    user = User.get_by_id(user_id)

    if not user:
        return handle_error_format('User with such id does not exist.',
                                   'Field \'userId\' in path parameters.'), 404

    user.first_name = first_name
    user.last_name = last_name
    user.save_to_db()

    return User.to_json(user)


@app.route('/user/<userId>', methods=['DELETE'])
@auth.login_required(role=['admin'])
@handle_server_exception
def delete_user_by_id(user_id: int):
    return User.delete_by_id(user_id)
