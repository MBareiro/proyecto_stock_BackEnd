from datetime import datetime
from flask import jsonify, request
from app import db, app
from models.salida_model import Salida, SalidaSchema

salida_schema = SalidaSchema()
salidas_schema = SalidaSchema(many=True)

@app.route('/salidas', methods=['GET'])
def get_salidas():
    try:
        all_salidas = Salida.query.all()
        result = salidas_schema.dump(all_salidas)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/salidas/<id>', methods=['GET'])
def get_salida(id):
    salida = Salida.query.get(id)
    return salida_schema.jsonify(salida)

@app.route('/salidas', methods=['POST'])
def create_salida():
    fecha_str = request.json['fecha']
    fecha = datetime.strptime(fecha_str, '%Y-%m-%dT%H:%M:%S.%fZ')  # Ajustar el formato de fecha
    new_salida = Salida(
        fecha=fecha,
    )

    db.session.add(new_salida)
    db.session.commit()

    return salida_schema.jsonify(new_salida)

@app.route('/salidas/<id>', methods=['PUT'])
def update_salida(id):
    salida = Salida.query.get(id)
    if salida is None:
        return jsonify({'message': 'Salida no encontrada'}), 404

    salida.fecha = request.json['fecha']

    db.session.commit()
    return salida_schema.jsonify(salida)

@app.route('/salidas/<id>', methods=['DELETE'])
def delete_salida(id):
    salida = Salida.query.get(id)
    if salida:
        db.session.delete(salida)
        db.session.commit()
        return salida_schema.jsonify(salida)
    else:
        return jsonify({'message': 'Salida no encontrada'}), 404
