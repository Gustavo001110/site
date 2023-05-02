from sitesitesite import app, database
from sitesitesite.models import Usuario, Post




with app.app_context():
    Usuario.query.all()
    meus_usuario = Usuario.query.filter_by(email='gustavo.dias.oli@gmail.com').first()
    print(meus_usuario.cursos)



