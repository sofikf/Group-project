from flask import Flask, send_from_directory, request, jsonify, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, current_user, logout_user
import os

from extensions import db, login_manager, bcrypt
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

# Login status check
@app.route('/whoami')
def whoami():
    if current_user.is_authenticated:
        return jsonify({'logged_in': True, 'username': current_user.username})
    return jsonify({'logged_in': False})

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

# Account page route
@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    if request.method == 'POST':
        new_username = request.form.get('username')
        new_email = request.form.get('email')

        if new_username:
            current_user.username = new_username
        if new_email:
            current_user.email = new_email

        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('account'))

    return render_template(
        'account.html',
        username=current_user.username,
        email=current_user.email
    )

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8080)
