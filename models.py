from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Administrador(db.Model):
    __tablename__ = "administrador"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<User {self.email}>"

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return Administrador.query.get(id)

    @staticmethod
    def get_by_email(email):
        return Administrador.query.filter_by(email=email).first()


class Pregunta(db.Model):
    __tablename__ = "pregunta"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.Text, nullable=False)
    respuestas = db.relationship("Respuesta", backref="pregunta", lazy=True)

    # Para convertir a JSON la consulta
    def serialize(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
        }

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return Pregunta.query.get(id)


class Respuesta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.Text, nullable=False)
    puntuacion = db.Column(db.Integer, nullable=False)
    id_pregunta = db.Column(db.Integer, db.ForeignKey("pregunta.id"), nullable=False)

    # Para convertir a JSON la consulta
    def serialize(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "puntuacion": self.puntuacion,
            "id_pregunta": self.id_pregunta,
        }

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return Respuesta.query.get(id)
