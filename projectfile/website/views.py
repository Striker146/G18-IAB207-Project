from flask import Blueprint,render_template, request, redirect, url_for
from . import db
from .models import Event, GameSystem

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    # Fetch the value of 'game_system_id' from the URL's query parameters.
    game_system_id = request.args.get('game_system_id')
    
    # Check if a game_system_id exists (i.e., a specific game system was selected by the user).
    if game_system_id:
    # If a specific game system is chosen, fetch all the events that match that game_system_id.
        events = db.session.scalars(db.select(Event).where(Event.game_system_id == game_system_id)).all()
    else:
    # If no specific game system is chosen (i.e., "All" option was selected or no filter is applied),
    # fetch all the events regardless of their game_system_id.
        events = db.session.scalars(db.select(Event)).fetchmany(4)
    # Fetch a list of all the available game systems for populating the dropdown.
    game_systems = db.session.scalars(db.select(GameSystem)).all()

    # Render the 'index.html' template with the list of events, list of game systems,
    # and the current selected game system (if any).
    return render_template('index.html', events=events, game_systems=game_systems, current_game_system=game_system_id)

#@bp.route('/event_creation')
#def event_creation():
#    return render_template('event_creation.html')

@bp.route('/search')
def search():
    if request.args['search'] and request.args['search'] != "":
        print(request.args['search'])
        query = "%" + request.args['search'] + "%"
        events = db.session.scalars(db.select(Event).where(Event.description.like(query)))
        return render_template('index.html', events= events)
    else:
        return redirect(url_for('events.list'))


