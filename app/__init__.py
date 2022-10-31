import os
from datetime import datetime
from flasgger import Swagger
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# Database selector configuration
if os.getenv('ENVIRONMENT').upper() in ['PRODUCTION', 'PRD']:
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
else:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///sqlite.db'
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

swagger = Swagger(app)
db = SQLAlchemy(app)
db.init_app(app)


# Register user's management endpoints
from app.user.view import user_bp
app.register_blueprint(user_bp)

# Create tables in database
with app.app_context():
    db.create_all()


@app.route('/health', methods=['GET'])
def health():
    """
    Health of application
    ---
    responses:
        200:
            description: status and current time
    """
    return jsonify({'status': 'OK', 'timesec': str(datetime.now())})
