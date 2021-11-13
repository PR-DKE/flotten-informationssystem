from main import app, db
from main.models import User, Triebwagen, Personenwaggon, Role

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Role': Role, 'Triebwagen': Triebwagen, 'Personenwaggon': Personenwaggon}
