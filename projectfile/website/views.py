from flask import Blueprint,render_template, request, redirect, url_for
from . import db
from .models import Event, GameSystem
from .forms import SearchForm

bp = Blueprint('main', __name__)


@bp.route('/', methods=['GET', 'POST'])
def index():
    game_system_id = 0
    Event.compare_dates()
    search_form = SearchForm()
    search_form.set_select_fields()
    events_query = db.session.query(Event)
    # Fetch the 4 events
    events = db.session.scalars(db.select(Event)).fetchmany(4)

    # If the form is submitted
    if request.method == 'POST':
        game_system_id = search_form.game_system.data
    

    print(type(game_system_id))
    if not game_system_id == '0':
            print("Searching Game System")
            print(game_system_id) 
            events_query = events_query.filter_by(game_system_id=game_system_id)
            events = events_query.all()
            events = events[:4]
    
    if request.method == "GET":
        events = db.session.scalars(db.select(Event)).fetchmany(4)
            
    # Render the 'index.html' template with the list of events
    return render_template('index.html', events=events,search_form=search_form)

#@bp.route('/event_creation')
#def event_creation():
#    return render_template('event_creation.html')

@bp.route('/search')
def search():
    if request.args['search'] and request.args['search'] != "":
        print(request.args['search'])
        search = request.args['search']

        return redirect(url_for('events.list', search=search))
    else:
        return redirect(url_for('events.list'))


