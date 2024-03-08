from datetime import datetime
from flask import jsonify, request
from app import db, app
from models.entrada_model import Entrada, EntradaSchema
entrada_schema = EntradaSchema()
entradas_schema = EntradaSchema(many=True)

@app.route('/entradas', methods=['GET'])
def get_entrada():
    try:
        all_entrada = Entrada.query.all()
        result = entrada_schema.dump(all_entrada)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/entradas/<id>', methods=['GET'])
def get_entradas(id):
    entrada = Entrada.query.get(id)
    return entrada_schema.jsonify(entrada)

@app.route('/entradas', methods=['POST'])
def create_entrada():
    fecha_str = request.json['fecha']
    fecha = datetime.strptime(fecha_str, '%Y-%m-%dT%H:%M:%S.%fZ')  # Ajustar el formato de fecha
    new_entrada = Entrada(
        fecha=fecha,
    )

    db.session.add(new_entrada)
    db.session.commit()

    return entrada_schema.jsonify(new_entrada)

@app.route('/entradas/<id>', methods=['PUT'])
def update_entrada(id):
    entrada = Entrada.query.get(id)
    if entrada is None:
        return jsonify({'message': 'Entrada no encontrada'}), 404

    entrada.fecha = request.json['fecha']

    db.session.commit()
    return entrada_schema.jsonify(entrada)

@app.route('/entradas/<id>', methods=['DELETE'])
def delete_entrada(id):
    entrada = Entrada.query.get(id)
    if entrada:
        db.session.delete(entrada)
        db.session.commit()
        return entrada_schema.jsonify(entrada)
    else:
        return jsonify({'message': 'Entrada no encontrada'}), 404
