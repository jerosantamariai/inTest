from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Roles (db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    rolename = db.Column(db.String(50), unique=True, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "rolename": self.rolename
        }

class Usuarios (db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(100), nullable=False)
    nombre = db.Column(db.String(100), nullable=True)
    apellido = db.Column(db.String(100), nullable=True)
    course = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), nullable=False)
    avatar = db.Column(db.String(100), nullable=True, default='defaultavatar.jpg')
    createdate = db.Column(db.DateTime, default=datetime.now())
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    role = db.relationship(Roles)
    
    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "course": self.course,
            "email": self.email,
            "avatar": self.avatar,
            "phone": self.phone,
            "createdate": self.createdate,
            "role": self.role.serialize(),
        }

class Pruebas (db.Model):
    __tablename__ = 'pruebas'
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.String(150), nullable=False)
    preguntass = db.relationship('Preguntas', backref='tests', lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "tipo": self.tipo,
            "descripcion": self.descripcion,
            "preguntass": self.preguntass.serialize()
        }

class Preguntas (db.Model):
    __tablename__ = 'preguntas'
    id = db.Column(db.Integer, primary_key=True)
    enunciado = db.Column(db.String(100), nullable=False)
    prueba_id = db.Column(db.Integer, db.ForeignKey('pruebas.id'))
    alternativass = db.relationship('Alternativas', backref='duda', lazy=True)

    def serialize(self):
        return {
                "id": self.id,
                "enunciado": self.enunciado,
                "alternativass": self.alternativass.serialize(),
            }

class Alternativas (db.Model):
    __tablename__ = 'alternativas'
    id = db.Column(db.Integer, primary_key=True)
    correcta = db.Column(db.String(100), nullable=False)
    pregunta_id = db.Column(db.Integer, db.ForeignKey('preguntas.id'))
    distracciones = db.relationship('Distraccion', backref='incorrectas', lazy=True)

    def serialize(self):
        return {
                "id": self.id,
                "correcta": self.correcta,
                "distracciones": self.distracciones.serialize(),
            }

class Distraccion (db.Model):
    __tablename__ = 'distraccion'
    id = db.Column(db.Integer, primary_key=True)
    incorrecta = db.Column(db.String(100), nullable=False)
    alternativa_id = db.Column(db.Integer, db.ForeignKey('alternativas.id'))

    def serialize(self):
        return {
                "id": self.id,
                "incorrecta": self.incorrecta,
            }

# -----------------------



# class Pruebas (db.Model):
#     __tablename__ = 'pruebas'
#     id = db.Column(db.Integer, primary_key=True)
#     tipo = db.Column(db.String(50), nullable=False)
#     descripcion = db.Column(db.String(150), nullable=False)

#     def serialize(self):
#         return {
#             "id": self.id,
#             "tipo": self.tipo,
#             "descripcion": self.descripcion,
#         }

# class Preguntas (db.Model):
#     __tablename__ = 'preguntas'
#     id = db.Column(db.Integer, primary_key=True)
#     enunciado = db.Column(db.String(100), nullable=False)
#     prueba_id = db.Column(db.Integer, db.ForeignKey('pruebas.id'), nullable=False)
#     prueba = db.relationship(Pruebas)

#     def serialize(self):
#         return {
#                 "id": self.id,
#                 "enunciado": self.enunciado,
#                 "prueba": self.prueba.serialize(),
#             }

# class Alternativas (db.Model):
#     __tablename__ = 'alternativas'
#     id = db.Column(db.Integer, primary_key=True)
#     correcta = db.Column(db.String(100), nullable=False)
#     pregunta_id = db.Column(db.Integer, db.ForeignKey('preguntas.id'), nullable=False)
#     pregunta = db.relationship(Preguntas)

#     def serialize(self):
#         return {
#                 "id": self.id,
#                 "correcta": self.correcta,
#                 "pregunta": self.pregunta.serialize(),
#             }

# class Distraccion (db.Model):
#     __tablename__ = 'distraccion'
#     id = db.Column(db.Integer, primary_key=True)
#     incorrecta = db.Column(db.String(100), nullable=False)
#     alternativa_id = db.Column(db.Integer, db.ForeignKey('alternativas.id'), nullable=False)
#     alternativa = db.relationship(Alternativas)

#     def serialize(self):
#         return {
#                 "id": self.id,
#                 "correcta": self.correcta,
#                 "alternativa": self.alternativa.serialize(),
#             }