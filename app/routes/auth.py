from flask import Blueprint, render_template, request, redirect, url_for, flash, session

auth_bp = Blueprint('auth', __name__)

# Dummy user credentials (in real apps, use a database and hashed passwords)
USER_CREDENTIALS = {
    'username': 'admin',
    'password': '1234'
}

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        if username == USER_CREDENTIALS['username'] and password == USER_CREDENTIALS['password']:
            session['user'] = username
            flash('Login successful', 'success')
            # Redirect to a home/dashboard page after login
            return redirect(url_for('tasks.view_task'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logout successful', 'success')
    # Redirect to login page after logout
    return redirect(url_for('auth.login'))
