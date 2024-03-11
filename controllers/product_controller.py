from flask import jsonify, request
from app import db, app
from models.product_model import Producto, ProductoSchema

producto_schema = ProductoSchema()
productos_schema = ProductoSchema(many=True)

@app.route('/productos', methods=['GET'])
def get_productos():
    try:
        all_productos = Producto.query.all()
        result = productos_schema.dump(all_productos)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/producto/<id>', methods=['GET'])
def get_producto(id):
    producto = Producto.query.get(id)
    return producto_schema.jsonify(producto)

@app.route('/productos', methods=['POST'])
def create_producto():
    nombre = request.json.get('nombre')  # Obtener el nombre del producto, si no existe, devolverá None
    if nombre is None:  # Verificar si se proporcionó el nombre
        return jsonify({'message': 'El nombre del producto es obligatorio'}), 400

    cantidad = request.json.get('cantidad')
    reserva = request.json.get('reserva')
    id_categoria = request.json.get('id_categoria')

    # Crear un nuevo producto solo con el nombre proporcionado
    new_producto = Producto(nombre=nombre)

    # Agregar los otros campos si se proporcionan en la solicitud
    if cantidad is not None:
        new_producto.cantidad = cantidad
    else:
        new_producto.cantidad = 0
    if reserva is not None:
        new_producto.reserva = reserva
    else:
        new_producto.reserva = 0
    if id_categoria is not None:
        new_producto.id_categoria = id_categoria
    else:
        new_producto.id_categoria = 0


    # Agregar el nuevo producto a la sesión y confirmar los cambios en la base de datos
    db.session.add(new_producto)
    db.session.commit()

    return producto_schema.jsonify(new_producto)


@app.route('/productos/<id>', methods=['PUT'])
def update_producto(id):
    producto = Producto.query.get(id)
    if producto is None:
        return jsonify({'message': 'Producto no encontrado'}), 404

    producto.nombre = request.json['nombre']
    producto.cantidad = request.json['cantidad']
    producto.reserva = request.json['reserva']
    producto.id_categoria = request.json['id_categoria']

    db.session.commit()
    return producto_schema.jsonify(producto)

@app.route('/productos/<id>', methods=['DELETE'])
def delete_producto(id):
    producto = Producto.query.get(id)
    if producto:
        db.session.delete(producto)
        db.session.commit()
        return producto_schema.jsonify(producto)
    else:
        return jsonify({'message': 'Producto no encontrado'}), 404

# Función para obtener productos por categoría
@app.route('/productos_por_categoria/<id_categoria>', methods=['GET'])
def get_products_by_category(id_categoria):
    try:
        productos = Producto.query.filter_by(id_categoria=id_categoria).all()
        result = productos_schema.dump(productos)
        print(result)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
