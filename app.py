from flask import Flask, send_from_directory, request, jsonify, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, current_user, logout_user
import os

from extensions import db, login_manager, bcrypt
from models import User, Reminder
from auth_routes import auth_bp

app = Flask(__name__, static_folder='public')
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

app.register_blueprint(auth_bp)

@app.before_request
def log_request():
    print(f"Incoming request: {request.method} {request.path}")

@app.route('/')
def serve_root():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:filename>')
def serve_static_file(filename):
    file_path = os.path.join(app.static_folder, filename)
    if os.path.exists(file_path):
        return send_from_directory(app.static_folder, filename)
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/whoami')
def whoami():
    if current_user.is_authenticated:
        return jsonify({'logged_in': True, 'username': current_user.username})
    return jsonify({'logged_in': False})

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    if request.method == 'POST':
        new_username = request.form.get('username')
        new_email = request.form.get('email')

        if new_username and new_username != current_user.username:
            if User.query.filter_by(username=new_username).first():
                flash('❌ That username is already taken.', 'error')
                return redirect(url_for('account'))
            current_user.username = new_username

        if new_email and new_email != current_user.email:
            if User.query.filter_by(email=new_email).first():
                flash('❌ That email is already in use.', 'error')
                return redirect(url_for('account'))
            current_user.email = new_email

        db.session.commit()
        flash('✅ Profile updated successfully!', 'success')
        return redirect(url_for('account'))

    return render_template(
        'account.html',
        username=current_user.username,
        email=current_user.email
    )

@app.route('/change-password', methods=['POST'])
@login_required
def change_password():
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')

    if not bcrypt.check_password_hash(current_user.password, current_password):
        flash('❌ Incorrect current password.', 'error')
        return redirect(url_for('account'))

    if new_password != confirm_password:
        flash('❌ New passwords do not match.', 'error')
        return redirect(url_for('account'))

    current_user.password = bcrypt.generate_password_hash(new_password).decode('utf-8')
    db.session.commit()
    flash('✅ Password changed successfully!', 'success')
    return redirect(url_for('account'))

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        date = request.form.get('date')
        hour = int(request.form.get('hour'))
        minute = request.form.get('minute')
        ampm = request.form.get('ampm')

        if ampm == 'PM' and hour != 12:
            hour += 12
        elif ampm == 'AM' and hour == 12:
            hour = 0
        time = f"{hour:02d}:{minute}"
        datetime_str = f"{date} {time}"

        if 'reminder_id' in request.form and request.form.get('reminder_id'):
            reminder_id = request.form.get('reminder_id')
            reminder = Reminder.query.filter_by(id=reminder_id, user_id=current_user.id).first()
            if reminder:
                reminder.title = title
                reminder.description = description
                reminder.datetime = datetime_str
                db.session.commit()
                flash('✅ Reminder updated!', 'success')
        else:
            if title:
                new_reminder = Reminder(
                    title=title,
                    description=description,
                    datetime=datetime_str,
                    user_id=current_user.id
                )
                db.session.add(new_reminder)
                db.session.commit()
                flash('✅ Reminder added!', 'success')

        return redirect(url_for('dashboard'))

    reminders = Reminder.query.filter_by(user_id=current_user.id).order_by(Reminder.datetime).all()
    print(f"Reminders found: {reminders}")
    return render_template('dashboard.html', reminders=reminders, username=current_user.username)

@app.route('/delete-reminder', methods=['POST'])
@login_required
def delete_reminder():
    reminder_id = request.form.get('reminder_id')
    reminder = Reminder.query.filter_by(id=reminder_id, user_id=current_user.id).first()
    if reminder:
        db.session.delete(reminder)
        db.session.commit()
        flash('✅ Reminder deleted.', 'success')
    else:
        flash('❌ Reminder not found or unauthorized.', 'error')
    return redirect(url_for('dashboard'))

@app.route('/api/reminders')
@login_required
def api_reminders():
    reminders = Reminder.query.filter_by(user_id=current_user.id).all()
    events = []
    for r in reminders:
        if r.datetime:
            try:
                date, time = r.datetime.split(' ')
                events.append({
                    'title': r.title,
                    'start': f"{date}T{time}",
                    'description': r.description
                })
            except ValueError:
                continue  # Skip malformed datetime
    return jsonify(events)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8080)
