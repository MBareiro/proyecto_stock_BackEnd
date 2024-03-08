from app import db, ma,app


class EntradaDetalle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_producto = db.Column(db.Integer, nullable=False)
    cantidad = db.Column(db.Numeric(10, 3), nullable=False)
    id_entrada = db.Column(db.Integer, nullable=False)

class EntradaDetalleSchema(ma.Schema):
    class Meta:
        fields = ('id', 'id_producto', 'cantidad', 'id_entrada', 'nombre_producto')

with app.app_context():
    db.create_all()