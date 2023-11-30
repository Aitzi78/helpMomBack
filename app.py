from flask import Flask, request, jsonify, abort
from config import ApplicationConfig
from models import db, Administrador, Pregunta, Respuesta
from flask_cors import CORS

# scrypt:32768:8:1$hFhnknx2H4qjTpy1$d0f2d7f7d9da14e3f0f84fb958afee7338d2e3e802ed5cfd5ad56fd356404a5c7983dd3d187895c090055b1055aa5756ef579cd35eda20a056a702335431dffc
# scrypt:32768:8:1$ar4t3w6X7KQsw2Ub$957af3deca15ef274b1e6693ba63248f0a48930a721adf15522b44cf4afb8816536c5b9dabeb1a85416becefa4289c6610898494386db8de76bcf2ac1bc57122

app = Flask(__name__)
app.config.from_object(ApplicationConfig)

# Solucionamos cors
cors = CORS(app)

# Iniciamos db
db.init_app(app)


### ENDPOINTS PREGUNTAS ###
@app.route("/api/preguntas")
def getAllPreguntas():
    preguntas = Pregunta.query.all()
    preguntas_json = jsonify([pregunta.serialize() for pregunta in preguntas])
    # Devolvemos una lista de objetos
    return preguntas_json


# Ruta para una pregunta concreta
@app.route("/api/preguntas/<int:id_pregunta>")
def getPregunta(id_pregunta):
    pregunta = Pregunta.get_by_id(id_pregunta)
    if pregunta is None:
        abort(404)
    return jsonify(pregunta.serialize())


# Ruta para crear una nueva pregunta
@app.route("/api/preguntas", methods=["POST"])
def createPregunta():
    # Obtenemos titulo
    titulo = request.json["titulo"]

    # Creamos nueva pregunta
    nueva_pregunta = Pregunta(titulo=titulo)
    nueva_pregunta.save()

    return jsonify(nueva_pregunta.serialize()), 201


# Ruta para actualizar una pregunta
@app.route("/api/preguntas/<int:id_pregunta>", methods=["PUT"])
def updatePregunta(id_pregunta):
    # Recuperamos datos
    titulo = request.json["titulo"]

    # Recuperamos pregunta y actualizamos
    pregunta = Pregunta.get_by_id(id_pregunta)

    if pregunta is None:
        abort(404)

    pregunta.titulo = titulo

    # Guardamos
    pregunta.save()

    # Devolvemos la pregunta actualizada en formato JSON
    return jsonify(pregunta.serialize())


# Ruta para borrar una pregunta
@app.route("/api/preguntas/<int:id_pregunta>", methods=["DELETE"])
def deletePregunta(id_pregunta):
    # Recuperamos la pregunta
    pregunta = Pregunta.get_by_id(id_pregunta)

    if pregunta is None:
        # return jsonify({"error": "pregunta invalida"}), 404
        abort(404)

    # La borramos
    pregunta.delete()

    return "", 204


### ENDPOINTS RESPUESTAS ###


# Ruta para obtener todas las respuestas
@app.route("/api/respuestas", methods=["GET"])
def getRespuestas():
    respuestas = Respuesta.query.all()

    respuestas_json = [respuesta.serialize() for respuesta in respuestas]
    return jsonify(respuestas_json)


# Ruta para obtener las respuestas a partir de la id de una pregunta
@app.route("/api/respuestas/<int:id_pregunta>", methods=["GET"])
def getRespuestasByPregunta(id_pregunta):
    respuestas = Respuesta.query.filter_by(id_pregunta=id_pregunta).all()

    respuestas_json = [respuesta.serialize() for respuesta in respuestas]

    return jsonify(respuestas_json)


# Ruta para crear una nueva respuesta a partir de la id de una pregunta
@app.route("/api/respuestas/<int:id_pregunta>", methods=["POST"])
def createRespuesta(id_pregunta):
    # Obtenemos datos de la nueva respuesta
    titulo = request.json["titulo"]
    puntuacion = request.json["puntuacion"]

    # Creamos la nueva respuesta
    nueva_respuesta = Respuesta(
        titulo=titulo, puntuacion=puntuacion, id_pregunta=id_pregunta
    )

    # La guardamos en la base de datos
    nueva_respuesta.save()

    # Devolvemos esa respuesta en formato JSON
    return jsonify(nueva_respuesta.serialize()), 201


# Ruta para actualizar una respuesta
@app.route("/api/respuestas/<int:id_respuesta>", methods=["PUT"])
def updateRespuesta(id_respuesta):
    # Recuperamos los datos de la nueva respuesta
    titulo = request.json["titulo"]
    puntuacion = request.json["puntuacion"]

    # Recuperamos la version anterior de la respuesta y la actualizamos
    respuesta = Respuesta.get_by_id(id_respuesta)

    if respuesta is None:
        abort(404)

    # Actualizamos los campos que hemos recogido
    respuesta.titulo = titulo
    respuesta.puntuacion = puntuacion

    # Guardamos en la base de datos
    respuesta.save()

    # Devolvemos la pregunta actualizada en formato JSON
    return jsonify(respuesta.serialize())


# Ruta para borrar una respuesta
@app.route("/api/respuestas/<int:id_respuesta>", methods=["DELETE"])
def deleteRespuesta(id_respuesta):
    # Recuperamos la respuesta
    respuesta = Respuesta.get_by_id(id_respuesta)

    if respuesta is None:
        abort(404)

    # Borramos la respuesta
    respuesta.delete()

    return "", 204


### ENDPOINTS ADMINISTRADOR ###
@app.route("/api/auth/login", methods=["POST"])
def login():
    username = request.json[
        "username"
    ].lower()  # Para evitar error de minúsculas y mayúsculas al comparar
    password = request.json["password"]

    admin = Administrador.query.filter_by(username=username).first()

    if admin is None:
        return jsonify({"error": "Unauthorized"}), 401

    if not admin.check_password(password):
        return jsonify({"error": "Unauthorized"}), 401

    return jsonify({"username": username, "password": password})


if __name__ == "__main__":
    app.run(debug=True)
