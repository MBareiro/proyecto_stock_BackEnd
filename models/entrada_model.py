from app import db, ma, app

class Entrada(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, nullable=False)

class EntradaSchema(ma.Schema):
    class Meta:
        fields = ('id', 'fecha')

with app.app_context():
    db.create_all()