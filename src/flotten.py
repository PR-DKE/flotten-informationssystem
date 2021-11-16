from main import app, db
from main.models import User, Triebwagen, Personenwaggon

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User,'Triebwagen': Triebwagen, 'Personenwaggon': Personenwaggon}
