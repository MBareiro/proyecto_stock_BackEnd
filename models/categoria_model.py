from app import db, ma, app

class CategoriaSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre','tiene_productos_en_reserva')

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

with app.app_context():
    db.create_all()
