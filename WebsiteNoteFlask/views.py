#https://www.youtube.com/watch?v=dam0GPOAvVI&ab_channel=TechWithTim
from flask import Blueprint, request, render_template, flash,jsonify
from flask_login import login_required, current_user
from .models import  Note
from . import db
import json
#bluefprints allows to create routes for the app in multiple files
# instead of just putting @app.route() only in our main file
#we can use @views.route() once views blueprint is defined in views.py
#or @auth.route() once auth blueprint is defined still all blueprints are accessing same main [app=Flask(__name__)]
#these routes have to be registered in __init__.py before use
#views is just name for route & blueprint it could be anything, just for easeness we gave it same as filename

views=Blueprint('views',__name__)

@views.route('/',methods=['GET','POST'])
@login_required
def home():
    if request.method=='POST':
        note=request.form.get('note')
        if len(note)<1:
            flash("note is too short", category='error')
        else:
            new_note=Note(data=note,user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()

    return render_template('home.html', user=current_user,fname="Neha",lname="Jain",boolean=True)
    #user =current_user is passed to the base html to show expected navigation buttons only based on
    # if user is authenticated or not, as only home and logout for authenticated, and login and signup only if not authenticated yet


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

