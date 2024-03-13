from flask import jsonify, request
from app import db, app
from models.categoria_model import Categoria, CategoriaSchema
from models.product_model import Producto
from sqlalchemy import and_

categoria_schema = CategoriaSchema()
categorias_schema = CategoriaSchema(many=True)

@app.route('/categorias', methods=['GET'])
def get_categorias():
    try:
        all_categorias = Categoria.query.all()

        # Verificar si alguna categoría tiene productos en reserva
        for categoria in all_categorias:
            productos_en_reserva = Producto.query.filter_by(id_categoria=categoria.id).filter(and_(Producto.reserva >= 0, Producto.reserva >= Producto.cantidad)).first()
            if productos_en_reserva:
                categoria.tiene_productos_en_reserva = True
            else:
                categoria.tiene_productos_en_reserva = False

        result = categorias_schema.dump(all_categorias)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/categorias/<id>', methods=['GET'])
def get_categoria(id):
    categoria = Categoria.query.get(id)
    return categoria_schema.jsonify(categoria)

@app.route('/categorias/<id>', methods=['DELETE'])
def delete_categoria(id):
    categoria = Categoria.query.get(id)
    if categoria:
        # Verificar si hay productos asociados a esta categoría
        productos_asociados = Producto.query.filter_by(id_categoria=id).first()
        if productos_asociados:
            return jsonify({'message': 'No se puede eliminar la categoría. Hay productos asociados.'}), 400

        db.session.delete(categoria)
        db.session.commit()
        return categoria_schema.jsonify(categoria)
    else:
        return jsonify({'message': 'Categoria no encontrada'}), 404

@app.route('/categorias', methods=['POST'])
def create_categoria():
    nombre = request.json['nombre']

    # Puedes realizar cualquier procesamiento adicional aquí
    new_categoria = Categoria(
        nombre=nombre
    )
    db.session.add(new_categoria)
    db.session.commit()

    return categoria_schema.jsonify(new_categoria)

@app.route('/categorias/<id>', methods=['PUT'])
def update_categoria(id):
    categoria = Categoria.query.get(id)
    if categoria is None:
        return jsonify({'message': 'Categoría no encontrada'}), 404
    categoria.nombre = request.json['nombre']
    # Puedes realizar cualquier procesamiento adicional aquí
    db.session.commit()
    return categoria_schema.jsonify(categoria)

