from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, login_user, logout_user
from . import db
from app.models import User, Branch
from app.forms import UserForm
from werkzeug.security import generate_password_hash, check_password_hash
from passlib.hash import sha256_crypt
from app.audit_helper import log_create, log_update, log_delete

users_bp = Blueprint('users', __name__)


@users_bp.route('/users', methods=['GET'])
@login_required
def users():
    users = User.query.all()
    return render_template('users.html', users=users)


@users_bp.route('/users/new', methods=['GET', 'POST'])
@login_required
def create_user():
    form = UserForm()
    if form.validate_on_submit():
        hashed_password = sha256_crypt.encrypt(form.password.data)
        new_user = User(
            branch_id=form.branch.data.id,
            email=form.email.data,
            password=hashed_password,
            name=form.name.data,
            role=form.role.data
        )

        db.session.add(new_user)
        db.session.commit()
        log_create(new_user)
        flash('User created successfully!')
        return redirect(url_for('users.users'))
    
    return render_template('users/create_user.html', form=form)


@users_bp.route('/users/<int:id>', methods=['GET'])
@login_required
def view_user(id):
    user = User.query.get_or_404(id)
    return render_template('users/view_user.html', user=user)


@users_bp.route('/users/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_user(id):
    user = User.query.get_or_404(id)
    user_old = user
    form = UserForm(obj=user)

    if form.validate_on_submit():
        user.branch_id = form.branch.data.id
        user.email = form.email.data
        user.name = form.name.data
        user.role = form.role.data
        
        if form.password.data:
            user.password = generate_password_hash(form.password.data, method='sha256')

        db.session.commit()
        log_update(user, user_old)
        flash('User updated successfully!')
        return redirect(url_for('users.users'))

    return render_template('users/update_user.html', form=form, user=user)


@users_bp.route('/users/delete/<int:id>', methods=['POST'])
@login_required
def delete_user(id):
    user = User.query.get_or_404(id)
    try:
        db.session.delete(user)
        db.session.commit()
        log_delete(user)
        flash('User deleted successfully!')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while deleting the user. Please try again.')

    return redirect(url_for('users.users'))

