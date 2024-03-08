from flask import jsonify, request
from app import db, app
from models.product_model import Producto
from models.salida_detalle_model import SalidaDetalle, SalidaDetalleSchema

salida_detalle_schema = SalidaDetalleSchema()
salidas_detalle_schema = SalidaDetalleSchema(many=True)

@app.route('/salidas_detalle', methods=['GET'])
def get_salidas_detalle():
    try:
        all_salidas_detalle = SalidaDetalle.query.all()
        result = salidas_detalle_schema.dump(all_salidas_detalle)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/salidas_detalle/<int:id>', methods=['GET'])
def get_salida_detalle(id):
    # Obtiene todos los detalles de salida para el ID proporcionado
    salida_detalles = SalidaDetalle.query.filter_by(id_salida=id).all()
    
    if not salida_detalles:
        return jsonify({'message': 'No se encontraron detalles de salida para el ID proporcionado'}), 404

    # Lista para almacenar los detalles de salida con el nombre del producto
    detalles_con_nombre_producto = []

    # Itera sobre cada detalle de salida para obtener el nombre del producto asociado
    for detalle in salida_detalles:
        producto = Producto.query.get(detalle.id_producto)
        if producto:
            detalle_con_nombre_producto = {
                'id': detalle.id,
                'nombre_producto': producto.nombre,
                'cantidad': detalle.cantidad,
                'id_salida': detalle.id_salida
            }
            detalles_con_nombre_producto.append(detalle_con_nombre_producto)
        else:
            # Si no se encuentra el producto, se omite este detalle
            continue

    return jsonify(detalles_con_nombre_producto)

@app.route('/salidas_detalle/<id_salida>', methods=['POST'])
def create_salida_detalle(id_salida):
    try:
        detalles_data = request.json
        
        # Guardar los detalles de la salida
        for detalle in detalles_data:
            id_producto = detalle['id_producto']
            cantidad = detalle['cantidad']
            id_salida = id_salida
            
            nuevo_detalle = SalidaDetalle(
                id_producto=id_producto,
                cantidad=cantidad,
                id_salida=id_salida
            )
            
            db.session.add(nuevo_detalle)
        
        # Actualizar la reserva en la tabla Producto
        for detalle in detalles_data:
            id_producto = detalle['id_producto']
            cantidad = detalle['cantidad']
            
            producto = Producto.query.get(id_producto)
            if producto:
                producto.cantidad -= cantidad
                db.session.commit()
            else:
                return jsonify({'message': f'Producto con ID {id_producto} no encontrado'}), 404
                
        db.session.commit()
        
        return jsonify({'message': 'Detalles de salida creados exitosamente'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/salidas_detalle/<id>', methods=['PUT'])
def update_salida_detalle(id):
    salida_detalle = SalidaDetalle.query.get(id)
    if salida_detalle is None:
        return jsonify({'message': 'Detalle de salida no encontrado'}), 404

    salida_detalle.id_producto = request.json['id_producto']
    salida_detalle.cantidad = request.json['cantidad']
    salida_detalle.id_salida = request.json['id_salida']

    db.session.commit()
    return salida_detalle_schema.jsonify(salida_detalle)

@app.route('/salidas_detalle/<id>', methods=['DELETE'])
def delete_salida_detalle(id):
    salida_detalle = SalidaDetalle.query.get(id)
    if salida_detalle:
        db.session.delete(salida_detalle)
        db.session.commit()
        return salida_detalle_schema.jsonify(salida_detalle)
    else:
        return jsonify({'message': 'Detalle de salida no encontrado'}), 404

