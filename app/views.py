from flask import render_template, url_for, flash, redirect, request
from app import app, db
from app.forms import LoginForm, UpdateAccountForm, PermissionForm
from app.models import User, Permission
from flask_login import login_user, current_user, logout_user, login_required
from app.utils.azure_api import fetch_permissions_for_user
from app.utils.data_processor import process_permissions_data

@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html', title='Home')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)

@app.route("/permissions", methods=['GET', 'POST'])
@login_required
def permissions():
    form = PermissionForm()
    if form.validate_on_submit():
        permissions_data = fetch_permissions_for_user(current_user.username)
        processed_data = process_permissions_data(permissions_data)
        permission = Permission(service_name=processed_data['service_name'], access_level=processed_data['access_level'], user_id=current_user.id)
        db.session.add(permission)
        db.session.commit()
        flash('Permissions updated successfully!', 'success')
        return redirect(url_for('permissions_report'))
    return render_template('permissions.html', title='Manage Permissions', form=form)

@app.route("/permissions_report")
@login_required
def permissions_report():
    user_permissions = Permission.query.filter_by(user_id=current_user.id).all()
    return render_template('report.html', permissions=user_permissions, title='Permissions Report')

if __name__ == '__main__':
    app.run(debug=True)
