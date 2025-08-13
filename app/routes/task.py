from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import Task

task_bp = Blueprint('tasks', __name__)

def login_required():
    if 'user' not in session:
        return False
    return True

@task_bp.route('/')
def view_task():
    if not login_required():
        return redirect(url_for('auth.login'))

    tasks = Task.query.all()
    return render_template('task.html', tasks=tasks)

@task_bp.route('/add', methods=['POST'])
def add_task():
    if not login_required():
        return redirect(url_for('auth.login'))

    title = request.form.get('title')
    if title:
        new_task = Task(title=title, status='pending')
        db.session.add(new_task)
        db.session.commit()
        flash('Task added successfully', 'success')
    else:
        flash('Task title cannot be empty', 'warning')

    return redirect(url_for('tasks.view_task'))

@task_bp.route('/toggle/<int:task_id>', methods=['POST'])
def toggle_status(task_id):
    if not login_required():
        return redirect(url_for('auth.login'))

    task = Task.query.get(task_id)
    if task:
        # Cycle status from pending -> working -> done -> pending (for example)
        if task.status == 'pending':
            task.status = 'working'
        elif task.status == 'working':
            task.status = 'done'
        else:
            task.status = 'pending'
        db.session.commit()
    else:
        flash('Task not found', 'danger')

    return redirect(url_for('tasks.view_task'))

@task_bp.route('/clear', methods=['POST'])
def clear_task():
    if not login_required():
        return redirect(url_for('auth.login'))

    Task.query.delete()
    db.session.commit()
    flash('All tasks cleared successfully', 'success')

    return redirect(url_for('tasks.view_task'))
