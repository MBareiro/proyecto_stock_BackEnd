from app import db, ma, app

class ProductoSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre', 'cantidad', 'reserva', 'id_categoria')

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    cantidad = db.Column(db.Numeric(10, 0))  # Sin decimales 
    reserva = db.Column(db.Numeric(10, 0), nullable=True)   # Sin decimales
    id_categoria = db.Column(db.Integer)

with app.app_context():
    db.create_all()