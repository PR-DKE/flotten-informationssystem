from main import app, db
from main.models import User, Triebwagen, Personenwaggon, Zug
from main.util import get_trains


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User,'Triebwagen': Triebwagen, 'Personenwaggon': Personenwaggon, 'Zug': Zug, 'get_trains': get_trains}
