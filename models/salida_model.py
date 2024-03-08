from app import db, ma, app

class Salida(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, nullable=False)

class SalidaSchema(ma.Schema):
    class Meta:
        fields = ('id', 'fecha')

with app.app_context():
    db.create_all()
