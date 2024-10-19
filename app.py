from flask import Flask,request,jsonify, abort
from config import Config
from estudiante import db, Estudiante

app = Flask(__name__)

#carga configuracion desde archivo config
app.config.from_object(Config)

#inicializa la base de datos
db.init_app(app)

#crea la tabla si no existe
with app.app_context():
    db.create_all()

#crea un nuevo estudiante
@app.route('/estudiante', methods=['POST'])
def crear_estudiante():
    body = request.get_json()

    if not body or 'nombre' not in body or 'apellido' not in body or 'edad' not in body:
        abort(404, 'not found')

    nuevo_estudiante = Estudiante(
        nombre = body['nombre'],
        apellido = body['apellido'],
        edad = body['edad']
    )
    
    db.session.add(nuevo_estudiante)
    db.session.commit()
    
    return jsonify(nuevo_estudiante.to_dict()), 201

#lista de estudiantes
@app.route('/estudiante', methods=['GET'])
def obtener_estudiantes():
    estudiantes = Estudiante.query.all()
    resultado = [estudiante.to_dict() for estudiante in estudiantes]
    return jsonify(resultado), 200

#busca un estudiante
@app.route('/estudiante/<int:id_estudiante>', methods = ['GET'])
def obtener_estudiante(id_estudiante):
    estudiante = Estudiante.query.get(id_estudiante)

    if not estudiante:
        abort(404, "Estudiante no encontrado")
    return jsonify(estudiante.to_dict()), 200

#elimina un estudiante
@app.route('/estudiante/<int:id_estudiante>', methods=['DELETE'])
def eliminar_estudiante(id_estudiante):
    estudiante = Estudiante.query.get(id_estudiante)

    if not estudiante:
        abort(404, "Estudiante no encontrado")

    db.session.delete(estudiante)    
    db.session.commit()

    return '', 204

#actualiza un estudiante
@app.route('/estudiante/<int:id_estudiante>', methods = ['PUT'])
def actualizar_estudiante(id_estudiante):
    estudiante = Estudiante.query.get(id_estudiante)
    if not estudiante:
        abort(404, 'Estudiante no encontrado')

    body = request.json

    if not body: 
        abort(400, 'Solicitud invalida')

    if 'nombre' in body:
        estudiante.nombre = body['nombre']
    if 'apellido' in body:
        estudiante.apellido = body['apellido']
    if 'edad' in body:
        estudiante.edad = body['edad']
    
    db.session.commit()

    return jsonify(estudiante.to_dict()), 200


if __name__ == '__main__':
    app.run(debug=True)
