from flask import Blueprint,render_template,request,flash,jsonify
from flask_login import login_required,current_user
from .models import Todo
from . import db
import json

views = Blueprint('views',__name__)

#route for homepage to add and show list item
@views.route('/',methods=['GET','POST'])
@login_required
def homepage():
    if request.method=="POST":
        task=request.form.get("task")
        if len(task)<1:
            flash('Invalid entry!',category='error')
        else:
            new_task=Todo(task=task,user_id=current_user.id)
            db.session.add(new_task)
            db.session.commit()
            flash("Task added successfully",category='success')
    return render_template("home.html",user=current_user)

# route for deleting a task
@views.route('/delete-task',methods=['POST'])
def delete_task():
    task=json.loads(request.data)
    taskId=task['taskId']
    task = Todo.query.get(taskId)
    if task:
        if task.user_id == current_user.id:
            db.session.delete(task)
            db.session.commit()

    return jsonify({})

