from flask import Flask, send_from_directory, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, current_user
import os

from extensions import db, login_manager
from models import User
from auth_routes import auth_bp

app = Flask(__name__, static_folder='public')
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

# Register blueprint
app.register_blueprint(auth_bp)

# Serve static frontend files
@app.before_request
def log_request():
    print(f"Incoming request: {request.method} {request.path}")

@app.route('/<path:subpath>name')
def serve_index(subpath):
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:filename>')
def serve_static_file(filename):
    file_path = os.path.join(app.static_folder, filename)
    if os.path.exists(file_path):
        return send_from_directory(app.static_folder, filename)
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/')
def serve_root():
    return send_from_directory(app.static_folder, 'index.html')

# Login status check route
@app.route('/whoami')
def whoami():
    if current_user.is_authenticated:
        return jsonify({'logged_in': True, 'username': current_user.username})
    return jsonify({'logged_in': False})

# Protected account route
@app.route('/account')
@login_required
def account():
    return f"<h1>Welcome, {current_user.username}</h1><p>This is your account page.</p>"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8080)
