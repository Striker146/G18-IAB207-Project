from flask import Blueprint,render_template, request, redirect, url_for
from . import db
from .models import Event

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    events = db.session.scalars(db.select(Event)).all()
    return render_template('index.html', events = events)

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
        return redirect(url_for('main.index'))

@bp.route('/my_events')
def my_events():
    return render_template('my_events.html')

