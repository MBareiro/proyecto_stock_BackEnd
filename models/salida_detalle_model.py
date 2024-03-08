from app import db, ma, app

class SalidaDetalle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_producto = db.Column(db.Integer, nullable=False)
    cantidad = db.Column(db.Numeric(10, 3), nullable=False)
    id_salida = db.Column(db.Integer, nullable=False)

    def __init__(self, id_producto, cantidad, id_salida):
        self.id_producto = id_producto
        self.cantidad = cantidad
        self.id_salida = id_salida

class SalidaDetalleSchema(ma.Schema):
    class Meta:
        fields = ('id', 'id_producto', 'cantidad', 'id_salida')

salida_detalle_schema = SalidaDetalleSchema()
salidas_detalle_schema = SalidaDetalleSchema(many=True)

with app.app_context():
    db.create_all()
