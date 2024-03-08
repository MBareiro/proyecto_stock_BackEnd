from flask import jsonify, request
from app import db, app
from models.entrada_detalle_model import EntradaDetalle, EntradaDetalleSchema
from models.product_model import Producto

entrada_detalle_schema = EntradaDetalleSchema()
entradas_detalle_schema = EntradaDetalleSchema(many=True)

@app.route('/entradas_detalle', methods=['GET'])
def get_entradas_detalle():
    try:
        all_entradas_detalle = EntradaDetalle.query.all()
        result = entradas_detalle_schema.dump(all_entradas_detalle)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/entradas_detalle/<int:id>', methods=['GET'])
def get_entrada_detalle(id):
    # Obtiene todos los detalles de entrada para el ID proporcionado
    entrada_detalles = EntradaDetalle.query.filter_by(id_entrada=id).all()
    
    if not entrada_detalles:
        return jsonify({'message': 'No se encontraron detalles de entrada para el ID proporcionado'}), 404

    # Lista para almacenar los detalles de entrada con el nombre del producto
    detalles_con_nombre_producto = []

    # Itera sobre cada detalle de entrada para obtener el nombre del producto asociado
    for detalle in entrada_detalles:
        producto = Producto.query.get(detalle.id_producto)
        if producto:
            detalle_con_nombre_producto = {
                'id': detalle.id,
                'nombre_producto': producto.nombre,
                'cantidad': detalle.cantidad,
                'id_entrada': detalle.id_entrada
            }
            detalles_con_nombre_producto.append(detalle_con_nombre_producto)
        else:
            # Si no se encuentra el producto, se omite este detalle
            continue

    return jsonify(detalles_con_nombre_producto)

@app.route('/entradas_detalle/<id_entrada>', methods=['POST'])
def create_entrada_detalle(id_entrada):
    try:
        detalles_data = request.json
        
        # Guardar los detalles de la entrada
        for detalle in detalles_data:
            id_producto = detalle['id_producto']
            cantidad = detalle['cantidad']
            id_entrada = id_entrada
            
            nuevo_detalle = EntradaDetalle(
                id_producto=id_producto,
                cantidad=cantidad,
                id_entrada=id_entrada
            )
            
            db.session.add(nuevo_detalle)
        
        # Actualizar la reserva en la tabla Producto
        for detalle in detalles_data:
            id_producto = detalle['id_producto']
            cantidad = detalle['cantidad']
            
            producto = Producto.query.get(id_producto)
            if producto:
                producto.cantidad += cantidad
                db.session.commit()
            else:
                return jsonify({'message': f'Producto con ID {id_producto} no encontrado'}), 404
        
        db.session.commit()
        
        return jsonify({'message': 'Detalles de entrada creados exitosamente'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/entradas_detalle/<id>', methods=['PUT'])
def update_entrada_detalle(id):
    entrada_detalle = EntradaDetalle.query.get(id)
    if entrada_detalle is None:
        return jsonify({'message': 'Detalle de entrada no encontrado'}), 404

    entrada_detalle.id_producto = request.json['id_producto']
    entrada_detalle.cantidad = request.json['cantidad']
    entrada_detalle.id_entrada = request.json['id_entrada']

    db.session.commit()
    return entrada_detalle_schema.jsonify(entrada_detalle)

@app.route('/entradas_detalle/<id>', methods=['DELETE'])
def delete_entrada_detalle(id):
    entrada_detalle = EntradaDetalle.query.get(id)
    if entrada_detalle:
        db.session.delete(entrada_detalle)
        db.session.commit()
        return entrada_detalle_schema.jsonify(entrada_detalle)
    else:
        return jsonify({'message': 'Detalle de entrada no encontrado'}), 404
