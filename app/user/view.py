from app import app, db
from app.user.model import User
from flask import request, jsonify, Blueprint
from flask.views import MethodView

user_bp = Blueprint('user', __name__)


class UserView(MethodView):
    def get(self, user_id=None, page=1):
        """
        Get user information.
        ---
        parameters:
            - name: user_id
              in: path
              type: integer
              required: false
        responses:
            200:
                description: A list of users or an unique user information
        """
        if not user_id:
            users = User.query.paginate(page=page, per_page=10).items
            response = []

            for user in users:
                response.append({
                    'id': user.id,
                    'name': user.username,
                    'created': str(user.created),
                })
        else:
            user = User.query.filter_by(id=user_id).first()
            if not user:
                return jsonify({'error': f'User id \'{user_id}\' not found.'}), 404
            response = {
                'id': user.id,
                'username': user.username,
                'age': user.age,
                'created': str(user.created),
                'updated': str(user.updated),
            }
        return jsonify(response)

    def post(self):
        """
        Create a new user.
        ---
        parameters:
            - name: user's info
              in: body
              example: '{"username": "", "age": 0}'
              required: true
        responses:
            201:
                description: created user's info
            400:
                description: when some user's info was not received
            500:
                description: internal error
        """
        try:
            name = request.json['username']
            age = request.json['age']
            user = User(name, age)

            db.session.add(user)
            db.session.commit()

            return jsonify({
                'id': user.id,
                'username': user.username,
                'age': user.age,
                'created': str(user.created),
                'updated': str(user.updated),
            }), 201
        except KeyError as error:
            return jsonify({
                'error': f'Parameter {error} not received'
            }), 400
        except Exception as error:
            return jsonify({
                'error': f'User creation error: {error}'
            }), 500

    def put(self, user_id=None):
        """
        Update an existing user.
        ---
        parameters:
            - name: user_id
              in: path
              type: integer
              required: true
            - name: user's info
              in: body
              example: '{"username": "", "age": 0}'
              required: true
        responses:
            200:
                description: created user's info
            500:
                description: internal error
        """
        try:
            user = User.query.filter_by(id=user_id).first()
            if not user:
                return jsonify({'error': f'User id \'{user_id}\' not found.'}), 404

            user.username = request.json.get('username', user.username)
            user.age = request.json.get('age', user.age)

            db.session.add(user)
            db.session.commit()

            return jsonify({
                'id': user.id,
                'username': user.username,
                'age': user.age,
                'created': str(user.created),
                'updated': str(user.updated),
            }), 200
        except Exception as error:
            return jsonify({
                'error': f'User update error: {error}'
            }), 500

    def delete(self, user_id):
        """
        Delete an existing user.
        ---
        parameters:
            - name: user_id
              in: path
              type: integer
              required: true
        responses:
            200:
                description: message with confirmation of delete action
            500:
                description: internal error
        """
        try:
            user = User.query.filter_by(id=user_id).first()
            if not user:
                return jsonify({'error': f'User id \'{user_id}\' not found.'}), 404
            db.session.delete(user)
            db.session.commit()
            return jsonify({'msg': 'User deleted successfully'}), 200
        except Exception as error:
            return jsonify({
                'error': f'User delete error: {error}'
            }), 500


user_view = UserView.as_view('user_view')
app.add_url_rule(
    '/user', view_func=user_view, methods=['POST', 'GET']
)
app.add_url_rule(
    '/user/<int:user_id>', view_func=user_view, methods=['GET', 'PUT', 'DELETE']
)
