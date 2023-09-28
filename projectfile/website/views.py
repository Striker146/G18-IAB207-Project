from flask import Blueprint,render_template

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/event_creation')
def event_creation():
    return render_template('event_creation.html')

@bp.route('/my_events')
def my_events():
    return render_template('my_events.html')

#@bp.route('/login')
#def login():
#    return render_template('login.html')