from flask import Blueprint, render_template,request,flash,jsonify
from flask_login import  login_required, current_user
from .models import Note, Parking_spot
from .import db
import json
#we are going to define this file is a blueprint of our app 

views = Blueprint('views',__name__)






@views.route('/', methods = ['GET','POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        new_note = Note(data =note, user_id = current_user.id)
        db.session.add(new_note)
        db.session.commit()
        flash('Note added!', category = 'success' )  
    return render_template("home.html", user = current_user)

@views.route('/spot', methods = ['GET','POST'])
@login_required
def spot():
    # admin entry
    if request.method == 'POST':
        spot_number = request.form.get('spot_number')
        location = request.form.get('location')
        spot_exist = Parking_spot.query.filter_by(spot_number = spot_number).first()
        if spot_exist:
            flash('Spot number already exists!', category = 'error')
        else:
            new_spot = Parking_spot(spot_number =spot_number, location=location, is_available = True, user_id=current_user.id)
            db.session.add(new_spot)
            db.session.commit()
            flash('Spot added!', category = 'success' )
    
          
    return render_template("spot.html", user = current_user)


@views.route('/delete-note', methods = ['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note  = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})

@views.route('/update-spot', methods = ['POST'])
def update_spot():
    spot = json.loads(request.data)

    spotId = spot['spotId']
    spot  = Parking_spot.query.get(spotId)
    if spot:
        if spot.user_id == current_user.id:
            db.session.delete(spot)
            db.session.commit()
            flash(f'{spot.spot_number} Spot Booked by {current_user.first_name}', category = 'success' )
    return jsonify({})

