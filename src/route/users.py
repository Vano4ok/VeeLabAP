from src.main import app
from src.model.user import User
from flask_restful import reqparse


@app.route('/users', methods=['POST'])
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

    user = User(
        username=username,
        firstName=first_name,
        lastName=last_name,
        email=email,
        password=User.generate_hash(data['password'])
    )

    try:
        user.save_to_db()

        return {'message': 'User was successfully created'}, 200
    except:
        return {'message': 'Something went wrong'}, 500
